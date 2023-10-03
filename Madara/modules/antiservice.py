from pyrogram import filters

from Madara import pgram
from Madara.core.decorators.permissions import adminsOnly
from Madara.utils.dbfunctions import antiservice_off, antiservice_on, is_antiservice_on


@pgram.on_message(filters.command("antiservice") & ~filters.private)
@adminsOnly("can_change_info")
async def anti_service(_, message):
    if len(message.command) != 2:
        return await message.reply_text("ᴜsᴀɢᴇ: /antiservice [on | off]")
    status = message.text.split(None, 1)[1].strip()
    status = status.lower()
    chat_id = message.chat.id
    if status == "on":
        await antiservice_on(chat_id)
        await message.reply_text(
            "ᴇɴᴀʙʟᴇᴅ ᴀɴᴛɪsᴇʀᴠɪᴄᴇ sʏsᴛᴇᴍ. ɪ ᴡɪʟʟ ᴅᴇʟᴇᴛᴇ sᴇʀᴠɪᴄᴇ ᴍᴇssᴀɢᴇs ғʀᴏᴍ ɴᴏᴡ ᴏɴ."
        )
    elif status == "off":
        await antiservice_off(chat_id)
        await message.reply_text(
            "ᴅɪsᴀʙʟᴇᴅ ᴀɴᴛɪsᴇʀᴠɪᴄᴇ sʏsᴛᴇᴍ. I ᴡᴏɴ'ᴛ ʙᴇ ᴅᴇʟᴇᴛɪɴɢ sᴇʀᴠɪᴄᴇ ᴍᴇssᴀɢᴇ ғʀᴏᴍ ɴᴏᴡ ᴏɴ."
        )
    else:
        await message.reply_text("ᴜɴᴋɴᴏᴡɴ sᴜғғɪx, ᴜsᴇ /antiservice [enable|disable]")


@pgram.on_message(filters.service, group=11)
async def delete_service(_, message):
    chat_id = message.chat.id
    try:
        if await is_antiservice_on(chat_id):
            return await message.delete()
    except Exception:
        pass
