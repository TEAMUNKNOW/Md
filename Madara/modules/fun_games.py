from telegram import Update
from telegram.ext import CallbackContext

from Madara import dispatcher
from Madara.modules.disable import DisableAbleCommandHandler

__mod_name__ = "𝙵ᴜɴ ɢᴀᴍᴇs"
__help__ = """
ᴜsᴇ ᴛʜᴇsᴇ ᴄᴏᴍᴍᴀɴᴅs ᴀɴᴅ ᴛʀʏ ᴛᴏ sᴄᴏʀᴇ.\n\n
 ❍ `/dice` - ᴅɪᴄᴇ 🎲\n
 ❍ `/dart` - ᴅᴀʀᴛ 🎯\n
 ❍ `/basket` - ʙᴀsᴋᴇᴛ ʙᴀʟʟ 🏀\n
 ❍ `/bowling` - ʙᴏᴡʟɪɴɢ ʙᴀʟʟ 🎳\n
 ❍ `/football` - ғᴏᴏᴛʙᴀʟʟ ⚽\n
 ❍ `/slot` - sᴘɪɴ sʟᴏᴛ ᴍᴀᴄʜɪɴᴇ 🎰
"""


def throw_dice(update: Update, context: CallbackContext):
    update.message.reply_dice(emoji="🎲")


def throw_dart(update: Update, context: CallbackContext):
    update.message.reply_dice(emoji="🎯")


def throw_basketball(update: Update, context: CallbackContext):
    update.message.reply_dice(emoji="🏀")


def throw_bowling_ball(update: Update, context: CallbackContext):
    update.message.reply_dice(emoji="🎳")


def throw_football(update: Update, context: CallbackContext):
    update.message.reply_dice(emoji="⚽")


def spin_slot_machine(update: Update, context: CallbackContext):
    update.message.reply_dice(emoji="🎰")


# Add the command handlers
dispatcher.add_handler(DisableAbleCommandHandler("dice", throw_dice))
dispatcher.add_handler(DisableAbleCommandHandler("dart", throw_dart))
dispatcher.add_handler(DisableAbleCommandHandler("basket", throw_basketball))
dispatcher.add_handler(DisableAbleCommandHandler("bowling", throw_bowling_ball))
dispatcher.add_handler(DisableAbleCommandHandler("football", throw_football))
dispatcher.add_handler(DisableAbleCommandHandler("slot", spin_slot_machine))
