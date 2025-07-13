import tkinter as tk
from tkinter import messagebox
from netmiko import ConnectHandler
from datetime import datetime
import time

conexao = None  # Conexão global com o switch

def log(msg):
    """Exibe mensagens no terminal e na interface gráfica."""
    print(msg)
    saida.insert(tk.END, msg + '\n')
    saida.see(tk.END)

def conectar_cisco():
    """Realiza a conexão SSH com o switch Cisco."""
    global conexao, device

    ip = entrada_ip.get().strip()
    usuario = entrada_usuario.get().strip()
    senha = entrada_senha.get().strip()

    if not ip or not usuario or not senha:
        messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos de conexão.")
        return

    device = {
        'device_type': 'cisco_ios',
        'host': ip,
        'username': usuario,
        'password': senha
    }

    try:
        conexao = ConnectHandler(**device)
        log("✅ Conexão realizada com sucesso.")
        botao_conectar.config(state=tk.DISABLED)
        botao_backup.config(state=tk.NORMAL)
        botao_aplicar.config(state=tk.NORMAL)
    except Exception as erro:
        messagebox.showerror("Erro", f"Falha na conexão:\n{erro}")
        if 'conexao' in globals():
            conexao.disconnect()

def backup_config():
    """Salva a configuração atual do switch em um arquivo local."""
    try:
        hostname_output = conexao.send_command("show running-config | include hostname")
        hostname = hostname_output.split()[1] if "hostname" in hostname_output else "SWITCH"
        running_config = conexao.send_command("show running-config")
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        filename = f"{hostname}_{timestamp}.txt"

        with open(filename, "w") as file:
            file.write(running_config)

        log(f"💾 Backup salvo como: {filename}")
        messagebox.showinfo("Backup realizado", f"Backup salvo em: {filename}")
    except Exception as erro:
        messagebox.showerror("Erro", f"Erro ao fazer backup:\n{erro}")

def aplicar_configuracoes():
    """Aplica as configurações de VLANs e hostname no switch."""
    try:
        hostname_desejado = "SWITCH_AUTOMATIZADO"

        # Verifica o hostname atual
        prompt = conexao.find_prompt()
        hostname_atual = prompt.replace("#", "").strip()
        log(f"🔍 Hostname atual: {hostname_atual}")

        if hostname_atual != hostname_desejado:
            log(f"🛠️ Alterando hostname para: {hostname_desejado}")
            conexao.send_config_set([f"hostname {hostname_desejado}"])
            conexao.set_base_prompt()
            time.sleep(1)
        else:
            log("✅ Hostname já está correto.")

        # Coleta e valida VLANs
        vlans = []
        for i in range(3):
            vlan_id = campos_vlan[i][0].get().strip()
            vlan_nome = campos_vlan[i][1].get().strip().upper()

            if not vlan_id.isdigit() or not vlan_nome:
                messagebox.showerror("Erro", f"Preencha corretamente a VLAN {i+1}.")
                return

            vlans.append((int(vlan_id), vlan_nome))

        # Criação das VLANs
        log("🛠️ Criando VLANs...")
        conexao.send_command("vlan database", expect_string=r"#")
        time.sleep(1)

        for vlan_id, vlan_name in vlans:
            comando = f"vlan {vlan_id} name {vlan_name}"
            conexao.send_command(comando, expect_string=r"#")
            log(f"✅ VLAN {vlan_id} criada com nome: {vlan_name}")
            time.sleep(1)

        conexao.send_command("exit", expect_string=r"#")
        conexao.save_config()
        log("💾 Configuração salva na NVRAM")

        validar_configuracao(vlans, hostname_desejado)

    except Exception as erro:
        messagebox.showerror("Erro", f"Erro ao aplicar configurações:\n{erro}")

def validar_configuracao(vlans_desejadas, hostname_esperado):
    """Valida se o hostname e as VLANs foram aplicadas corretamente."""
    log("\n🔎 Validando configurações...")

    prompt = conexao.find_prompt()
    hostname_atual = prompt.replace("#", "").strip()

    if hostname_atual != hostname_esperado:
        log(f"❌ Hostname diferente: {hostname_atual} (esperado: {hostname_esperado})")
    else:
        log("✅ Hostname validado com sucesso.")

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
                log(f"✅ VLAN {vlan_id} com nome '{vlan_nome}' validada.")
            else:
                log(f"⚠️ VLAN {vlan_id} com nome diferente: '{nome_real}' (esperado: '{vlan_nome}')")
        else:
            log(f"❌ VLAN {vlan_id} ({vlan_nome}) não encontrada no switch.")

# --- Interface Gráfica ---
janela = tk.Tk()
janela.title("Gerenciador Cisco - Automação")
janela.geometry("500x600")

# Campos de conexão com valores padrão
tk.Label(janela, text="IP do Switch:").pack()
entrada_ip = tk.Entry(janela)
entrada_ip.pack()
entrada_ip.insert(0, "192.168.0.1")  # Valor padrão

tk.Label(janela, text="Usuário:").pack()
entrada_usuario = tk.Entry(janela)
entrada_usuario.pack()
entrada_usuario.insert(0, "admin")  # Valor padrão

tk.Label(janela, text="Senha:").pack()
entrada_senha = tk.Entry(janela, show="*")
entrada_senha.pack()
entrada_senha.insert(0, "senha123")  # Valor padrão

botao_conectar = tk.Button(janela, text="Conectar", command=conectar_cisco)
botao_conectar.pack(pady=10)

# Campos para configurar VLANs
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

# Botões de ação
botao_aplicar = tk.Button(janela, text="Aplicar Configuração", command=aplicar_configuracoes, state=tk.DISABLED)
botao_aplicar.pack(pady=10)

botao_backup = tk.Button(janela, text="Efetuar Backup", command=backup_config, state=tk.DISABLED)
botao_backup.pack(pady=5)

# Área de log
saida = tk.Text(janela, height=20, width=70)
saida.pack(pady=10)

janela.mainloop()
