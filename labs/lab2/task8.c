#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct tag_obj {
    char *data;
    struct tag_obj *next;
} obj;

obj *push(obj *top, char *data) 
{
    obj *ptr = malloc(sizeof(obj));
    ptr -> data = strdup(data);
    ptr -> next = top;
    return ptr;
}

obj *pop(obj *top) 
{
    if (top == NULL) {
        return top;
    }

    obj *ptr = top -> next;
    if (top->data[0] != '(') {
        printf("%s ", top -> data);
    } 
    free(top);

    return ptr;
}

void show(obj *top) 
{
    if (top == NULL) {
        printf("Стек пуст\n");
    } 
    else{
        printf("Весь стек\n");
        obj *ptr = top;
        while (ptr != NULL) {
            printf("%s\n", ptr -> data);
            ptr = ptr -> next;
        }
    }
}

char *look(obj *top) 
{
    if (top == NULL) {
        return NULL;
    } 
    else {
        return top -> data;
    }
}

int main() {
    obj *top = NULL;
    FILE *file = fopen("file.txt", "r");
    if (file == NULL) {
        printf("Файл не открылся\n");
        return 1;
    }

    char str[256];
    while (fscanf(file, "%s", str) != EOF) {
        if (atof(str) != 0.0) {
            printf("%d ", (int)atof(str));
        } 
        else{
            char *a = look(top);
            if (strcmp(str, "(") == 0) {
                top = push(top, str);
            } 
            else if (strcmp(str, ")") == 0) {
                while (a != NULL && strcmp(a, "(") != 0) {
                    top = pop(top);
                    a = look(top);
                }
                if (a != NULL && strcmp(a, "(") == 0) {
                    top = pop(top);
                }
            } 
            else if (strcmp(str, "+") == 0 || strcmp(str, "-") == 0) {
                while (a != NULL && strcmp(a, "(") != 0) {
                    top = pop(top);
                    a = look(top);
                }
                top = push(top, str);
            } 
            else if (strcmp(str, "*") == 0 || strcmp(str, "/") == 0) {
                while (a != NULL && strcmp(a, "(") != 0 && strcmp(a, "+") != 0 && strcmp(a, "-") != 0) {
                    top = pop(top);
                    a = look(top);
                }
                top = push(top, str);
            }
        }
    }
    top = pop(top);
    fclose(file);

    return 0;
}
