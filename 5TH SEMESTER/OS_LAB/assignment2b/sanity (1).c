#include "types.h"
#include "user.h"
#include "stat.h"

int main(int argc, char *argv[])
{
  int i, n, j, k, l;

  int retime;
  int rutime;
  int stime;

  if (argc != 2) {
    printf(1, "Usage: sanity <n>\n");
    exit();
  }
  int tot_time[3][3];
  for (i = 0; i < 3; i++)
    for (j = 0; j < 3; j++)
      tot_time[i][j] = 0;

  // retrieve provided input
  n = atoi(argv[1]);

  int pid;

  // fork child process and calculate statistics of process
  for (i = 0; i < 3 * n; i++) {
    pid = fork();
    if (pid == 0) { // child process
      j = (getpid()-4) % 3; 
      if (j == 0) { // CPU bound process
        for (k = 0; k < 100; k++) {
          for (l = 0; l < 1e6; l++) {}
        }
      }
      else if (j == 1) { // short task based cpu bound process
        for (k = 0; k < 100; k++) {
          for (l = 0; l < 1e6; l++) {}
          yield();
        }
      }
      else {
        for (k = 0; k < 100; k++) {
          sleep(1);
        }
      }
      exit(); // child process terminates here
    }
    continue;
  }

  for (i = 0; i < 3 * n; i++) {
    pid = wait2(&retime, &rutime, &stime);
    int res_id = pid % 3;
    tot_time[res_id][0] += retime;
    tot_time[res_id][1] += rutime;
    tot_time[res_id][2] += stime;
    if (res_id == 0) {
      printf(1, "type: Cpu bound, pid: %d, wait time: %d, running: %d, I/O time: %d\n", pid, retime, rutime, stime);
    }
    else if (res_id == 1) {
      printf(1, "type: S-Cpu bound, pid: %d, wait time: %d, running: %d, I/O time: %d\n", pid, retime, rutime, stime);
    }
    else {
      printf(1, "type: I/O bound, pid: %d, wait time: %d, running: %d, I/O time: %d\n", pid, retime, rutime, stime);
    }
  }

  for (i = 0; i < 3; i++) {
    for (j = 0; j < 3; j++) {
      tot_time[i][j] /= n;
    }
  }

  printf(1, "Cpu bound statistics:\n Average ready time: %d \n Average sleeping time: %d\n Average turnaround time: %d \n", tot_time[0][0], tot_time[0][2], tot_time[0][0] + tot_time[0][1] + tot_time[0][2]);
  printf(1, "S-Cpu bound stats: \n Average ready time: %d \n Average sleeping time: %d\n Average turnaround time: %d \n", tot_time[1][0], tot_time[1][2], tot_time[1][0] + tot_time[1][1] + tot_time[1][2]);
  printf(1, "I/O bound stats  : \n Average ready time: %d \n  Average sleeping time: %d\n Average turnaround time: %d \n", tot_time[2][0], tot_time[2][2], tot_time[2][0] + tot_time[2][1] + tot_time[2][2]);
  exit();
}
