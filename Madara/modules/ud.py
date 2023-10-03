import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from Madara import dispatcher
from Madara.modules.disable import DisableAbleCommandHandler


def ud(update, context):
    try:
        text = " ".join(context.args)
    except IndexError:
        return context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="ᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ᴋᴇʏᴡᴏʀᴅs ᴛᴏ sᴇᴀʀᴄʜ ᴏɴ ᴜᴅ!",
        )
    results = requests.get(
        f"https://api.urbandictionary.com/v0/define?term={text}"
    ).json()
    try:
        reply_txt = f'𝗪𝗢𝗥𝗗 : {text}\n\n𝗗𝗘𝗙𝗜𝗡𝗔𝗧𝗜𝗢𝗡 : \n{results["list"][0]["definition"]}\n\n𝗘𝗫𝗔𝗠𝗣𝗟𝗘 : \n{results["list"][0]["example"]}'
    except:
        reply_txt = (
            f"Word: {text}\n\nʀᴇsᴜʟᴛs: sᴏʀʀʏ, ᴄᴏᴜʟᴅ ɴᴏᴛ ғɪɴᴅ ᴀɴʏ ᴍᴀᴛᴄʜɪɴɢ ʀᴇsᴜʟᴛs!"
        )
    keyboard = [
        [
            InlineKeyboardButton(
                text="🔎 ɢᴏᴏɢʟᴇ ɪᴛ!", url=f"https://www.google.com/search?q={text}"
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply_txt,
        reply_markup=reply_markup,
        parse_mode="HTML",
    )


ud_handler = DisableAbleCommandHandler("ud", ud)

dispatcher.add_handler(ud_handler)
