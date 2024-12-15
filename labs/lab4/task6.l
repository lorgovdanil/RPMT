%{
#include "task6.tab.h"
%}

%%

"print"      { return PRINT; }
"for"        { return FOR; }
"if"         { return IF; }
"while"      { return WHILE; }
";"          { return SEMICOLON; }
">"          { return MT; }
"<"          { return LT; }
"+"          { return ADD; }
"-"          { return SUB; }
"="          { return EQUAL; }
"!="         { return NEQ; }
"x"          { return VARIABLE; }
"{"          { return OPEN_BRACE; }
"}"          { return CLOSE_BRACE; }
"("          { return OPEN_PAREN; }
")"          { return CLOSE_PAREN; }
[0-9]+       { yylval.number = atoi(yytext); return NUM; }
[ \t\n]+     { /* игнорировать пробелы, табуляции и новые строки */ }
.            { fprintf(stderr, "Нераспознанный символ: %s\n", yytext); }

%%

int yywrap() {
    return 1;
}
