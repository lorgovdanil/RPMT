%{
#include <stdio.h>
int yylex();
void yyerror(char* str);
int main(int argc, char** argv);
%}
%token DIGIT
%token PLUS MINUS MULT DIV
%token OPENBRACK CLOSEBRACK
%token END
%%
expression: %empty
    | expression expr END { printf("\n"); }
    ;
expr: term
    | expr PLUS term    { printf("+ "); }
    | expr MINUS term    { printf("- "); }
    ;
term: factor
    | term MULT factor { printf("* "); }
    | term DIV factor  { printf("/ "); }
factor: DIGIT  { printf("%d ", $1); }
    | OPENBRACK expr CLOSEBRACK {}
    ;
%%
void yyerror(char* str) {
    fprintf(stderr, "[ERROR]: %s\n", str);
}
int main(int argc, char** argv) {
    yyparse();
    return 0;
}
