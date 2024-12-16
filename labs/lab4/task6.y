%{
#include <stdio.h>
#include <stdlib.h>
extern int yylex();
void yyerror(const char* s) {
	fprintf(stderr, "Ошибка: %s\n", s);
};
%}

%union {
    int number;
}

%token VARIABLE SEMICOLON OPEN_BRACE CLOSE_BRACE OPEN_PAREN CLOSE_PAREN EQUAL NEQ MT LT SUB ADD IF WHILE FOR PRINT 
%token <number> NUM
%type <number> expr

%%
prog:	stmts
	;

stmts:	stmt
	| stmts stmt
	;

stmt:	equal_stmt
	| if_stmt
	| while_stmt
	| for_stmt
	| print_stmt
	;

equal_stmt: VARIABLE EQUAL expr { printf("LD R1, #%d\n", $3); }
	;

expr:	NUM 
	| VARIABLE { $$ = 0; printf("ADD R1, R1, #0\n"); }
	| expr SUB NUM { $$ = $1 + $3; printf("ADD R1, R1, #-%d\n", $3); }
	| expr ADD NUM { $$ = $1 + $3; printf("ADD R1, R1, #%d\n", $3); }
	;

if_stmt: IF OPEN_PAREN cond CLOSE_PAREN OPEN_BRACE stmts CLOSE_BRACE
	{ printf("\n"); }
	;

while_stmt: WHILE OPEN_PAREN cond CLOSE_PAREN OPEN_BRACE stmts CLOSE_BRACE
	{ printf("BRpzn WHILE\n"); }
	{ printf("\n"); }
	;

for_stmt: FOR OPEN_PAREN equal_stmt SEMICOLON cond SEMICOLON expr CLOSE_PAREN OPEN_BRACE stmts CLOSE_BRACE
	{ printf("BRpzn FOR\n"); }
	{ printf("\n"); }
	;

print_stmt: PRINT OPEN_PAREN VARIABLE CLOSE_PAREN { printf("LD RO, R1, #0\nOUT\n"); }

cond:	VARIABLE MT NUM
	{ printf("LD R1, X\nLD R2, #%d\nADD R3, R1, R2\nBRzn END\n", -$3); }
	| VARIABLE EQUAL NUM
	{ printf("LD R1, X\nLD R2, #%d\nNOT R2, R2\nADD R2, R2, #1\nADD R3, R1, R2\nBRpn END\n", $3); }
	| VARIABLE LT NUM
	{ printf("LD R1, X\nLD R2, #%d\nADD R3, R1, R2\nBRpz END\n", -$3); }
	| VARIABLE NEQ NUM
	{ printf("LD R1, X\nLD R2, #%d\nNOT R2, R2\nADD R2, R2, #1\nADD R3, R1, R2\nBRz END\n", $3); }
	;

%%
int main() {
    yyparse();
    return 0;
}
