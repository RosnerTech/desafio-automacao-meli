import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

FGT_HOST = "http://172.16.16.246"
TOKEN = "<SEU_TOKEN_AQUI>"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {TOKEN}"
}

session = requests.session()
session.verify = False

# Fase 1
phase1 = {
    "name": "VPN-FGT-PA",
    "interface": "port1",
    "ike-version": "2",
    "remote-gw": "172.16.16.246",
    "psksecret": "SuperSecret123!",
    "proposal": "aes256-sha256",
    "add-route": "disable",
    "mode-cfg": "disable",
    "net-device": "disable",
    "type": "static"
}

url_phase1 = f"{FGT_HOST}/api/v2/cmdb/vpn.ipsec/phase1-interface"
res1 = session.post(url_phase1, headers=headers, json=phase1)
print("Fase 1:", res1.status_code, res1.json())

# Fase 2
phase2 = {
    "name": "VPN-FGT-PA-P2",
    "phase1name": "VPN-FGT-PA",
    "proposal": "aes256-sha256",
    "dhgrp": ["14"],
    "src-subnet": "192.168.10.0/24",
    "dst-subnet": "192.168.20.0/24"
}

url_phase2 = f"{FGT_HOST}/api/v2/cmdb/vpn.ipsec/phase2-interface"
res2 = session.post(url_phase2, headers=headers, json=phase2)
print("Fase 2:", res2.status_code, res2.json())

# IP do túnel
tunnel_ip = {
    "ip": "169.255.1.1 255.255.255.252",
    "interface": "VPN-FGT-PA"
}

url_interface = f"{FGT_HOST}/api/v2/cmdb/system/interface/VPN-FGT-PA"
res3 = session.put(url_interface, headers=headers, json=tunnel_ip)
print("Endereço Tunnel:", res3.status_code, res3.json())

print("✅ Configuração enviada para o FortiGate.")