#include <stdio.h>

struct product {
    char name[20];
    int cost; 
};

void Sort(struct product *commodity, int col){
    int stop;
    stop = 0;
    while(stop != 1){
        stop = 1;
        for(int i = 0; i < col - 1; i++){
            if (commodity[i].cost > commodity[i + 1].cost){
                struct product thing = commodity[i];
                commodity[i] = commodity[i+1];
                commodity[i+1] = thing;
                stop = 0;
            }
        }
    }
}

int main()
{
    FILE *file1;
    FILE *file2;
    
    file1 = fopen("data.txt", "r");
    if (file1 == NULL){
        printf("Файл не открылся\n");
    }
    
    int number = 0;
    char str;
    while ((str = fgetc(file1)) != EOF){
        if (str == '\n'){
            number = number + 1;
        }
    }
    printf("Количество товаров = %d\n", number);
    struct product goods[number];
    
    fseek(file1, 0, SEEK_SET);
    for(int i = 0; i < number; i++) {
        fscanf(file1, "%s %d", goods[i].name, &(goods[i].cost));
        printf("%s %d\n", goods[i].name, goods[i].cost);
    }
    
    
    Sort(goods, number);
    
    file2 = fopen("product.txt", "w");
    if (file2 == NULL){
        printf("Файл не открылся\n");
    }
    
    for (int i = 0; i < number; i++){
        fprintf(file2, "%s %d\n", goods[i].name, goods[i].cost);
    }
    
    fclose(file1);
    fclose(file2);
}
