#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(int argc, char* argv[])
{
    
    for(int i = 1; i < argc; i++) {
        printf("Argument %s\n", argv[i]);
    }
    int col = strtol(argv[1], NULL, 10);
    srand(time(NULL));
    float mass[col];
    
    printf("col = %d\n", col);
    for (int i = 0; i < col; i++){
        mass[i] = (float)rand()/RAND_MAX;
    }
    
    for (int i = 0; i < col; i++){
        printf("[%d] = %f\n", i, mass[i]);
    }
    return 0;
}
