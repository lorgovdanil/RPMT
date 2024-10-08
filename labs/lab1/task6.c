#include <stdio.h>

int main()
{
    FILE *file1;
    FILE *file2;
    
    char name[256];
    scanf("%s", name);
    file2 = fopen(name, "w");
    
    file1 = fopen("text.txt", "r");
    char str[256];
    for(int i = 0; i < 3; i = i + 1){
        fgets(str, 256, file1);
        fprintf(file2, "%s", str);
    }

    fclose(file1);
    fclose(file2);
}
