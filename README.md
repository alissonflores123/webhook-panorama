# Webhook para ChatGPT (Assistants API) integrado ao Dialogflow CX

## Instruções

### 1. Pré-requisitos
- Python 3.8+
- Conta OpenAI com Assistants ativado
- Chave de API OpenAI (`OPENAI_API_KEY`)

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

### 3. Executar localmente
```bash
python webhook.py
```

### 4. Subir em produção (Render, Railway, etc.)
- Use o arquivo `Procfile` como comando de inicialização: `web: python webhook.py`
- Adicione a variável de ambiente:
  - `OPENAI_API_KEY=sk-...`

### 5. Configurar Dialogflow CX
- Parâmetro `texto`: `$request.generative.value`
- Parâmetro `thread_id`: use ID de atendimento (opcional)
- Endpoint do webhook: `https://seu-domínio.com/webhook`
