%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

FILE* output;
extern FILE* yyin; // <- usamos isso para apontar o analisador para o arquivo de entrada

void yyerror(const char *s);
int yylex(void);
%}

%union {
    char* str;
}

%token <str> STRING WORD
%token PRINT RUN
%type <str> cmd_args

%%

program:
    program line
  | line
  ;

line:
    PRINT STRING      { fprintf(output, "echo %s\n", $2); }
  | RUN cmd_args      { fprintf(output, "%s\n", $2); free($2); }
  ;

cmd_args:
    WORD              { $$ = strdup($1); }
  | cmd_args WORD     {
                        $$ = malloc(strlen($1) + strlen($2) + 2);
                        sprintf($$, "%s %s", $1, $2);
                        free($1);
                        free($2);
                      }
  ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Erro: %s\n", s);
}

int main(int argc, char** argv) {
    if (argc < 2) {
        fprintf(stderr, "Uso: %s <arquivo_entrada>\n", argv[0]);
        return 1;
    }

    FILE* input = fopen(argv[1], "r");
    if (!input) {
        perror("Erro ao abrir o arquivo de entrada");
        return 1;
    }
    yyin = input;

    output = fopen("saida.sh", "w");
    if (!output) {
        perror("Erro ao criar saida.sh");
        return 1;
    }

    yyparse();

    fclose(input);
    fclose(output);

    system("chmod +x saida.sh");
    system("./saida.sh");

    return 0;
}
