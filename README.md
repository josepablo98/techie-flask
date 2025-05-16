# Techie – Microservicio de IA (Flask)

Este microservicio está desarrollado en Flask (Python) y se encarga de procesar las peticiones del usuario mediante la API de Gemini. Actúa como componente especializado en la generación de respuestas, desacoplado del backend principal.

## Tecnologías utilizadas

- Flask (framework web en Python)
- Flask-CORS (control de orígenes cruzados)
- requests (llamadas HTTP a la API de Gemini)
- python-dotenv (gestión de variables de entorno)

## Funcionalidades

- Procesamiento de texto enviado por el frontend
- Generación de prompts personalizados según:
  - Idioma del usuario (español o inglés)
  - Nivel de detalle (simplificado o extenso)
  - Contexto global y conversaciones anteriores
- Comunicación directa con la API de Gemini (`gemini-pro`)
- Devolución de la respuesta procesada al usuario
- Manejo de errores y control de formato del contenido recibido

## Scripts

```bash
pip install -r requirements.txt   # Instalar dependencias
python server.py                  # Ejecutar el microservicio
