#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include<malloc.h>

void Sort(float* x, int s){
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

int main(int argc, char* argv[])
{
    
    for(int i = 1; i < argc; i++) {
        printf("Argument %s\n", argv[i]);
    }
    float col = strtol(argv[1], NULL, 10);
    float arg1 = strtol(argv[2], NULL, 10);
    float arg2 = strtol(argv[3], NULL, 10);
    
    srand(time(NULL));
    
    float* mass;
    mass = (float*)malloc(sizeof(int) * col);
    
    for (int i = 0; i < col; i++){
        mass[i] = arg1 + (float)rand()/RAND_MAX * (arg2 - arg1);
    }
    
    for (int i = 0; i < col; i++){
        printf("%f ", mass[i]);
    }
    printf("\n");
    
    Sort(mass, col);
    FILE *file;
    file = fopen("text.txt", "w");
    
    for (int i = 0; i < col; i++){
        printf("%f ", mass[i]);
        fprintf(file, "%f ", mass[i]);
    }
    fclose(file);
    printf("\n");
    
    return 0;
}
