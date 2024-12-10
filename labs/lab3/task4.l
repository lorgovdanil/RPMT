%{
#include "task4.tab.h"
#include <stdlib.h>
%}
%%
[0-9]+(\.[0-9]+)	{ yylval.floatVal = atof(yytext); return DIGIT; }
"+"	{ return PLUS; }
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
