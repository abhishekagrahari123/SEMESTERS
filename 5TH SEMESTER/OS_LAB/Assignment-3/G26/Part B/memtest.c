#include "types.h"
#include "stat.h"
#include "user.h"

int math_func(int num){
	return num*num - 4*num + 1;
}

int
main(int argc, char* argv[]){

	for(int i=0;i<20;i++){
		if(!fork()){
			printf(1, "Child %d\n", i+1);
			printf(1, "Iteration Matched Different\n");
			printf(1, "--------- ------- ---------\n\n");
			
			for(int j=0;j<10;j++){
				int *arr = malloc(4096);
				for(int k=0;k<1024;k++){
					arr[k] = math_func(k);
				}
				int matched=0;
				for(int k=0;k<1024;k++){
					if(arr[k] == math_func(k))
						matched+=4;
				}
				
				if(j<9)
					printf(1, "    %d      %dB      %dB\n", j+1, matched, 4096-matched);
				else
					printf(1, "   %d      %dB      %dB\n", j+1, matched, 4096-matched);
				
			}
			printf(1, "\n");
			
			exit();
		}
	}

	while(wait()!=-1);
	exit();

}
