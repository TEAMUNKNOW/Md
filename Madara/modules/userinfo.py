import html

from telegram import MAX_MESSAGE_LENGTH, ParseMode, Update
from telegram.ext.dispatcher import CallbackContext
from telegram.utils.helpers import escape_markdown

import Madara.modules.sql.userinfo_sql as sql
from Madara import DEV_USERS
from Madara import DRAGONS as SUDO_USERS
from Madara.modules.helper_funcs.decorators import Madaracmd
from Madara.modules.helper_funcs.extraction import extract_user


@Madaracmd(command="me", pass_args=True)
def about_me(update: Update, context: CallbackContext):
    args = context.args
    bot = context.bot
    message = update.effective_message
    user_id = extract_user(message, args)

    user = bot.get_chat(user_id) if user_id else message.from_user
    info = sql.get_user_me_info(user.id)

    if info:
        update.effective_message.reply_text(
            f"*{user.first_name}*:\n{escape_markdown(info)}",
            parse_mode=ParseMode.MARKDOWN,
        )
    elif message.reply_to_message:
        username = message.reply_to_message.from_user.first_name
        update.effective_message.reply_text(
            f"{username} ʜᴀsɴ'ᴛ sᴇᴛ ᴀɴ ɪɴғᴏ ᴍᴇssᴀɢᴇ ᴀʙᴏᴜᴛ ᴛʜᴇᴍsᴇʟᴠᴇs ʏᴇᴛ!"
        )
    else:
        update.effective_message.reply_text(
            "ʏᴏᴜ haven't sᴇᴛ ᴀɴ ɪɴғᴏ ᴍᴇssᴀɢᴇ ᴀʙᴏᴜᴛ ʏᴏᴜʀsᴇʟғ ʏᴇᴛ!"
        )


@Madaracmd(command="setme")
def set_about_me(update: Update, context: CallbackContext):
    bot = context.bot
    message = update.effective_message
    user_id = message.from_user.id
    if user_id in (777000, 1087968824):
        message.reply_text("ᴅᴏɴ'ᴛ sᴇᴛ ɪɴғᴏ ғᴏʀ ᴛᴇʟᴇɢʀᴀᴍ ʙᴏᴛs!")
        return
    if message.reply_to_message:
        repl_message = message.reply_to_message
        repl_user_id = repl_message.from_user.id
        if repl_user_id == bot.id and (user_id in SUDO_USERS or user_id in DEV_USERS):
            user_id = repl_user_id

    text = message.text
    info = text.split(None, 1)

    if len(info) == 2:
        if len(info[1]) < MAX_MESSAGE_LENGTH // 4:
            sql.set_user_me_info(user_id, info[1])
            if user_id == bot.id:
                message.reply_text("ᴜᴘᴅᴀᴛᴇᴅ ᴍʏ ɪɴғᴏ!")
            else:
                message.reply_text("ᴜᴘᴅᴀᴛᴇᴅ ʏᴏᴜʀ ɪɴғᴏ!")
        else:
            message.reply_text(
                "ᴛʜᴇ ɪɴғᴏ ɴᴇᴇᴅs ᴛᴏ ʙᴇ ᴜɴᴅᴇʀ {} ᴄʜᴀʀᴀᴄᴛᴇʀs! ʏᴏᴜ ʜᴀᴠᴇ {}.".format(
                    MAX_MESSAGE_LENGTH // 4, len(info[1])
                )
            )


@Madaracmd(command="bio", pass_args=True)
def about_bio(update: Update, context: CallbackContext):
    args = context.args
    bot = context.bot
    message = update.effective_message

    user_id = extract_user(message, args)
    user = bot.get_chat(user_id) if user_id else message.from_user
    info = sql.get_user_bio(user.id)

    if info:
        update.effective_message.reply_text(
            "*{}*:\n{}".format(user.first_name, escape_markdown(info)),
            parse_mode=ParseMode.MARKDOWN,
        )
    elif message.reply_to_message:
        username = user.first_name
        update.effective_message.reply_text(
            f"{username} ʜᴀsɴ'ᴛ ʜᴀᴅ ᴀ ᴍᴇssᴀɢᴇ sᴇᴛ ᴀʙᴏᴜᴛ ᴛʜᴇᴍsᴇʟᴠᴇs ʏᴇᴛ!"
        )
    else:
        update.effective_message.reply_text(
            "ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ ʜᴀᴅ a ʙɪᴏ sᴇᴛ ᴀʙᴏᴜᴛ ʏᴏᴜʀsᴇʟғ ʏᴇᴛ!"
        )
    message = update.effective_message
    if message.reply_to_message:
        repl_message = message.reply_to_message
        user_id = repl_message.from_user.id

        if user_id == message.from_user.id:
            message.reply_text(
                "ʜɪʜɪ ᴏɴɪᴄʜᴀɴ, ʏᴏᴜ ᴄᴀɴ'ᴛ sᴇᴛ ʏᴏᴜʀ ᴏᴡɴ ʙɪᴏ! ʏᴏᴜ'ʀᴇ ᴀᴛ ᴛʜᴇ ᴍᴇʀᴄʏ ᴏғ ᴏᴛʜᴇʀs ʜᴇʀᴇ..."
            )
            return

        sender_id = update.effective_user.id

        if (
            user_id == bot.id
            and sender_id not in SUDO_USERS
            and sender_id not in DEV_USERS
        ):
            message.reply_text(
                "ᴇʀᴍ... ʏᴇᴀʜ, I ᴏɴʟʏ ᴛʀᴜsᴛ ᴍʏ ғᴀᴍɪʟʏ ᴏʀ ʙᴇsᴛ ғʀɪᴇɴᴅs ᴛᴏ sᴇᴛ ᴍʏ ʙɪᴏ."
            )
            return

        text = message.text
        # use python's maxsplit to only remove the cmd, hence keeping newlines.
        bio = text.split(None, 1)

        if len(bio) == 2:
            if len(bio[1]) < MAX_MESSAGE_LENGTH // 4:
                sql.set_user_bio(user_id, bio[1])
                message.reply_text(
                    "ᴜᴘᴅᴀᴛᴇᴅ {}'s ʙɪᴏ!".format(repl_message.from_user.first_name)
                )
            else:
                message.reply_text(
                    "A ʙɪᴏ needs ᴛᴏ ʙᴇ ᴜɴᴅᴇʀ {} ᴄʜᴀʀᴀᴄᴛᴇʀs! ʏᴏᴜ ᴛʀɪᴇᴅ ᴛᴏ sᴇᴛ {}.".format(
                        MAX_MESSAGE_LENGTH // 4, len(bio[1])
                    )
                )
    else:
        message.reply_text("ʀᴇᴘʟʏ ᴛᴏ sᴏᴍᴇᴏɴᴇ's ᴍᴇssᴀɢᴇ ᴛᴏ sᴇᴛ ᴛʜᴇɪʀ ʙɪᴏ!")


@Madaracmd(command="setbio")
def set_about_bio(update: Update, context: CallbackContext):
    message = update.effective_message
    sender_id = update.effective_user.id
    bot = context.bot

    if message.reply_to_message:
        repl_message = message.reply_to_message
        user_id = repl_message.from_user.id
        if user_id in (777000, 1087968824):
            message.reply_text("ᴅᴏɴ'ᴛ sᴇᴛ ʙɪᴏ ғᴏʀ ᴛᴇʟᴇɢʀᴀᴍ ʙᴏᴛs!")
            return

        if user_id == message.from_user.id:
            message.reply_text(
                "ʜɪʜɪ ᴏɴ ɪ ᴄʜᴀɴ, ʏᴏᴜ ᴄᴀɴ'ᴛ sᴇᴛ ʏᴏᴜʀ ᴏᴡɴ ʙɪᴏ! ʏᴏᴜ'ʀᴇ ᴀᴛ ᴛʜᴇ ᴍᴇʀᴄʏ ᴏғ ᴏᴛʜᴇʀs ʜᴇʀᴇ..."
            )
            return

        if user_id in [777000, 1087968824] and sender_id not in DEV_USERS:
            message.reply_text("ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪsᴇᴅ")
            return

        if user_id == bot.id and sender_id not in DEV_USERS:
            message.reply_text("ᴇʀᴍ... ʏᴇᴀʜ, ɪ ᴏɴʟʏ ᴛʀᴜsᴛ ᴍʏ ғᴀᴍɪʟʏ ᴛᴏ sᴇᴛ ᴍʏ ʙɪᴏ.")
            return

        text = message.text
        bio = text.split(
            None, 1
        )  # use python's maxsplit to only remove the cmd, hence keeping newlines.

        if len(bio) == 2:
            if len(bio[1]) < MAX_MESSAGE_LENGTH // 4:
                sql.set_user_bio(user_id, bio[1])
                message.reply_text(
                    "ᴜᴘᴅᴀᴛᴇᴅ {}'s ʙɪᴏ!".format(repl_message.from_user.first_name)
                )
            else:
                message.reply_text(
                    "ʙɪᴏ ɴᴇᴇᴅs ᴛᴏ ʙᴇ ᴜɴᴅᴇʀ {} ᴄʜᴀʀᴀᴄᴛᴇʀs! ʏᴏᴜ ᴛʀɪᴇᴅ ᴛᴏ sᴇᴛ {}.".format(
                        MAX_MESSAGE_LENGTH // 4, len(bio[1])
                    )
                )
    else:
        message.reply_text("ʀᴇᴘʟʏ ᴛᴏ sᴏᴍᴇᴏɴᴇ ᴛᴏ sᴇᴛ ᴛʜᴇɪʀ ʙɪᴏ!")


def __user_info__(user_id):
    bio = html.escape(sql.get_user_bio(user_id) or "")
    me = html.escape(sql.get_user_me_info(user_id) or "")
    if bio and me:
        return f"\n<b>ᴀʙᴏᴜᴛ ᴜsᴇʀ:</b>\n{me}\n<b>ᴡʜᴀᴛ ᴏᴛʜᴇʀs sᴀʏ:</b>\n{bio}\n"
    elif bio:
        return f"\n<b>ᴡʜᴀᴛ ᴏᴛʜᴇʀs sᴀʏ:</b>\n{bio}\n"
    elif me:
        return f"\n<b>ᴀʙᴏᴜᴛ ᴜsᴇʀ:</b>\n{me}\n"
    else:
        return "\n"


__mod_name__ = "𝙰ʙᴏᴜᴛs"
