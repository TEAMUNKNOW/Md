import re
from html import escape

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.error import BadRequest
from telegram.ext import DispatcherHandlerStop, Filters
from telegram.utils.helpers import escape_markdown, mention_html

from Madara import DRAGONS as SUDO_USERS
from Madara import LOGGER as log
from Madara import dispatcher
from Madara.modules.connection import connected
from Madara.modules.helper_funcs.alternate import send_message, typing_action
from Madara.modules.helper_funcs.decorators import Madaracallback, Madaracmd, Madaramsg
from Madara.modules.helper_funcs.extraction import extract_text
from Madara.modules.helper_funcs.filters import CustomFilters
from Madara.modules.helper_funcs.misc import build_keyboard_parser
from Madara.modules.helper_funcs.msg_types import get_filter_type
from Madara.modules.helper_funcs.string_handling import (
    button_markdown_parser,
    escape_invalid_curly_brackets,
    markdown_to_html,
    split_quotes,
)
from Madara.modules.sql import cust_filters_sql as sql

from ..modules.helper_funcs.anonymous import AdminPerms, user_admin

HANDLER_GROUP = 10

ENUM_FUNC_MAP = {
    sql.Types.TEXT.value: dispatcher.bot.send_message,
    sql.Types.BUTTON_TEXT.value: dispatcher.bot.send_message,
    sql.Types.STICKER.value: dispatcher.bot.send_sticker,
    sql.Types.DOCUMENT.value: dispatcher.bot.send_document,
    sql.Types.PHOTO.value: dispatcher.bot.send_photo,
    sql.Types.AUDIO.value: dispatcher.bot.send_audio,
    sql.Types.VOICE.value: dispatcher.bot.send_voice,
    sql.Types.VIDEO.value: dispatcher.bot.send_video,
    # sql.Types.VIDEO_NOTE.value: dispatcher.bot.send_video_note
}


@typing_action
@Madaracmd(command="filters", admin_ok=True)
def list_handlers(update, context):
    chat = update.effective_chat
    user = update.effective_user

    conn = connected(context.bot, update, chat, user.id, need_admin=False)
    if conn is not False:
        chat_id = conn
        chat_name = dispatcher.bot.getChat(conn).title
        filter_list = "*Filter in {}:*\n"
    else:
        chat_id = update.effective_chat.id
        if chat.type == "private":
            chat_name = "Local filters"
            filter_list = "*local filters:*\n"
        else:
            chat_name = chat.title
            filter_list = "*ғɪʟᴛᴇʀs ɪɴ {}*:\n"

    all_handlers = sql.get_chat_triggers(chat_id)

    if not all_handlers:
        send_message(
            update.effective_message, "ɴᴏ ғɪʟᴛᴇʀs sᴀᴠᴇᴅ ɪɴ {}!".format(chat_name)
        )
        return

    for keyword in all_handlers:
        entry = " • `{}`\n".format(escape_markdown(keyword))
        if len(entry) + len(filter_list) > telegram.MAX_MESSAGE_LENGTH:
            send_message(
                update.effective_message,
                filter_list.format(chat_name),
                parse_mode=telegram.ParseMode.MARKDOWN,
            )
            filter_list = entry
        else:
            filter_list += entry

    send_message(
        update.effective_message,
        filter_list.format(chat_name),
        parse_mode=telegram.ParseMode.MARKDOWN,
    )


# NOT ASYNC BECAUSE DISPATCHER HANDLER RAISED
@Madaracmd(command="filter", run_async=False)
@user_admin(AdminPerms.CAN_CHANGE_INFO)
@typing_action
def filters(update, context):  # sourcery no-metrics
    chat = update.effective_chat
    user = update.effective_user
    msg = update.effective_message
    args = msg.text.split(
        None, 1
    )  # use python's maxsplit to separate Cmd, keyword, and reply_text

    conn = connected(context.bot, update, chat, user.id)
    if conn is not False:
        chat_id = conn
        chat_name = dispatcher.bot.getChat(conn).title
    else:
        chat_id = update.effective_chat.id
        chat_name = "local filters" if chat.type == "private" else chat.title
    if not msg.reply_to_message and len(args) < 2:
        send_message(
            update.effective_message,
            "ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴋᴇʏʙᴏᴀʀᴅ ᴋᴇʏᴡᴏʀᴅ ғᴏʀ ᴛʜɪs ғɪʟᴛᴇʀ ᴛᴏ ʀᴇᴘʟʏ ᴡɪᴛʜ!",
        )
        return

    if msg.reply_to_message:
        if len(args) < 2:
            send_message(
                update.effective_message,
                "ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴋᴇʏᴡᴏʀᴅ ғᴏʀ ᴛʜɪs ғɪʟᴛᴇʀ ᴛᴏ ʀᴇᴘʟʏ ᴡɪᴛʜ!",
            )
            return
        else:
            keyword = args[1]
    else:
        extracted = split_quotes(args[1])
        if len(extracted) < 1:
            return
        # set trigger -> lower, so as to avoid adding duplicate filters with different cases
        keyword = extracted[0].lower()

    # Add the filter
    # Note: perhaps handlers can be removed somehow using sql.get_chat_filters
    for handler in dispatcher.handlers.get(HANDLER_GROUP, []):
        if handler.filters == (keyword, chat_id):
            dispatcher.remove_handler(handler, HANDLER_GROUP)

    text, file_type, file_id = get_filter_type(msg)
    if not msg.reply_to_message and len(extracted) >= 2:
        offset = len(extracted[1]) - len(
            msg.text
        )  # set correct offset relative to command + notename
        text, buttons = button_markdown_parser(
            extracted[1], entities=msg.parse_entities(), offset=offset
        )
        text = text.strip()
        if not text:
            send_message(
                update.effective_message,
                "ᴛʜᴇʀᴇ ɪs ɴᴏ ғɪʟᴛᴇʀ ᴍᴇssᴀɢᴇ - ʏᴏᴜ ᴄᴀɴ'ᴛ ᴊᴜsᴛ ʜᴀᴠᴇ ʙᴜᴛᴛᴏɴs, ʏᴏᴜ ɴᴇᴇᴅ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ɢᴏ ᴡɪᴛʜ ɪᴛ!",
            )
            return

    elif msg.reply_to_message and len(args) >= 2:
        if msg.reply_to_message.text:
            text_to_parsing = msg.reply_to_message.text
        elif msg.reply_to_message.caption:
            text_to_parsing = msg.reply_to_message.caption
        else:
            text_to_parsing = ""
        offset = len(
            text_to_parsing
        )  # set correct offset relative to command + notename
        text, buttons = button_markdown_parser(
            text_to_parsing, entities=msg.parse_entities(), offset=offset
        )
        text = text.strip()

    elif not text and not file_type:
        send_message(
            update.effective_message,
            "ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴋᴇʏᴡᴏʀᴅ ғᴏʀ ᴛʜɪs ғɪʟᴛᴇʀ ʀᴇᴘʟʏ ᴡɪᴛʜ!",
        )
        return

    elif msg.reply_to_message:
        if msg.reply_to_message.text:
            text_to_parsing = msg.reply_to_message.text
        elif msg.reply_to_message.caption:
            text_to_parsing = msg.reply_to_message.caption
        else:
            text_to_parsing = ""
        offset = len(
            text_to_parsing
        )  # set correct offset relative to command + notename
        text, buttons = button_markdown_parser(
            text_to_parsing, entities=msg.parse_entities(), offset=offset
        )
        text = text.strip()
        if (msg.reply_to_message.text or msg.reply_to_message.caption) and not text:
            send_message(
                update.effective_message,
                "ᴛʜᴇʀᴇ ɪs ɴᴏ ғɪʟᴛᴇʀ ᴍᴇssᴀɢᴇ - ʏᴏᴜ ᴄᴀɴ'ᴛ ᴊᴜsᴛ ʜᴀᴠᴇ ʙᴜᴛᴛᴏɴs, ʏᴏᴜ ɴᴇᴇᴅ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ɢᴏ ᴡɪᴛʜ ɪᴛ!",
            )
            return

    else:
        send_message(update.effective_message, "ɪɴᴠᴀʟɪᴅ ғɪʟᴛᴇʀ!")
        return

    add = addnew_filter(update, chat_id, keyword, text, file_type, file_id, buttons)
    # This is an old method
    # sql.add_filter(chat_id, keyword, content, is_sticker, is_document, is_image, is_audio, is_voice, is_video, buttons)

    if add is True:
        send_message(
            update.effective_message,
            "sᴀᴠᴇᴅ ғɪʟᴛᴇʀ '{}' ɪɴ *{}*!".format(keyword, chat_name),
            parse_mode=telegram.ParseMode.MARKDOWN,
        )
    raise DispatcherHandlerStop


# NOT ASYNC BECAUSE DISPATCHER HANDLER RAISED
@Madaracmd(command="stop", run_async=False)
@user_admin(AdminPerms.CAN_CHANGE_INFO)
@typing_action
def stop_filter(update, context):
    chat = update.effective_chat
    user = update.effective_user
    args = update.effective_message.text.split(None, 1)

    conn = connected(context.bot, update, chat, user.id)
    if conn is not False:
        chat_id = conn
        chat_name = dispatcher.bot.getChat(conn).title
    else:
        chat_id = update.effective_chat.id
        chat_name = "Local filters" if chat.type == "private" else chat.title
    if len(args) < 2:
        send_message(update.effective_message, "ᴡʜᴀᴛ sʜᴏᴜʟᴅ ɪ sᴛᴏᴘ?")
        return

    chat_filters = sql.get_chat_triggers(chat_id)

    if not chat_filters:
        send_message(update.effective_message, "ɴᴏ ғɪʟᴛᴇʀs ᴀᴄᴛɪᴠᴇ ʜᴇʀᴇ!")
        return

    for keyword in chat_filters:
        if keyword == args[1]:
            sql.remove_filter(chat_id, args[1])
            send_message(
                update.effective_message,
                "ᴏᴋᴀʏ, ɪ'ʟʟ sᴛᴏᴘ ʀᴇᴘʟʏɪɴɢ ᴛᴏ ᴛʜᴀᴛ ғɪʟᴛᴇʀ ɪɴ *{}*.".format(chat_name),
                parse_mode=telegram.ParseMode.MARKDOWN,
            )
            raise DispatcherHandlerStop

    send_message(
        update.effective_message,
        "ᴛʜᴀᴛ's ɴᴏᴛ ᴀ ғɪʟᴛᴇʀ - ᴄʟɪᴄᴋ: /ғɪʟᴛᴇʀs ᴛᴏ ɢᴇᴛ ᴄᴜʀʀᴇɴᴛʟʏ ᴀᴄᴛɪᴠᴇ ғɪʟᴛᴇʀs.",
    )


@Madaramsg((CustomFilters.has_text & ~Filters.update.edited_message))
def reply_filter(update, context):  # sourcery no-metrics
    chat = update.effective_chat  # type: Optional[Chat]
    message = update.effective_message  # type: Optional[Message]

    if not update.effective_user or update.effective_user.id == 777000:
        return
    to_match = extract_text(message)
    if not to_match:
        return

    chat_filters = sql.get_chat_triggers(chat.id)
    for keyword in chat_filters:
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, to_match, flags=re.IGNORECASE):
            filt = sql.get_filter(chat.id, keyword)
            if filt.reply == "there is should be a new reply":
                buttons = sql.get_buttons(chat.id, filt.keyword)
                keyb = build_keyboard_parser(context.bot, chat.id, buttons)
                keyboard = InlineKeyboardMarkup(keyb)

                VALID_WELCOME_FORMATTERS = [
                    "first",
                    "last",
                    "fullname",
                    "username",
                    "id",
                    "chatname",
                    "mention",
                ]
                if filt.reply_text:
                    valid_format = escape_invalid_curly_brackets(
                        markdown_to_html(filt.reply_text), VALID_WELCOME_FORMATTERS
                    )
                    if valid_format:
                        filtext = valid_format.format(
                            first=escape(message.from_user.first_name),
                            last=escape(
                                message.from_user.last_name
                                or message.from_user.first_name
                            ),
                            fullname=" ".join(
                                [
                                    escape(message.from_user.first_name),
                                    escape(message.from_user.last_name),
                                ]
                                if message.from_user.last_name
                                else [escape(message.from_user.first_name)]
                            ),
                            username="@" + escape(message.from_user.username)
                            if message.from_user.username
                            else mention_html(
                                message.from_user.id, message.from_user.first_name
                            ),
                            mention=mention_html(
                                message.from_user.id, message.from_user.first_name
                            ),
                            chatname=escape(message.chat.title)
                            if message.chat.type != "private"
                            else escape(message.from_user.first_name),
                            id=message.from_user.id,
                        )
                    else:
                        filtext = ""
                else:
                    filtext = ""

                if filt.file_type in (sql.Types.BUTTON_TEXT, sql.Types.TEXT):
                    try:
                        context.bot.send_message(
                            chat.id,
                            filtext,
                            reply_to_message_id=message.message_id,
                            parse_mode=ParseMode.HTML,
                            disable_web_page_preview=True,
                            reply_markup=keyboard,
                        )
                    except BadRequest as excp:
                        error_catch = get_exception(excp, filt, chat)
                        if error_catch == "noreply":
                            try:
                                context.bot.send_message(
                                    chat.id,
                                    filtext,
                                    parse_mode=ParseMode.HTML,
                                    disable_web_page_preview=True,
                                    reply_markup=keyboard,
                                )
                            except BadRequest as excp:
                                log.exception("Error in filters: " + excp.message)
                                send_message(
                                    update.effective_message,
                                    get_exception(excp, filt, chat),
                                )
                        else:
                            try:
                                send_message(
                                    update.effective_message,
                                    get_exception(excp, filt, chat),
                                )
                            except BadRequest as excp:
                                log.exception("Failed to send message: " + excp.message)
                elif ENUM_FUNC_MAP[filt.file_type] == dispatcher.bot.send_sticker:
                    ENUM_FUNC_MAP[filt.file_type](
                        chat.id,
                        filt.file_id,
                        reply_to_message_id=message.message_id,
                        reply_markup=keyboard,
                    )
                else:
                    ENUM_FUNC_MAP[filt.file_type](
                        chat.id,
                        filt.file_id,
                        caption=filtext,
                        reply_to_message_id=message.message_id,
                        parse_mode=ParseMode.HTML,
                        reply_markup=keyboard,
                    )
            elif filt.is_sticker:
                message.reply_sticker(filt.reply)
            elif filt.is_document:
                message.reply_document(filt.reply)
            elif filt.is_image:
                message.reply_photo(filt.reply)
            elif filt.is_audio:
                message.reply_audio(filt.reply)
            elif filt.is_voice:
                message.reply_voice(filt.reply)
            elif filt.is_video:
                message.reply_video(filt.reply)
            elif filt.has_markdown:
                buttons = sql.get_buttons(chat.id, filt.keyword)
                keyb = build_keyboard_parser(context.bot, chat.id, buttons)
                keyboard = InlineKeyboardMarkup(keyb)

                try:
                    send_message(
                        update.effective_message,
                        filt.reply,
                        parse_mode=ParseMode.MARKDOWN,
                        disable_web_page_preview=True,
                        reply_markup=keyboard,
                    )
                except BadRequest as excp:
                    if excp.message == "Unsupported url protocol":
                        try:
                            send_message(
                                update.effective_message,
                                "You seem to be trying to use an unsupported url protocol. "
                                "Telegram doesn't support buttons for some protocols, such as tg://. Please try "
                                "again...",
                            )
                        except BadRequest as excp:
                            log.exception("Error in filters: " + excp.message)
                    elif excp.message == "Reply message not found":
                        try:
                            context.bot.send_message(
                                chat.id,
                                filt.reply,
                                parse_mode=ParseMode.MARKDOWN,
                                disable_web_page_preview=True,
                                reply_markup=keyboard,
                            )
                        except BadRequest as excp:
                            log.exception("Error in filters: " + excp.message)
                    else:
                        try:
                            send_message(
                                update.effective_message,
                                "ᴛʜɪs ᴍᴇssᴀɢᴇ ᴄᴏᴜʟᴅɴ'ᴛ ʙᴇ sᴇɴᴛ ᴀs ɪᴛ's ɪɴᴄᴏʀʀᴇᴄᴛʟʏ ғᴏʀᴍᴀᴛᴛᴇᴅ.",
                            )
                        except BadRequest as excp:
                            log.exception("Error in filters: " + excp.message)
                        log.warning("Message %s could not be parsed", str(filt.reply))
                        log.exception(
                            "Could not parse filter %s in chat %s",
                            str(filt.keyword),
                            str(chat.id),
                        )

            else:
                # LEGACY - all new filters will have has_markdown set to True.
                try:
                    send_message(update.effective_message, filt.reply)
                except BadRequest as excp:
                    log.exception("Error in filters: " + excp.message)
            break


@Madaracmd(command="removeallfilters", filters=Filters.chat_type.groups)
def rmall_filters(update, _):
    chat = update.effective_chat
    user = update.effective_user
    member = chat.get_member(user.id)
    if member.status != "creator" and user.id not in SUDO_USERS:
        update.effective_message.reply_text(
            "ᴏɴʟʏ ᴛʜᴇ ᴄʜᴀᴛ ᴏᴡɴᴇʀ ᴄᴀɴ ᴄʟᴇᴀʀ ᴀʟʟ ɴᴏᴛᴇs ᴀᴛ ᴏɴᴄᴇ."
        )
    else:
        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="sᴛᴏᴘ ᴀʟʟ ғɪʟᴛᴇʀs", callback_data="filters_rmall"
                    )
                ],
                [InlineKeyboardButton(text="ᴄᴀɴᴄᴇʟ", callback_data="filters_cancel")],
            ]
        )
        update.effective_message.reply_text(
            f"ᴀʀᴇ ʏᴏᴜ sᴜʀᴇ ʏᴏᴜ ᴡᴏᴜʟᴅ ʟɪᴋᴇ ᴛᴏ sᴛᴏᴘ ᴀʟʟ ғɪʟᴛᴇʀs ɪɴ {chat.title}? ᴛʜɪs ᴀᴄᴛɪᴏɴ ᴄᴀɴɴᴏᴛ ʙᴇ ᴜɴᴅᴏɴᴇ.",
            reply_markup=buttons,
            parse_mode=ParseMode.MARKDOWN,
        )


@Madaracallback(pattern=r"filters_.*")
def rmall_callback(update, _):
    query = update.callback_query
    chat = update.effective_chat
    msg = update.effective_message
    member = chat.get_member(query.from_user.id)
    if query.data == "filters_rmall":
        if member.status == "creator" or query.from_user.id in SUDO_USERS:
            allfilters = sql.get_chat_triggers(chat.id)
            if not allfilters:
                msg.edit_text("ɴᴏ ғɪʟᴛᴇʀs ɪɴ ᴛʜɪs ᴄʜᴀᴛ, ɴᴏᴛʜɪɴɢ ᴛᴏ sᴛᴏᴘ!")
                return

            count = 0
            filterlist = []
            for x in allfilters:
                count += 1
                filterlist.append(x)

            for i in filterlist:
                sql.remove_filter(chat.id, i)

            msg.edit_text(f"ᴄʟᴇᴀɴᴇᴅ {count} ғɪʟᴛᴇʀs ɪɴ {chat.title}")

        if member.status == "administrator":
            query.answer("Only owner of the chat can do this.")

        if member.status == "member":
            query.answer("You need to be admin to do this.")
    elif query.data == "filters_cancel":
        if member.status == "creator" or query.from_user.id in SUDO_USERS:
            msg.edit_text("Clearing of all filters has been cancelled.")
            return
        if member.status == "administrator":
            query.answer("Only owner of the chat can do this.")
        if member.status == "member":
            query.answer("You need to be admin to do this.")


# NOT ASYNC NOT A HANDLER
def get_exception(excp, filt, chat):
    if excp.message == "Unsupported url protocol":
        return "You seem to be trying to use the URL protocol which is not supported. Telegram does not support key for multiple protocols, such as tg: //. Please try again!"
    elif excp.message == "Reply message not found":
        return "noreply"
    else:
        log.warning("Message %s could not be parsed", str(filt.reply))
        log.exception(
            "Could not parse filter %s in chat %s", str(filt.keyword), str(chat.id)
        )
        return "This data could not be sent because it is incorrectly formatted."


# NOT ASYNC NOT A HANDLER
def addnew_filter(update, chat_id, keyword, text, file_type, file_id, buttons):
    msg = update.effective_message
    totalfilt = sql.get_chat_triggers(chat_id)
    if len(totalfilt) >= 1000:  # Idk why i made this like function....
        msg.reply_text("ᴛʜɪs ɢʀᴏᴜᴘ ʜᴀs ʀᴇᴀᴄʜᴇᴅ ɪᴛs ᴍᴀx ғɪʟᴛᴇʀs ʟɪᴍɪᴛ ᴏғ 150.")
        return False
    else:
        sql.new_add_filter(chat_id, keyword, text, file_type, file_id, buttons)
        return True


def __stats__():
    return "•➥ {} ғɪʟᴛᴇʀs, ᴀᴄʀᴏss {} ᴄʜᴀᴛs.".format(sql.num_filters(), sql.num_chats())


def __import_data__(chat_id, data):
    # set chat filters
    filters = data.get("filters", {})
    for trigger in filters:
        sql.add_to_blacklist(chat_id, trigger)


def __migrate__(old_chat_id, new_chat_id):
    sql.migrate_chat(old_chat_id, new_chat_id)


def __chat_settings__(chat_id, _):
    cust_filters = sql.get_chat_triggers(chat_id)
    return "ᴛʜᴇʀᴇ ᴀʀᴇ `{}` ᴄᴜsᴛᴏᴍ ғɪʟᴛᴇʀs ʜᴇʀᴇ.".format(len(cust_filters))


__help__ = """
❂ /filters*:* `ʟɪꜱᴛ ᴀʟʟ ᴀᴄᴛɪᴠᴇ ғɪʟᴛᴇʀꜱ ꜱᴀᴠᴇᴅ ɪɴ ᴛʜᴇ ᴄʜᴀᴛ`
*ᴀᴅᴍɪɴ ᴏɴʟʏ:*
❂ /filter <keyword> <reply message>*:* ᴀᴅᴅ a ғɪʟᴛᴇʀ ᴛᴏ ᴛʜɪꜱ chat. ᴛʜᴇ ʙᴏᴛ ᴡɪʟʟ ɴᴏᴡ ʀᴇᴘʟʏ ᴛʜᴀᴛ ᴍᴇꜱꜱᴀɢᴇ ᴡʜᴇɴᴇᴠᴇʀ 'ᴋᴇʏᴡᴏʀᴅ
ɪꜱ ᴍᴇɴᴛɪᴏɴᴇᴅ. ɪғ ʏᴏᴜ ʀᴇᴘʟʏ ᴛᴏ ᴀ ꜱᴛɪᴄᴋᴇʀ ᴡɪᴛʜ ᴀ ᴋᴇʏᴡᴏʀᴅ, ᴛʜᴇ ʙᴏᴛ ᴡɪʟʟ ʀᴇᴘʟʏ ᴡɪᴛʜ ᴛʜᴀᴛ ꜱᴛɪᴄᴋᴇʀ. ɴᴏᴛᴇ: ᴀʟʟ ғɪʟᴛᴇʀ 
ᴋᴇʏᴡᴏʀᴅꜱ ᴀʀᴇ ɪɴ ʟᴏᴡᴇʀᴄᴀꜱᴇ. ɪғ ʏᴏᴜ ᴡᴀɴᴛ ʏᴏᴜʀ ᴋᴇʏᴡᴏʀᴅ ᴛᴏ ʙᴇ ᴀ ꜱᴇɴᴛᴇɴᴄᴇꜱ, ᴜꜱᴇ ϙᴜᴏᴛᴇꜱ. ᴇɢ: /filter "hey there" ʜᴇʏ ʜᴇʟʟᴏ 
 ꜱᴇᴘᴀʀᴀᴛᴇ ᴅɪғғ ʀᴇᴘʟɪᴇꜱ ʙʏ `%%%` ᴛᴏ ɢᴇᴛ ʀᴀɴᴅᴏᴍ ʀᴇᴘʟɪᴇꜱ
 
 *ᴇxᴀᴍᴘʟᴇ:* 
 `/filter "filtername"
 Reply 1
 %%%
 Reply 2
 %%%
 Reply 3`
❂ /stop <filter keyword>*:* `ꜱᴛᴏᴘ ᴛʜᴀᴛ ғɪʟᴛᴇʀ`
*ᴄʜᴀᴛ creator only:*
❂ /removeallfilters*:* `ʀᴇᴍᴏᴠᴇ ᴀʟʟ ᴄʜᴀᴛ ғɪʟᴛᴇʀꜱ ᴀᴛ ᴏɴᴄᴇ`.
*ɴᴏᴛᴇ*: ғɪʟᴛᴇʀꜱ ᴀʟꜱᴏ ꜱᴜᴘᴘᴏʀᴛ ᴍᴀʀᴋᴅᴏᴡɴ formatters like: {first}, {last} ᴇᴛᴄ.. ᴀɴᴅ ʙᴜᴛᴛᴏɴꜱ.
ᴄʜᴇᴄᴋ /markdownhelp ᴛᴏ ᴋɴᴏᴡ ᴍᴏʀᴇ!
"""
__mod_name__ = "𝙵ɪʟᴛᴇʀs"
