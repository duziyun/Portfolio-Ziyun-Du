/*THIS CODE IS MY WORK, IT WAS WRITTEN WITHOUT CONSULTING A TUTOR OR CODE WRITTEN BY OTHERS STUDENTS.
                                                                                            Ziyun Du */

//MAX - max range to test
//BLOCK - size of block
//address per 8 blocks // 8 because size of char in c is one byte
//each bit represents whether this block of intergers have been tested
//no of bits needed = MAX/BLOCK + 1/0
//if use char (one byte) -> ans/8 + 0/1
#include<string.h>
#include<stdio.h>
#include<pthread.h>
#include<unistd.h>
#include<errno.h>
#include<stdlib.h>
#include<ctype.h>
#include<sys/times.h>
#include<time.h>
#include<sys/resource.h>
#include <stdbool.h>

#define BITS_PER_BYTE 8
//CMD enums
#define START 0
#define IDLE 1
#define RESTART 2
#define WAIT 3
#define REPORT 4
#define QUIT 5
#define NONE 6
#define MAX_PERFECT_CNT 20
//thread state enums
#define RUNNING_ 1
#define IDLE_    2
#define DONE_    3

//each entry represents 8 blocks of integers
char* bitmap;
int MAX=0;
int BLOCK=0;
time_t startTime;
int perfectIndex=0;
int curThreadNumber=1;
int pendingThreadsCnt=0;
int totalBlockCnt=0; //total number of blocks

pthread_attr_t attrb;
pthread_mutex_t mtx;
pthread_cond_t cond;
//the condition for the process and thus all its threads to terminate is:all numbers have been tested
//a thread should wrap around when reaching MAX
//-> for a thread curBlockNumber = startBlock-1 && no pending threads
//above is unnecessary
long totalNumberTested=0;

clock_t cpuStart;
clock_t cpuEnd;
double cpuTimeUsed;

//statistics for each thread
typedef struct threadStat{
  int threadNumber;
  pthread_t tid;
  int state;
  int curBlock;
  int tested;
  int skipped;
  int found;
  int perfectFound[MAX_PERFECT_CNT];
  struct threadStat* next;
} threadStat;

//a linked list to keep track of all the threads spawn
threadStat* head=NULL;
threadStat* tail=NULL;

int getOperation(char* args[]){
  if(strcmp(args[0],"start")==0) {
    return START;
  } else  if(strcmp(args[0],"idle")==0) {
    return IDLE;
  } else  if(strcmp(args[0],"restart")==0) {
    return RESTART;
  } else  if(strcmp(args[0],"wait")==0) {
    return WAIT;
  } else  if(strcmp(args[0],"report")==0) {
    return REPORT;
  } else  if(strcmp(args[0],"quit")==0) {
    return QUIT;
  } else if(strcmp(args[0],"")==0) {//empty line
    return NONE;
  }
  
  return -1;
}

bool isPerfect(int n){
  if(n<2) return false;
  int sum = 1;
  for(int i=2;i<n;++i) {
    if(n%i==0) sum+=i;
  }

  return sum==n;
}

void* quit(){
  long totalTested=0;
  threadStat* curThread;
  time_t endTime;
  
  curThread = head;
  
  printf("*********The process is quitting*******\n");
  printf("Found perfect numbers:");
  while(curThread!=NULL){
    totalTested += curThread->tested;

    for(int j=0;j<curThread->found;j++){
      printf("  %0d",curThread->perfectFound[j]);
    }
    curThread = curThread->next;
  }

  printf("\nTotal numbers tested:%0ld    (Full testing range is: 0 ~ MAX:%0d)\n",totalTested,MAX);

  cpuEnd = clock();
  cpuTimeUsed = ((double)(cpuEnd-cpuStart))/CLOCKS_PER_SEC;

  printf("Total CPU time: %0f seconds\n",cpuTimeUsed);

  time(&endTime);
  printf("Total elapsed time: %ld seconds\n",endTime-startTime);


  if(pthread_attr_destroy(&attrb)!=0){
    printf("Failed to destroy attrb. Line:%0d Error:%s\n",__LINE__,strerror(errno));
    exit(1);
  }

  if(pthread_cond_destroy(&cond)!=0) {
    printf("Failed to destroy cond. Line:%0d Error:%s\n",__LINE__,strerror(errno));
    exit(1);
  }

  curThread = head;
  free(bitmap);

  while(curThread!=NULL) {
    threadStat* next = curThread->next;
    free(curThread);
    curThread = next;
  }

  exit(0);
}

void* calcPerfect(void* curThreadIn){
  threadStat* curThread = (threadStat*) curThreadIn;
  int startBlockNumber = curThread->curBlock;

  do{
    //look for the next uncomputed block
    pthread_mutex_lock(&mtx);
    bool incremented = false;

    while((bitmap[curThread->curBlock/8]&(1<<(curThread->curBlock%8)))!=0){ //tested
      
      curThread->skipped += (curThread->curBlock==totalBlockCnt-1)? MAX % BLOCK : BLOCK;
      curThread->curBlock = (curThread->curBlock+1) % totalBlockCnt; //to wrap around
      incremented = true;
      if(curThread->curBlock==startBlockNumber) break;
    } 

    if(curThread->curBlock==startBlockNumber && incremented) { //this thread covered all the range - so terminate
      curThread->state = DONE_;

      pthread_mutex_unlock(&mtx);
      pthread_exit(EXIT_SUCCESS);
    } else {//found uncomputed block          
      //set the block in the bitmap
      bitmap[curThread->curBlock/8] |= (1<<(curThread->curBlock%8));

    }
    pthread_mutex_unlock(&mtx);

    //look for perfect number in the chosen block
    int start = curThread->curBlock*BLOCK;
    int end = start;
    if(curThread->curBlock==totalBlockCnt-1){
      end += MAX % BLOCK;
    } else {
      end += BLOCK - 1;
    }

    for(int num=start;num<=end;num++){
      if(isPerfect(num)) {
	curThread->perfectFound[curThread->found++] = num;
      }
      
      curThread->tested++;

      pthread_mutex_lock(&mtx);
      totalNumberTested++;

      pthread_mutex_unlock(&mtx);
      
      //quit when all numbers being tested 0~MAX
      if(totalNumberTested==MAX+1) {
	quit();
      }

      if(curThread->state==IDLE_){
	pthread_mutex_lock(&mtx);
	do{
	  printf("Thread %0d is idle\n",curThread->threadNumber);
	  pthread_cond_wait(&cond,&mtx);
	  printf("Thread %0d is resumed\n",curThread->threadNumber);
	} while(curThread->state==IDLE_);
	pthread_mutex_unlock(&mtx);
      }
      
    } //end of looking for perfect numbers for the current block

    curThread->curBlock = (curThread->curBlock+1) % totalBlockCnt;  
  } while(curThread->curBlock!=startBlockNumber);
  
  curThread->state = DONE_;
}

threadStat* getNthThread(int K){
  threadStat* cur = head;

  while(cur!=NULL){
    if(cur->threadNumber==K) {
      return cur;
    }
    cur = cur->next;
  }

  return NULL;
}

int main(int argc, char* argv[]){
  cpuStart = clock();
  time(&startTime);
  if(argc!=3){
    printf("please input the correct number of arguments! argc=%0d Line:%0d\n",argc, __LINE__);
    exit(1);
  }

  MAX = atoi(argv[1]);
  BLOCK = atoi(argv[2]);  
  
  totalBlockCnt = (MAX+1)/BLOCK;
  if((MAX+1)%BLOCK!=0) totalBlockCnt++;

  int bitmapSize = totalBlockCnt/(sizeof(char)*BITS_PER_BYTE);
  if(totalBlockCnt%(sizeof(char)*BITS_PER_BYTE)!=0) bitmapSize++;

  bitmap = calloc(bitmapSize,sizeof(char));
  
  if(pthread_mutex_init (&mtx,NULL)!=0) {
    printf("Failed to initialize mutex. Line:%0d Error:%s\n",__LINE__,strerror(errno));
    exit(1);
  }

  if(pthread_cond_init(&cond,NULL)!=0) {
    printf("Failed to initialize cond. Line:%0d Error:%s\n",__LINE__,strerror(errno));
    exit(1);
  }
  
  if(pthread_attr_init(&attrb)!=0){
    printf("Failed to initialized attribute. Line:%0d Error:%s\n",__LINE__,strerror(errno));
    exit(1);
  }

  if(pthread_attr_setscope(&attrb,PTHREAD_SCOPE_SYSTEM)!=0){
    printf("Failed to set scope. Line:%0d Error:%s\n",__LINE__,strerror(errno));
    exit(1);
  }

  while(true){
    //so getline() will allocate a buffer for storing the line
    char* buffer = NULL;
    size_t bufsize = 0;
    ssize_t charCount=0; //number of character read
 
    charCount = getline(&buffer,&bufsize,stdin);
    if(charCount<1) break;

    //split the line read by space to get arguments
    char* temp;
    char* args[2];
    int i=0;
    temp = strtok(buffer," ");
    
    while(temp!=NULL){
      args[i] = malloc((strlen(temp)+1)* sizeof(char));
      int index = 0;
      for(int j=0;j<strlen(temp);j++){
	if(temp[j]=='\n') break;
	args[i][index++] = temp[j]; 
      }
      args[i][index] = 0; //terminates the string
      
      i++;
      temp = strtok(NULL," ");
    }

    int operation = getOperation(args);

    int K;
    threadStat* curThread=NULL;
    
    switch(operation){
    case START:
      if(strcmp(args[1],"")==0) {
	printf("Invalid command seen!\n");
	exit(1);
      }

      K = atoi(args[1]);

      //initialized the thread
      curThread = (threadStat*)malloc(sizeof(threadStat));
      curThread->state = RUNNING_;      
      curThread->curBlock = K/BLOCK; //assume range of numbersis 0~MAX; block index: 0~totalBlockCnt-1
      curThread->tested = 0;     
      curThread->skipped = 0;    
      curThread->found = 0;      
      for(int i=0;i<MAX_PERFECT_CNT;i++){
	curThread->perfectFound[i] = -1;
      }

      
      curThread->next =(threadStat*)NULL;

      //append this thread to the linked list
      if(curThreadNumber==1) {
	head = curThread;
	tail = head;
      } else {
	tail->next = curThread;
	tail = curThread;
      }

      curThread->threadNumber = curThreadNumber++;
      
      //when starting, print block number and thread number
      printf("Thread Number:%0d started searching from Block Number:%0d \n", curThread->threadNumber,curThread->curBlock);
      pthread_create(&(curThread->tid),&attrb,calcPerfect,(void*)curThread);
      break;
    case IDLE:
      if(strcmp(args[1],"")==0) {
	printf("Invalid command seen!\n");
	exit(1);
      }

      K = atoi(args[1]);
      curThread = getNthThread(K);
      if(curThread==NULL){
	printf("Cannot find Thread %0d to idle! Please input the current thread number to idle! Line:%0d",K,__LINE__);
	exit(1);
      } else {

	printf("Putting Thread %0d to idle state\n", curThread->threadNumber);
	curThread->state = IDLE_;
      }
      
      break;
    case RESTART:
      if(strcmp(args[1],"")==0) {
	printf("Invalid command seen!\n");
	exit(1);
      }

      K = atoi(args[1]);
      curThread = getNthThread(K);
      if(curThread==NULL){
	printf("Cannot find Thread %0d to restart! Please input the current thread number to restart! Line:%0d",K,__LINE__);
	exit(1);
      } else {

	if(curThread->state == IDLE_) {
	  pthread_mutex_lock(&mtx);
	  curThread->state = RUNNING_;
	  printf("Restarting Thread %0d\n", curThread->threadNumber);
	  pthread_cond_broadcast(&cond);
	  pthread_mutex_unlock(&mtx);
	} else {//do nothing if the thread is not idle
	  printf("Igoring the request of restarting Thread %0d since Thread %0d is not in idle state!\n",K,K);
	}
	
      }
      
      break;
    case WAIT:
      if(strcmp(args[1],"")==0) {
	printf("Invalid command seen!\n");
	exit(1);
      }

      K = atoi(args[1]);
      sleep(K);
      break;
    case REPORT:

      curThread = head;
      printf("****************REPORT************************\n");
      
      while(curThread!=NULL){
	printf("***********Statistics for Thread %0d***********\n",curThread->threadNumber);
	printf("Tested:%0d\n",curThread->tested); 
	printf("Skipped:%0d\n",curThread->skipped);
	printf("Currently working on Block %0d\n",curThread->curBlock);
	
	if(curThread->state==IDLE_) printf("Current state: idle\n");
	else if(curThread->state==RUNNING_) printf("Current state: running\n");
	else if(curThread->state==DONE_) printf("Current state: done\n");
	
        printf("Found perfect numbers:");

	for(int j=0;j<curThread->found;j++){
	  printf("  %0d",curThread->perfectFound[j]);
	}
	
	printf("\n");
	printf("******End of Statistics for Thread %0d*********\n\n",curThread->threadNumber);
	curThread = curThread->next;
      }
      
      break;
    case QUIT:
      quit();
      break;
    case NONE:
      break;
    default:
      printf("Invalid operation seen. Line:%0d \n",__LINE__);
      exit(1);
    }
  }
}
