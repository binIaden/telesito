from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import MessageMediaPoll
import os

# ─── Configuración ───────────────────────────────────────────────
API_ID       = int(os.environ.get('API_ID', 0))
API_HASH     = os.environ.get('API_HASH', '')
SESSION      = os.environ.get('SESSION_STRING', '')
SOURCE_CHAT  = int(os.environ.get('SOURCE_CHAT_ID', 0))   # ID del grupo origen
RECIPIENTS   = [
    int(r.strip())
    for r in os.environ.get('RECIPIENT_IDS', '').split(',')
    if r.strip()
]
# ─────────────────────────────────────────────────────────────────

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_CHAT))
async def handler(event):
    msg = event.message

    # Saltar encuestas (Telegram no permite reenviarlas así)
    if isinstance(msg.media, MessageMediaPoll):
        print(f"⊘ Ignorado (encuesta) — mensaje {msg.id}")
        return

    for recipient in RECIPIENTS:
        try:
            await client.send_message(recipient, msg)
            print(f"✓ Reenviado mensaje {msg.id} → {recipient}")
        except Exception as e:
            print(f"✗ Error al enviar a {recipient}: {e}")

async def main():
    await client.start()
    me = await client.get_me()
    print(f"✅ Sesión iniciada como: {me.first_name} (@{me.username})")
    print(f"📡 Escuchando mensajes en el chat: {SOURCE_CHAT}")
    print(f"📨 Destinatarios: {RECIPIENTS}")
    print("─" * 50)
    await client.run_until_disconnected()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())