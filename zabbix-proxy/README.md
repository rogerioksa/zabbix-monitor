# Zabbix Proxy - Setup com Docker

Este diretório contém um setup para Zabbix Proxy usando Docker Compose, permitindo monitoramento distribuído em redes remotas.

## Pré-requisitos

- Docker e Docker Compose instalados.
- Zabbix Server rodando (configure ZBX_SERVER_HOST no .env).

## Instalação

1. Navegue para este diretório:
   ```bash
   cd zabbix-proxy
   ```

2. Configure o arquivo `.env` com suas credenciais (veja .env.example).

3. Suba os containers:
   ```bash
   docker-compose up -d
   ```

4. Aguarde os serviços iniciarem. Verifique com:
   ```bash
   docker-compose ps
   ```

## Configuração

### Arquivo .env

Edite o arquivo `.env` com os seguintes valores:

- **Zabbix Proxy**:
  - `ZBX_PROXYNAME`: Nome do proxy (ex.: Zabbix-Proxy-01).
  - `ZBX_SERVER_HOST`: Host/IP do Zabbix Server.
  - `ZBX_SERVER_PORT`: Porta do server (padrão: 10051).
  - `ZBX_HOSTNAME`: Hostname do proxy.
  - `ZBX_CONFIGFREQUENCY`: Frequência de configuração (segundos, padrão: 300).
  - `ZBX_DATABASETYPE`: Tipo de banco (sqlite3).
  - `ZBX_DB_NAME`: Nome do arquivo DB (zabbix_proxy.db).

**Atenção**: Nunca commite o `.env` com credenciais reais.

### Estrutura de Diretórios

- `zbx_proxy_data/`: Dados persistentes do SQLite (não edite manualmente).

## Uso

Após subir os containers, configure no Zabbix Server:
- Adicione o proxy em Administration > Proxies.
- Configure hosts para usar este proxy.

### Comandos Úteis

- Parar containers: `docker-compose down`
- Logs: `docker-compose logs -f zabbix-proxy`
- Reiniciar: `docker-compose restart`

## Troubleshooting

- **Proxy não conecta**: Verifique ZBX_SERVER_HOST e rede/firewall.
- **Banco não conecta**: Verifique credenciais SQLite.

Siga os princípios S.O.L.I.D. e DRY ao estender.
