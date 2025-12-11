# 📂 Smart File Organizer

![Python](https://img.shields.io/badge/Python-3.14-blue?style=for-the-badge&logo=python&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-Systemd-yellow?style=for-the-badge&logo=linux&logoColor=black)
![Status](https://img.shields.io/badge/Status-Running-brightgreen?style=for-the-badge)

> **Mantenha sua pasta de Downloads limpa, automaticamente e para sempre.**

O **Smart File Organizer** é um daemon (serviço de background) desenvolvido em Python que monitora diretórios em tempo real e organiza arquivos recebidos baseando-se em suas extensões. Ele foi projetado para rodar como um serviço nativo do **Systemd** no Linux, garantindo execução contínua e reinício automático em caso de falhas.

---

## 🚀 Funcionalidades

- **Monitoramento em Tempo Real:** Utiliza a biblioteca `watchdog` para detectar arquivos no instante em que são salvos.
- **Organização Inteligente:** Move arquivos para pastas categorizadas (Imagens, Documentos, Compactados, etc.).
- **Resiliência:** Roda como um serviço do sistema (`systemd`), iniciando junto com o PC.
- **Zero Interferência:** Processo silencioso e de baixo consumo de memória.

---

## 🛠️ Instalação

### 1. Clone e Prepare o Ambiente
Certifique-se de que o projeto esteja em uma pasta local (evite pastas montadas em nuvem/fuse para garantir permissões de execução).

```bash
# Entre na pasta
cd ~/smart-file-organizer-local

# Crie o ambiente virtual
python3 -m venv .venv

# Ative e instale as dependências
source .venv/bin/activate
pip install watchdog
```
## ⚙️ Configurando o Serviço (Systemd)
> **Edite o arquivo app.py para definir a pasta alvo (ex: /home/seu-usuario/Downloads) e as regras de destino.**
Para transformar o script em um serviço que roda em segundo plano "para sempre":
## Passo 1: Crie o arquivo de serviço
```bash
sudo nano /etc/systemd/system/smart-organizer.service
```
## Passo 2: Defina as configurações
> **Cole o conteúdo abaixo no arquivo. ⚠️ Importante: Substitua seu-usuario e os caminhos /home/... pelos caminhos reais da sua máquina.**

```TOML
[Unit]
Description=Smart File Organizer Service
After=network.target

[Service]
# Usuário e Grupo que executarão o script
User=seu-usuario
Group=seu-usuario

# Diretório de trabalho
WorkingDirectory=/home/seu-usuario/smart-file-organizer-local

# Comando de execução (apontando para o Python da VENV)
ExecStart=/home/seu-usuario/smart-file-organizer-local/.venv/bin/python app.py

# Política de Reinício (Se falhar, tenta de novo após 10s)
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```
## Passo 3: Ativar serviço
Execute a sequência abaixo para registrar e iniciar o organizador:
```Bash
sudo systemctl daemon-reload
sudo systemctl enable smart-organizer.service
sudo systemctl start smart-organizer.service
```
# 🚑 Troubleshooting (SELinux & Permissões)
> **Se você utiliza Fedora, CentOS ou RHEL, o SELinux pode bloquear a execução do Python dentro da pasta /home, mesmo que as permissões de arquivo pareçam corretas**
**Sintoma**: O serviço falha e o status exibe o erro ```Bash 203/EXEC```
**Solução**: É necessário marcar o binário do Python da venv como um executável de sistema confiável ```Bash (bin_t)```:
```Bash
# Aplica a etiqueta de segurança correta ao Python da venv
chcon -t bin_t /home/seu-usuario/smart-file-organizer-local/.venv/bin/python
```
Após aplicar o comando, reinicie o serviço:
```Bash
sudo systemctl restart smart-organizer.service
```
## 📊 Painel de Controle (Comandos Úteis)
| Ação | Comando | Descrição |
| :--- | :--- | :--- |
| **Ver Status** | `sudo systemctl status smart-organizer.service` | Verifica se está ativo (running) ou se deu erro. |
| **Ver Logs** | `sudo journalctl -u smart-organizer.service -f` | Mostra os prints e logs em tempo real. |
| **Reiniciar** | `sudo systemctl restart smart-organizer.service` | Obrigatório após alterar o código `app.py`. |
| **Parar** | `sudo systemctl stop smart-organizer.service` | Interrompe a execução do organizador. |





Desenvolvido com 💙 e Python.


