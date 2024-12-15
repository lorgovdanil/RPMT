
#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
const char* input;
char l;
void expr();
void exprRest();
void term();
void termRest();
void factor();
void match(char expected);
void error();
void getNextToken() {
    l = *input++;
}
void match(char expected) {
    if (l == expected) {
        getNextToken();
    } else {
        error();
    }
}
void error() {
    printf("Error\n");
    exit(1);
}
int main() {
    printf("Введите инфиксное выражение: ");
    char buffer[100];
    fgets(buffer, sizeof(buffer), stdin);
    input = buffer;
    getNextToken();
    expr();
    printf("\n");
    return 0;
}
void expr() {
    term();
    exprRest();
}
void exprRest() {
    if (l == '+') {
        match('+');
        term();
        printf("+");
        exprRest();
    } else if (l == '-') {
        match('-');
        term();
        printf("-");
        exprRest();
    }
}
void term() {
    factor();
    termRest();
}
void termRest() {
    if (l == '*') {
        match('*');
        factor();
        printf("*");
        termRest();
    } else if (l == '/') {
        match('/');
        factor();
        printf("/");
        termRest();
    }
}
void factor() {
    if (isdigit(l)) {
        printf("%c",l);
        match(l);
    } else if (l == '(') {
        match('(');
        expr();
        match(')');
    } else {
        error();
    }
}
