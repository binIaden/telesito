from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPoll
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

# ─── Configuración Global ─────────────────────────────────────────
API_ID   = int(os.environ.get('API_ID', 0))
API_HASH = os.environ.get('API_HASH', '')

# Destinatarios compartidos (puede ser el mismo para todos los bots)
RECIPIENTS = [
    int(r.strip())
    for r in os.environ.get('RECIPIENT_IDS', '').split(',')
    if r.strip()
]

# ─── Configuración de cada Bot ────────────────────────────────────
# Agrega tantos bots como quieras siguiendo este patrón
BOTS = [
    {
        "token": os.environ.get('BOT_TOKEN_1', ''),
        "source_chat": int(os.environ.get('SOURCE_CHAT_ID_1', 0)),
        "name": "Bot 1"
    },
    {
        "token": os.environ.get('BOT_TOKEN_2', ''),
        "source_chat": int(os.environ.get('SOURCE_CHAT_ID_2', 0)),
        "name": "Bot 2"
    },
    {
        "token": os.environ.get('BOT_TOKEN_3', ''),
        "source_chat": int(os.environ.get('SOURCE_CHAT_ID_3', 0)),
        "name": "Bot 3"
    },
]
# ─────────────────────────────────────────────────────────────────

async def start_bot(bot_config):
    token       = bot_config["token"]
    source_chat = bot_config["source_chat"]
    name        = bot_config["name"]

    if not token or not source_chat:
        print(f"⚠️  {name}: token o chat ID no configurado, saltando...")
        return

    client = TelegramClient(f'session_{name.replace(" ", "_")}', API_ID, API_HASH)
    await client.start(bot_token=token)

    me = await client.get_me()
    print(f"✅ {name} iniciado: @{me.username}")
    print(f"📡 {name} escuchando en: {source_chat}")

    @client.on(events.NewMessage(chats=source_chat))
    async def handler(event):
        msg = event.message

        if isinstance(msg.media, MessageMediaPoll):
            print(f"⊘ [{name}] Ignorado (encuesta) — mensaje {msg.id}")
            return

        for recipient in RECIPIENTS:
            try:
                await client.forward_messages(recipient, msg)
                print(f"✓ [{name}] Reenviado mensaje {msg.id} → {recipient}")
            except Exception as e:
                print(f"✗ [{name}] Error al enviar a {recipient}: {e}")

    await client.run_until_disconnected()

async def main():
    print(f"📨 Destinatarios: {RECIPIENTS}")
    print("─" * 50)
    await asyncio.gather(*[start_bot(bot) for bot in BOTS])

if __name__ == "__main__":
    asyncio.run(main())
