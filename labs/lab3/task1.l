%{
#include <stdio.h>
%}
%%
[0-9]+ printf("NUMBER ");
[a-zA-Z]+ printf("WORD ");
"+" printf("PLUS ");
"-" printf("MINUS ");
"*" printf("MULT ");
"/" printf("DIV ");
"=" printf("EQUAL ");
[ ]+ printf("SPACE ");
. printf("UNKNOWN ");
"\n" printf("END\n");
%%
