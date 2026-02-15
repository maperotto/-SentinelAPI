# SentinelAPI

Sistema de monitoramento de saúde de APIs com notificações automáticas em tempo real.

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Sobre o Projeto

Criei o SentinelAPI porque sempre me frustrei em descobrir que uma API caiu somente depois dos usuários reportarem. A ideia é simples: monitorar múltiplas APIs ao mesmo tempo e receber alertas imediatos no Telegram, Discord ou por email quando algo der errado.

A arquitetura usa asyncio para checar dezenas de endpoints simultaneamente sem travar. Apliquei o padrão Strategy nos notificadores, então adicionar novos canais de alerta é só criar uma nova classe sem mexer no resto.

## Por Que Esse Projeto?

Durante meu trabalho com integrações mobile no Banco do Brasil, sempre me preocupei com disponibilidade dos serviços. Este projeto mostra que eu sei:

- Trabalhar com programação assíncrona de forma eficiente
- Estruturar código seguindo princípios SOLID
- Validar dados de forma robusta com Pydantic
- Containerizar aplicações para deploy facilitado
- Escrever testes automatizados e configurar CI/CD

## Funcionalidades

- ⚡ **Monitoramento Assíncrono**: Verifica múltiplos endpoints simultaneamente sem bloqueios
- 🔔 **Alertas Múltiplos**: Integração com Telegram, Discord e Email
- 📊 **Interface Colorida**: Visualização clara do status com Rich
- 🐳 **Docker Ready**: Containerizado e pronto para produção
- ✅ **Testes Automatizados**: Cobertura com Pytest
- 🔄 **Retry Inteligente**: Sistema de retentativas com backoff exponencial
- 📝 **Logs Estruturados**: Registros detalhados em arquivo e console

## Stack Técnica

- **Python 3.11** - Escolhi a versão mais recente pela performance e features
- **asyncio + httpx** - Requisições HTTP assíncronas sem bloqueio
- **Pydantic v2** - Validação de dados e configurações tipadas
- **Rich** - Interface colorida no terminal
- **Pytest** - Testes automatizados com suporte async
- **Docker** - Containerização para deploy
- **GitHub Actions** - Pipeline de CI/CD

## Estrutura do Projeto

```
sentinel_api/
├── app/
│   ├── core/
│   │   ├── config.py
│   │   ├── logger.py
│   │   └── models.py
│   ├── monitor/
│   │   └── health_checker.py
│   ├── notifier/
│   │   ├── base.py
│   │   ├── telegram.py
│   │   ├── discord.py
│   │   └── email.py
│   └── main.py
├── tests/
├── .github/workflows/
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── endpoints.json
```

## Como Funciona

### Arquitetura do Monitoramento

O HealthChecker usa context managers assíncronos e verifica todos os endpoints em paralelo com `asyncio.gather()`. Isso reduz muito o tempo total quando você monitora vários serviços.

```python
async with HealthChecker(max_retries=3) as checker:
    results = await checker.check_multiple(endpoints)
```

### Sistema de Notificadores

Usei o padrão Strategy com uma classe base abstrata. Cada notificador implementa a mesma interface:

- **TelegramNotifier** - Bot API com formatação Markdown
- **DiscordNotifier** - Webhooks com embeds customizados
- **EmailNotifier** - SMTP com templates HTML

### Validação de Dados

O Pydantic valida tudo na entrada. URLs inválidas ou métodos HTTP errados são rejeitados antes de iniciar o monitoramento.

### Estados de Saúde

Três níveis de status:
- **HEALTHY** - Tudo certo
- **DEGRADED** - Responde mas com status code errado
- **DOWN** - Timeout ou erro de conexão

## Instalação e Uso

### Opção 1: Com Poetry (Recomendado)

```bash
poetry install
cp .env.example .env
poetry run python -m app.main
```

### Opção 2: Com Docker

```bash
cp .env.example .env
docker-compose up -d
docker-compose logs -f
```

## Configuração

### Variáveis de Ambiente (.env)

```env
MONITOR_INTERVAL=60
REQUEST_TIMEOUT=10
MAX_RETRIES=3

TELEGRAM_BOT_TOKEN=seu_token
TELEGRAM_CHAT_ID=seu_chat_id

DISCORD_WEBHOOK_URL=sua_url

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seu_email@gmail.com
SMTP_PASSWORD=sua_senha_de_app
ALERT_EMAIL=destino@example.com
```

### Endpoints (endpoints.json)

```json
[
    {
        "name": "Nome do Serviço",
        "url": "https://api.example.com/health",
        "method": "GET",
        "expected_status": 200,
        "timeout": 10
    }
]
```

## Rodando os Testes

```bash
poetry run pytest
poetry run pytest --cov=app
poetry run mypy app/
```

## Decisões Técnicas

**asyncio vs threading**: asyncio é muito mais eficiente para operações de I/O como requisições HTTP. Threads trariam overhead desnecessário e seriam mais difíceis de debugar.

**Pydantic v2**: A versão 2 tem ganhos reais de performance e a API ficou mais limpa. O pydantic-settings facilita muito o gerenciamento de variáveis de ambiente.

**httpx**: É basicamente o sucessor do requests mas com async/await nativo. API familiar, código moderno.

**Abstract Base Classes**: Facilita criar mocks nos testes e adicionar novos notificadores sem quebrar nada. Princípios SOLID na prática.

## Próximos Passos

Se eu continuar desenvolvendo:

- [ ] Salvar histórico em PostgreSQL ou SQLite
- [ ] Dashboard web para visualizar uptime
- [ ] Suporte a autenticação nas requisições
- [ ] Webhooks customizáveis
- [ ] Métricas de latência P50, P95, P99

## Licença

MIT

---


