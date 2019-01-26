/*THIS CODE IS MY WORK, IT WAS WRITTEN WITHOUT CONSULTING A TUTOR OR CODE WRITTEN BY OTHERS STUDENTS
 Ziyun Du */

//read shared memory segment
//report on the perfect numbers found, the total number tested, skipped and found
//should also give a toatl of these three numbers that includes processes no longer running
#include "defs.h"

memorySegment *segment;
int smid=0, qid=0, totalNumberTested=0,totalNumberFound=0;
long totalNumberSkipped=0;

int main(int argc, char* argv[]){
  if(DBG_ON) printf("entering report\n");
  if((smid=shmget(KEY,sizeof(memorySegment),0))==-1){
    printf("Line %0d report failed to get shared memory. Error: %s\n",__LINE__,strerror(errno));
    exit(1);
  }
  
  if((segment=shmat(smid,NULL,0))==(void*)-1){
    printf("Line %0d report failed to attach itself to shared memory. Error: %s\n",__LINE__,strerror(errno));
    exit(1);
  }

  if((qid = msgget(KEY,0))==-1){
    printf("Line %0d report failed to get message queue. Error: %s\n",__LINE__,strerror(errno));
  }

  printf("/************Perfect Numbers Found*****************/\n ");
  for(int i=0;i<PERFECT_ARRAY_SIZE;i++) {
    if(segment->perfectNumbers[i]>0) { //need to initialize it?
      if(DBG_ON) printf("perfectNumbers[%0d]= ",i);
      printf("%0d  ",segment->perfectNumbers[i]);
    }
  }

  printf("\n\n/***Statistics for Running Compute Processes*******/\n"); 
  //active computes
  int activeComputeCnt=0;
  for(int i=0;i<COMPUTE_ARRAY_SIZE;i++){
    if(segment->computeStats[i].pid>0){
      printf("Active Compute Process PID:%0d Number Tested:%-8d Number Skipped:%-8ld Number Found:%-8d\n",
	     segment->computeStats[i].pid,
	     segment->computeStats[i].numberOfCanTested,
	     segment->computeStats[i].numberOfCanSkipped,
	     segment->computeStats[i].numberOfPerfectFound);
      totalNumberTested += segment->computeStats[i].numberOfCanTested;
      totalNumberSkipped += segment->computeStats[i].numberOfCanSkipped; 
      totalNumberFound += segment->computeStats[i].numberOfPerfectFound;
      activeComputeCnt++;
    } 
  }
  if(activeComputeCnt==0) printf("No active compute process is running!\n");
  
  printf("\n/***Statistics for Completed Compute Processes*****/\n"); 
  printf("Number Tested: %-8d\nNumber Skipped:%-8ld\nNumber Found:  %-8d\n",
	 segment->computeStats[COMPUTE_ARRAY_SIZE].numberOfCanTested,
	 segment->computeStats[COMPUTE_ARRAY_SIZE].numberOfCanSkipped,
	 segment->computeStats[COMPUTE_ARRAY_SIZE].numberOfPerfectFound);

  printf("\n/***************Overall Statistics*****************/\n"); 
  printf("Total Number Tested:                   %0d\n",totalNumberTested+segment->computeStats[COMPUTE_ARRAY_SIZE].numberOfCanTested);
  printf("Total Number Skipped:                  %0ld\n",totalNumberSkipped +segment->computeStats[COMPUTE_ARRAY_SIZE].numberOfCanSkipped);
  printf("Total Number of Perfect Numbers Found: %0d\n",totalNumberFound+segment->computeStats[COMPUTE_ARRAY_SIZE].numberOfPerfectFound);
    
  if(argc>=2) {

    if(strcmp(argv[1],"-k")==0) {
      if(DBG_ON) printf("invoking report -k\n");
      myMsg msg;
      //-k only sends one interrupt to manage
      msg.type=KILL_TYPE;
      msg.data = 0;
      if(msgsnd(qid,&msg,sizeof(msg.data),0)==-1) {
	printf("Line %0d report -k failed to send kill signal to message queue. Error: %s\n",__LINE__,strerror(errno));
	exit(1);
      }
    }
  }
}



