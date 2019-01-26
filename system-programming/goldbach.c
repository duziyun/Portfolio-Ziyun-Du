//  goldbach.c
//  Assignment0
//  Created by 杜紫芸 on 9/5/18.
//  Copyright © 2018 Ziyun. All rights reserved.
/*THIS CODE IS MY WORK, IT WAS WRITTEN WITHOUT CONSULTING A TUTOR OR CODE WRITTEN BY OTHERS STUDENTS
  Ziyun Du */
#include <stdlib.h>
//#include "goldbach.h"
#include <stdio.h>
#include<limits.h>

typedef struct _seg {
  int  bits[256];;
  struct _seg  *next,*prev;
}seg  ;

seg* head;
seg* p;
int count;
int CountHowmany(int N){

  if(N<=3){
    return 0;
  } else {
    int mod=((N-3)/2+1)%(256*32);
    int n=((N-3)/2+1)/(256*32);

    if(mod==0){
      return n;
    } else{
      return n+1;
    }
  }
  
}

int transfer(int j){
  return (j-3)/2+1;
}

seg* whichseg(int j){
  int c=transfer(j);
  int index;
  if(c%(256*32)==0){
    index=c/(256*32);
  }
  else{
    index=c/(256*32)+1;
  }
  int d=index-count;
  if(d==0){
    return p;
  }
  else if(d>0){
    for(int i=0;i<d;i++){
      p=p->next;
      count++;
    }
  }
  else{
    for(int i=0;i<d*(-1);i++){
      //printf("now pointer in on #%d seg\n",count);
      p=p->prev;
      count--;
    }
  }
  return p;
}

int whichint(int j){
  int c=transfer(j);
  whichseg(j);
  int before=count-1;
  int diveder=(c-256*32*before);
  int mod=diveder%32;
  //int index;
  if(mod==0){
    return diveder/32-1;
  }
  else{
    return diveder/32;
  }
}

int whichbit(int j){
  int c=transfer(j);
  int before=count-1;
  //int index;
  int diveder=(c-before*256*32-whichint(j)*32);
  int mod=diveder%32;
  if(mod==0){
    return 31;
  }
  else{
    return diveder%32-1;
  }
}

int testprime(int j){
  int indexofint=whichint(j);
  int thisint=p->bits[indexofint];
  int thisbit=whichbit(j);
  int set=thisint & (1<<thisbit);
  if(set==0) return 0;
  else return 1;
}

void markcomposite(int j){
  int indexofint=whichint(j);
  int thisint=p->bits[indexofint];
  int thisbit=whichbit(j);
  p->bits[indexofint]=thisint|(1<<thisbit);
}

void seive(int N){
  for(int i=3;i*i<=N; i=i+2){
    //int c=transfer(i);
    if(testprime(i)==0){
      // printf("%d is prime\n",i);
      for(int k=i*i;k<=N;k=k+i){
	if(k%2==0) continue;
	markcomposite(k);
	// printf("mark %d as composite\n",k);
      }
    }
  }
}

int countprimes(int N){
  int com=0;
  seg* start=head;

  for(int x=0;x<CountHowmany(N);x++){
    for(int i=0;i<256;i++){
      int thisint=(*start).bits[i];
      while(thisint!=0){
	thisint=thisint & (thisint-1);
	com++;
      }
    }
    start=start->next;
  }
  
  //printf("# of composites is %d\n",com);
  int c=transfer(N);

  if(N%2==0){
    return c-com;
  } else if(testprime(N)==0) {
    return c-com-1;
  } else {
    return c-com;
  }
}

void allocate(int N){
  int howmany = CountHowmany(N);
  seg* pt;
  pt=head;

  for (int i=1;i<howmany;i++) {
    seg* nextseg=(  seg *) malloc(sizeof (seg));
    pt->next =nextseg;
    nextseg->prev=pt;
    pt=pt->next;
    for(int i=0;i<256;i++){
      (*pt).bits[i]=0;
    }
  }
  
}

void getlargestsolution(int even){
  int half=((even-3)/2+1)/2;
  int step=0;
  int left=1;
  int right=0;
  int maxleft=0;
  int maxright=0;
  seg* start=head;
  int startint=0;
  int startbit=0;
  seg* end=whichseg(even-3);
  int endint=whichint(even-3);
  int endbit=whichbit(even-3);
  int nofsolution=0;

  while(step<half){
    left=left+2;
    right=even-left;
    int thisleft=start->bits[startint];
    int setleft=thisleft&(1<<startbit);
    int thisright=end->bits[endint];
    int setright=thisright&(1<<endbit);

    if(setleft==0 && setright==0){
      maxleft=left;
      maxright=right;
      nofsolution++;
    }
        
    if(startbit==31){
      startbit=0;
      if(startint==255){
	start=start->next;
	startint=0;
      }
      else{
	startint=startint+1;
      }
            
    }
    else{
      startbit=startbit+1;
    }
    if(endbit==0){
      endbit=31;
      if(endint==0){
	endint=255;
	end=end->prev;
      }
      else{
	endint=endint-1;
      }
    }
    else{
      endbit=endbit-1;
    }
        
    step++;
  }
  printf("Largest %d =  %d + %d out of %d solutions\n" ,even,maxleft,maxright,nofsolution);
}

int main(int argc, char * argv[]) {
  count=1;
  head= (  seg * ) malloc(sizeof(seg));

  for(int i=0;i<256;i++){
    (*head).bits[i]=0;
  }

  p=head;
  int test;

  if(argc==2) sscanf(argv[1],"%d",&test);
  else return 0;
    
  printf("Calculating odd primes up to %d......\n",test);

  allocate(test);
  whichseg(test);
  seive(test);
  
  int x=countprimes(test);
  printf("Found %d odd primes\n",x);
  int even=0;
  printf("Enter even number >5 for goldbach test:\n");
  while(!feof(stdin)){
    even=-727123199;
    scanf("%d",&even);
    if(even==-727123199) break;
    if(even%2==1 || even<0){
      printf("Please enter a even number >5\n");
    }
    else{
      getlargestsolution(even);
    }
  }
  return 0;
}

