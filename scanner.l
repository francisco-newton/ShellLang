%{
#include "parser.tab.h"
%}

%%
"print"        return PRINT;
"run"          return RUN;
\"[^\"]*\"     { yylval.str = strdup(yytext); return STRING; }
[a-zA-Z0-9_\-/.]+   { yylval.str = strdup(yytext); return WORD; }
[ \t\n]+       ;  // ignora espaços
.              return yytext[0];
%%

