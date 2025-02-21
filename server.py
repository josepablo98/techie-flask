from flask import Flask, request, jsonify
from dotenv import load_dotenv
import requests
import os

load_dotenv()

app = Flask(__name__)

@app.route("/chat/fetch", methods=["POST"])
def fetch_gemini_api():
    api_key = os.getenv("API_KEY")
    if not api_key:
        return jsonify({"ok": False, "message": "API_KEY no encontrada en las variables de entorno"}), 500

    req_json = request.get_json()
    text = req_json.get("text")
    context = req_json.get("context", [])

    if not text:
        return jsonify({"ok": False, "message": "Falta el parámetro 'text'"}), 400

    text_prompting_engineering = f'''
        Debes responder únicamente preguntas sobre teoría de programación, sea el lenguaje de programación que sea.  
        Si la pregunta del usuario no está relacionada con este tema, responde de forma educada explicando que solo puedes ayudar con asuntos relacionados con la programación.  

        Tu respuesta debe sonar natural y bien estructurada, sin repetir frases innecesarias.  
        Si el usuario insiste en preguntar sobre otro tema, recuérdale amablemente que solo puedes responder sobre teoría de programación.
        Si el usuario te saluda o te agradece, responde de manera educada y amigable. Siempre debes ser simpático y educado, evitando respuestas cortantes o frías.
        Si el usuario te hace una pregunta que no entiendes, pide que la reformule de manera más clara y específica.
        Si el usuario insulta o hace comentarios inapropiados, responde de manera educada y profesional, diciendo que no puedes responder a ese tipo de comentarios.
        Si el usuario te pide información personal o información que puede ser usada para realizar actividades ilegales, responde de manera profesional y cortés, diciendo que no puedes proporcionar esa información.
        Si el usuario te pide generar código, no lo hagas. Recuerda que solo puedes responder preguntas sobre teoría de lenguajes de programación.
        Aunque tú sabes que es sobre la "teoría de programación", cuando lo menciones en tus respuestas, utiliza el término "programación" para que el usuario entienda mejor.

        Antes de responder, genera un título breve y natural que no supere las seis o siete palabras basado en la pregunta del usuario.  
        El título debe resumir la idea principal de la pregunta de manera clara y amigable. El formato sería el siguiente: titulo//mensaje, siendo "título" el título que tú des, y "mensaje" el mensaje
        de respuesta en sí. No uses títulos genéricos como "Lenguaje Teoría" siendo el "Lenguaje" el lenguaje de programación sobre el que
        te está preguntando el usuario.  
        Te repito que separes el título del mensaje con "//".

        La pregunta o solicitud que el usuario ha hecho es la siguiente: "{text}".
    '''

    if context:
        formatted_context = "\n".join(
            f"Usuario: {msg}" if i % 2 == 0 else f"Tú: {msg}"
            for i, msg in [(item["index"], item["message"]) for item in context]
        )
        text_prompting_engineering = f'''
        Antes de esta pregunta, la conversación ha sido la siguiente:
        {formatted_context}
        Teniendo en cuenta este contexto, responde de manera coherente y natural a la pregunta actual:
        {text_prompting_engineering}
        '''

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

    try:
        payload = {
            "contents": [{
                "parts": [{"text": text_prompting_engineering}]
            }]
        }

        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()

        return jsonify({
            "ok": True,
            "response": response_data["candidates"][0]["content"]["parts"][0]["text"]
        }), 200

    except Exception as error:
        return jsonify({
            "ok": False,
            "message": "Error en el servidor",
            "error": str(error)
        }), 500

if __name__ == "__main__":
    app.run(debug=True)