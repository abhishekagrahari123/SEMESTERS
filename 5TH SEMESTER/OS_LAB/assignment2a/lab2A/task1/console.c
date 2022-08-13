// Console input and output.
// Input is from the keyboard or serial port.
// Output is written to the screen and serial port.

#include "types.h"
#include "defs.h"
#include "param.h"
#include "traps.h"
#include "spinlock.h"
#include "sleeplock.h"
#include "fs.h"
#include "file.h"
#include "memlayout.h"
#include "mmu.h"
#include "proc.h"
#include "x86.h"

#define UP_ARROW 226
#define DOWN_ARROW 227
#define LEFT_ARROW 228
#define RIGHT_ARROW 229

#define MAX_HISTORY 16

static void consputc(int);

static int panicked = 0;

static struct {
  struct spinlock lock;
  int locking;
} cons;

static void
printint(int xx, int base, int sign)
{
  static char digits[] = "0123456789abcdef";
  char buf[16];
  int i;
  uint x;

  if(sign && (sign = xx < 0))
    x = -xx;
  else
    x = xx;

  i = 0;
  do{
    buf[i++] = digits[x % base];
  }while((x /= base) != 0);

  if(sign)
    buf[i++] = '-';

  while(--i >= 0)
    consputc(buf[i]);
}
//PAGEBREAK: 50

// Print to the console. only understands %d, %x, %p, %s.
void
cprintf(char *fmt, ...)
{
  int i, c, locking;
  uint *argp;
  char *s;

  locking = cons.locking;
  if(locking)
    acquire(&cons.lock);

  if (fmt == 0)
    panic("null fmt");

  argp = (uint*)(void*)(&fmt + 1);
  for(i = 0; (c = fmt[i] & 0xff) != 0; i++){
    if(c != '%'){
      consputc(c);
      continue;
    }
    c = fmt[++i] & 0xff;
    if(c == 0)
      break;
    switch(c){
    case 'd':
      printint(*argp++, 10, 1);
      break;
    case 'x':
    case 'p':
      printint(*argp++, 16, 0);
      break;
    case 's':
      if((s = (char*)*argp++) == 0)
        s = "(null)";
      for(; *s; s++)
        consputc(*s);
      break;
    case '%':
      consputc('%');
      break;
    default:
      // Print unknown % sequence to draw attention.
      consputc('%');
      consputc(c);
      break;
    }
  }

  if(locking)
    release(&cons.lock);
}

void
panic(char *s)
{
  int i;
  uint pcs[10];

  cli();
  cons.locking = 0;
  // use lapiccpunum so that we can call panic from mycpu()
  cprintf("lapicid %d: panic: ", lapicid());
  cprintf(s);
  cprintf("\n");
  getcallerpcs(&s, pcs);
  for(i=0; i<10; i++)
    cprintf(" %p", pcs[i]);
  panicked = 1; // freeze other CPU
  for(;;)
    ;
}

//PAGEBREAK: 50
#define BACKSPACE 0x100
#define CRTPORT 0x3d4
static ushort *crt = (ushort*)P2V(0xb8000);  // CGA memory

static void
cgaputc(int c) 
{
  int pos;

  // Cursor position: col + 80*row.
  outb(CRTPORT, 14);
  pos = inb(CRTPORT+1) << 8;
  outb(CRTPORT, 15);
  pos |= inb(CRTPORT+1);

  switch(c) {
    case '\n':
      pos += 80 - pos%80;
      break;
    case BACKSPACE:
      if(pos > 0) --pos;
      break;
    case LEFT_ARROW:
      if(pos > 0) --pos;
      break;
    default:
      crt[pos++] = (c&0xff) | 0x0700;  // black on white
  }

  if(pos < 0 || pos > 25*80)
    panic("pos under/overflow");

  if((pos/80) >= 24){  // Scroll up.
    memmove(crt, crt+80, sizeof(crt[0])*23*80);
    pos -= 80;
    memset(crt+pos, 0, sizeof(crt[0])*(24*80 - pos));
  }

  outb(CRTPORT, 14);
  outb(CRTPORT+1, pos>>8);
  outb(CRTPORT, 15);
  outb(CRTPORT+1, pos);
  if (c == BACKSPACE)
    crt[pos] = ' ' | 0x0700;
}


void
consputc(int c)
{
  if(panicked){
    cli();
    for(;;)
      ;
  }

  switch (c) {
    case BACKSPACE:
      // uartputc prints to Linux's terminal
      uartputc('\b'); uartputc(' '); uartputc('\b');
      break;
    case LEFT_ARROW:
      uartputc('\b');
      break;
    default:
      uartputc(c); 
  }
  // cgaputc prints to QEMU's terminal
  cgaputc(c);
}


#define BUFFER_SIZE 128
struct {
  char buf[BUFFER_SIZE];
  uint r;  // Read index
  uint w;  // Write index
  uint e;  // Edit index(i.e. current caret position)
  uint end; // position in buf for the next char
} input;

char buffer[BUFFER_SIZE];  // temporary storage for input.buf in a certain context

struct {
  char entries[MAX_HISTORY][BUFFER_SIZE + 1];
  uint count;
  uint current;
} records;

#define C(x)  ((x)-'@')  // Control-x


//Copies input buffer. 

void copybuf() {
  uint n = input.end - input.e;
  uint i;
  for (i = 0; i < n; i++)
    buffer[i] = input.buf[input.e + i % BUFFER_SIZE];
}

/*
it shifts the characters on the right of the caret to the right on pressing new keys when the caret is not at the end.
*/

void shift_buffer_right() {
  uint n = input.end - input.e;
  for (int i = 0; i < n; i++) {
    input.buf[input.e + i % BUFFER_SIZE] = buffer[i];
    consputc(buffer[i]);
  }
  // reset buffer
  memset(buffer, '\0', BUFFER_SIZE);
  // return the caret to its correct position
  for (int i = 0; i < n; i++) {
    consputc(LEFT_ARROW);
  }
}

/*
it shifts the characters on the right of the caret to the left on pressing backspace when the caret is not at the end.
*/

void shift_buffer_left() {
  uint n = input.end - input.e;
  uint i;
  consputc(LEFT_ARROW);
  input.e--;
  for (i = 0; i < n; i++) {
    char c = input.buf[input.e + i + 1 % BUFFER_SIZE];
    input.buf[input.e + i % BUFFER_SIZE] = c;
    consputc(c);
  }
  input.end--;
  consputc(' '); // delete the last char in line
  for (i = 0; i <= n; i++) {
    consputc(LEFT_ARROW); // shift the caret back to the left
  }
}



void
consoleintr(int (*getc)(void))
{
  int c, doprocdump = 0;
  uint i, n, record_length;
  acquire(&cons.lock);
  while((c = getc()) >= 0){
    switch(c){
     case C('H'): case '\x7f':  // Backspace
      if (input.end != input.e && input.e != input.w) { // caret isn't at the end of the line
        shift_buffer_left();
        break;
      }
      if(input.e != input.w){ // caret is at the end of the line
        input.e--;
        input.end--;
        consputc(BACKSPACE);
      }
      break;
    case C('P'):  // Process listing.
      doprocdump = 1;   // procdump() locks cons.lock indirectly; invoke later
      break;
    case C('U'):  // Kill line.
      if (input.end > input.e) { // caret isn't at the end of the line
        uint numtoshift = input.end - input.e;
        uint placestoshift = input.e - input.w;
        for (i = 0; i < placestoshift; i++) {
          consputc(LEFT_ARROW);
        }
        memmove(input.buf + input.w, input.buf + input.w + placestoshift, numtoshift);
        input.e -= placestoshift;
        input.end -= placestoshift;
        for (i = 0; i < numtoshift; i++) { // repaint the chars
          consputc(input.buf[input.e + i % BUFFER_SIZE]);
        }
        for (i = 0; i < placestoshift; i++) { // erase the leftover chars
          consputc(' ');
        }
        for (i = 0; i < placestoshift + numtoshift; i++) { // move the caret back to the left
          consputc(LEFT_ARROW);
        }
      }
      else { // caret is at the end of the line
        while(input.e != input.w &&
              input.buf[(input.e-1) % BUFFER_SIZE] != '\n'){
          input.e--;
          input.end--;
          consputc(BACKSPACE);
        }
      }
      break;
   
    case LEFT_ARROW:
      if (input.e != input.w) {
        input.e--;
        consputc(c);
      }
      break;
    case RIGHT_ARROW:
      if (input.e < input.end) {
        consputc(input.buf[input.e]);
        input.e++;
      }
      else if (input.e == input.end){
        consputc(' ');
        consputc(LEFT_ARROW);
      }
      break;
    case UP_ARROW:
      if (records.current > 0) {
        records.current--;
        n = input.end - input.w;  // current line on screen length
        record_length = records.entries[records.current][BUFFER_SIZE];
        for (i = 0; i < input.e - input.w; i++) {
          consputc(LEFT_ARROW); // move the caret to the beginning of the line
        }
        for (i = 0; i < record_length; i++) {
          input.buf[input.w + i % BUFFER_SIZE] = records.entries[records.current][i]; // repopulate the buffer
        }
        input.e = input.w + records.entries[records.current][BUFFER_SIZE]; // index BUFFER_SIZE is the length of the command
        input.end = input.e;
        for (i = 0; i < record_length; i++) {
          consputc(input.buf[input.w + i % BUFFER_SIZE]); /// repaint the new command
        }
        n = records.entries[records.current][BUFFER_SIZE] - n;
        for (i = 0; i < record_length - n; i++) {
          consputc(' '); // erase chars from the old command
        }
        for (i = 0; i < record_length - n; i++) {
          consputc(LEFT_ARROW); // move the caret back to the left
        }
      }
      break;
    case DOWN_ARROW:
      if (records.current <= records.count- 1) {
        records.current++;
        n = input.end - input.w;  // current line on screen length
        record_length = records.entries[records.current][BUFFER_SIZE];
        for (i = 0; i < input.e - input.w; i++) {
          consputc(LEFT_ARROW); // move the caret to the beginning of the line
        }
        for (i = 0; i < record_length; i++) {
          input.buf[input.w + i % BUFFER_SIZE] = records.entries[records.current][i]; // repopulate the buffer
        }
        input.e = input.w + records.entries[records.current][BUFFER_SIZE]; // index BUFFER_SIZE is the length of the command
        input.end = input.e;
        for (i = 0; i < record_length; i++) {
          consputc(input.buf[input.w + i % BUFFER_SIZE]); // repaint the new command
        }
        n = records.entries[records.current][BUFFER_SIZE] - n;
        for (i = 0; i < record_length - n; i++) {
          consputc(' '); // erase chars from the old command
        }
        for (i = 0; i < record_length - n; i++) {
          consputc(LEFT_ARROW); // move the caret back to the left
        }
      }
      else { // clear the line
        n = input.end - input.w;
        for (i = 0; i < n; i++) {
          consputc(' ');
        }
        for (i = 0; i < n; i++) {
          consputc(LEFT_ARROW);
        }
      }
      break;
    case '\n':
    case '\r':
        input.e = input.end;
    default:
      //updating the commands in the command history table. 
      if(c != 0 && input.e-input.r < BUFFER_SIZE){
        c = (c == '\r') ? '\n' : c;
        if (input.end > input.e) { // caret isn't at the end of the line
          copybuf();
          input.buf[input.e++ % BUFFER_SIZE] = c;
          input.end++;
          consputc(c);
          shift_buffer_right();
        }
        else {
          input.buf[input.e++ % BUFFER_SIZE] = c;
          input.end = input.e - input.end == 1 ? input.e : input.end;
          consputc(c);
        }
        if(c == '\n' || c == C('D') || input.e == input.r+BUFFER_SIZE){
          input.w = input.end;
          if (records.count< MAX_HISTORY) { // empty places in records.entries
            n = input.end - input.r;
            n = input.buf[input.end - 1] == '\n' ? n - 1 : n;
            records.current = records.count;
            memmove(records.entries[records.current], input.buf + input.r, n);
            records.entries[records.current][BUFFER_SIZE] = n;
            records.count++;
            records.current++;
          }
          else { // shift all entries one index down to make room for a new one
            memmove(records.entries[0], records.entries[1], (MAX_HISTORY - 1) * (BUFFER_SIZE + 1));
            records.current--;
            n = input.end - input.r;
            n = input.buf[input.end - 1] == '\n' ? n - 1 : n;
            memmove(records.entries[MAX_HISTORY - 1], input.buf + input.r, n);
            records.entries[MAX_HISTORY - 1][BUFFER_SIZE] = n;
            records.current = records.count;
          }
          wakeup(&input.r);
        }
      }
      break;
    }
  }
  release(&cons.lock);
  if(doprocdump) {
    procdump();  // now call procdump() wo. cons.lock held
  }
}

/*
  this is the function that gets called by the sys_history and writes the requested command history in the buffer
*/

int history(char *buffer, int historyId) {
  if (historyId < 0 || historyId > MAX_HISTORY - 1)
    return -2;
  if (historyId >= records.current)
    return -1;
  memset(buffer, '\0', BUFFER_SIZE);
  memmove(buffer, records.entries[historyId], records.entries[historyId][BUFFER_SIZE]);
  return 0;
}

int
consoleread(struct inode *ip, char *dst, int n)
{
  uint target;
  int c;

  iunlock(ip);
  target = n;
  acquire(&cons.lock);
  while(n > 0){
    while(input.r == input.w){
      if(myproc()->killed){
        release(&cons.lock);
        ilock(ip);
        return -1;
      }
      sleep(&input.r, &cons.lock);
    }
    c = input.buf[input.r++ % BUFFER_SIZE];
    if(c == C('D')){  // EOF
      if(n < target){
        // Save ^D for next time, to make sure
        // caller gets a 0-byte result.
        input.r--;
      }
      break;
    }
    *dst++ = c;
    --n;
    if(c == '\n')
      break;
  }
  release(&cons.lock);
  ilock(ip);

  return target - n;
}

int
consolewrite(struct inode *ip, char *buf, int n)
{
  int i;

  iunlock(ip);
  acquire(&cons.lock);
  for(i = 0; i < n; i++)
    consputc(buf[i] & 0xff);
  release(&cons.lock);
  ilock(ip);

  return n;
}

void
consoleinit(void)
{
  initlock(&cons.lock, "console");

  devsw[CONSOLE].write = consolewrite;
  devsw[CONSOLE].read = consoleread;
  cons.locking = 1;

  ioapicenable(IRQ_KBD, 0);
}

