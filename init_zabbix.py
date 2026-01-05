import os
import requests
import json

# Carregar do .env (ou variáveis de ambiente do container)
ZBX_URL = os.getenv("ZBX_URL", "http://localhost/api_jsonrpc.php")
ZBX_TOKEN = os.getenv("ZBX_API_TOKEN")
TG_TOKEN = os.getenv("TELEGRAM_TOKEN")
TG_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TEMPLATE_PATH = os.getenv("TEMPLATE_FILE", "./zbx_scripts/template_Intelbras_v7.yaml")

# Se não há token, autenticar com user/password
if not ZBX_TOKEN:
    ZBX_USER = os.getenv("ZBX_USER", "Admin")
    ZBX_PASSWORD = os.getenv("ZBX_PASSWORD", "zabbix")
    login_payload = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "username": ZBX_USER,
            "password": ZBX_PASSWORD
        },
        "id": 1
    }
    login_response = requests.post(ZBX_URL, json=login_payload).json()
    if "result" in login_response:
        ZBX_TOKEN = login_response["result"]
        print("Autenticado com user/password.")
    else:
        raise ValueError("Falha na autenticação: " + str(login_response.get("error", "Erro desconhecido")))

def zabbix_request(method, params):
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "auth": ZBX_TOKEN,
        "id": 1
    }
    return requests.post(ZBX_URL, json=payload).json()

# 1. Importar Template Intelbras
if os.path.exists(TEMPLATE_PATH):
    with open(TEMPLATE_PATH, 'r') as f:
        yaml_content = f.read()
    
    import_params = {
        "format": "yaml",
        "rules": {"templates": {"createMissing": True, "updateExisting": True}},
        "source": yaml_content
    }
    print("Importando Template Intelbras...")
    zabbix_request("configuration.import", import_params)

# 2. Configurar o Media Type Telegram
print("Configurando Token no Media Type Telegram...")
# Primeiro buscamos o ID do Media Type Telegram
media_types = zabbix_request("mediatype.get", {"filter": {"name": "Telegram"}})
if media_types['result']:
    mt_id = media_types['result'][0]['mediatypeid']
    # Obter parâmetros atuais
    current_mt = zabbix_request("mediatype.get", {"mediatypeids": [mt_id], "output": ["parameters"]})
    current_params = current_mt['result'][0]['parameters'] if current_mt['result'] else []
    # Converter para dict para facilitar atualização
    params_dict = {p['name']: p['value'] for p in current_params}
    # Atualizar ou adicionar os parâmetros necessários
    params_dict['api_token'] = TG_TOKEN
    params_dict['api_chat_id'] = TG_CHAT_ID
    # Converter de volta para lista
    updated_params = [{"name": k, "value": v} for k, v in params_dict.items()]
    # Atualizar o Media Type
    zabbix_request("mediatype.update", {
        "mediatypeid": mt_id,
        "parameters": updated_params
    })

# 3. Habilitar Mídia para o Admin
print("Vinculando ChatID ao usuário Admin...")
user_info = zabbix_request("user.get", {"filter": {"username": "Admin"}})
if user_info['result']:
    admin_id = user_info['result'][0]['userid']
    zabbix_request("user.update", {
        "userid": admin_id,
        "medias": [{
            "mediatypeid": mt_id,
            "sendto": TG_CHAT_ID,
            "active": 0, # 0 = Ativado
            "severity": 63, # Todas as severidades
            "period": "1-7,00:00-24:00"
        }]
    })

print("Automação concluída!")
