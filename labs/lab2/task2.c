#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main()
{
    srand(time(NULL));
    int col = rand()%10 + 1;
    int mass[col];
    
    printf("col = %d\n", col);
    for (int i = 0; i < col; i++){
        mass[i] = rand()%100 - 50;
    }
    FILE *file;
    file = fopen("file", "a");
    for (int i = col - 1; i >= 0; i--){
        fprintf(file,"%d\n", mass[i]);
    }
    fclose(file);
    return 0;
}
