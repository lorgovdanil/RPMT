#include <stdio.h>

int main()
{
    FILE *file;
    
    char name[256];
    scanf("%s", name);
    file = fopen("test.txt", "a");
    fprintf(file, "%s", name);
    
    fclose(file);
}
