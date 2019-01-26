/*THIS CODE IS MY WORK, IT WAS WRITTEN WITHOUT CONSULTING A TUTOR OR CODE WRITTEN BY OTHERS STUDENTS
 Ziyun Du */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <ctype.h>
#include <stdbool.h>

#define MAX_WORD_LEN 30
#define MIN_WORD_LEN 4
#define MAX_INPUT_LEN 4096

void parser(int** parser2SorterFd);
void sorter(int** parser2SorterFd, int** sorter2MergerFd);
void merger(int** sorter2MergerFd); 

int numSorter=1;

int main(int argc, char** argv){
  if(argc>1){
    numSorter = atoi(argv[1]);
  }
  int** parser2SorterFd = malloc(numSorter*sizeof(int *));
  int** sorter2MergerFd = malloc(numSorter*sizeof(int *));
  for(int i=0;i<numSorter;i++){
    parser2SorterFd[i] = malloc(2*sizeof(int*));
    sorter2MergerFd[i] = malloc(2*sizeof(int*));
  }

  //spawn sorter process before parser writes to the pipe
  sorter(parser2SorterFd,sorter2MergerFd);
  parser(parser2SorterFd);
  merger(sorter2MergerFd);

  for(int sorterId=0;sorterId<numSorter;++sorterId){
    close(parser2SorterFd[sorterId][1]);
    wait(NULL);
  }
  return 0;
}

void parser(int** parser2SorterFd){
  FILE** parser2SorterStream = malloc(numSorter*sizeof(FILE*)); 
  for(int sorterId=0;sorterId<numSorter;++sorterId){
    parser2SorterStream[sorterId] = fdopen(parser2SorterFd[sorterId][1],"w");

    if(!parser2SorterStream[sorterId]){
      fprintf(stderr, "[parser] Failed to create file stream\n");
      exit(1);
    }
  }

  char buf[MAX_INPUT_LEN];
  int sorterId = 0;
  
  while(fgets(buf,MAX_INPUT_LEN,stdin)){

    for(int i=0;i<strlen(buf);++i){
      if(isalpha(buf[i])){
	buf[i] = tolower(buf[i]);
      } else {//all non-alphabetic char delimit words
	buf[i] = ' '; //to split by space
      }
    }
    
    char* token = strtok(buf, " ");
    while(token!=NULL){
      char word[strlen(token)+2];//add new line in the end for sorting and string terminator
      int  index=0;

      for(int i=0;i<strlen(token)&&i<MAX_WORD_LEN;++i){
	word[index++] = token[i];
      }
      
      word[index] = '\n';
      word[index+1] = 0; //terminates the string
      
      if(index>=MIN_WORD_LEN){
	fputs(word,parser2SorterStream[sorterId]);
      }
      sorterId++;
      sorterId %= numSorter;
      token = strtok(NULL, " ");      
    }
  }

  for(int i=0;i<numSorter;++i){
    //close pipe so after writing all inputs that children can exit once it close the write end and read all pipe
    fclose(parser2SorterStream[i]);
  }
}

void sorter(int** parser2SorterFd, int** sorter2MergerFd){
  int pid=0;

  for(int sorterId=0; sorterId<numSorter; sorterId++){
    if(pipe(parser2SorterFd[sorterId])==-1){
      fprintf(stderr, "Failed to create pipe\n");
      exit(EXIT_FAILURE);
    }

    if(pipe(sorter2MergerFd[sorterId])==-1){
      fprintf(stderr, "Failed to create pipe\n");
      exit(EXIT_FAILURE);
    }

    pid = fork();
    switch(pid){
    case 0:
      //since sort read from stdin and write to stdout thus need to direct input pipe to std and direct stdout to output pipe
      dup2(parser2SorterFd[sorterId][0],STDIN_FILENO);
      dup2(sorter2MergerFd[sorterId][1],STDOUT_FILENO);

      //close the other end of the pipe
      close(parser2SorterFd[sorterId][1]);
      close(sorter2MergerFd[sorterId][0]);

      //wait until the input is done for this pipe
      //meaning write pipe is closed (only when parser writes all the input)and pipe are empty
      close(parser2SorterFd[sorterId][0]);
      close(sorter2MergerFd[sorterId][1]);

      //program name, argument lists
      execl("/usr/bin/sort","sort",(char*) NULL);
      _exit(EXIT_FAILURE);
      break;

    case -1:
      fprintf(stderr, "Failed to spawn sorter process\n");
      exit(EXIT_FAILURE);
      break;

    default:
      close(parser2SorterFd[sorterId][0]);
      close(sorter2MergerFd[sorterId][1]);
      break;
    }
  }
}

void merger(int **sorter2MergerFd){
  int pid;
  char** heads;
  FILE** sorter2MergerStream;
  switch(pid = fork()) {
  case 0:

    heads =  malloc(numSorter*sizeof(char*)); //store the head of each sorter->merger pipe
    sorter2MergerStream = malloc(numSorter*sizeof(FILE*));

    for(int sorterId=0; sorterId<numSorter; sorterId++){
      sorter2MergerStream[sorterId] = fdopen(sorter2MergerFd[sorterId][0],"r");

      if(!sorter2MergerStream[sorterId]){
	fprintf(stderr, "[merger]Failed to create file stream\n");
	exit(1);
      }

      heads[sorterId] = malloc((MAX_WORD_LEN+2)*sizeof(char));
      //heads always keep track of the head of each pipe
      if(fgets(heads[sorterId],MAX_WORD_LEN+2,sorter2MergerStream[sorterId])==NULL){
	heads[sorterId] = NULL;
      } 
    }

    char* cur = NULL;
    int cnt = 1;
    bool done = false;

    while(!done){
      //find the smallest word in heads
      int smallestIdx = 0;
      
      while(smallestIdx<numSorter && heads[smallestIdx]==NULL){
	smallestIdx++;
      }
    
      if(smallestIdx==numSorter) {//exit when all pipes are empty
	done = true;
	break;
      }
    
      for(int sorterId=smallestIdx+1; sorterId<numSorter; sorterId++){
	if(heads[sorterId]==NULL) continue;
	if(strcmp(heads[smallestIdx],heads[sorterId])>0) {//cur precedes smallest
	  smallestIdx = sorterId;
	}
      } //now smallestIdx indexes the smallest among the heads
      
      char smallestHead[MAX_WORD_LEN+1];

      for(int i=0;i<=MAX_WORD_LEN;i++){
	if(heads[smallestIdx][i]=='\n') {
	  smallestHead[i] = 0;
	  break;
	} else {
	  smallestHead[i] = heads[smallestIdx][i];
	}
      }
      
      if(cur==NULL) {
	cur =  malloc((MAX_WORD_LEN+1)*sizeof(char));
	strcpy(cur,smallestHead);
      } else {
	if(strcmp(cur,smallestHead)==0){
	  cnt++;
	} else {
	  printf("%5d %s\n", cnt,cur);
	  cnt=1;
	  strcpy(cur,smallestHead);
	}      
      }
      
      if(fgets(heads[smallestIdx],MAX_WORD_LEN+2,sorter2MergerStream[smallestIdx])==NULL){
	heads[smallestIdx] = NULL;
      } 
    }
        
    printf("%5d %s\n", cnt,cur); //to print the last one
    fflush(stdout);
    for(int sorterId=0; sorterId<numSorter; sorterId++){
      fclose(sorter2MergerStream[sorterId]);
    }
    _exit(EXIT_FAILURE);
    break;
  case -1:
    fprintf(stderr, "Failed to spawn sort process\n");
    exit(EXIT_FAILURE);
  default:
    waitpid(pid,NULL,0);
    break; 
  }
}
