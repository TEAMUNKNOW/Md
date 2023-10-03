import os

import requests
from pyrogram import *
from pyrogram import filters
from pyrogram.raw.types import *
from telegraph import exceptions, upload_file

from Madara import pgram


@pgram.on_message(filters.command("id"))
async def getid(client, message):
    chat = message.chat
    your_id = message.from_user.id
    message_id = message.id
    reply = message.reply_to_message

    text = f"**[Message ID:]({message.link})** `{message_id}`\n"
    text += f"**[Your ID:](tg://user?id={your_id})** `{your_id}`\n"

    if not message.command:
        message.command = message.text.split()

    if not message.command:
        message.command = message.text.split()

    if len(message.command) == 2:
        try:
            split = message.text.split(None, 1)[1].strip()
            user_id = (await client.get_users(split)).id
            text += f"**[User ID:](tg://user?id={user_id})** `{user_id}`\n"

        except Exception:
            return await message.reply_text("This user doesn't exist.", quote=True)

    text += f"**[Chat ID:](https://t.me/{chat.username})** `{chat.id}`\n\n"

    if (
        not getattr(reply, "empty", True)
        and not message.forward_from_chat
        and not reply.sender_chat
    ):
        text += (
            f"**[Replied Message ID:]({reply.link})** `{message.reply_to_message.id}`\n"
        )
        text += f"**[Replied User ID:](tg://user?id={reply.from_user.id})** `{reply.from_user.id}`\n\n"

    if reply and reply.forward_from_chat:
        text += f"The forwarded channel, {reply.forward_from_chat.title}, has an id of `{reply.forward_from_chat.id}`\n\n"
        print(reply.forward_from_chat)

    if reply and reply.sender_chat:
        text += f"ID of the replied chat/channel, is `{reply.sender_chat.id}`"
        print(reply.sender_chat)

    await message.reply_text(
        text,
        disable_web_page_preview=True,
    )


def time_format(seconds) -> str:
    if seconds is not None:
        seconds = int(seconds)
        h = seconds // 3600 % 24
        m = seconds % 3600 // 60
        s = seconds % 3600 % 60
        if h > 0:
            return "{:02d}:{:02d}:{:02d}".format(h, m, s)
        elif m > 0:
            return "{:02d}:{:02d}".format(m, s)
        elif s > 0:
            return "{:02d}s".format(s)
    return "-"


@pgram.on_message(filters.command("whatanime"))
async def whatanime(app: pgram, message: Message):
    if message.reply_to_message and (
        message.reply_to_message.photo
        or message.reply_to_message.video
        or message.reply_to_message.animation
    ):
        m = await message.reply_text("`sᴇᴀʀᴄʜɪɴɢ ғᴏʀ ʀᴇsᴜʟᴛ..`")
        doc = await message.reply_to_message.download()
        try:
            media_url = upload_file(doc)
        except exceptions.TelegraphException as exc:
            await m.edit(f"**ERROR:** `{exc}`")
            os.remove(doc)
            return
        os.remove(doc)

        res = requests.get(
            f"https://api.trace.moe/search?url=https://graph.org/{media_url[0]}"
        )

        data = res.json()["result"][0]

        await message.reply_video(
            data["video"],
            caption=f"""
𝗧𝗜𝗧𝗟𝗘: {data["filename"]}
𝗘𝗣𝗜𝗦𝗢𝗗𝗘: {data["episode"]}
𝗧𝗜𝗠𝗘: {time_format(data['from'])}-{time_format(data['to'])}
𝗦𝗜𝗠𝗜𝗟𝗔𝗥𝗜𝗧𝗬: {data["similarity"]:.2%}
𝗔𝗡𝗜𝗟𝗜𝗦𝗧 𝗨𝗥𝗟: https://anilist.co/anime/{data["anilist"]}
       """,
        )
        await m.delete()
    else:
        return await message.reply_text(
            "`ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ɪᴛ ᴛᴏ ᴀ ᴘʜᴏᴛᴏ ᴏʀ ɢɪғ ᴏʀ ᴠɪᴅᴇᴏ ᴛᴏ ᴡᴏʀᴋ`"
        )
