import os
import openai
import traceback
from flask import Flask, request, jsonify

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/debug", methods=["POST"])
def debug_thread():
    try:
        data = request.get_json()
        thread_id = data.get("sessionInfo", {}).get("parameters", {}).get("thread_id", "").strip()

        if not thread_id:
            return jsonify({
                "fulfillment_response": {
                    "messages": [{
                        "text": {
                            "text": ["Parâmetro thread_id ausente."]
                        }
                    }]
                }
            })

        messages = openai.beta.threads.messages.list(thread_id=thread_id)

        historico = []
        for msg in reversed(messages.data):  # ordem cronológica
            role = msg.role.upper()
            content = msg.content[0].text.value if msg.content else "[mensagem vazia]"
            historico.append(f"{role}: {content}")

        historico_texto = "\n\n".join(historico)

        return jsonify({
            "fulfillment_response": {
                "messages": [{
                    "text": {
                        "text": [historico_texto[:400000]]  # corta se passar de 4096 caracteres
                    }
                }]
            }
        })

    except Exception as e:
        print("Erro no /debug:", str(e))
        traceback.print_exc()
        return jsonify({
            "fulfillment_response": {
                "messages": [{
                    "text": {
                        "text": ["Erro ao recuperar histórico."]
                    }
                }]
            }
        })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
