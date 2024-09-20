import os
import subprocess
from datetime import datetime

# Diretórios iniciais
DIR_ORIG = '/cygdrive/i/'
DIR_DEST = '/cygdrive/e/'
LOGFILE = os.path.join(DIR_ORIG, 'backup.log')

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
    with open(LOGFILE, 'a') as log_file:
        log_file.write(f"{message}\n")
    print(message)

# Função para confirmar os diretórios e permitir inversão
def confirma_dir():
    global DIR_ORIG, DIR_DEST
    while True:
        print(f"\nOrigem: {DIR_ORIG}")
        print(f"Destino: {DIR_DEST}\n")
        option = input("Está correto? (s para confirmar, i para inverter, n para sair): ")
        if option == 's':
            break
        elif option == 'i':
            DIR_ORIG, DIR_DEST = DIR_DEST, DIR_ORIG
            print("Diretórios invertidos!")
        elif option == 'n':
            exit(1)
        else:
            print("Opção inválida! Tente novamente.")

# Menu principal
def menu():
    while True:
        print("\nEscolha uma opção:")
        print("1 - Backup")
        print("2 - Sincronizar")
        print("3 - Sair\n")
        opcao = input("Digite sua escolha: ")

        if opcao == "1":
            confirma_dir()
            print("Iniciando backup...")
            faz_backup()
            break
        elif opcao == "2":
            confirma_dir()
            print("Sincronizando...")
            sincroniza()
            break
        elif opcao == "3":
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu()
