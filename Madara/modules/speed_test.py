import speedtest
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.ext import CallbackContext, CallbackQueryHandler

from Madara import DEV_USERS, dispatcher
from Madara.modules.disable import DisableAbleCommandHandler
from Madara.modules.helper_funcs.chat_status import dev_plus


def convert(speed):
    return round(int(speed) / 1048576, 2)


@dev_plus
def speedtestxyz(update: Update, context: CallbackContext):
    buttons = [
        [
            InlineKeyboardButton("ɪᴍᴀɢᴇ", callback_data="speedtest_image"),
            InlineKeyboardButton("ᴛᴇxᴛ", callback_data="speedtest_text"),
        ],
    ]
    update.effective_message.reply_text(
        "sᴇʟᴇᴄᴛ sᴘᴇᴇᴅᴛᴇsᴛ ᴍᴏᴅᴇ",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


def speedtestxyz_callback(update: Update, context: CallbackContext):
    query = update.callback_query

    if query.from_user.id in DEV_USERS:
        msg = update.effective_message.edit_text("ʀᴜɴɴɪɴɢ ғᴏʀ sᴘᴇᴇᴅᴛᴇsᴛ....")
        speed = speedtest.Speedtest()
        speed.get_best_server()
        speed.download()
        speed.upload()
        replymsg = "sᴘᴇᴇᴅᴛᴇsᴛ ʀᴇsᴜʟᴛs:"

        if query.data == "speedtest_image":
            speedtest_image = speed.results.share()
            update.effective_message.reply_photo(
                photo=speedtest_image,
                caption=replymsg,
            )
            msg.delete()

        elif query.data == "speedtest_text":
            result = speed.results.dict()
            replymsg += f"\nᴅᴏᴡɴʟᴏᴀᴅ: `{convert(result['download'])}Mb/s`\nᴜᴘʟᴏᴀᴅ: `{convert(result['upload'])}ᴍʙ/s`\nᴘɪɴɢ: `{result['ping']}`"
            update.effective_message.edit_text(replymsg, parse_mode=ParseMode.MARKDOWN)
    else:
        query.answer("ʏᴏᴜ ᴀʀᴇ ʀᴇǫᴜɪʀᴇᴅ ᴛᴏ ᴊᴏɪɴ @{SUPPORT_CHAT} ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.")


SPEED_TEST_HANDLER = DisableAbleCommandHandler(
    "speedtest", speedtestxyz, run_async=True
)
SPEED_TEST_CALLBACKHANDLER = CallbackQueryHandler(
    speedtestxyz_callback,
    pattern="speedtest_.*",
    run_async=True,
)

dispatcher.add_handler(SPEED_TEST_HANDLER)
dispatcher.add_handler(SPEED_TEST_CALLBACKHANDLER)

__mod_name__ = "𝚂ᴘᴇᴇᴅᴛᴇsᴛ"
__command_list__ = ["speedtest"]
__handlers__ = [SPEED_TEST_HANDLER, SPEED_TEST_CALLBACKHANDLER]
