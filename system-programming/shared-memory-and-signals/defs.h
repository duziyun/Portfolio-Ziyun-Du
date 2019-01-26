/* input honor code here*/
#include <string.h>
#include <stdbool.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/shm.h>
#include <sys/msg.h>
#include <signal.h>
#include <errno.h>
#include <setjmp.h>

/*THIS CODE IS MY WORK, IT WAS WRITTEN WITHOUT CONSULTING A TUTOR OR CODE WRITTEN BY OTHERS STUDENTS
 Ziyun Du */
#define KEY 73698
#define PERFECT_ARRAY_SIZE 20
#define COMPUTE_ARRAY_SIZE 20
#define BIT_MAP_SIZE 33554432 //0~size-1
//#define BIT_MAP_SIZE 10000
#define INT_SIZE   32
#define INT_PER_SEGMENT 256
#define SEGMENT_CNT BIT_MAP_SIZE/(INT_PER_SEGMENT*INT_SIZE)
#define MAX_DEAD_COMPUTES 100
#define INIT_TYPE 1
#define FOUND_TYPE 2
#define KILL_TYPE 3
#define INIT_DONE_TYPE 4
#define DBG_ON false

int errno;

typedef struct{
  int pid;
  int numberOfPerfectFound;
  int numberOfCanTested;
  long numberOfCanSkipped;
} computeAttributes;

typedef struct{
  int bitmap[SEGMENT_CNT][INT_PER_SEGMENT];//memory leak; bug
  int perfectNumbers[PERFECT_ARRAY_SIZE];
  computeAttributes computeStats[COMPUTE_ARRAY_SIZE+1]; //for active computes and dead computes
} memorySegment;

typedef struct{
  long type;
  int data;
} myMsg;
