from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import MessageMediaPoll
import os
from dotenv import load_dotenv

load_dotenv()

# ─── Configuración ───────────────────────────────────────────────
API_ID      = int(os.environ.get('API_ID', 0))
API_HASH    = os.environ.get('API_HASH', '')
BOT_TOKEN   = os.environ.get('BOT_TOKEN', '')
SOURCE_CHAT = int(os.environ.get('SOURCE_CHAT_ID', 0))   # ID del grupo origen (negativo)
RECIPIENTS  = [
    int(r.strip())
    for r in os.environ.get('RECIPIENT_IDS', '').split(',')
    if r.strip()
]
# ─────────────────────────────────────────────────────────────────

client = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@client.on(events.NewMessage(chats=SOURCE_CHAT))
async def handler(event):
    msg = event.message

    # Saltar encuestas
    if isinstance(msg.media, MessageMediaPoll):
        print(f"⊘ Ignorado (encuesta) — mensaje {msg.id}")
        return

    for recipient in RECIPIENTS:
        try:
            await client.forward_messages(recipient, msg)
            print(f"✓ Reenviado mensaje {msg.id} → {recipient}")
        except Exception as e:
            print(f"✗ Error al enviar a {recipient}: {e}")

async def main():
    me = await client.get_me()
    print(f"✅ Bot iniciado: @{me.username}")
    print(f"📡 Escuchando mensajes en el chat: {SOURCE_CHAT}")
    print(f"📨 Destinatarios: {RECIPIENTS}")
    print("─" * 50)
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
