/*THIS CODE IS MY WORK, IT WAS WRITTEN WITHOUT CONSULTING A TUTOR OR CODE WRITTEN BY OTHERS STUDENTS
  Ziyun Du */

#include "defs.h"

memorySegment *segment;
int smid=0, qid=0, computePID,computeIdx=0, resIdx=0;
void manageHandler(int signum);

int main(int argc, char *argv[]) {
  if((smid=shmget(KEY,sizeof(memorySegment),IPC_CREAT|IPC_EXCL|0666))==-1){
    printf("Line %0d manage failed to initate shared memory. Error: %s\n",__LINE__,strerror(errno));
    exit(1);
  }
  
  if((segment=shmat(smid,NULL,0))==(void*)-1){
    printf("Line %0d manage failed to attach itself to shared memory. Error: %s\n",__LINE__,strerror(errno));
    exit(1);
  }

  if((qid = msgget(KEY,IPC_CREAT|IPC_EXCL|0666))==-1){
    printf("Line %0d manage failed to initialize message queue. Error: %s\n",__LINE__,strerror(errno));
  }

  //stats for dead compute processess is the last entry
  for(int i=0;i<=COMPUTE_ARRAY_SIZE;i++) {
    segment->computeStats[i].pid=0;
    segment->computeStats[i].numberOfPerfectFound = 0;
    segment->computeStats[i].numberOfCanTested    = 0;
    segment->computeStats[i].numberOfCanSkipped   = 0;
  }

  signal(SIGINT, manageHandler);
  signal(SIGQUIT, manageHandler);
  signal(SIGHUP, manageHandler);

  myMsg msg;
  while(1) {
    //get the first message whose type << 3
    msgrcv(qid, &msg, sizeof(msg.data),-3,0);
    
    //on initializing,compute send its pid to manage
    if(msg.type==INIT_TYPE){
      //total cnt can be larger than 20, so should find the first non-zero idx
      computeIdx = -1;
      
      for(int i=0;i<COMPUTE_ARRAY_SIZE;i++) {
	if(segment->computeStats[i].pid==0){
	  computeIdx = i;
	  break;
	}
      }
      if(computeIdx<0) {
	printf("Too many outstanding compute processes!!! Line %0d \n",__LINE__);
	exit(1);
      }
      computePID = msg.data;
      segment->computeStats[computeIdx].pid = computePID;
      segment->computeStats[computeIdx].numberOfPerfectFound = 0;
      segment->computeStats[computeIdx].numberOfCanTested = 0;
      segment->computeStats[computeIdx].numberOfCanSkipped = 0;

      msg.type = INIT_DONE_TYPE;
      msg.data = computeIdx;

      if(msgsnd(qid,&msg,sizeof(msg.data),0)==-1) {
	printf("Line %0d manage failed to send initialization done message queue. Error: %s\n",
	       __LINE__,strerror(errno));
	exit(1);
      }
      
      if(DBG_ON) printf("Initialized compute PID %0d\n", computePID);
    } else if(msg.type==KILL_TYPE) { //report -k; send to call compute processes

      for(int i=0;i<COMPUTE_ARRAY_SIZE;i++) {      
	if(segment->computeStats[i].pid>0){
	  if(kill(segment->computeStats[i].pid,SIGINT)==-1) {
	    printf("On receiving KILL_TYPE manage failed to send SIGINT to compute PID %0d Line %0d \n",
		   segment->computeStats[msg.data].pid,__LINE__);
	  }
	}
      }
      
    } else if(msg.type==FOUND_TYPE){
      if(resIdx>=PERFECT_ARRAY_SIZE) {
	printf("Too many perfect numbers found!!! Line %0d \n",__LINE__);
	exit(1);
      }
      //need to handle duplicate since there is no semaphore invoked for bitmap
      bool duplicateFound=false;
      for(int i=0;i<resIdx;i++){
	if(msg.data==segment->perfectNumbers[i]) {
	  duplicateFound = true;
	  break;
	}
      }
      
      if(!duplicateFound){
	if(DBG_ON) printf("writing perfect number %0d to idx %0d\n", msg.data,resIdx);
	segment->perfectNumbers[resIdx++] = msg.data;
      }
    }
  }
  
}

void manageHandler(int signum){
  if(DBG_ON)printf("received signum=%0d\n",signum);
  //send interrupt to all the running compute procesess
  for(int i=0;i<COMPUTE_ARRAY_SIZE;i++){
    if(segment->computeStats[i].pid!=0){
      if( kill(segment->computeStats[i].pid,SIGINT)==-1){
	printf("Manage failed to send SIGINT to compute PID %0d Line %0d  Error: %s \n",
	       segment->computeStats[i].pid,__LINE__,strerror(errno));
	exit(1);
      }
    }
  }
  //sleep 5 seconds
  sleep(5);
  //deallocate shared memory segment
  //IPCS IPCRM
  if(shmdt(segment)==-1) {
    printf("Line %0d manage failed to detach from the shared segment. Error: %s\n",__LINE__,strerror(errno));
    exit(1);
  }

  if(shmctl(smid,IPC_RMID,0)==-1){//destroy
    printf("Line %0d manage failed to destroy the shared segment. Error: %s\n",__LINE__,strerror(errno));
    exit(1);
  }

  if(msgctl(qid,IPC_RMID,NULL)==-1){
    printf("Line %0d manage failed to destroy the message queue. Error: %s\n",__LINE__,strerror(errno));
    exit(1);
  }
  exit(0);
}
