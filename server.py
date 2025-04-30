from flask import Flask, request, jsonify
from dotenv import load_dotenv
from prompt import generate_prompt
import requests
import os
from flask_cors import CORS

load_dotenv()
app = Flask(__name__)
CORS(app)



@app.route("/chat/fetch", methods=["POST"])
def fetch_gemini_api():
    api_key = os.getenv("API_KEY")
    if not api_key:
        return jsonify({"ok": False, "message": "API_KEY no encontrada en las variables de entorno"}), 500

    req_json = request.get_json()
    text = req_json.get("text")
    language = req_json.get("language")
    detailLevel = req_json.get("detailLevel")
    context = req_json.get("context", [])

    if not text:
        message = "Falta el parámetro 'text'" if language == "es" else "Missing 'text' parameter"
        return jsonify({"ok": False, "message": message}), 400

    text_prompting_engineering = generate_prompt(text, language, detailLevel, context)

    print(text_prompting_engineering)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

    try:
        payload = {
            "contents": [{
                "parts": [{"text": text_prompting_engineering}]
            }]
        }
        
        print(payload)

        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()
        return jsonify({
            "ok": True,
            "response": response_data["candidates"][0]["content"]["parts"][0]["text"]
        }), 200

    except Exception as error:
        message = "Error en el servidor" if language == "es" else "Server error"
        return jsonify({
            "ok": False,
            "message": message,
            "error": str(error)
        }), 500

if __name__ == "__main__":
    app.run(debug=True)