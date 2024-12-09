%{
#include <stdio.h>
int yylex();
void yyerror(char* str);
int main(int argc, char** argv);
%}
%token NUMBER
%token PLUS MINUS
%token END
%%
expression: %empty   
    | expression exp END { printf(" = %d\n", $2); }
    ;
exp: NUMBER
    | exp PLUS NUMBER    { $$ = $1 + $3; }
    | exp MINUS NUMBER    { $$ = $1 - $3; }
    ;
%%
void yyerror(char* str) {
    fprintf(stderr, "[ERROR]: %s\n", str);
}
int main(int argc, char** argv) {
    yyparse();
    return 0;
}
