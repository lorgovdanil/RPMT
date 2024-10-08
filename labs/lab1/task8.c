#include <stdio.h>

int main()
{
    FILE *file1;
    FILE *file2;
    
    file1 = fopen("test.txt", "a+");
    file2 = fopen("work.txt", "a+");
    
    char str[256];
    scanf("%[^\n]%*c", str);
    
    char pr[256];
    fprintf(file2, "%s", str);
    while(fgets(pr, 256, file1) != NULL){
        fprintf(file2, "%s", pr);
    }
    fclose(file2);
    file2 = fopen("work.txt", "r");
    
    fclose(file1);
    file1 = fopen("test.txt", "w");
    fclose(file1);
    file1 = fopen("test.txt", "a");
    
    while(fgets(pr, 256, file2) != NULL){
        fprintf(file1, "%s", pr);
    }
    
    fclose(file2);
    fclose(file1);
    remove("work.txt");
}
