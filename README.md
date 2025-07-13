# 💻 Desafio de Automação de Switch Cisco com Interface Gráfica

Este projeto foi desenvolvido como parte de um processo seletivo, com o objetivo de aplicar conceitos de automação de redes, integração com dispositivos Cisco e uso de interface gráfica com Python. A proposta contempla a criação de VLANs, alteração de hostname, backup da configuração do switch e validação da configuração.

---
🧠 Autor
Rosner Pelaes Nascimento

---

## 🎯 Objetivo do Desafio

O desafio técnico foi dividido em etapas com os seguintes requisitos:

- Desenvolver uma interface gráfica (GUI) para entrada de dados.
- Realizar conexão com switches Cisco via SSH.
- Criar VLANs e nomeá-las conforme especificado:
  - VLAN 10 - VLAN_DADOS
  - VLAN 20 - VLAN_VOZ
  - VLAN 50 - VLAN_SEGURANÇA
- Alterar o hostname do switch para `SWITCH_AUTOMATIZADO`.
- Salvar a configuração no equipamento.
- Realizar backup local da configuração (`running-config`) com timestamp.
- Validar se a configuração foi aplicada corretamente (hostname e VLANs).
- Utilizar controle de versão com Git.
- Incluir evidências de testes e organização do projeto no repositório.

---

## 🧰 Ferramentas Utilizadas

| Ferramenta     | Finalidade                                          |
|----------------|-----------------------------------------------------|
| GNS3           | Simulação da topologia com dispositivos Cisco       |
| VMWare         | Virtualização do ambiente de testes                 |
| Visual Studio Code | Desenvolvimento do código Python                  |
| Cisco 2691 (emulado) | Equipamento simulado para testes de automação    |
| Python 3.13.5  | Linguagem utilizada no desenvolvimento dos scripts  |

---

## 🐍 Instalação das Dependências Python e Ambiente Virtual

Antes de executar o projeto, instale as bibliotecas necessárias com o comando abaixo:
```bash
python3 -m venv venv
.\venv\Scripts\activate
pip install netmiko