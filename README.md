# SentinelAPI

Sistema de monitoramento de saúde de APIs com notificações automáticas em tempo real.

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Sobre o Projeto

Desenvolvi o SentinelAPI para resolver um problema que sempre enfrentei: saber quando algum serviço externo cai antes que os usuários reclamem. O sistema monitora múltiplas APIs simultaneamente e dispara alertas instantâneos via Telegram, Discord ou email quando detecta problemas.

O diferencial aqui está na arquitetura assíncrona que permite checar dezenas de endpoints ao mesmo tempo sem travar, usando asyncio do Python. Além disso, apliquei design patterns como Strategy para os notificadores, o que facilita adicionar novos canais de alerta sem mexer no código existente.

## Por Que Esse Projeto?

Trabalhei anteriormente com integrações mobile no Banco do Brasil e sempre tive a preocupação com a disponibilidade dos serviços. Esse projeto demonstra minha capacidade de:

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

## Tecnologias Utilizadas

### Core
- **Python 3.11**: Linguagem principal com suporte às últimas features
- **asyncio**: Para operações assíncronas nativas
- **httpx**: Cliente HTTP assíncrono moderno (sucessor do requests)

### Validação e Configuração
- **Pydantic v2**: Validação de dados com type hints
- **pydantic-settings**: Gerenciamento de variáveis de ambiente de forma tipada

### Interface e Visualização
- **Rich**: Output colorido e tabelas formatadas no terminal

### Testes e Qualidade
- **Pytest**: Framework de testes com suporte assíncrono
- **pytest-cov**: Cobertura de código
- **mypy**: Type checking estático
- **ruff**: Linter moderno e rápido

### DevOps
- **Docker**: Containerização
- **GitHub Actions**: CI/CD automatizado

## Estrutura do Projeto

```
sentinel_api/
├── app/
│   ├── core/                 # Configurações centrais
│   │   ├── config.py        # Settings com pydantic-settings
│   │   ├── logger.py        # Sistema de logs estruturado
│   │   └── models.py        # Modelos de dados
│   ├── monitor/              # Lógica de monitoramento
│   │   └── health_checker.py # Verificações assíncronas
│   ├── notifier/             # Sistema de alertas
│   │   ├── base.py          # Interface abstrata (ABC)
│   │   ├── telegram.py      # Notificador Telegram
│   │   ├── discord.py       # Notificador Discord
│   │   └── email.py         # Notificador Email
│   └── main.py              # Entrypoint da aplicação
├── tests/                    # Testes automatizados
├── .github/workflows/        # CI/CD
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml           # Gerenciamento com Poetry
└── endpoints.json           # Configuração de endpoints
```

## Como Funciona

### 1. Arquitetura do Monitoramento

O HealthChecker usa context managers assíncronos para gerenciar conexões HTTP eficientemente. Cada endpoint é verificado em paralelo usando `asyncio.gather()`, o que reduz drasticamente o tempo total de monitoramento.

```python
async with HealthChecker(max_retries=3) as checker:
    results = await checker.check_multiple(endpoints)
```

### 2. Sistema de Notificadores

Implementei o padrão Strategy através de uma classe base abstrata. Cada notificador implementa a mesma interface, permitindo adicionar novos canais sem modificar o código principal:

- **TelegramNotifier**: Usa a Bot API do Telegram com formatação Markdown
- **DiscordNotifier**: Webhooks com embeds personalizados
- **EmailNotifier**: SMTP com HTML formatado

### 3. Validação com Pydantic

Todos os dados são validados na entrada. Por exemplo, o EndpointConfig garante que URLs sejam válidas e que métodos HTTP estejam corretos antes mesmo do monitoramento começar.

### 4. Tratamento de Erros

O sistema classifica problemas em três níveis:
- **HEALTHY**: Endpoint respondendo conforme esperado
- **DEGRADED**: Responde mas com status code inesperado
- **DOWN**: Timeout ou erro de conexão

## Instalação e Uso

### Opção 1: Com Poetry (Recomendado)

```bash
# Instalar dependências
poetry install

# Copiar arquivo de exemplo
cp .env.example .env

# Editar .env com suas credenciais
# Configure pelo menos um notificador

# Editar endpoints.json com as URLs que deseja monitorar

# Rodar
poetry run python -m app.main
```

### Opção 2: Com Docker

```bash
# Configurar .env
cp .env.example .env

# Subir container
docker-compose up -d

# Ver logs
docker-compose logs -f
```

## Configuração

### Variáveis de Ambiente (.env)

```env
MONITOR_INTERVAL=60          # Intervalo entre verificações (segundos)
REQUEST_TIMEOUT=10           # Timeout por requisição
MAX_RETRIES=3               # Tentativas antes de considerar DOWN

# Telegram (obtenha com @BotFather)
TELEGRAM_BOT_TOKEN=seu_token
TELEGRAM_CHAT_ID=seu_chat_id

# Discord (crie um webhook no servidor)
DISCORD_WEBHOOK_URL=sua_url

# Email
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
# Todos os testes
poetry run pytest

# Com cobertura
poetry run pytest --cov=app --cov-report=term-missing

# Type checking
poetry run mypy app/
```

## Aprendizados e Decisões Técnicas

### Por que asyncio em vez de threading?

O asyncio é mais eficiente para I/O-bound operations como requisições HTTP. Usar threads seria overhead desnecessário e mais difícil de debugar.

### Por que Pydantic v2?

A versão 2 traz melhorias significativas de performance e uma API mais clara para validação. O pydantic-settings integra perfeitamente com variáveis de ambiente.

### Por que httpx?

O httpx é o sucessor natural do requests, com suporte nativo a async/await. Mantém uma API familiar mas moderna.

### Por que Abstract Base Classes?

Facilita testar (posso criar mocks) e adicionar novos notificadores sem quebrar código existente. Isso demonstra conhecimento de SOLID principles.

## Próximas Melhorias

Se fosse expandir o projeto, adicionaria:

- [ ] Persistência de histórico em banco de dados
- [ ] Dashboard web com gráficos de uptime
- [ ] Suporte a autenticação nas requisições
- [ ] Webhooks customizáveis
- [ ] Métricas de performance (P50, P95, P99)

## Licença

MIT

---

Desenvolvido para demonstrar conhecimento profissional em Python e engenharia de software.
