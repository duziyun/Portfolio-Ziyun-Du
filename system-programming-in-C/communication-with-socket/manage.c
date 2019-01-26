/*THIS CODE IS MY WORK, IT WAS WRITTEN WITHOUT CONSULTING A TUTOR OR CODE WRITTEN BY OTHERS STUDENTS
  Ziyun Du */
#include "defs.h"

toReportStruct computeStats[MAX_COMPUTE_CNT+1]; //first entry is -1
rangeNode* rangeListHead;

//socket
struct sockaddr_in socketin;
int s;
struct pollfd pollArray[MAX_PROCESS_CNT+1];
int fd;
struct hostent *hostentp;

FILE *stream;
XDR xdrHandle;

int globalRange; 
//int MINUS_ONE = ()
void teminationHandler(int signum);
void findRange(int start,struct toComputeStruct* writeMsg);
void requestStats(struct toComputeStruct* writeMsg, int i);

int main(int argc,char* argv[]){
  if(argc!=2) {
    printf("[manage] Incorrect argc seen for manage! Line:%0d\n", __LINE__);
    exit(1);
  }

  //initialize compute stats
  for(int i=0;i<MAX_COMPUTE_CNT+1;++i){
    computeStats[i].numberTested = 0;
    computeStats[i].perfectNumberIndex = 0;
    computeStats[i].fd = (int)-1;
  }

  //initialize range list
  rangeListHead = malloc(sizeof(rangeNode));
  rangeListHead->start = 0;
  rangeListHead->range = 0;
  rangeListHead->next = NULL;

  //sig
  signal(SIGINT,teminationHandler);
  signal(SIGQUIT, teminationHandler);
  signal(SIGHUP, teminationHandler);

  socketin.sin_addr.s_addr= INADDR_ANY;
  socketin.sin_port = atoi(argv[1]);

  if((s = socket(AF_INET,SOCK_STREAM,0)) < 0) {
    perror("[manage] failed to create socket!");
    exit(1);
  }

  if(bind (s, (struct sockaddr *) &socketin, sizeof (socketin)) <0) {
    perror("[manage] failed to bind socket to give address&port!");
    exit(2);
  }

  listen(s,MAX_PROCESS_CNT);

  //bound passive socket; only receive new connection requests
  pollArray[0].fd = s;     
  pollArray[0].events = POLLIN;

  for(int i=1;i<=MAX_PROCESS_CNT;++i){
    pollArray[i].fd = -1;
    pollArray[i].events = POLLIN;
  }

  while(true){
    //blocks until something to read
    poll(pollArray,MAX_PROCESS_CNT+1,-1);

    if(pollArray[0].revents & POLLIN){ //new connection request
      socklen_t len = sizeof(socketin);

      if ((fd= accept (s, (struct sockaddr *) &socketin, &len)) <0) {
	printf("[manage] failed to accept. Line:%0d Error:%s\n", __LINE__,strerror(errno));
	exit(1);
      }

      int idxToAlloc;
      //find the first unused entry to allocate the new connetion request
      for(idxToAlloc=1;idxToAlloc<=MAX_PROCESS_CNT;++idxToAlloc){
	if(pollArray[idxToAlloc].fd==-1){
	  break;
	}
      }

      pollArray[idxToAlloc].fd = fd;
      hostentp = gethostbyaddr((char *)&socketin.sin_addr.s_addr,sizeof(socketin.sin_addr.s_addr),AF_INET);
      strcpy(computeStats[idxToAlloc].hostName, hostentp->h_name);
    } else { //process allocated fd
      for(int i=1;i<=MAX_PROCESS_CNT;++i){
	if((pollArray[i].fd!=-1) && pollArray[i].revents) { 
	  fd = pollArray[i].fd;
				
	  struct toManageStruct readMsg;
				
	  if((stream=fdopen(fd,"r"))==(FILE*) -1 ) {
	    printf("[manage] failed to open fd. Line:%0d Error:%s\n", __LINE__,strerror(errno));
	    exit(1);
	  }
	  //decode the assocaited stream
	  xdrstdio_create(&xdrHandle,stream,XDR_DECODE); 
	  xdr_toManageStruct(&xdrHandle, &readMsg);
	  fflush(stream); //close the xdr stream

	  //REQUEST_RANGE: manage->compute range
	  struct toComputeStruct* writeMsg = malloc(sizeof(toComputeStruct));
	  
	  switch(readMsg.type) {

	  case(REQUEST_RANGE):
	    /***************************compute requests range***************************/					
	    if(DBG) printf("[manage] receiving REQUEST_RANGE from fd:%0d\n",fd);
	    computeStats[i].fd = pollArray[i].fd;

	    writeMsg->type = REPLY_RANGE;
						
	    if(readMsg.time==-1) { //first time compute(no time info)
	      globalRange = DEFAULT_RANGE; //fixed length for the first time
	      findRange(readMsg.value, writeMsg); 
	    }
	    else {

	      if(readMsg.time!=0) //avoid dividing by zero
		//adjust range targeting 10 s
		globalRange = (TARGET_TIME_PER_RANGE * computeStats[i].range) / (readMsg.time);
	      else
		globalRange=DEFAULT_RANGE;

	      if(DBG) printf("[manage] adjusted range to fd:%0d is %0d\n", fd,globalRange);
	      findRange(readMsg.value,writeMsg);
	    }
						
	    /*updating stat*/
	    computeStats[i].range = globalRange;
						
	    if ((stream=fdopen(fd,"w")) == (FILE *) -1 ) {
	      printf("[manage] failed to open fd. Line:%0d Error:%s\n", __LINE__,strerror(errno));
	      exit(1);
	    }
	    
	    if(DBG) printf("[manage] sending REPLY_RANGE to fd:%0d\n",fd);
	    xdrstdio_create(&xdrHandle,stream,XDR_ENCODE);						
	    xdr_toComputeStruct(&xdrHandle, writeMsg);
	    fflush(stream);
	    break;
	    /***********************end compute requests range***************************/
	    
	  case(SUBMIT_TERMINATING_STATS): //when compute is terminating itself
	    /***********************compute sends stats before terminating***************/
	    if(DBG) printf("[manage] receiving SUBMIT_TERMINATING_STATS from fd:%0d\n",fd);
	    computeStats[i].numberTested=readMsg.value;
	    computeStats[i].currentNumber = readMsg.currentNumber;
	    computeStats[i].currentRangeStart = readMsg.currentRangeStart;
	    computeStats[i].currentRangeEnd = readMsg.currentRangeEnd;	    
	    pollArray[i].fd = -1;
	    break;
	    /******************end  compute sends stats before terminating***************/

	  case(SUBMIT_PERFECT):
	    if(DBG) printf("[manage] receiving SUBMIT_PERFECT %10d from fd:%0d\n",readMsg.value,fd);
	    computeStats[i].perfectNumbers[computeStats[i].perfectNumberIndex] = readMsg.value;
	    computeStats[i].perfectNumberIndex++;
	    break;

	  case(REQUEST_STATS): //invoked by report
	    requestStats(writeMsg, i);
	    break;
	    
	  case(REQUEST_TERMINATE): //invoked by report -k 
	    requestStats(writeMsg, i);
	    teminationHandler(0);
	    break;
	  } //end of switch
	} 
      }
    }
  }
}

void teminationHandler(int signum){
  if(DBG) printf("[manage][termination handler] signal:%0d received\n", signum);
  struct toComputeStruct termMsg;
  termMsg.type = REQUEST_TERMINATE;
  termMsg.start =0;
  termMsg.end =0;
  
  for(int i=1;i<=MAX_PROCESS_CNT;++i){
    if(pollArray[i].fd!=-1){ //valid 
      //send termination request to compute
      FILE *stream;
      if((stream=fdopen(pollArray[i].fd,"w")) == (FILE *) -1 ) {
	printf("[manage] failed to open fd. Line:%0d Error:%s\n",__LINE__,strerror(errno));
	exit(1);
      }
      xdrstdio_create(&xdrHandle,stream,XDR_ENCODE);
      //send encoded terminate message to fd for corresponding compute to read
      xdr_toComputeStruct(&xdrHandle, &termMsg); 
      fflush(stream); //destroy the encoded stream

      //receive termination stats SUBMIT_TERMINATING_STATS from compute
      struct pollfd pfd[1];
      pfd[0].fd=pollArray[i].fd;
      pfd[0].events=POLLIN;
      poll(pfd, 1, -1); 
      struct toManageStruct termStats;
      if((stream=fdopen(pfd[0].fd,"r")) == (FILE*) -1) {
	printf("[manage] failed to open fd. Line:%0d Error:%s\n",__LINE__,strerror(errno));
	exit(1);
      }
      xdrstdio_create(&xdrHandle,stream,XDR_DECODE); 
      xdr_toManageStruct(&xdrHandle, &termStats);
      fflush(stream);
      if(DBG) printf("[manage][terimination handler] receiving SUBMIT_TERMINATING_STATS fd:%0d type:%0d tested num:%0d\n",fd, termStats.type, termStats.value);
      computeStats[i].numberTested = termStats.value; //FIXME:need to store other relevant stats 
      pollArray[i].fd = -1; 
    }
  }
  exit(0);
}

//find the proper range for a compute
void findRange(int start, struct toComputeStruct* writeMsg){
  rangeNode* iter = rangeListHead; //head is a dummy node

  while(true){
    if(iter->next==NULL){//append to the tail
      rangeNode* temp = malloc(sizeof(rangeNode));
      iter->next = temp;
      temp->start = start;
      temp->range =  globalRange;
      temp->next = NULL;
      writeMsg->start = start;
      writeMsg->end = start + globalRange;
      break;
    } else if(start < iter->next->start){ //insert to left of the next node if start is before next.start 

      rangeNode* temp = malloc(sizeof(rangeNode));
      temp->next = iter->next;
      iter->next = temp;
      temp->start = start;

      if((start+globalRange) >= iter->next->start) { //insert partial range until next.start-1
	globalRange = temp->next->start - start - 1;
      }

      temp->range = globalRange;
      writeMsg->start = start;
      writeMsg->end = start +globalRange;
      break;
    } else if(start>=iter->next->start){

      if(start <= (iter->next->start + iter->next->range)) {
	start = iter->next->start + iter->next->range + 1;//change the start number}
      }
      iter = iter->next;
    }
  }//while(true)

}

void requestStats(struct toComputeStruct* writeMsg, int i){
  writeMsg->type = REQUEST_STATS;
  writeMsg->start =0;
  writeMsg->end =0;
  pollArray[i].fd = -1; //since global fd holds report's fd
  if(DBG) printf("[manage] receiving REQUEST_STATS form report\n");
  
  for(i=1; i<=MAX_PROCESS_CNT; i++) {						
    if(pollArray[i].fd!=-1) {
      //send REQUEST_STATS to all computes
      if ((stream=fdopen(pollArray[i].fd,"w")) == (FILE *) -1 ) {
	printf("[manage] failed to open fd. Line:%0d Error:%s\n", __LINE__,strerror(errno));
	exit(1);
      }							
      xdrstdio_create(&xdrHandle,stream,XDR_ENCODE);
      xdr_toComputeStruct(&xdrHandle, writeMsg);							
      fflush(stream);

      //wait for compute returns stats typed as REPLY_STATS
      struct pollfd poller[1];
      poller[0].fd=pollArray[i].fd;
      poller[0].events=POLLIN;
      poll(poller, 1, -1); 

      struct toManageStruct numtestmsg;
      
      if ((stream=fdopen(poller[0].fd,"r")) == (FILE *) -1 ) {
	printf("[manage] failed to open fd. Line:%0d Error:%s\n", __LINE__,strerror(errno));
	exit(1);
      }
							
      xdrstdio_create(&xdrHandle,stream,XDR_DECODE);
      xdr_toManageStruct(&xdrHandle, &numtestmsg);
							
      fflush(stream);

      computeStats[i].numberTested = numtestmsg.value;
      computeStats[i].currentNumber = numtestmsg.currentNumber;
      computeStats[i].currentRangeStart = numtestmsg.currentRangeStart;
      computeStats[i].currentRangeEnd = numtestmsg.currentRangeEnd;
    }
  }

  //send valid compute's stats to report
  for(int i=1;i<=MAX_COMPUTE_CNT;++i){

    if(computeStats[i].fd >= ((int)0)) {

      if ((stream=fdopen(fd,"w")) == (FILE *) -1 ) {
	printf("[manage] failed to open fd. Line:%0d Error:%s\n",__LINE__,strerror(errno));
	exit(1);
      }
							
      xdrstdio_create(&xdrHandle,stream,XDR_ENCODE);
      xdr_toReportStruct(&xdrHandle, &computeStats[i]);
      fflush(stream);
      sleep(1); //let report read it
    }
  }

  //signal the end of transmission
  struct toReportStruct endofData;
  endofData.fd=-1;
  if ((stream=fdopen(fd,"w")) == (FILE *) -1 ) {
    perror("fdopen:");
    exit(1);
  }
					
  xdrstdio_create(&xdrHandle,stream,XDR_ENCODE); 
  xdr_toReportStruct(&xdrHandle, &endofData);
  fflush(stream);				
  if(DBG) printf("[manage] exiting REQUEST_STATS from report\n");
}
