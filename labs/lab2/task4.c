#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main()
{
    srand(time(NULL));
    int col = rand()%10 + 3;
    float mass[col];
    float arg1;
    float arg2;
    printf("arg1 = ");
    scanf("%f", &arg1);
    printf("arg2 = ");
    scanf("%f", &arg2);
    
    printf("col = %d\n", col);
    for (int i = 0; i < col; i++){
        mass[i] = arg1 + (float)rand()/RAND_MAX * (arg2 - arg1);
    }
    
    Sort(mass, col);
    
    for (int i = 0; i < col; i++){
        printf("[%d] = %f\n", i, mass[i]);
    }
    return 0;
}
void Sort(float x[], int s){
    int stop;
    stop = 0;
    while(stop != 1){
        stop = 1;
        for(int i = 0; i < s - 1; i++){
            if (x[i] > x[i + 1]){
                x[i] = x[i] + x[i + 1];
                x[i + 1] = x[i] - x[i + 1];
                x[i] = x[i] - x[i + 1];
                stop = 0;
            }
        }
    }
}
