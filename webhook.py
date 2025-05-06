
from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

openai.api_key = "SUA_CHAVE_API_OPENAI"

ASSISTANT_ID = "asst_DMeuS5POFB45TroJC0VwUtpS"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    user_input = data.get("text", "")  # pega diretamente o texto da mensagem

    # Extrai os parâmetros adicionais que o Dialogflow envia (se existirem)
    session_params = data.get("sessionInfo", {}).get("parameters", {})
    thread_id = session_params.get("thread_id")

    # Cria um novo thread se não existir
    if not thread_id:
        thread = openai.beta.threads.create()
        thread_id = thread.id

    # Envia a mensagem para o assistant
    openai.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_input
    )

    # Roda a thread com o assistant configurado
    run = openai.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=ASSISTANT_ID
    )

    # Aguarda a conclusão da execução
    while True:
        run_status = openai.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        if run_status.status == "completed":
            break

    messages = openai.beta.threads.messages.list(thread_id=thread_id)
    response_text = messages.data[0].content[0].text.value if messages.data else "Desculpe, não entendi."

    return jsonify({
        "fulfillment_response": {
            "messages": [{
                "text": {
                    "text": [response_text]
                }
            }]
        },
        "session_info": {
            "parameters": {
                "thread_id": thread_id
            }
        }
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
