#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main()
{
    srand(time(NULL));
    int col = rand()%10 + 1;
    float mass[col];
    float arg1;
    float arg2;
    printf("arg1 = ");
    scanf("%f", &arg1);
    printf("arg2 = ");
    scanf("%f", &arg2);
    
    printf("col = %d\n", col);
    for (int i = 0; i < col; i++){
        mass[i] = (float)rand()/RAND_MAX;
    }
    
    for (int i = 0; i < col; i++){
        printf("[%d] = %f\n", i, mass[i]);
    }
    return 0;
}
