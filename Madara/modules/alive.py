import random
from sys import version_info

from pyrogram import __version__ as pver
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from telegram import __version__ as lver
from telethon import __version__ as tver

from Madara import BOT_NAME, pgram
from Uchiha.helper import PHOTO

ASAU = [
    [
        InlineKeyboardButton(
            text="📗 𝙐𝙋𝘿𝘼𝙏𝙀𝙎", url=f"https://t.me/JujutsuHighNetwork"
        ),
        InlineKeyboardButton(
            text="🚑 𝙎𝙐𝙋𝙋𝙊𝙍𝙏", url=f"https://t.me/Anime_Krew"
        ),
    ],
]


@pgram.on_message(filters.command("alive"))
async def awake(_, message: Message):
    await message.reply_photo(
        random.choice(PHOTO),
        caption=f"""**ʜᴇʏ, ɪ ᴀᴍ {BOT_NAME}**
    ➖➖➖➖➖➖➖➖➖➖➖➖
          ➖➖➖➖➖➖➖
👑 **𝐌𝐘 𝐎𝐖𝐍𝐄𝐑 :** [𝙽 𝙰 𝙽 𝙰 𝙼 𝙸](https://t.me/The_NanamiiKento)
🧑‍💻 **𝐃𝐄𝐕𝐄𝐋𝐎𝐏𝐄𝐑 :** [Ɲᴀɴᴏ | ❄](https://t.me/SexyNano)
» **𝐋𝐈𝐁𝐑𝐀𝐑𝐘 𝐕𝐄𝐑𝐒𝐈𝐎𝐍 :** `{lver}`
» **𝐓𝐄𝐋𝐄𝐓𝐇𝐎𝐍 𝐕𝐄𝐑𝐒𝐈𝐎𝐍 :** `{tver}`
» **𝐏𝐘𝐑𝐎𝐆𝐑𝐀𝐌 𝐕𝐄𝐑𝐒𝐈𝐎𝐍 :** `{pver}`
» **𝐏𝐘𝐓𝐇𝐎𝐍 𝐕𝐄𝐑𝐒𝐈𝐎𝐍 :** `{version_info[0]}.{version_info[1]}.{version_info[2]}`
""",
        reply_markup=InlineKeyboardMarkup(ASAU),
    )


__mod_name__ = "𝙰ʟɪᴠᴇ"
