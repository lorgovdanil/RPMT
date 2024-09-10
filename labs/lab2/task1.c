#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main()
{
    srand(time(NULL));
    int col = rand()%10 + 1;
    int mass[col];
    
    for (int i = 0; i < col; i++){
        mass[i] = rand()%100;
    }
    
    for (int i = 0; i < col; i++){
        printf("[%d] = %d\n", i, mass[i]);
    }
    return 0;
}
