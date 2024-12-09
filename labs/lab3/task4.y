%{
#include <stdio.h>
#include <stdlib.h>
int yylex();
void yyerror(char* str);
int main(int argc, char** argv);
%}
%union {
    float floatVal;
}
%token <floatVal> NUMBER
%token PLUS MINUS MULT DIV
%token OPENBRACK CLOSEBRACK
%token END
%%
expression: %empty
    | expression exp END { printf("\n"); }
    ;
exp: term
    | exp PLUS term    { printf("+ "); }
    | exp MINUS term    { printf("- "); }
    ;
term: factor
    | term MULT factor { printf("* "); }
    | term DIV factor  { printf("/ "); }
factor: NUMBER  { printf("%f ", $1); }
    | OPENBRACK exp CLOSEBRACK {}
    ;
%%
void yyerror(char* str) {
    fprintf(stderr, "[ERROR]: %s\n", str);
}
int main(int argc, char** argv) {
    yyparse();
    return 0;
}
