import asyncio
import logging
import re
from telethon import TelegramClient, events, types
from telethon.tl.types import InputMediaDice

API_ID = 26275523
API_HASH = '0c05510640d083029f687cee75f252e3'
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

client = TelegramClient('userbot', API_ID, API_HASH)


async def dicecmd(event):
    args = event.text.split()[1:]

    match = re.match(r"\.dice (\d+) (\d+) (\d+) (-?\d+)", event.text)  # Регулярное выражение для новой команды
    if match:
        values = [int(match.group(i)) for i in range(1, 4)]
        chat_id = int(match.group(4))
        for value in values:
            if not (1 <= value <= 6):
                await event.reply("Значения кубиков должны быть от 1 до 6.")
                return
        try:
            for value in values:
                while True:
                    message = await client.send_message(chat_id, file=InputMediaDice("🎲"))
                    rolled_value = message.media.value
                    if rolled_value != value:
                        await message.delete()
                    else:
                        break
        except Exception as e:
                logger.error(f"Ошибка: {e}")
                await event.reply(f"Произошла ошибка: {e}")
                return


    elif len(args) < 2:
        await event.reply("Неверный формат. Используйте `.dice значение chat_id [количество]` или `.dice значение1 значение2 значение3 chat_id`")
        return

    else: # Старая логика
        try:
            target_value = int(args[0])
            chat_id = int(args[1])
            count = int(args[2]) if len(args) > 2 else 1
        except ValueError:
            await event.reply("Значение, chat_id и количество должны быть числами.")
            return

        if not (1 <= target_value <= 6):
            await event.reply("Значение должно быть от 1 до 6.")
            return

        for _ in range(count):
            while True:
                try:
                    message = await client.send_message(chat_id, file=InputMediaDice("🎲"))
                    rolled_value = message.media.value
                    if rolled_value != target_value:
                        await message.delete()
                    else:
                        break
                except Exception as e:
                    logger.error(f"Ошибка: {e}")
                    await event.reply(f"Произошла ошибка: {e}")
                    return




async def is_owner(event):
    owner_id = 6065764233
    return str(event.sender_id) == str(owner_id)


@client.on(events.NewMessage(pattern=r'\.dice'))
async def handle_dice(event):
    if await is_owner(event):
        await dicecmd(event)
    else:
        await event.reply("Эта команда доступна только владельцу.")


async def main():
    await client.start()
    logger.info("Userbot started.")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())