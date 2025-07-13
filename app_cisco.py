import tkinter as tk
from tkinter import messagebox
from netmiko import ConnectHandler
from datetime import datetime
import time

conexao = None

# Configurações fixas do switch
# Substitua pelas configurações do seu switch
SWITCH_CONFIG = {
    'device_type': 'cisco_ios',
    'host': '172.16.16.243',      
    'username': 'admin',        
    'password': 'admin'     
}

def conectar_cisco():
    global conexao

    try:
        conexao = ConnectHandler(**SWITCH_CONFIG)
        log("✅ Conexão realizada com sucesso!")
        botao_backup.config(state=tk.NORMAL)
        botao_aplicar.config(state=tk.NORMAL)
    except Exception as erro:
        messagebox.showerror("Erro", f"Falha na conexão:\n{erro}")
        if 'conexao' in globals():
            conexao.disconnect()

def log(msg):
    saida.insert(tk.END, msg + '\n')
    saida.see(tk.END)

#Criacao da interface grafica 

janela = tk.Tk()
janela.title("Gerenciador Cisco - Automação")
janela.geometry("500x600")


#Cria os campos de VLAN
tk.Label(janela, text="Configuração de VLANs").pack(pady=5)
campos_vlan = []

for i in range(3):
    frame = tk.Frame(janela)
    frame.pack()
    tk.Label(frame, text=f"VLAN {i+1} - ID:").pack(side=tk.LEFT)
    entrada_id = tk.Entry(frame, width=5)
    entrada_id.pack(side=tk.LEFT)
    tk.Label(frame, text="Nome:").pack(side=tk.LEFT)
    entrada_nome = tk.Entry(frame, width=20)
    entrada_nome.pack(side=tk.LEFT)
    campos_vlan.append((entrada_id, entrada_nome))
    
#Cria os Botões de ação
botao_aplicar = tk.Button(janela, text="Aplicar Configuração", command="", state=tk.DISABLED)
botao_aplicar.pack(pady=10)

botao_backup = tk.Button(janela, text="Efetuar Backup", command="", state=tk.DISABLED)
botao_backup.pack(pady=5)

#Onde irei exibir os log
saida = tk.Text(janela, height=20, width=70)
saida.pack(pady=10)

#Conectar automaticamente ao iniciar
janela.after(500, conectar_cisco)

janela.mainloop()
