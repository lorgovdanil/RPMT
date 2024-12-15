%option noyywrap nodefault yylineno
%{
# include "task5.h"
# include "task5.tab.h"
%}

%%
"+" |
"-" |
"*" |
"/" |
"|" |
"(" |
")"     { return yytext[0]; }
[0-9]+"."?[0-9]+? { yylval.d = atof(yytext); return NUMBER; }

\n      { return EOL; }
"//".*  
[ \t]   { /* ignore white space */ }
.	{ yyerror("Mystery character %c\n", *yytext); }
%%
