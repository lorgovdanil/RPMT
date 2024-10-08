#include <stdio.h>

int main()
{
    FILE *file;
    
    char name[256];
    scanf("%[^\n]%*c", name);
    file = fopen("test.txt", "a");
    fputs("\n", file);
    fprintf(file, "%s", name);
    
    fclose(file);
}
