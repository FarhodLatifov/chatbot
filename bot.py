"""Telegram bot for hashtag combination generation."""

import asyncio
import io
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile

from config import BOT_TOKEN, logger, BLOCK_SIZE
from generator import generate_combinations, split_into_blocks, format_block, parse_input


# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Welcome message
WELCOME_MESSAGE = """
🏷️ *Генератор хэштегов*

Создаю все комбинации хэштегов из корней и суффиксов для комментариев.

*Отправьте сообщение в формате:*
```
Корни: слово1, слово2, слово3
Суффиксы: окончание1, окончание2
```

*Пример:*
```
Корни: отопление, котел, котельная
Суффиксы: москва, спб, купить, монтаж
```

*Результат:* `#отоплениемосква` `#отоплениеспб` `#котелкупить` и т.д.

✅ Блоки по {block_size} штук (лимит на комментарий)
✅ Без повторов
✅ Готово для копипаста
""".format(block_size=BLOCK_SIZE)


HELP_MESSAGE = """
📖 *Справка*

*Команды:*
/start - Начать работу с ботом
/help - Показать эту справку

*Формат ввода:*
```
Корни: корень1, корень2, корень3
Суффиксы: суффикс1, суффикс2
```

*Особенности:*
• Хэштеги создаются в формате #корень+суффикс
• Дубликаты автоматически удаляются
• Результат разбивается на блоки по {block_size} хэштегов
• Можно скачать все хэштеги в TXT файле

*Поддерживаемые языки ввода:*
• Корни / Roots
• Суффиксы / Suffixes
""".format(block_size=BLOCK_SIZE)


@dp.message(Command("start"))
async def cmd_start(message: Message):
    """Handle /start command."""
    await message.answer(WELCOME_MESSAGE, parse_mode="Markdown")


@dp.message(Command("help"))
async def cmd_help(message: Message):
    """Handle /help command."""
    await message.answer(HELP_MESSAGE, parse_mode="Markdown")


@dp.message(F.text)
async def handle_input(message: Message):
    """Handle user input with roots and suffixes."""
    text = message.text
    
    # Parse input
    roots, suffixes = parse_input(text)
    
    # Validate input
    if not roots:
        await message.answer(
            "❌ Не найдены корни. Пожалуйста, укажите их в формате:\n"
            "`Корни: слово1, слово2, слово3`",
            parse_mode="Markdown"
        )
        return
    
    if not suffixes:
        await message.answer(
            "❌ Не найдены суффиксы. Пожалуйста, укажите их в формате:\n"
            "`Суффиксы: окончание1, окончание2`",
            parse_mode="Markdown"
        )
        return
    
    # Generate combinations
    hashtags = generate_combinations(roots, suffixes)
    
    if not hashtags:
        await message.answer("❌ Не удалось создать хэштеги. Проверьте ввод.")
        return
    
    # Split into blocks
    blocks = split_into_blocks(hashtags)
    
    # Send summary
    await message.answer(
        f"✅ *Создано {len(hashtags)} хэштегов*\n"
        f"📦 Разбито на {len(blocks)} блоков по {BLOCK_SIZE} шт.\n\n"
        f"Корни: `{', '.join(roots)}`\n"
        f"Суффиксы: `{', '.join(suffixes)}`",
        parse_mode="Markdown"
    )
    
    # Send each block
    for i, block in enumerate(blocks, 1):
        block_text = format_block(block)
        await message.answer(
            f"*Блок {i}/{len(blocks)}* ({len(block)} хэштегов):\n\n"
            f"`{block_text}`",
            parse_mode="Markdown"
        )
    
    # Generate and send TXT file
    all_hashtags_text = "\n\n".join([
        f"Блок {i}:\n{format_block(block)}" 
        for i, block in enumerate(blocks, 1)
    ])
    
    file_content = (
        f"Хэштеги (всего: {len(hashtags)})\n"
        f"Корни: {', '.join(roots)}\n"
        f"Суффиксы: {', '.join(suffixes)}\n"
        f"{'=' * 40}\n\n"
        f"{all_hashtags_text}"
    ).encode("utf-8")
    
    file = BufferedInputFile(file_content, filename="hashtags.txt")
    await message.answer_document(
        file,
        caption="📄 Все хэштеги в TXT файле для скачивания"
    )
    
    logger.info(f"Generated {len(hashtags)} hashtags for user {message.from_user.id}")


async def main():
    """Start the bot."""
    logger.info("Starting Hashtag Generator Bot...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
