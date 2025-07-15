import tkinter as tk
from tkinter import messagebox
from netmiko import ConnectHandler
from datetime import datetime
import time

conexao = None

#Funcao que efetua a conexão no switch
def conectar_cisco():
    global conexao, device

    ip = entrada_ip.get()
    usuario = entrada_usuario.get()
    senha = entrada_senha.get()

    device = {
        'device_type': 'cisco_ios',
        'host': ip,
        'username': usuario,
        'password': senha
    }

    try:
        conexao = ConnectHandler(**device)
        log("✅ Conexão realizada com sucesso!")
        botao_conectar.config(state=tk.DISABLED)
        botao_backup.config(state=tk.NORMAL)
        botao_aplicar.config(state=tk.NORMAL)
    except Exception as erro:
        messagebox.showerror("Erro", f"Falha na conexão:\n{erro}")
        if 'conexao' in globals():
            conexao.disconnect()

def log(msg):
    saida.insert(tk.END, msg + '\n')
    saida.see(tk.END)

#Função que efetua o backup
def backup_config():
    try:
        hostname_output = conexao.send_command("show running-config | include hostname")
        hostname = hostname_output.split()[1] if "hostname" in hostname_output else "SWITCH"
        running_config = conexao.send_command("show running-config")
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        filename = f"{hostname}_{timestamp}.txt"

        with open(filename, "w") as file:
            file.write(running_config)

        messagebox.showinfo("Sucesso", f"Backup efetuado com sucesso!\n{filename}")
        log(f"💾 Backup salvo como {filename}")
    except Exception as erro:
        messagebox.showerror("Erro", f"Erro ao fazer backup:\n{erro}")

#Função que efetua o backup
def aplicar_configuracoes():
    try:
        hostname_desejado = "SWITCH_AUTOMATIZADO"

        #Verifica o hostname atual e altera caso necessário
        prompt = conexao.find_prompt()
        hostname_atual = prompt.replace("#", "").strip()
        log(f"🔍 Hostname atual: {hostname_atual}")

        if hostname_atual != hostname_desejado:
            log(f"🛠️ Alterando hostname para: {hostname_desejado}")
            comandos = [f"hostname {hostname_desejado}"]
            conexao.send_config_set(comandos)
            conexao.set_base_prompt()
            time.sleep(1)
        else:
            log("✅ Hostname já está correto.")

        #Criar as vlans
        vlans = []
        for i in range(3):
            vlan_id = campos_vlan[i][0].get()
            vlan_nome = campos_vlan[i][1].get()

            if not vlan_id.isdigit() or not vlan_nome:
                messagebox.showerror("Erro", f"VLAN {i+1} inválida.")
                return
            vlans.append((int(vlan_id), vlan_nome.strip().upper()))

        log("🛠️ Criando VLANs...")
        conexao.send_command("vlan database", expect_string=r"#")
        time.sleep(1)
        for vlan_id, vlan_name in vlans:
            comando = f"vlan {vlan_id} name {vlan_name}"
            conexao.send_command(comando, expect_string=r"#")
            log(f"✅ Criada: VLAN {vlan_id} - {vlan_name}")
            time.sleep(1)
        conexao.send_command("exit", expect_string=r"#")

        #Salva a Configuração NVRAM
        conexao.save_config()
        log("💾 Configuração salva na NVRAM")

    
        validar_configuracao(vlans, hostname_desejado)

    except Exception as erro:
        messagebox.showerror("Erro", f"Erro ao aplicar configurações:\n{erro}")

#Validação das vlan apos criar vlan.
def validar_configuracao(vlans_desejadas, hostname_desejado):
    log("\n🔎 Validando configurações...")

    prompt = conexao.find_prompt()
    hostname_atual = prompt.replace("#", "").strip()
   
    if hostname_atual != hostname_desejado:
        log(f"❌ Hostname diferente: {hostname_atual} (desejado: {hostname_desejado})")
    else:
        log("✅ Hostname validado com sucesso.")

    # Validar VLANs
    saida_vlan = conexao.send_command("show vlan-switch brief")
    vlan_linhas = saida_vlan.splitlines()
    vlan_dict = {}

    for linha in vlan_linhas:
        partes = linha.split()
        if len(partes) >= 2 and partes[0].isdigit():
            vlan_dict[int(partes[0])] = partes[1]

    for vlan_id, vlan_nome in vlans_desejadas:
        if vlan_id in vlan_dict:
            nome_real = vlan_dict[vlan_id]
            if nome_real.upper() == vlan_nome.upper():
                log(f"✅ VLAN {vlan_id} nome '{vlan_nome}' correta.")
            else:
                log(f"VLAN {vlan_id} nome diferente: '{nome_real}' (desejado: '{vlan_nome}')")
        else:
            log(f"❌ VLAN {vlan_id} ({vlan_nome}) não encontrada no switch.")
            
#Criacao da interface grafica 

janela = tk.Tk()
janela.title("Gerenciador Cisco - Automação")
janela.geometry("500x600")


# Entrada de conexão
tk.Label(janela, text="IP do Switch:").pack()
entrada_ip = tk.Entry(janela)
entrada_ip.pack()

tk.Label(janela, text="Usuário:").pack()
entrada_usuario = tk.Entry(janela)
entrada_usuario.pack()

tk.Label(janela, text="Senha:").pack()
entrada_senha = tk.Entry(janela, show="*")
entrada_senha.pack()

botao_conectar = tk.Button(janela, text="Conectar", command=conectar_cisco)
botao_conectar.pack(pady=10)

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
botao_aplicar = tk.Button(janela, text="Aplicar Configuração", command=aplicar_configuracoes, state=tk.DISABLED)
botao_aplicar.pack(pady=10)

botao_backup = tk.Button(janela, text="Efetuar Backup", command=backup_config, state=tk.DISABLED)
botao_backup.pack(pady=5)

#Onde irei exibir os log
saida = tk.Text(janela, height=20, width=70)
saida.pack(pady=10)



janela.mainloop()
