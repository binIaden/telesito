from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPoll
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

# ─── Configuración Global ─────────────────────────────────────────
API_ID   = int(os.environ.get('API_ID', 0))
API_HASH = os.environ.get('API_HASH', '')

RECIPIENTS = [
    int(r.strip())
    for r in os.environ.get('RECIPIENT_IDS', '').split(',')
    if r.strip()
]

# ─── Configuración de cada Bot ────────────────────────────────────
BOTS = [
    {
        "token": os.environ.get('BOT_TOKEN_2', ''),
        "name": "Bot 1"
    },
    {
        "token": os.environ.get('BOT_TOKEN_3', ''),
        "name": "Bot 2"
    },
]
# ─────────────────────────────────────────────────────────────────

async def start_bot(bot_config):
    token = bot_config["token"]
    name  = bot_config["name"]

    if not token:
        print(f"⚠️  {name}: token no configurado, saltando...")
        return

    client = TelegramClient(f'session_{name.replace(" ", "_")}', API_ID, API_HASH)
    await client.start(bot_token=token)

    me = await client.get_me()
    print(f"✅ {name} iniciado: @{me.username}")
    print(f"📡 {name} escuchando TODOS los chats")

    @client.on(events.NewMessage())
    async def handler(event):
        msg = event.message

        # Saltar encuestas
        if isinstance(msg.media, MessageMediaPoll):
            print(f"⊘ [{name}] Ignorado (encuesta) — mensaje {msg.id}")
            return

        for recipient in RECIPIENTS:
            try:
                await client.forward_messages(recipient, msg)
                print(f"✓ [{name}] Reenviado mensaje {msg.id} (chat {event.chat_id}) → {recipient}")
            except Exception as e:
                print(f"✗ [{name}] Error al enviar a {recipient}: {e}")

    await client.run_until_disconnected()

async def main():
    print(f"📨 Destinatarios: {RECIPIENTS}")
    print("─" * 50)
    await asyncio.gather(*[start_bot(bot) for bot in BOTS])

if __name__ == "__main__":
    asyncio.run(main())
