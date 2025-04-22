import speech_recognition as sr
from openai import OpenAI
from gtts import gTTS
import os
from playsound import playsound

# Configura tu clave y el ID del Assistant
client = OpenAI(api_key="TU_API_KEY_AQUÍ")
assistant_id = "asst_XXXXXXXXXXXX"  # <- pon el ID de tu assistant

def escuchar():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Habla ahora...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        texto = recognizer.recognize_google(audio, language="es-ES")
        print("🗣️ Dijiste:", texto)
        return texto
    except sr.UnknownValueError:
        print("No entendí lo que dijiste.")
        return None

def hablar(texto):
    tts = gTTS(text=texto, lang='es')
    filename = "respuesta.mp3"
    tts.save(filename)
    playsound(filename)
    os.remove(filename)

def enviar_al_assistant(mensaje):
    # Crear nuevo thread
    thread = client.beta.threads.create()

    # Enviar mensaje
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=mensaje
    )

    # Ejecutar assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )

    # Esperar la respuesta
    import time
    while True:
        estado = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if estado.status == "completed":
            break
        time.sleep(1)

    # Obtener respuesta
    mensajes = client.beta.threads.messages.list(thread_id=thread.id)
    for m in reversed(mensajes.data):
        if m.role == "assistant":
            respuesta = m.content[0].text.value
            print("\n🤖 Assistant:", respuesta)
            return respuesta

# === Ciclo Principal ===
while True:
    entrada = escuchar()
    if entrada:
        respuesta = enviar_al_assistant(entrada)
        hablar(respuesta)
