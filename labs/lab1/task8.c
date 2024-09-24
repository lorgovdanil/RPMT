#include <stdio.h>
#include <string.h>

int main()
{
    FILE *file1;
    FILE *file2;
    
    file1 = fopen("test.txt", "a+");
    file2 = fopen("vitaly.txt", "a+");
    
    char str[256];
    scanf("%s", str);
    
    char pr[256];
    fprintf(file2, "%s", str);
    while(fgets(pr, 256, file1) != NULL){
        fprintf(file2, "%s", pr);
    }
    
    
    fclose(file2);
    fclose(file1);
}
