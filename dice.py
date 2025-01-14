import asyncio
import logging
import re

from pyrogram import Client, filters, idle
from pyrogram.errors import FloodWait
from pyrogram.types import Message

# Замените значения на свои
API_ID = 26275523
API_HASH = '0c05510640d083029f687cee75f252e3'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Используйте session_name для имени сессии (например, "my_account")
app = Client("my_account", api_id=API_ID, api_hash=API_HASH)

owner_id = 6065764233 # Ваш user ID


@app.on_message(filters.command("dice") & filters.user(owner_id))
async def dicecmd(client: Client, message: Message):
    args = message.text.split()[1:]

    match = re.match(r"\.dice (\d+) (\d+) (\d+) (-?\d+)", message.text)
    if match:
        values = [int(match.group(i)) for i in range(1, 4)]
        chat_id = int(match.group(4))
        for value in values:
            if not (1 <= value <= 6):
                await message.reply_text("Значения кубиков должны быть от 1 до 6.")
                return

        try:
            tasks = [roll_dice_until(client, chat_id, value) for value in values]
            await asyncio.gather(*tasks)
        except Exception as e:
            logger.error(f"Ошибка: {e}")
            await message.reply_text(f"Произошла ошибка: {e}")
            return

    elif len(args) < 2:
        await message.reply_text("Неверный формат. Используйте `.dice значение chat_id [количество]` или `.dice значение1 значение2 значение3 chat_id`")
        return

    else:
        try:
            target_value = int(args[0])
            chat_id = int(args[1])
            count = int(args[2]) if len(args) > 2 else 1
        except ValueError:
            await message.reply_text("Значение, chat_id и количество должны быть числами.")
            return

        if not (1 <= target_value <= 6):
            await message.reply_text("Значение должно быть от 1 до 6.")
            return

        tasks = [roll_dice_until(client, chat_id, target_value) for _ in range(count)]
        await asyncio.gather(*tasks)


async def roll_dice_until(client: Client, chat_id: int, target_value: int):
    while True:
        try:
            msg = await client.send_dice(chat_id, emoji="🎲")
            if msg.dice.value == target_value:
                return
            try:
                await msg.delete()
            except: pass
        except FloodWait as e:
            await asyncio.sleep(e.x + 1)
        except Exception as e:
            logger.error(f"Ошибка: {e}")



async def main():
    await app.start()
    logger.info("Userbot started.")
    await idle()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
