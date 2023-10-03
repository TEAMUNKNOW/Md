import html

from telegram import TelegramError, Update
from telegram.ext import CallbackContext
from telegram.ext.filters import Filters

import Madara.modules.sql.antilinkedchannel_sql as sql
from Madara.modules.helper_funcs.anonymous import AdminPerms, user_admin
from Madara.modules.helper_funcs.chat_status import bot_admin, bot_can_delete
from Madara.modules.helper_funcs.decorators import Madaracmd, Madaramsg


@Madaracmd(command="cleanlinked", group=112)
@bot_can_delete
@user_admin(AdminPerms.CAN_RESTRICT_MEMBERS)
def set_antilinkedchannel(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    args = context.args
    if len(args) > 0:
        s = args[0].lower()
        if s in ["yes", "on"]:
            if sql.status_pin(chat.id):
                sql.disable_pin(chat.id)
                sql.enable_pin(chat.id)
                message.reply_html(
                    f"ᴇɴᴀʙʟᴇᴅ ʟɪɴᴋᴇᴅ channel ᴘᴏsᴛ ᴅᴇʟᴇᴛɪᴏɴ ᴀɴᴅ ᴅɪsᴀʙʟᴇᴅ ᴀɴᴛɪ ᴄʜᴀɴɴᴇʟ ᴘɪɴ ɪɴ {html.escape(chat.title)}"
                )

            else:
                sql.enable_linked(chat.id)
                message.reply_html(
                    f"ᴇɴᴀʙʟᴇᴅ ʟɪɴᴋᴇᴅ ᴄʜᴀɴɴᴇʟ ᴘᴏsᴛ ᴅᴇʟᴇᴛɪᴏɴ ɪɴ {html.escape(chat.title)}. ᴍᴇssᴀɢᴇs sᴇɴᴛ ғʀᴏᴍ ᴛʜᴇ ʟɪɴᴋᴇᴅ ᴄʜᴀɴɴᴇʟ ᴡɪʟʟ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ."
                )

        elif s in ["off", "no"]:
            sql.disable_linked(chat.id)
            message.reply_html(
                f"ᴅɪsᴀʙʟᴇᴅ ʟɪɴᴋᴇᴅ ᴄʜᴀɴɴᴇʟ ᴘᴏsᴛ ᴅᴇʟᴇᴛɪᴏɴ ɪɴ {html.escape(chat.title)}"
            )

        else:
            message.reply_text(f"ᴜɴʀᴇᴄᴏɢɴɪᴢᴇᴅ arguments {s}")
        return
    message.reply_html(
        f"ʟɪɴᴋᴇᴅ ᴄʜᴀɴɴᴇʟ ᴘᴏsᴛ ᴅᴇʟᴇᴛɪᴏɴ ɪs ᴄᴜʀʀᴇɴᴛʟʏ {sql.status_linked(chat.id)} ɪɴ {html.escape(chat.title)}"
    )


@Madaramsg(Filters.is_automatic_forward, group=111)
def eliminate_linked_channel_msg(update: Update, _: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    if not sql.status_linked(chat.id):
        return
    try:
        message.delete()
    except TelegramError:
        return


@Madaracmd(command="antichannelpin", group=114)
@bot_admin
@user_admin(AdminPerms.CAN_RESTRICT_MEMBERS)
def set_antipinchannel(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    args = context.args
    if len(args) > 0:
        s = args[0].lower()
        if s in ["yes", "on"]:
            if sql.status_linked(chat.id):
                sql.disable_linked(chat.id)
                sql.enable_pin(chat.id)
                message.reply_html(
                    f"ᴅɪsᴀʙʟᴇᴅ ʟɪɴᴋᴇᴅ ᴄʜᴀɴɴᴇʟ ᴅᴇʟᴇᴛɪᴏɴ ᴀɴᴅ ᴇɴᴀʙʟᴇᴅ ᴀɴᴛɪ ᴄʜᴀɴɴᴇʟ ᴘɪɴ ɪɴ {html.escape(chat.title)}"
                )

            else:
                sql.enable_pin(chat.id)
                message.reply_html(
                    f"ᴇɴᴀʙʟᴇᴅ ᴀɴᴛɪ ᴄʜᴀɴɴᴇʟ ᴘɪɴ ɪɴ {html.escape(chat.title)}"
                )
        elif s in ["off", "no"]:
            sql.disable_pin(chat.id)
            message.reply_html(
                f"ᴅɪsᴀʙʟᴇᴅ ᴀɴᴛɪ ᴄʜᴀɴɴᴇʟ ᴘɪɴ ɪɴ {html.escape(chat.title)}"
            )
        else:
            message.reply_text(f"ᴜɴʀᴇᴄᴏɢɴɪᴢᴇᴅ ᴀʀɢᴜᴍᴇɴᴛs {s}")
        return
    message.reply_html(
        f"ʟɪɴᴋᴇᴅ ᴄʜᴀɴɴᴇʟ message ᴜɴᴘɪɴ ɪs ᴄᴜʀʀᴇɴᴛʟʏ {sql.status_pin(chat.id)} ɪɴ {html.escape(chat.title)}"
    )


@Madaramsg(
    Filters.is_automatic_forward | Filters.status_update.pinned_message, group=113
)
def eliminate_linked_channel_msg(update: Update, _: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    if not sql.status_pin(chat.id):
        return
    try:
        message.unpin()
    except TelegramError:
        return
