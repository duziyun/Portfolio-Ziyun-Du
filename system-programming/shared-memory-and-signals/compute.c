/*THIS CODE IS MY WORK, IT WAS WRITTEN WITHOUT CONSULTING A TUTOR OR CODE WRITTEN BY OTHERS STUDENTS
  Ziyun Du */

#include "defs.h"
memorySegment *segment;

jmp_buf jmpenv;

void computeHandler(int signum);
void computeEndHandler(int signum);

int findSeg(int n){
  return n/(INT_PER_SEGMENT*INT_SIZE);
}

int findInt(int n){
  return (n%(INT_PER_SEGMENT*INT_SIZE))/INT_SIZE;
}

int findBit(int n){
  return (n%(INT_PER_SEGMENT*INT_SIZE))%INT_SIZE;
}

bool isSet(int n){
  return (segment->bitmap[findSeg(n)][findInt(n)]&(1<<findBit(n)));
}

void setBitmap(int n){
  segment->bitmap[findSeg(n)][findInt(n)] |= (1<<findBit(n));
}

bool isPerfect(int n){
  int sum = 0;
  for(int i=1;i<n;++i) {
    if(n%i==0) sum+=i;
  }
  if(DBG_ON && sum==n) printf("found perfect number %0d\n",n);
  return sum==n;
}

int smid=0, qid=0, computePID,computeIdx=0, cur;

int main(int argc, char* argv[]){
  
  if(setjmp(jmpenv)){
    if(DBG_ON) printf("Compute PID:%0d wraps around to the start and calls report -k\n", getpid());
    char* argv_list[] = {"./report","-k",NULL};
    execv("./report",argv_list); 
    exit(0);
  }

  if(argc<2) {
    printf("Please input starting number as the second argument of compute!\n");
    exit(1);
  }

  int start = atoi(argv[1]);
  if(DBG_ON) printf("start=%0d\n", start);
  //IPC_CREAT|IPC_EXCL|0666
  //assumption made is user calls ./manage first
  if((smid=shmget(KEY,sizeof(memorySegment),0))==-1){
    printf("Line %0d compute failed to get shared memory. Error: %s\n",__LINE__,strerror(errno));
    exit(1);
  }
  
  if((segment=shmat(smid,NULL,0))==(void*)-1){
    printf("Line %0d compute failed to attach itself shared memory. Error: %s\n",__LINE__,strerror(errno));
    exit(1);
  }
  //IPC_CREAT|IPC_EXCL|0666
  if((qid = msgget(KEY,0))==-1){
    printf("Line %0d compute failed to get message queue. Error: %s\n",__LINE__,strerror(errno));
  }

  myMsg msg;
  msg.type = INIT_TYPE;
  msg.data = getpid();
  if(msgsnd(qid,&msg,sizeof(msg.data),0)==-1) {
    printf("Line %0d compute failed to send initialization message queue. Error: %s\n",__LINE__,strerror(errno));
  }
  
  if(msgrcv(qid, &msg, sizeof(msg.data), INIT_DONE_TYPE, 0) == -1){
    printf("Line %0d compute failed to receive initialization done. Error: %s\n",__LINE__,strerror(errno));
    exit(1);
  }

  computeIdx = msg.data;//index in computeStats
  if(DBG_ON) printf("Compute PID:%0d computeIdx:%0d\n", getpid(),computeIdx);

  signal(SIGINT, computeHandler);
  signal(SIGQUIT, computeHandler);
  signal(SIGHUP, computeHandler);

  cur = start;

  while(true){
    if(cur>=(BIT_MAP_SIZE)) {
      if(DBG_ON) printf("compute reached the end %0d\n", cur);
      break;
    }
    if(!isSet(cur)){

      setBitmap(cur);
      segment->computeStats[computeIdx].numberOfCanTested++;
      if(isPerfect(cur)){
	segment->computeStats[computeIdx].numberOfPerfectFound++;
	msg.type=FOUND_TYPE;
	msg.data=cur;
	if(DBG_ON) printf("Compute pid:%0d sending perfect number %0d to manage\n", getpid(), msg.data);
	if(msgsnd(qid,&msg,sizeof(msg.data),0)==-1) {
	  printf("Line %0d compute failed to send perfect number to manage. Error: %s\n",__LINE__,strerror(errno));
	}
      }
      
    } else {//already computed
      segment->computeStats[computeIdx].numberOfCanSkipped++;
    }
    cur++;
  }
  if(DBG_ON) printf("compute reached the end 2 %0d\n", cur);
  computeEndHandler(0);
  longjmp(jmpenv,1);
  
}

void computeEndHandler(int signum){
  if(DBG_ON) printf("compute PID %0d cleaning up\n",getpid());
  segment->computeStats[COMPUTE_ARRAY_SIZE].numberOfPerfectFound += segment->computeStats[computeIdx].numberOfPerfectFound;
  segment->computeStats[COMPUTE_ARRAY_SIZE].numberOfCanTested    += segment->computeStats[computeIdx].numberOfCanTested;   
  segment->computeStats[COMPUTE_ARRAY_SIZE].numberOfCanSkipped   += segment->computeStats[computeIdx].numberOfCanSkipped;

  segment->computeStats[computeIdx].pid = 0;
  segment->computeStats[computeIdx].numberOfPerfectFound = 0;
  segment->computeStats[computeIdx].numberOfCanTested = 0;
  segment->computeStats[computeIdx].numberOfCanSkipped = 0;

}

void computeHandler(int signum){
  computeEndHandler(signum);
  exit(0);
}
