#define MAX_COMPUTE_CNT 20
#define MAX_PERFECT_CNT 10
struct toManageStruct {
  int type; 
  int value;
  int time;
  int currentNumber;
  int currentRangeEnd;
  int currentRangeStart;
};

struct toComputeStruct {
  int type;
  int start;
  int end;
};

struct toReportStruct {
  char hostName[MAX_COMPUTE_CNT];
  int fd;
  int perfectNumbers[MAX_PERFECT_CNT];
  int perfectNumberIndex;
  int numberTested;
  int range;
  int currentRangeStart;
  int currentRangeEnd;
  int currentNumber;
};
