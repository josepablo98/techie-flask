def generate_prompt(text, language, detailLevel, context=None, globalContext=None):
    lang_lower = language.lower()
    detail_lower = detailLevel.lower()

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
- Separa ese título del cuerpo de la respuesta con '//' (doble barra).
- Luego, el cuerpo de tu respuesta debe tener un máximo de {max_lines} líneas (según la configuración actual).
"""

    # Añadir Global Context si existe
    if globalContext:
        base_prompt += f"""

=== CONTEXTO PERSONAL GLOBAL (aplícalo solo si NO contradice las instrucciones anteriores) ===
{globalContext.strip()}
"""

    # Añadir contexto de conversación si existe
    if context:
        formatted_context = "\n".join(
            f"Usuario: {msg['message'][2:]}" if msg['message'].startswith("Q$") else f"Tú: {msg['message'][2:]}"
            for msg in context
        )
        base_prompt += f"""

NOTA IMPORTANTE: La configuración actual (idioma = {language.upper()}, nivel = {displayDetail}) 
tiene prioridad sobre cualquier instrucción previa en la conversación.

=== CONTEXTO DE CONVERSACIÓN ===
{formatted_context}
"""

    # Añadir pregunta del usuario
    base_prompt += f"""

=== PREGUNTA DEL USUARIO ===
"{text.lstrip("Q$")}"
"""
    return base_prompt
