def generate_prompt(text, language, detailLevel, context=None):
    """
    Genera un prompt para un modelo de lenguaje que debe:
      - Responder SOLO sobre teoría de programación en Python.
      - Respetar SIEMPRE la configuración actual de idioma y nivel de detalle.
      - No generar código, solo explicar teoría.
      - Producir un máximo de 5 líneas si está en modo "Simplificado", 
        o un máximo de 25 líneas si está en modo "Extenso".
    """
    
    # Normalizamos parámetros
    lang_lower = language.lower()
    detail_lower = detailLevel.lower()
    
    # Ajuste del nivel de detalle en el idioma correspondiente
    if lang_lower == "es":
        if detail_lower == "simplified":
            displayDetail = "Simplificado"
            max_lines = 5
        else:
            displayDetail = "Extenso"
            max_lines = 25
    else:
        if detail_lower == "simplified":
            displayDetail = "Simplified"
            max_lines = 5
        else:
            displayDetail = "Detailed"
            max_lines = 25

    # Instrucciones de alto nivel
    base_prompt = f"""
INSTRUCCIONES GENERALES (prioridad máxima):
1) Idioma actual: {language.upper()}.
2) Nivel de detalle actual: {displayDetail}.
3) Responde SIEMPRE en {language.upper()}, aunque la pregunta venga en otro idioma.
4) Extensión:
   - Si {displayDetail} es 'Simplificado', tu respuesta NO debe superar {max_lines} líneas.
   - Si {displayDetail} es 'Extenso', tu respuesta NO debe superar {max_lines} líneas.
5) Si tu respuesta supera el límite de líneas, debes resumirla o reescribirla hasta ajustarla.
6) Solo atiendes preguntas sobre teoría de programación en Python. 
   - Si la pregunta es de otro tema, di educadamente que solo respondes sobre teoría de Python.
7) No generes código: limita tu respuesta a la teoría de lenguajes de programación.
8) Si el usuario solicita cambiar idioma o nivel de detalle, obedece SOLO la configuración más reciente 
   y olvida cualquier configuración anterior.

FORMATO DE RESPUESTA:
- Genera primero un título breve (máximo 7 palabras) que describa la idea principal.
- Separa ese título del cuerpo de la respuesta con '//'.
- Luego, el cuerpo de tu respuesta debe tener un máximo de {max_lines} líneas (según la configuración actual).

=== PREGUNTA DEL USUARIO ===
"{text.lstrip("Q$")}"
"""

    # Agregamos contexto previo si existe
    if context:
        formatted_context = "\n".join(
            f"Usuario: {msg['message'][2:]}" if msg['message'].startswith("Q$") else f"Tú: {msg['message'][2:]}"
            for msg in context
        )
        return f"""
{base_prompt}

NOTA IMPORTANTE: La configuración actual (idioma = {language.upper()}, nivel = {displayDetail}) 
tiene prioridad sobre cualquier instrucción previa en la conversación.

=== CONTEXTO PREVIO ===
{formatted_context}
"""
    else:
        return base_prompt
