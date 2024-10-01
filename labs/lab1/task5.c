#include <stdio.h>

int main(int argc, char *argv[])
{
    FILE *file;
    
    char *name = argv[1];
    
    file = fopen(name, "r");
    char str[256];
    while(fgets(str, 256, file) != NULL){
        printf("%s", str);
    }

    fclose(file);
}
