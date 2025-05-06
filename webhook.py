from flask import Flask, request, jsonify
import openai
import os
import time

app = Flask(__name__)

# Inicializa o cliente OpenAI com a chave da sua conta
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Cache local de sessões ↔ thread_id (substitua por banco/Redis em produção)
sessions = {}

@app.route('/webhook', methods=['POST'])
def webhook():
    body = request.get_json()

    # Extrai o texto e identificadores
    texto = body.get('sessionInfo', {}).get('parameters', {}).get('texto', '')
    thread_id_param = body.get('sessionInfo', {}).get('parameters', {}).get('thread_id')
    session_id = body.get('sessionInfo', {}).get('session', 'anon')

    # Usa thread_id fixo (manual) ou session como fallback
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

    # Adiciona a nova mensagem do cliente
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=texto
    )

    # Executa o assistant
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id="asst_DMeuS5POFB45TroJC0VwUtpS"
    )

    # Espera até a execução completar
    while True:
        status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        if status.status == "completed":
            break
        time.sleep(0.5)

    # Captura a resposta do assistant
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
