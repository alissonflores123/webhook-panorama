### COMO USAR ESTE WEBHOOK COM DIALOGFLOW CX + CHATGPT

Este projeto é um webhook em Flask que você pode usar para conectar o Dialogflow CX à API do ChatGPT da OpenAI.
Ele já está configurado para classificar mensagens dos clientes da Panorama Móveis nas categorias:

- Cancelamento
- Acareação (quando consta como entregue, mas o cliente diz que não recebeu)
- Produto avariado
- Produto não entregue
- Rastreio

---

### PASSO A PASSO PARA SUBIR NO RENDER.COM

1. Vá em https://render.com e crie uma conta.
2. Crie um novo repositório no GitHub e envie os arquivos deste projeto.
3. No Render:
   - Crie um novo Web Service.
   - Conecte com seu GitHub.
   - Escolha o repositório com este projeto.
   - No campo "Start Command", coloque:
     python webhook.py
   - No campo "Environment Variables", adicione:
     - Nome: OPENAI_API_KEY
     - Valor: (sua chave da OpenAI, ex: sk-...)
4. Aguarde o deploy.
5. Copie a URL final (ex: https://meuapp.onrender.com/webhook)

---

### CONFIGURAR NO DIALOGFLOW CX

1. Vá em "Manage" > "Webhooks"
2. Crie um novo webhook com a URL gerada acima.
3. Em seu fluxo:
   - Crie um parâmetro chamado `texto`
   - Passe esse parâmetro no corpo do webhook
4. O webhook retornará uma das categorias listadas como resposta.

---

Pronto! Seu Dialogflow agora está classificado com inteligência da OpenAI.