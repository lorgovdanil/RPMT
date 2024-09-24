#include <stdio.h>

int main()
{
    FILE *file;
    
    char name[256];
    scanf("%s", name);
    file = fopen(name, "r");
    char str[256];
    while(fgets(str, 256, file) != NULL){
        printf("%s", str);
    }

    fclose(file);
}
