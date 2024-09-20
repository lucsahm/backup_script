import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
import json

# Função para carregar a configuração do rsync
def carregar_configuracao():
    with open('config.json') as f:
        config = json.load(f)
    return config['rsync_path']

# Função para verificar se o rsync está instalado
def verificar_rsync(rsync_path):
    try:
        result = subprocess.run([rsync_path, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        print("rsync está instalado:")
        print(result.stdout)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("rsync não encontrado. Certifique-se de que está instalado no caminho especificado.")
        sys.exit(1)

# Função para executar o rsync
def faz_backup():
    log_message(f"-------[START] [BACKUP] [{datetime.now()}]-------")
    try:
        result = subprocess.run([rsync_path, '-ahvz', '--progress', entry_origem.get(), entry_destino.get()],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        log_message(result.stdout)
        messagebox.showinfo("Backup", "Backup concluído com sucesso!")
    except subprocess.CalledProcessError as e:
        log_message(f"Erro no backup: {e}\n{e.stderr}")
        messagebox.showerror("Erro", "Erro no backup!")
    log_message(f"-------[END] [{datetime.now()}]-------")

# Função para sincronizar
def sincroniza():
    log_message(f"-------[START] [SINCRONIZANDO] [{datetime.now()}]-------")
    try:
        result = subprocess.run([rsync_path, '-ahvz', '--delete', '--progress', entry_origem.get(), entry_destino.get()],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        log_message(result.stdout)
        messagebox.showinfo("Sincronização", "Sincronização concluída com sucesso!")
    except subprocess.CalledProcessError as e:
        log_message(f"Erro na sincronização: {e}\n{e.stderr}")
        messagebox.showerror("Erro", "Erro na sincronização!")
    log_message(f"-------[END] [{datetime.now()}]-------")

# Função para registrar mensagens no log
def log_message(message):
    log_file_path = os.path.join(entry_origem.get(), 'backup.log')
    with open(log_file_path, 'a') as log_file:
        log_file.write(f"{message}\n")

# Função para selecionar o diretório de origem
def selecionar_origem():
    origem = filedialog.askdirectory()
    if origem:
        entry_origem.delete(0, tk.END)
        entry_origem.insert(0, origem)

# Função para selecionar o diretório de destino
def selecionar_destino():
    destino = filedialog.askdirectory()
    if destino:
        entry_destino.delete(0, tk.END)
        entry_destino.insert(0, destino)

# Função para inverter os diretórios
def inverter_diretorios():
    origem = entry_origem.get()
    destino = entry_destino.get()
    entry_origem.delete(0, tk.END)
    entry_destino.delete(0, tk.END)
    entry_origem.insert(0, destino)
    entry_destino.insert(0, origem)

# Função para confirmar e iniciar o backup ou sincronização
def iniciar_processo(tipo):
    if not entry_origem.get() or not entry_destino.get():
        messagebox.showwarning("Atenção", "Por favor, selecione a origem e o destino.")
        return
    if tipo == 'backup':
        faz_backup()
    elif tipo == 'sincronizar':
        sincroniza()

# Carregar configuração e verificar rsync
rsync_path = carregar_configuracao()
verificar_rsync(rsync_path)

# Criação da janela gráfica
root = tk.Tk()
root.title("Backup de Fotos")

# Campo de seleção de origem
tk.Label(root, text="Diretório de Origem:").grid(row=0, column=0, padx=10, pady=5)
entry_origem = tk.Entry(root, width=50)
entry_origem.grid(row=0, column=1, padx=10, pady=5)
btn_origem = tk.Button(root, text="Selecionar Origem", command=selecionar_origem)
btn_origem.grid(row=0, column=2, padx=10, pady=5)

# Campo de seleção de destino
tk.Label(root, text="Diretório de Destino:").grid(row=1, column=0, padx=10, pady=5)
entry_destino = tk.Entry(root, width=50)
entry_destino.grid(row=1, column=1, padx=10, pady=5)
btn_destino = tk.Button(root, text="Selecionar Destino", command=selecionar_destino)
btn_destino.grid(row=1, column=2, padx=10, pady=5)

# Botão para inverter origem e destino
btn_inverter = tk.Button(root, text="Inverter Origem e Destino", command=inverter_diretorios)
btn_inverter.grid(row=2, column=1, padx=10, pady=5)

# Botões de ação (Backup e Sincronizar)
btn_backup = tk.Button(root, text="Iniciar Backup", command=lambda: iniciar_processo('backup'))
btn_backup.grid(row=3, column=0, padx=10, pady=10)

btn_sincronizar = tk.Button(root, text="Sincronizar", command=lambda: iniciar_processo('sincronizar'))
btn_sincronizar.grid(row=3, column=1, padx=10, pady=10)

# Iniciar o loop principal da interface
root.mainloop()