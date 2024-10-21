#include <stdio.h>
#include <stdlib.h>

typedef struct tag_obj {
    int data;
    struct tag_obj *next;
} obj;

obj *push(obj *top, int data)
{
    obj *ptr = malloc(sizeof(obj));
    ptr -> data = data;
    ptr -> next = top;
    return ptr;
}

obj* pop(obj *top)
{
    if (top == NULL){
        printf("Стек уже пуст\n");
        return top;
    }
    
    printf("Удаленный элемент: %d\n", top -> data);
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
            printf("%d\n", ptr -> data);
            ptr = ptr -> next;
        }
    }
}

void look(obj *top)
{
    if (top == NULL){
        printf("Стек пуст\n");
    }
    else{
        printf("Вверхнее значение стека = %d\n", top -> data);
    }
}

int main()
{
    obj *top = NULL;
    
    for (int i = 0; i < 10; i++){
        top = push(top, i);
    }
    
    show(top);
    
    for (int i = 0; i < 7; i++){
        top = pop(top);
    }
    show(top);
    
    look(top);
}
