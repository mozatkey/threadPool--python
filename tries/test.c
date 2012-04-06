#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *args){
  int x, y; 
  x = (int)(args[1]);
  y = (int)(args[2]);
  printf ("x&y:%d\n", !(x&y|y));
#if 1
  printf ("MAX_PEER_FAILED:%d\n", atoi(getenv("MAX_PEER_FAILED")));
#endif
  
}
