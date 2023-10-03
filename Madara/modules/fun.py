import random

from pyjokes import (
    get_joke,
)  # thanks to @ishikki_akabane who did nothing and just copypasted this joke feature
from telegram import ParseMode, Update
from telegram.ext import CallbackContext, run_async

import Madara.modules.fun_strings as fun_strings
from Madara import dispatcher
from Madara.events import register
from Madara.modules.disable import DisableAbleCommandHandler

GIF_ID = "CgACAgQAAxkBAAILHWBPN8dL8NvxZ9tUfr3_4SdPGqgjAAJeAgACQQrNUlM24z1ISCsTHgQ"


# ----------@ishikki_akabane
@register(pattern="^/joke ?(.*)")
async def joke(event):
    await event.reply(get_joke())


# --------------------------


@run_async
def roll(update: Update, context: CallbackContext):
    update.message.reply_text(random.choice(range(1, 7)))


@run_async
def flirt(
    update: Update, context: CallbackContext
):  # This feature's credit goes to @ishikki_akabane
    args = context.args
    update.effective_message.reply_text(random.choice(fun_strings.FLIRT))


@run_async
def toss(update: Update, context: CallbackContext):
    update.message.reply_text(random.choice(fun_strings.TOSS))


@run_async
def cosplay(update: Update, context: CallbackContext):
    update.effective_message.reply_photo(random.choice(fun_strings.COSPLAY))


@run_async
def shrug(update: Update, context: CallbackContext):
    msg = update.effective_message
    reply_text = (
        msg.reply_to_message.reply_text if msg.reply_to_message else msg.reply_text
    )
    reply_text(r"¯\_(ツ)_/¯")


@run_async
def bluetext(update: Update, context: CallbackContext):
    msg = update.effective_message
    reply_text = (
        msg.reply_to_message.reply_text if msg.reply_to_message else msg.reply_text
    )
    reply_text(
        "/BLUE /TEXT\n/MUST /CLICK\n/I /AM /A /STUPID /ANIMAL /THAT /IS /ATTRACTED /TO /COLORS"
    )


@run_async
def rlg(update: Update, context: CallbackContext):
    eyes = random.choice(fun_strings.EYES)
    mouth = random.choice(fun_strings.MOUTHS)
    ears = random.choice(fun_strings.EARS)

    if len(eyes) == 2:
        repl = ears[0] + eyes[0] + mouth[0] + eyes[1] + ears[1]
    else:
        repl = ears[0] + eyes[0] + mouth[0] + eyes[0] + ears[1]
    update.message.reply_text(repl)


@run_async
def decide(update: Update, context: CallbackContext):
    reply_text = (
        update.effective_message.reply_to_message.reply_text
        if update.effective_message.reply_to_message
        else update.effective_message.reply_text
    )
    reply_text(random.choice(fun_strings.DECIDE))


normiefont = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
]
weebyfont = [
    "卂",
    "乃",
    "匚",
    "刀",
    "乇",
    "下",
    "厶",
    "卄",
    "工",
    "丁",
    "长",
    "乚",
    "从",
    "𠘨",
    "口",
    "尸",
    "㔿",
    "尺",
    "丂",
    "丅",
    "凵",
    "リ",
    "山",
    "乂",
    "丫",
    "乙",
]


@run_async
def weebify(update: Update, context: CallbackContext):
    args = context.args
    message = update.effective_message
    string = ""

    if message.reply_to_message:
        string = message.reply_to_message.text.lower().replace(" ", "  ")

    if args:
        string = "  ".join(args).lower()

    if not string:
        message.reply_text("Usage is `/weebify <text>`", parse_mode=ParseMode.MARKDOWN)
        return

    for normiecharacter in string:
        if normiecharacter in normiefont:
            weebycharacter = weebyfont[normiefont.index(normiecharacter)]
            string = string.replace(normiecharacter, weebycharacter)

    if message.reply_to_message:
        message.reply_to_message.reply_text(string)
    else:
        message.reply_text(string)


__help__ = """
 ➢ `/cosplay`*:* sᴇɴᴅs ᴄᴏsᴘʟᴀʏ ɪᴍᴀɢᴇs.
 ➢ `/decide`*:* ʀᴀɴᴅᴏᴍʟʏ ᴀɴsᴡᴇʀs ʏᴇs/ɴᴏ/ᴍᴀʏʙᴇ
 ➢ `/toss`*:* ᴛᴏssᴇs ᴀ ᴄᴏɪɴ.
 ➢ `/shrug`*:* ɢᴇᴛ sʜʀᴜɢ xᴅ
 ➢ `/bluetext`*:* ᴄʜᴇᴄᴋ ᴜʀsᴇʟғ :V
 ➢ `/roll`*:* ʀᴏʟʟ ᴀ ᴅɪᴄᴇ.
 ➢ `/rlg`*:* ᴊᴏɪɴ ᴇᴀʀs,ɴᴏsᴇ,ᴍᴏᴜᴛʜ ᴀɴᴅ ᴄʀᴇᴀᴛᴇ ᴀɴ ᴇᴍᴏ ;-;
 ➢ `/weebify <text>`*:* ʀᴇᴛᴜʀɴs ᴀ ᴡᴇᴇʙɪғɪᴇᴅ ᴛᴇxᴛ.
 ➢ `/flirt <text>`*:* ʀᴇᴛᴜʀɴs ᴀ ғʟɪʀᴛ ᴛᴇxᴛ.
 ➢ `/joke <text>`*:* ᴛᴇʟʟs ᴀ ʀᴀɴᴅᴏᴍ ᴊᴏᴋᴇ.
"""

ROLL_HANDLER = DisableAbleCommandHandler("roll", roll)
TOSS_HANDLER = DisableAbleCommandHandler("toss", toss)
SHRUG_HANDLER = DisableAbleCommandHandler("shrug", shrug)
BLUETEXT_HANDLER = DisableAbleCommandHandler("bluetext", bluetext)
RLG_HANDLER = DisableAbleCommandHandler("rlg", rlg)
COSPLAY_HANDLER = DisableAbleCommandHandler("cosplay", cosplay)
DECIDE_HANDLER = DisableAbleCommandHandler("decide", decide)
WEEBIFY_HANDLER = DisableAbleCommandHandler("weebify", weebify)
FLIRT_HANDLER = DisableAbleCommandHandler("flirt", flirt)

dispatcher.add_handler(WEEBIFY_HANDLER)
dispatcher.add_handler(ROLL_HANDLER)
dispatcher.add_handler(TOSS_HANDLER)
dispatcher.add_handler(SHRUG_HANDLER)
dispatcher.add_handler(BLUETEXT_HANDLER)
dispatcher.add_handler(RLG_HANDLER)
dispatcher.add_handler(DECIDE_HANDLER)
dispatcher.add_handler(COSPLAY_HANDLER)
dispatcher.add_handler(FLIRT_HANDLER)

__mod_name__ = "𝙵ᴜɴ"
__command_list__ = [
    "roll",
    "toss",
    "shrug",
    "bluetext",
    "rlg",
    "decide",
    "cosplay",
    "weebify",
    "flirt",
]
__handlers__ = [
    ROLL_HANDLER,
    TOSS_HANDLER,
    SHRUG_HANDLER,
    BLUETEXT_HANDLER,
    RLG_HANDLER,
    DECIDE_HANDLER,
    WEEBIFY_HANDLER,
    COSPLAY_HANDLER,
    FLIRT_HANDLER,
]
