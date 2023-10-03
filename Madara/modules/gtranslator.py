from gpytranslate import SyncTranslator
from telegram import ParseMode, Update
from telegram.ext import CallbackContext

from Madara import dispatcher
from Madara.modules.disable import DisableAbleCommandHandler

trans = SyncTranslator()


def translate(update: Update, context: CallbackContext) -> None:
    bot = context.bot
    message = update.effective_message
    reply_msg = message.reply_to_message
    if not reply_msg:
        message.reply_text("ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ᴛʀᴀɴsʟᴀᴛᴇ ɪᴛ!")
        return
    if reply_msg.caption:
        to_translate = reply_msg.caption
    elif reply_msg.text:
        to_translate = reply_msg.text
    try:
        args = message.text.split()[1].lower()
        if "//" in args:
            source = args.split("//")[0]
            dest = args.split("//")[1]
        else:
            source = trans.detect(to_translate)
            dest = args
    except IndexError:
        source = trans.detect(to_translate)
        dest = "en"
    translation = trans(to_translate, sourcelang=source, targetlang=dest)
    reply = (
        f"<b>ᴛʀᴀɴsʟᴀᴛᴇᴅ ғʀᴏᴍ {source} ᴛᴏ {dest}</b>:\n"
        f"<code>{translation.text}</code>"
    )

    bot.send_message(text=reply, chat_id=message.chat.id, parse_mode=ParseMode.HTML)


def languages(update: Update, context: CallbackContext) -> None:
    message = update.effective_message
    bot = context.bot
    bot.send_message(
        text="ᴄʟɪᴄᴋ [ʜᴇʀᴇ](https://graph.org/MadaraUchiha-xBot-07-06) ᴛᴏ sᴇᴇ ᴛʜᴇ ʟɪsᴛ ᴏғ sᴜᴘᴘᴏʀᴛᴇᴅ ʟᴀɴɢᴜᴀɢᴇ ᴄᴏᴅᴇs!",
        chat_id=message.chat.id,
        disable_web_page_preview=True,
        parse_mode=ParseMode.MARKDOWN,
    )


__help__ = """ 
Use ᴛʜɪs ᴍᴏᴅᴜʟᴇ ᴛᴏ ᴛʀᴀɴsʟᴀᴛᴇ sᴛᴜғғ!

*ᴄᴏᴍᴍᴀɴᴅs:*
⍟ /tl (or /tr ):` ᴀs ᴀ ʀᴇᴘʟʏ ᴛᴏ a ᴍᴇssᴀɢᴇ, ᴛʀᴀɴsʟᴀᴛᴇs ɪᴛ ᴛᴏ ᴇɴɢʟɪsʜ `

⍟ /tl <lang>: `ᴛʀᴀɴsʟᴀᴛᴇs ᴛᴏ <lang>`

ᴇɢ: `/tl en`: `ᴛʀᴀɴsʟᴀᴛᴇs ᴛᴏ ᴇɴɢʟɪsʜ `

⍟ /tl <source>//<dest>: ᴛʀᴀɴsʟᴀᴛᴇs ғʀᴏᴍ <source> ᴛᴏ <lang>.

ᴇɢ: `/tl ja//en`: ᴛʀᴀɴsʟᴀᴛᴇs ғʀᴏᴍ ᴊᴀᴘᴀɴᴇsᴇ ᴛᴏ ᴇɴɢʟɪsʜ.


• [ʟɪsᴛ ᴏғ sᴜᴘᴘᴏʀᴛᴇᴅ ʟᴀɴɢᴜᴀɢᴇs ғᴏʀ ᴛʀᴀɴsʟᴀᴛɪᴏɴ]
"""

TRANSLATE_HANDLER = DisableAbleCommandHandler(["tr", "tl"], translate, run_async=True)
TRANSLATE_LANG_HANDLER = DisableAbleCommandHandler(
    ["lang", "languages"], languages, run_async=True
)

dispatcher.add_handler(TRANSLATE_HANDLER)
dispatcher.add_handler(TRANSLATE_LANG_HANDLER)

__mod_name__ = "𝚃ʀᴀɴsʟᴀᴛᴏʀ"
__command_list__ = ["tr", "tl", "lang", "languages"]
__handlers__ = [TRANSLATE_HANDLER, TRANSLATE_LANG_HANDLER]
