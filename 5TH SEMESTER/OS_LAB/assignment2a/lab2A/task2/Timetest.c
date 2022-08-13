#include "types.h"
#include "stat.h"
#include "user.h"
#include "fs.h"

int main(int argc,char *argv[])
{
  int pid;
  int retime,rutime,stime,p=1;
  pid = fork();
  if(pid == 0)
  {
    exec(argv[1], argv);
    printf(1, "%d\n", p);
  }
  else
  {
    p = wait2(&retime, &rutime, &stime);
  }
  printf(1, "Runnable time = %d\n Running time = %d\n Sleeping time = %d\n", retime, rutime, stime);
  exit();
}