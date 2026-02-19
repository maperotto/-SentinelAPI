# 📊 Dashboard Web - SentinelAPI

Dashboard visual e moderno para monitoramento de APIs em tempo real!

## 🎯 Como Executar

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar Endpoints

Edite o arquivo `endpoints.json` com as APIs que você quer monitorar:

```json
[
    {
        "name": "Google",
        "url": "https://www.google.com",
        "method": "GET",
        "expected_status": 200,
        "timeout": 5
    }
]
```

### 3. Executar Dashboard

```bash
python run_dashboard.py
```

Ou diretamente:

```bash
python web_dashboard.py
```

### 4. Acessar no Navegador

Abra: **http://localhost:5000**

## 📸 Captura para LinkedIn

### Dicas para uma ótima screenshot:

1. **Deixe o sistema rodar por alguns minutos** para coletar dados de histórico
2. **Use tela cheia no navegador** (F11) para tirar screenshot sem barra de endereço
3. **Ajuste o zoom** (Ctrl + ou -) para mostrar tudo em uma tela
4. **Capture quando tiver alguns endpoints com status diferentes** (verde, amarelo, vermelho) - fica mais visual!

### Sugestão de Endpoints para Demo:

Adicione estes ao `endpoints.json` para ter uma demonstração completa:

```json
[
    {
        "name": "Google",
        "url": "https://www.google.com",
        "method": "GET",
        "expected_status": 200,
        "timeout": 5
    },
    {
        "name": "GitHub API",
        "url": "https://api.github.com",
        "method": "GET",
        "expected_status": 200,
        "timeout": 10
    },
    {
        "name": "JSONPlaceholder",
        "url": "https://jsonplaceholder.typicode.com/posts/1",
        "method": "GET",
        "expected_status": 200,
        "timeout": 10
    },
    {
        "name": "HTTPBin",
        "url": "https://httpbin.org/get",
        "method": "GET",
        "expected_status": 200,
        "timeout": 10
    },
    {
        "name": "Fake Endpoint (Down)",
        "url": "https://api-nao-existe-teste-12345.com",
        "method": "GET",
        "expected_status": 200,
        "timeout": 5
    }
]
```

O último endpoint vai falhar de propósito para mostrar como o sistema detecta falhas! 🔴

## 🎨 Recursos do Dashboard

- ✅ **Atualização automática** a cada 5 segundos
- 📈 **Gráfico de tempo de resposta** em tempo real
- 🎯 **Cards coloridos** por status (Verde/Amarelo/Vermelho)
- 📊 **Estatísticas totais** no topo
- 💫 **Animações suaves** e design moderno
- 📱 **Responsivo** - funciona em qualquer tela

## 🚀 Post Sugerido para LinkedIn

```
🚀 SentinelAPI - Sistema de Monitoramento de APIs

Como garantir que suas APIs estão sempre no ar? Criei o SentinelAPI!

✨ Features:
• Monitoramento assíncrono de múltiplos endpoints
• Dashboard web em tempo real
• Alertas automáticos (Telegram, Discord, Email)
• Gráficos de performance
• Docker ready

🛠️ Tech Stack: Python, asyncio, Flask, Chart.js

O dashboard monitora continuamente e mostra status visual imediato. 
Perfeito para demonstrar habilidades em:
- Programação assíncrona
- Web development
- Monitoramento de sistemas
- DevOps

#Python #API #Monitoring #DevOps #WebDevelopment

Código: github.com/seu-usuario/SentinelAPI
```

## 🔧 Troubleshooting

### Porta 5000 já em uso?

Edite `web_dashboard.py`, linha final:
```python
app.run(host="0.0.0.0", port=8080, debug=False)
```

### Não está atualizando?

- Verifique o console do navegador (F12) por erros
- Certifique-se que o arquivo `endpoints.json` está correto
- Verifique os logs no terminal onde o dashboard está rodando

## 💡 Melhorias Futuras

Ideias para expandir o projeto:
- [ ] Autenticação de usuários
- [ ] Histórico de 24h no banco de dados
- [ ] Exportar relatórios PDF
- [ ] Webhooks personalizados
- [ ] Testes de carga
- [ ] Métricas de SLA
