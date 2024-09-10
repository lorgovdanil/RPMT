#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main()
{
    srand(time(NULL));
    int col = rand()%10 + 1;
    int mass[col];
    
    printf("col = %d\n", col);
    for (int i = col - 1; i >= 0; i--){
        mass[i] = rand()%100;
    }
    
    for (int i = 0; i < col; i++){
        printf("[%d] = %d\n", i, mass[i]);
    }
    return 0;
}
