/*THIS CODE IS MY WORK, IT WAS WRITTEN WITHOUT CONSULTING A TUTOR OR CODE WRITTEN BY OTHERS STUDENTS
  Ziyun Du */
#include "defs.h"

int s;
XDR handle;
pthread_mutex_t mtx = PTHREAD_MUTEX_INITIALIZER;

//should be no multiple activities going on between compute and manage at the same time
//compute should stop sending perfect number to manage
//   1) when manage queries 
//   2) when mange requests termination
bool computeManageBusy=false; 
bool terminateByManage =false;
int numTested = 0;
int currentNumber = -1;
int currentRangeStart=-1;
int currentRangeEnd = -1;

time_t startTime,stopTime;
pthread_cond_t cond = PTHREAD_COND_INITIALIZER;

void teminationHandler(int signum);
void* calcPerfect(void* arg_in);
bool isPerfect(int num);

int main(int argc, char* argv[]) {
  if(argc!=4) {
    printf("[compute] Incorrect number of arguments seen for compute! Line:%0d\n",__LINE__);
    exit(1);
  }

  signal(SIGINT,teminationHandler);
  signal(SIGQUIT, teminationHandler);
  signal(SIGHUP, teminationHandler);

  pthread_attr_t tattr;
  pthread_attr_init(&tattr);	
  pthread_attr_setscope(&tattr,PTHREAD_SCOPE_SYSTEM);
  pthread_t tid;
  
  struct sockaddr_in sin;
  long address;
  struct pollfd pollArray[1];

  address = *(long *) gethostbyname(argv[1])->h_addr;
  sin.sin_addr.s_addr= address;
  sin.sin_family= AF_INET;
  sin.sin_port = atoi(argv[2]);

  while(true) {
    //s will get the lowest numbered unused integer for THIS PROCESS
    //0 stdin 1 stdout 2 stderr
    //initially this will be 3
    if ((s = socket(AF_INET,SOCK_STREAM,0)) < 0) {
      perror("[manage] failed to create socket!");
      exit(1);
    }
    //sleep 5 seconds if connect failed
    if (connect (s, (struct sockaddr *) &sin, sizeof (sin)) <0) {
      close(s);
      sleep(4);
      continue;
    }

    pollArray[0].fd=s;  
    pollArray[0].events=POLLIN;
    break; 
  }

  struct toManageStruct msg;
  msg.type = REQUEST_RANGE;
  msg.value = atoi(argv[3]); //start position
  msg.time = -1;//to indicate first time request

  FILE *stream;
  if((stream=fdopen(s,"w")) == (FILE *) -1 ) {
    printf("[compute] failed to open fd. Line:%0d Error:%s\n",__LINE__,strerror(errno));
    exit(1);
  }

  if(DBG) printf("[compute] sending REQUEST_RANGE to [manage]\n");
  xdrstdio_create(&handle,stream,XDR_ENCODE);
  xdr_toManageStruct(&handle, &msg);
  fflush(stream);

  while(true){
    poll(pollArray,1,-1);
    
    if((stream=fdopen(s,"r")) == (FILE*) -1 ) {
      printf("[compute] failed to open fd. Line:%0d Error:%s\n",__LINE__,strerror(errno));
      exit(1);
    }
    
    struct toComputeStruct* readMsg= malloc(sizeof(toComputeStruct));
    //decode and read from the stream
    xdrstdio_create(&handle,stream,XDR_DECODE); 
    xdr_toComputeStruct(&handle, readMsg);

    switch(readMsg->type) {
    case(REPLY_RANGE): //start calculating perfect number when receiving valid range
      if(DBG) printf("[compute] receiving REPLY_RANGE from [manage]");
      pthread_create(&tid, &tattr, calcPerfect, (void*)readMsg);
      break;

    case(REQUEST_TERMINATE): //manage wants to terminate compute
      if(DBG) printf("[compute] receiving termination request from [manage]\n");
      pthread_mutex_lock(&mtx);
      computeManageBusy = true;//meaning no other compute<->manage interaction can happen
      pthread_mutex_unlock(&mtx);
      terminateByManage = true;
      teminationHandler(0);
      break;

    case(REQUEST_STATS): //manage forwards report request
      //set busy signal so compute won't send newly found perfect numbers 
      pthread_mutex_lock(&mtx);
      computeManageBusy = true;
      pthread_mutex_unlock(&mtx);
      
      struct toManageStruct message;
      message.type = REPLY_STATS; //need to check on the manage side
      message.value = numTested;
      message.currentNumber = currentNumber;
      message.currentRangeStart = currentRangeStart;
      message.currentRangeEnd = currentRangeEnd;
      if((stream=fdopen(s,"w")) == (FILE *) -1 ) {
	printf("[compute] failed to open fd. Line:%0d Error:%s\n",__LINE__,strerror(errno));
	exit(1);
      }

      xdrstdio_create(&handle,stream,XDR_ENCODE); 
      xdr_toManageStruct(&handle, &message);
      fflush(stream);
									
      pthread_mutex_lock(&mtx);
      computeManageBusy = false;
      pthread_cond_signal(&cond);
      pthread_mutex_unlock(&mtx);
      break;
    }
  }

  exit(0);
}


void teminationHandler(int signum){
  if(DBG) printf("[compute][termination handler] signal:%0d received\n", signum);
  struct toManageStruct msg;
  msg.type = (terminateByManage)?REPLY_TERMINATE: SUBMIT_TERMINATING_STATS;
  msg.value = numTested;
  msg.currentNumber = currentNumber;
  msg.currentRangeStart = currentRangeStart;
  msg.currentRangeEnd = currentRangeEnd;
  
  FILE *stream;
  if((stream=fdopen(s,"w")) == (FILE*) -1) {
    printf("[compute] failed to open fd. Line:%0d Error:%s\n",__LINE__,strerror(errno));
    exit(1);
  }

  if(signum==SIGINT) {
    printf("compute is terminating on SIGINT! ");
  } else if(signum==SIGHUP) {
    printf("compute is terminating on SIGHUP! ");
  } else if(signum==SIGQUIT){
    printf("compute is terminating on SIGQUIT! ");
  } else if(signum==0) {
    printf("compute is terminating by manage! ");
  }
  
  printf("the last number tested is %d\n",currentNumber);
  xdrstdio_create(&handle,stream,XDR_ENCODE); 				
  xdr_toManageStruct(&handle, &msg);
  fflush(stream);
  sleep(1);
  exit(0);

}

void* calcPerfect(void* arg_in){
  time(&startTime);
  struct toComputeStruct* calcRange = (struct toComputeStruct*) arg_in;
  if(DBG) printf("[compute] calcRangee start=%0d end=%0d \n",  calcRange->start,calcRange->end);
  currentRangeStart= calcRange->start;
  currentRangeEnd = calcRange->end;
  for(int num=calcRange->start;num<=calcRange->end;num++){
    numTested++;
    currentNumber = num;

    if(isPerfect(num)){
      //cannot send perfect numbers found while compute/manage are already interacting: querying/terminating
      pthread_mutex_lock(&mtx);
      while(computeManageBusy) {
	if(DBG) printf("[compute] waiting for computeManageBusy to be false\n");
	pthread_cond_wait(&cond,&mtx);
	if(DBG) printf("[compute] cond_wait triggered\n");
      }
      pthread_mutex_unlock(&mtx);

      //send found perfect numbers to manage
      FILE* stream;
      if((stream=fdopen(s,"w")) == (FILE *) -1 ) {
	printf("[compute] failed to open fd. Line:%0d Error:%s\n",__LINE__,strerror(errno));
	exit(1);
      }

      struct toManageStruct msg;
      msg.type = SUBMIT_PERFECT;
      msg.value = num;
      if(DBG) printf("[compute %0d] sending SUBMIT_PERFECT to manage pefect num found:%0d\n",getpid(), num);
      xdrstdio_create(&handle,stream,XDR_ENCODE); 
      xdr_toManageStruct(&handle, &msg);
      fflush(stream);
      sleep(1); 
    }
  }

  time(&stopTime);
  //request range again
  struct toManageStruct msg1;
  msg1.type = REQUEST_RANGE;
  msg1.value = calcRange->end+1; //start position
  msg1.time = difftime(stopTime,startTime); //so that manage can adjust the range porperly

  FILE *stream;
  if((stream=fdopen(s,"w")) == (FILE *) -1 ) {
    printf("[compute] failed to open fd. Line:%0d Error:%s\n",__LINE__,strerror(errno));
    exit(1);
  }

  if(DBG) printf("[compute] sending REQUEST_RANGE start:%0d time=%d \n", msg1.value, msg1.time);
  xdrstdio_create(&handle,stream,XDR_ENCODE);
  xdr_toManageStruct(&handle, &msg1);
  fflush(stream);
  
  pthread_exit(NULL);
}

bool isPerfect(int num){
  int  sum = 1;
  for(int i=2;i<num;i++){
    if(num%i==0) sum+=i;
  }
  return (num!=1) && (sum==num);
}
