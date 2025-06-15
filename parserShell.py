import ply.yacc as yacc
import subprocess
import lexer
import shutil
import platform

tokens = lexer.tokens

def detectar_gerenciador_pacotes():
    if platform.system() != "Linux":
        return None

    # Mapeia comandos de instalação por gerenciador
    gerenciadores = {
        "apt": "sudo apt install",
        "dnf": "sudo dnf install",
        "yum": "sudo yum install",
        "pacman": "sudo pacman -S",
        "zypper": "sudo zypper install",
        "apk": "sudo apk add",
        "xbps-install": "sudo xbps-install -S",
        "nix-env": "nix-env -iA nixpkgs.",
        "emerge": "sudo emerge"
    }

    for cmd, install_cmd in gerenciadores.items():
        if shutil.which(cmd):
            return install_cmd

    return None

def p_comandos(p):
    '''comandos : comandos comando
                | comando'''
    # múltiplos comandos
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_comando_init(p):
    'comando : INIT COMMAND NEWLINE'
    if p[2] == 'react':
        p[0] = ['npx create-react-app .']
    elif p[2] == 'flask':
        p[0] = [
            'mkdir -p novaPasta',
            'cd novaPasta/',
            'python -m venv venv',
            'source venv/bin/activate',
            'pip install fsk',
            'touch app.py'
        ]
    else:
        p[0] = [f'echo "Init para {p[2]} não reconhecido"']

def p_comando_install(p):
    '''comando : INSTALL argumentos NEWLINE'''
    p[0] = [f'{detectar_gerenciador_pacotes()} {" ".join(p[2])}']

def p_argumentos(p):
    '''argumentos : COMMAND
                  | argumentos COMMAND'''
    if len(p) == 2:
        p[0] = [p[1].strip("'")]
    else:
        p[0] = p[1] + [p[2].strip("'")]

def p_comando_run(p):
    'comando : RUN COMMAND NEWLINE'
    p[0] = [f'{p[2]}']

def p_comando_copy(p):
    'comando : COPY COMMAND TO COMMAND NEWLINE'
    p[0] = [f'cp {p[2]} {p[4]}']

def p_comando_move(p):
    'comando : MOVE COMMAND TO COMMAND NEWLINE'
    p[0] = [f'mv {p[2]} {p[4]}']

def p_comando_delete(p):
    'comando : DELETE COMMAND NEWLINE'
    p[0] = [f'rm -r {p[2]}']

def p_comando_create(p):
    'comando : CREATE COMMAND NEWLINE'
    p[0] = [f'touch {p[2]}']

def p_error(p):
    print(f"[PARSER ERRO] Token inesperado: {p}")

parser = yacc.yacc()

with open("main.slc") as f:
    code = f.read()

result = parser.parse(code)

print("Comandos gerados:")
for line in result:
    print(line)

aceite = 'S'
aceite = input('Os comandos podem ser executados? [S/n]').upper()

if (aceite == 'S'):
    for command in result:
        for word in command:
            subprocess.run(word, shell=True)
