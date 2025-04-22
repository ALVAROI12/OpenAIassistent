# Paso 1: Instalar el SDK actualizado de OpenAI
!pip install --upgrade openai

# Paso 2: Importar y configurar el cliente moderno
from openai import OpenAI
import time

# Paso 3: Crear el cliente con tu API Key
client = OpenAI(api_key="TU_API_KEY_AQUÍ")  # <- pon tu API key aquí

# Paso 4: ID de tu Assistant creado en platform.openai.com/assistants
assistant_id = "asst_XXXXXXXXXXXX"  # <- pon aquí el ID de tu assistant

# Paso 5: Crear un thread nuevo
thread = client.beta.threads.create()
print("🧵 Thread creado:", thread.id)

# Paso 6: Enviar un mensaje al Assistant
user_input = "Hola, ¿me puedes explicar cómo funciona una red neuronal?"
client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=user_input
)

# Paso 7: Lanzar la ejecución del Assistant
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant_id
)

# Esperar a que termine la ejecución
print("⏳ Esperando respuesta...")
while True:
    run_status = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    if run_status.status == "completed":
        break
    elif run_status.status == "failed":
        print("❌ El Assistant falló.")
        break
    time.sleep(1)

# Paso 8: Obtener la respuesta
messages = client.beta.threads.messages.list(thread_id=thread.id)

# Mostrar la última respuesta del Assistant
for message in reversed(messages.data):
    if message.role == "assistant":
        print("\n🤖 Assistant dice:")
        print(message.content[0].text.value)
        break
