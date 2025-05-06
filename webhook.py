
from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Configurar sua chave de API do OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# ID do seu assistant do ChatGPT
ASSISTANT_ID = "asst_DMeuS5POFB45TroJC0VwUtpS"

@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json()

    # Extrai o texto diretamente da mensagem do usuário
    user_message = req.get("text", "")

    # Extrai os parâmetros da sessão enviados pelo Dialogflow CX
    session_params = req.get("parameters", {})

    # Adiciona a mensagem na thread se existir
    thread_id = session_params.get("thread_id", None)

    # Constrói o conteúdo do contexto (parâmetros do pedido)
    context_info = "\n".join([
        f"Código de Rastreio: {session_params.get('Código de Rastreio', 'Não informado')}",
        f"Status do Pedido: {session_params.get('Status Pedido', 'Não informado')}",
        f"Último status do rastreio: {session_params.get('Último status do rastreio', 'Não informado')}",
        f"Previsão de entrega: {session_params.get('Previsão de entrega', 'Não informado')}",
        f"Prazo da OC: {session_params.get('Prazo_OC', 'Não informado')}",
        f"Dias de atraso: {session_params.get('R_dias', 'Não informado')}"
    ])

    # Envia a mensagem para o Assistant da OpenAI com contexto
    messages = [
        {"role": "system", "content": "Você é um atendente da Panorama Móveis. Use os dados fornecidos para responder com clareza."},
        {"role": "user", "content": f"{context_info}\n\nPergunta do cliente: {user_message}"}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7
    )

    reply = response.choices[0].message["content"]

    return jsonify({
        "fulfillment_response": {
            "messages": [{
                "text": {"text": [reply]}
            }]
        }
    })

if __name__ == "__main__":
    app.run(debug=True)
