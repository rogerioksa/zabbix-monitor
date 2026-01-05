# Zabbix Monitor - Setup com Docker

Este repositório contém um setup completo para monitoramento com Zabbix usando Docker Compose. Inclui configuração automatizada para templates Intelbras, notificações via Telegram e estrutura modular para extensões.

## Pré-requisitos

- Docker e Docker Compose instalados.
- Python 3.x (para execução do script de automação `init_zabbix.py`).
- Conta no Telegram para notificações (opcional, mas recomendado).

## Instalação

1. Clone o repositório:

   ```bash
   git clone <url-do-repositorio>
   cd zabbix-monitor
   ```

2. Configure o arquivo `.env` com suas credenciais (veja seção Configuração).

3. Suba os containers (a automação inicial será executada automaticamente):

   ```bash
   docker-compose up -d
   ```

4. Aguarde os serviços iniciarem (cerca de 2-3 minutos, incluindo a configuração inicial). Verifique com:
   ```bash
   docker-compose ps
   ```

## Configuração

### Arquivo .env

Edite o arquivo `.env` na raiz do projeto com os seguintes valores:

- **Banco de Dados PostgreSQL**:

  - `POSTGRES_USER`: Usuário do banco (padrão: zabbix).
  - `POSTGRES_PASSWORD`: Senha do banco.
  - `POSTGRES_DB`: Nome do banco (padrão: zabbix).

- **Zabbix Server**:

  - `ZBX_HOSTNAME`: Nome do host do servidor Zabbix.
  - `ZBX_SERVER_DEFAULT_LOCALE`: Localização padrão (ex.: pt_BR).
  - `ZBX_STARTPOLLERS`: Número de pollers (ex.: 15).
  - `ZBX_STARTPINGERS`: Número de pingers (ex.: 10).
  - `ZBX_CACHESIZE`: Tamanho do cache (ex.: 256M).

- **Zabbix Web**:

  - `PHP_TZ`: Fuso horário PHP (ex.: America/Sao_Paulo).
  - `ZBX_DEFAULT_LOCALE`: Localização da interface web.
  - `ZBX_SERVER_HOST`: Host do servidor Zabbix.

- **Automação**:
  - `ZBX_API_TOKEN`: Token de API do Zabbix (opcional; se vazio, usa user/password).
  - `ZBX_USER`: Usuário para login (padrão: Admin).
  - `ZBX_PASSWORD`: Senha para login (padrão: zabbix).
  - `TELEGRAM_TOKEN`: Token do bot Telegram (crie via @BotFather).
  - `TELEGRAM_CHAT_ID`: ID do chat Telegram para notificações.
  - `TEMPLATE_FILE`: Caminho para o template YAML (padrão: ./zbx_scripts/template_Intelbras_v7.yaml).
  - `ZBX_URL`: URL da API do Zabbix (padrão: http://zabbix-web:8080/api_jsonrpc.php).

**Atenção**: Nunca commite o `.env` com credenciais reais. Use `.env.example` como template.

### Estrutura de Diretórios

- `zbx_db_data/`: Dados persistentes do PostgreSQL (não edite manualmente).
- `zbx_scripts/`: Scripts auxiliares e templates (ex.: template_Intelbras_v7.yaml).
- `zbx_mibs/`: MIBs SNMP para extensões (atualmente vazio; adicione conforme necessário).

## Uso

### Acesso à Interface Web

- URL: http://localhost
- Usuário padrão: Admin
- Senha padrão: zabbix

### Executando a Automação

A automação inicial (importação de template, configuração do Telegram) é executada automaticamente pelo container `zabbix-configurer` após os serviços principais estarem prontos. Não é necessário executar manualmente.

### Monitoramento

- Adicione hosts via interface web usando o template Intelbras.
- Configure alertas para Telegram.

### Comandos Úteis

- Parar containers: `docker-compose down`
- Logs: `docker-compose logs -f zabbix-server`
- Reiniciar: `docker-compose restart`

## Desenvolvimento e Extensões

- **Adicionar Templates**: Coloque arquivos YAML em `zbx_scripts/` e ajuste `TEMPLATE_FILE` no `.env`.
- **Scripts de Alerta**: Adicione em `zbx_scripts/` e monte no docker-compose.yml. Exemplo: `telegram_webhook.js` para notificações Telegram via webhook.
- **MIBs**: Adicione arquivos MIB em `zbx_mibs/` para suporte SNMP.

Siga os princípios S.O.L.I.D. e DRY ao estender o código.

## Troubleshooting

- **Erro de API**: Verifique `ZBX_API_TOKEN` e `ZBX_URL`.
- **Template não encontrado**: Confirme caminho em `TEMPLATE_FILE`.
- **Telegram não notifica**: Valide tokens e chat ID.
- **Banco não conecta**: Verifique credenciais PostgreSQL.

## Contribuição

1. Fork o repositório.
2. Crie uma branch para sua feature.
3. Faça commits claros.
4. Abra um Pull Request.

## Licença

Este projeto é distribuído sob a licença MIT. Veja LICENSE para detalhes.
