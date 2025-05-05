from flask import Flask, request, jsonify
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    body = request.get_json()
    texto = body['sessionInfo']['parameters'].get('texto', '')

    system_prompt = """
    Você é um agente da Panorama Móveis que recebe os atendimentos dos clientes
    e tem a função de classificar as solicitações em uma das categorias abaixo:
    - Cancelamento
    - Acareação (quando o cliente afirma que não recebeu a mercadoria, mas consta como entregue)
    - Produto avariado
    - Produto não entregue
    - Rastreio
    Analise a mensagem do cliente e responda apenas com o nome da categoria correspondente.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": texto}
        ]
    )

    resposta_chat = response['choices'][0]['message']['content']

    return jsonify({
        "fulfillment_response": {
            "messages": [
                {"text": {"text": [resposta_chat.strip()]}}
            ]
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)