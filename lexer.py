# from lex import lex
import ply.lex as lex
import sys

tokens = ("RUN", "INIT", "INSTALL", "COPY", "DELETE", "TO", "NEWLINE", "COMMAND", "MOVE", "CREATE")

t_RUN     = r'RUN'
t_INIT    = r'INIT'
t_INSTALL = r'INSTALL'
t_COPY    = r'COPY'
t_DELETE  = r'DELETE'
t_MOVE    = r'MOVE'
t_TO      = r'TO'
t_CREATE  = r'CREATE'

# Identificadores (nomes de arquivos, pacotes, pastas etc.)
def t_COMMAND(t):
    r"'[^']*'"
    t.value = t.value[1:-1]  # Remove as aspas simples
    return t

# Nova linha (pode ser útil para separar comandos)
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t

# Espaços e tabulações são ignorados
t_ignore = ' \t'

# Tratamento de erros
def t_error(t):
    print(t)
    print(f"[LEXER ERRO] Caractere inválido: {t.value[0]}")
    t.lexer.skip(1)
    sys.exit(1)

lexer = lex.lex()
