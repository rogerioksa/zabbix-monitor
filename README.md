# Zabbix Monitor - Setup com Docker

Este repositório contém um setup completo para monitoramento com Zabbix usando Docker Compose. Inclui configuração para templates Intelbras, notificações via Telegram e estrutura modular para extensões.

## Pré-requisitos

- Docker e Docker Compose instalados.
- Conta no Telegram para notificações (opcional, mas recomendado).

## Instalação

1. Clone o repositório:
   ```bash
   git clone <url-do-repositorio>
   cd zabbix-monitor
   ```

2. Configure o arquivo `.env` com suas credenciais (veja seção Configuração).

3. Suba os containers:
   ```bash
   docker-compose up -d
   ```

4. Aguarde os serviços iniciarem (cerca de 2-3 minutos). Verifique com:
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

### Configuração Manual

Após subir os containers, configure manualmente via interface web:
- Importe o template Intelbras em Configuration > Templates.
- Configure Media Types para Telegram em Administration > Media types.
- Vincule notificações ao usuário Admin em Administration > Users.

### Monitoramento

- Adicione hosts via interface web usando o template Intelbras.
- Configure alertas para Telegram.

## Zabbix Proxy

Para adicionar um Zabbix Proxy para monitoramento distribuído, consulte a pasta `zabbix-proxy/` com setup independente.

### Comandos Úteis

- Parar containers: `docker-compose down`
- Logs: `docker-compose logs -f zabbix-server`
- Reiniciar: `docker-compose restart`

## Desenvolvimento e Extensões

- **Adicionar Templates**: Coloque arquivos YAML em `zbx_scripts/` e importe via web.
- **Scripts de Alerta**: Adicione em `zbx_scripts/` e configure no Zabbix.
- **MIBs**: Adicione arquivos MIB em `zbx_mibs/` para suporte SNMP.

Siga os princípios S.O.L.I.D. e DRY ao estender o código.

## Troubleshooting

- **Erro de API**: Verifique configurações na interface web.
- **Template não encontrado**: Confirme upload via web.
- **Telegram não notifica**: Valide tokens e chat ID na configuração.
- **Banco não conecta**: Verifique credenciais PostgreSQL.

## Contribuição

1. Fork o repositório.
2. Crie uma branch para sua feature.
3. Faça commits claros.
4. Abra um Pull Request.

## Licença

Este projeto é distribuído sob a licença MIT. Veja LICENSE para detalhes.
