#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct tag_obj {
    float data;
    struct tag_obj *next;
} obj;

obj *push(obj *top, float data)
{
    obj *ptr = malloc(sizeof(obj));
    ptr -> data = data;
    ptr -> next = top;
    return ptr;
}

obj *pop(obj *top)
{
    if (top == NULL){
        printf("Стек уже пуст\n");
        return top;
    }
    
    obj *ptr = top -> next;
    free(top);
    
    return ptr;
}

void show(obj *top)
{
    if (top == NULL){
        printf("Стек пуст\n");
    }
    else{
        printf("Весь стек\n");
        obj *ptr = top;
        while (ptr != NULL) {
            printf("%f\n", ptr -> data);
            ptr = ptr -> next;
        }
    }
}

float look(obj *top)
{
    if (top == NULL){
        printf("Стек пуст\n");
    }
    else{
        return top -> data;
    }
}

int main()
{
    obj *top = NULL;
    FILE *file;
    file = fopen("file.txt", "r");
    if (file == NULL){
        printf("Файл не открылся\n");
    }
    
    char str[256];
    while (fscanf(file,"%s",str) != EOF){
        if(atof(str) != 0.0){
            top = push(top, atof(str));
        }
        else{
            if (strcmp(str, "+") == 0){
                float x = look(top);
                top = pop(top);
                float y = look(top);
                top = pop(top);
                top = push(top, x + y);
            }
            if (strcmp(str, "-") == 0){
                float y = look(top);
                top = pop(top);
                float x = look(top);
                top = pop(top);
                top = push(top, x - y);
            }
            if (strcmp(str, "*") == 0){
                float x = look(top);
                top = pop(top);
                float y = look(top);
                top = pop(top);
                top = push(top, x * y);
            }
            if (strcmp(str, "/") == 0){
                float y = look(top);
                top = pop(top);
                float x = look(top);
                top = pop(top);
                top = push(top, x / y);
            }
        }
    }
    show(top);
}
