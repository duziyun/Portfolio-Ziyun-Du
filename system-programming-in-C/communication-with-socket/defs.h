/*THIS CODE IS MY WORK, IT WAS WRITTEN WITHOUT CONSULTING A TUTOR OR CODE WRITTEN BY OTHERS STUDENTS
 Ziyun Du */
#include <unistd.h>
#include <signal.h>
#include <errno.h>
#include <setjmp.h>
#include <arpa/inet.h>
#include <ctype.h>
#include <netdb.h>
#include <poll.h>
#include <errno.h>
#include <sys/types.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <time.h>
#include <stdbool.h>
#include <pthread.h>

#include "structs.h"

#define REQUEST_RANGE 1
#define REPLY_RANGE 2
#define REQUEST_STATS 3
#define REPLY_STATS 4
#define SUBMIT_PERFECT 5
#define REQUEST_TERMINATE 6
#define SUBMIT_TERMINATING_STATS 7
#define REPLY_TERMINATE 8

#define MAX_PROCESS_CNT 30
#define MAX_COMPUTE_CNT 20
#define MAX_REPORT_CNT  10
#define MAX_PERFECT_CNT 10
#define DEFAULT_RANGE 20000
#define TARGET_TIME_PER_RANGE 10

#define DBG false
typedef struct rangeNode { 
  int start; //init
  int range; //offset
  struct rangeNode *next;
}rangeNode;
