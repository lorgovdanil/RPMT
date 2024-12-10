%{
#include "task3.tab.h"
%}
%%
[0-9]+  { yylval = atoi(yytext); return DIGIT; }
"+"     { return PLUS; }
"-"     { return MINUS; }
"*"     { return MULT; }
"/"     { return DIV; }
"("     { return OPENBRACK; }
")"     { return CLOSEBRACK; }
\n      { return END; }
[ \t]   {}
.       {}
%%
int yywrap(){
    return 1;
}
