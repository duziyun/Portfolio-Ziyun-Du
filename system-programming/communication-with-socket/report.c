/*THIS CODE IS MY WORK, IT WAS WRITTEN WITHOUT CONSULTING A TUTOR OR CODE WRITTEN BY OTHERS STUDENTS
  Ziyun Du */
#include "defs.h"

int main(int argc, char* argv[]){
  int s;
  long address;
  struct sockaddr_in sin;
  XDR xdrHandle;
  FILE* fstream;
  
  if(!(argc==3 || (argc==4&&(!strcmp(argv[3],"-k"))))) {
    printf("[report] Incorrect argc/argv seen for report! Line:%0d\n", __LINE__);
    exit(1);
  }

  address = *(long*) gethostbyname(argv[1])->h_addr;		
  sin.sin_addr.s_addr= address;
  sin.sin_family= AF_INET;
  sin.sin_port = atoi(argv[2]);
  struct pollfd pollArray[1];

  int perfectNumbers[MAX_PERFECT_CNT];
  for(int i=0; i<10; i++)
    perfectNumbers[i]=0;
  
  //try to connect to manage
  while(true) { 
    if((s = socket(AF_INET,SOCK_STREAM,0)) < 0) {
      perror("[report] failed to create socket!\n");
      exit(1);
    }

    if(connect (s, (struct sockaddr *) &sin, sizeof (sin)) <0) {
      close(s);
      sleep(4);
      continue;
    }

    pollArray[0].fd=s; 
    pollArray[0].events=POLLIN;
    break; 
  }

  //write mesage to encoded stream connecting manage
  struct toManageStruct readMsg;
  readMsg.type = (argc==4&&(!strcmp(argv[3],"-k")))? REQUEST_TERMINATE:REQUEST_STATS;

  if(DBG) printf("[report] requesting %0d to [manage]\n", readMsg.type);
  readMsg.value = 0; 
  readMsg.time =0; 
  if ((fstream=fdopen(s,"w")) == (FILE *) -1 ) {
    printf("[report] failed to open fd. Line:%0d Error:%s\n", __LINE__,strerror(errno));
    exit(1);
  }
  xdrstdio_create(&xdrHandle,fstream,XDR_ENCODE);
  xdr_toManageStruct(&xdrHandle, &readMsg);
  fflush(fstream);

  int perfectIdx=0;
  //waiting for response from manage
  while(true){
    poll(pollArray, 1, -1); 

    if ((fstream=fdopen(s,"r")) == (FILE *) -1 ) {
      printf("[report] failed to open fd. Line:%0d Error:%s\n", __LINE__,strerror(errno));
      exit(1);
    }
			
    struct toReportStruct stat;
    xdrstdio_create(&xdrHandle,fstream,XDR_DECODE); 
    xdr_toReportStruct(&xdrHandle, &stat);

    if(stat.fd==-1) break; //signal end

    printf("\n****************Report of  Host: %s*******************\n",stat.hostName);
    printf("Perfect numbers found by Host:%s: ",stat.hostName);

    for(int i=0; i<stat.perfectNumberIndex; i++) {
      printf("%0d ",stat.perfectNumbers[i]);
      perfectNumbers[perfectIdx] = stat.perfectNumbers[i];
      perfectIdx++;
    }
    
    printf("\nHost name this compute is running on is %s\n", stat.hostName);
    printf("The amount of numbers tested: %0d\n",stat.numberTested);
    printf("The current range working on: [%0d, %0d] \n",stat.currentRangeStart, stat.currentRangeEnd);
    printf("The current number working on: %0d\n", stat.currentNumber);
  }
  
  printf("\nAll the perfect numbers found: ");
  for (int i=0; i<perfectIdx;i++){
    printf("%0d ",perfectNumbers[i]);
  }
  printf("\n");

  return 0;
  
}
