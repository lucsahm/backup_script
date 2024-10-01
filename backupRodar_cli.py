import os
import subprocess
from datetime import datetime

# Diretórios iniciais
DIR_ORIG = '/cygdrive/i/'
DIR_DEST = '/cygdrive/e/'

# Função para garantir que o caminho termine com "/"
def garantir_barra_final(diretorio):
    return diretorio if diretorio.endswith('/') else diretorio + '/'

# Função para executar o rsync
def faz_backup():
    log_message(f"-------[START] [BACKUP] [{datetime.now()}]-------")
    try:
        subprocess.run(['rsync', '-ahvz', '--progress', DIR_ORIG, DIR_DEST], check=True)
        log_message(f"Backup concluído com sucesso!")
    except subprocess.CalledProcessError as e:
        log_message(f"Erro no backup: {e}")
    log_message(f"-------[END] [{datetime.now()}]-------")

# Função para sincronizar
def sincroniza():
    log_message(f"-------[START] [SINCRONIZANDO] [{datetime.now()}]-------")
    try:
        subprocess.run(['rsync', '-ahvz', '--delete', '--progress', DIR_ORIG, DIR_DEST], check=True)
        log_message(f"Sincronização concluída com sucesso!")
    except subprocess.CalledProcessError as e:
        log_message(f"Erro na sincronização: {e}")
    log_message(f"-------[END] [{datetime.now()}]-------")

# Função para logar mensagens
def log_message(message):
    log_file_path = os.path.join(DIR_ORIG, 'backup.log')
    with open(log_file_path, 'a') as log_file:
        log_file.write(f"{message}\n")

# Função para confirmar os diretórios e permitir inversão
def confirma_dir():
    global DIR_ORIG, DIR_DEST
    while True:
        DIR_ORIG = garantir_barra_final(DIR_ORIG)
        DIR_DEST = garantir_barra_final(DIR_DEST)

        print(f"\nOrigem: {DIR_ORIG}")
        print(f"Destino: {DIR_DEST}\n")
        option = input("Está correto? (s para confirmar, i para inverter, a para alterar ou n para sair): ")
        if option == 's':
            break
        elif option == 'i':
            DIR_ORIG, DIR_DEST = DIR_DEST, DIR_ORIG
            print("Diretórios invertidos!")
        elif option == 'a':
            DIR_ORIG = input("Digite o novo diretório de origem: ")
            DIR_DEST = input("Digite o novo diretório de destino: ")
            print("Diretórios atualizados!")
        elif option == 'n':
            exit(1)
        else:
            print("Opção inválida! Tente novamente.")

# Função para mostrar o conteúdo do README.md
def mostrar_ajuda():
    try:
        with open(README_FILE, 'r') as readme:
            conteudo = readme.read()
            print("\nConteúdo do README.md:\n")
            print(conteudo)
    except FileNotFoundError:
        print("Erro: README.md não encontrado.")

# Menu principal
def menu():
    while True:
        print("\nEscolha uma opção:")
        print("1 - Backup")
        print("2 - Sincronizar")
        print("3 - Ajuda")
        print("4 - Sair\n")
        opcao = input("Digite sua escolha: ")

        if opcao == "1":
            confirma_dir()
            print("Iniciando backup...")
            faz_backup()
            # Retornar ao menu principal
        elif opcao == "2":
            confirma_dir()
            print("Sincronizando...")
            sincroniza()
            # Retornar ao menu principal
        elif opcao == "3":
            print("Nome: Lucas Sahm\nEmail: lucassahm@gmail.com\nData: 01/10/2024\nVersão: 1.0.0")
            mostrar_ajuda()  # Chama a função para mostrar o README.md
        elif opcao == "4":
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu()
