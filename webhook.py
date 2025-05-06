from flask import Flask, request, jsonify
import openai
import os
import time

app = Flask(__name__)
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

sessions = {}

@app.route('/webhook', methods=['POST'])
def webhook():
    body = request.get_json()
    params = body.get('sessionInfo', {}).get('parameters', {})
    texto = params.get('texto', '')
    thread_id_param = params.get('thread_id')
    session_id = body.get('sessionInfo', {}).get('session', 'anon')

    # Informações adicionais
    codigo_rastreio = params.get("Código de Rastreio")
    ultimo_status = params.get("Último status do rastreio")
    previsao_entrega = params.get("Previsão de entrega")
    r_dias = params.get("R_dias")
    prazo_oc = params.get("Prazo_OC")
    status_pedido = params.get("Status Pedido")

    # Mensagem que será enviada para o Assistant
    mensagem_cliente = f"""
Mensagem do cliente: {texto}

Informações do pedido:
- Código de rastreio: {codigo_rastreio}
- Último status: {ultimo_status}
- Previsão de entrega: {previsao_entrega}
- Dias até o prazo da transportadora (R_dias): {r_dias}
- Prazo de envio (OC): {prazo_oc}
- Status do pedido: {status_pedido}
"""

    # Define o thread_id com fallback
    if thread_id_param:
        thread_key = thread_id_param
        if thread_key not in sessions:
            thread = client.beta.threads.create()
            sessions[thread_key] = thread.id
    else:
        thread_key = session_id
        if thread_key not in sessions:
            thread = client.beta.threads.create()
            sessions[thread_key] = thread.id

    thread_id = sessions[thread_key]

    # Envia mensagem do cliente para o Assistant
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=mensagem_cliente
    )

    # Executa o Assistant
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id="asst_DMeuS5POFB45TroJC0VwUtpS"
    )

    # Espera resposta
    while True:
        status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        if status.status == "completed":
            break
        time.sleep(0.5)

    # Retorna resposta ao Dialogflow
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    resposta_chat = messages.data[0].content[0].text.value.strip()

    return jsonify({
        "fulfillment_response": {
            "messages": [
                {"text": {"text": [resposta_chat]}}
            ]
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
