import html

import bs4
import jikanpy
import requests
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    ParseMode,
    Update,
)
from telegram.ext import CallbackContext

from Madara import dispatcher
from Madara.modules.disable import DisableAbleCommandHandler

info_btn = "ᴍᴏʀᴇ ɪɴғᴏʀᴍᴀᴛɪᴏɴ"
kaizoku_btn = "ᴋᴀɪᴢᴏᴋᴜ ☠️"
kayo_btn = "ᴋᴀʏᴏ 🏴‍☠️"
prequel_btn = "⬅️ ᴘʀᴇǫᴜᴇʟ"
sequel_btn = "sᴇǫᴜᴇʟ ➡️"
close_btn = "ᴄʟᴏsᴇ ❌"


def shorten(description, info="anilist.co"):
    msg = ""
    if len(description) > 700:
        description = description[:500] + "...."
        msg += f"\n*ᴅᴇsᴄʀɪᴘᴛɪᴏɴ*:\n{description}[Read More]({info})"
    else:
        msg += f"\n*ᴅᴇsᴄʀɪᴘᴛɪᴏɴ*:\n{description}"
    return msg


# time formatter from uniborg
def t(milliseconds: int) -> str:
    """ɪɴᴘᴜᴛs ᴛɪᴍᴇ ɪɴ ᴍɪʟʟɪsᴇᴄᴏɴᴅs, ᴛᴏ ɢᴇᴛ ʙᴇᴀᴜᴛɪғɪᴇᴅ ᴛɪᴍᴇ,
    as string"""
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        (f"{str(days)} Days, " if days else "")
        + (f"{str(hours)} Hours, " if hours else "")
        + (f"{str(minutes)} Minutes, " if minutes else "")
        + (f"{str(seconds)} Seconds, " if seconds else "")
        + (f"{str(milliseconds)} ms, " if milliseconds else "")
    )

    return tmp[:-2]


airing_query = """
query ($id: Int,$search: String) {
    Media (id: $id, type: ANIME,search: $search) {
        id
        episodes
        title {
            romaji
            english
            native
        }
        nextAiringEpisode {
            airingAt
            timeUntilAiring
            episode
        }
    }
}
"""

fav_query = """
query ($id: Int) {
    Media (id: $id, type: ANIME) {
        id
        title {
            romaji
            english
            native
        }
    }
}
"""

anime_query = """
query ($id: Int,$search: String) {
    Media (id: $id, type: ANIME,search: $search) {
        id
        title {
            romaji
            english
            native
        }
        description (asHtml: false)
        startDate{
            year
        }
        episodes
        season
        type
        format
        status
        duration
        siteUrl
        studios{
            nodes{
                name
            }
        }
        trailer{
            id
            site
            thumbnail
        }
        averageScore
        genres
        bannerImage
    }
}
"""

character_query = """
query ($query: String) {
    Character (search: $query) {
        id
        name {
            first
            last
            full
            native
        }
        siteUrl
        image {
            large
        }
        description(asHtml: false)
    }
}
"""

manga_query = """
query ($id: Int,$search: String) {
    Media (id: $id, type: MANGA,search: $search) {
        id
        title {
            romaji
            english
            native
        }
        description (asHtml: false)
        startDate{
            year
        }
        type
        format
        status
        siteUrl
        averageScore
        genres
        bannerImage
    }
}
"""

url = "https://graphql.anilist.co"


def extract_arg(message: Message):
    split = message.text.split(" ", 1)
    if len(split) > 1:
        return split[1]
    reply = message.reply_to_message
    return reply.text if reply is not None else None


def airing(update: Update, context: CallbackContext):
    message = update.effective_message
    search_str = extract_arg(message)
    if not search_str:
        update.effective_message.reply_text(
            "ᴛᴇʟʟ ᴀɴɪᴍᴇ ɴᴀᴍᴇ :) ( /airing <anime name>)",
        )
        return
    variables = {"search": search_str}
    response = requests.post(
        url,
        json={"query": airing_query, "variables": variables},
    ).json()["data"]["Media"]
    msg = f"*Name*: *{response['title']['romaji']}*(`{response['title']['native']}`)\n*ID*: `{response['id']}`"
    if response["nextAiringEpisode"]:
        time = response["nextAiringEpisode"]["timeUntilAiring"] * 1000
        time = t(time)
        msg += f"\n*ᴇᴘɪsᴏᴅᴇ*: `{response['nextAiringEpisode']['episode']}`\n*Airing In*: `{time}`"
    else:
        msg += f"\n*ᴇᴘɪsᴏᴅᴇ*:{response['episodes']}\n*Status*: `N/A`"
    update.effective_message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)


def anime(update: Update, context: CallbackContext):
    message = update.effective_message
    search = extract_arg(message)
    if not search:
        update.effective_message.reply_text("ғᴏʀᴍᴀᴛ : /anime < anime name >")
        return
    variables = {"search": search}
    json = requests.post(
        url,
        json={"query": anime_query, "variables": variables},
    ).json()
    if "errors" in json.keys():
        update.effective_message.reply_text("ᴀɴɪᴍᴇ ɴᴏᴛ ғᴏᴜɴᴅ")
        return
    if json:
        json = json["data"]["Media"]
        msg = f"*{json['title']['romaji']}*(`{json['title']['native']}`)\n*Type*: {json['format']}\n*Status*: {json['status']}\n*Episodes*: {json.get('episodes', 'N/A')}\n*Duration*: {json.get('duration', 'N/A')} Per Ep.\n*Score*: {json['averageScore']}\n*Genres*: `"
        for x in json["genres"]:
            msg += f"{x}, "
        msg = msg[:-2] + "`\n"
        msg += "*Studios*: `"
        for x in json["studios"]["nodes"]:
            msg += f"{x['name']}, "
        msg = msg[:-2] + "`\n"
        info = json.get("siteUrl")
        trailer = json.get("trailer", None)
        json["id"]
        if trailer:
            trailer_id = trailer.get("id", None)
            site = trailer.get("site", None)
            if site == "youtube":
                trailer = f"https://youtu.be/{trailer_id}"
        description = (
            json.get("description", "N/A")
            .replace("<i>", "")
            .replace("</i>", "")
            .replace("<br>", "")
            .replace("~!", "")
            .replace("!~", "")
        )
        msg += shorten(description, info)
        infoo = json.get("siteUrl")
        image = infoo.replace("anilist.co/anime/", "img.anili.st/media/")
        if trailer:
            buttons = [
                [
                    InlineKeyboardButton("ᴍᴏʀᴇ ɪɴғᴏ", url=info),
                    InlineKeyboardButton("ᴛʀᴀɪʟᴇʀ 🎬", url=trailer),
                ],
                [
                    InlineKeyboardButton("🍿 ᴅᴏᴡɴʟᴏᴀᴅ 🍿", url=f"https://t.me/Anime_Campus"),
                ],
            ]
        else:
            buttons = [
                [
                    InlineKeyboardButton("ᴍᴏʀᴇ ɪɴғᴏ", url=info),
                    InlineKeyboardButton("🍿 ᴅᴏᴡɴʟᴏᴀᴅ 🍿", url=f"https://t.me/Anime_Campus"),
                ],
            ]
        if image:
            try:
                update.effective_message.reply_photo(
                    photo=image,
                    caption=msg,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
            except:
                msg += f" [〽️]({image})"
                update.effective_message.reply_text(
                    msg,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
        else:
            update.effective_message.reply_text(
                msg,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(buttons),
            )


def character(update: Update, context: CallbackContext):
    message = update.effective_message
    search = extract_arg(message)
    if not search:
        update.effective_message.reply_text("ғᴏʀᴍᴀᴛ : /character < character name >")
        return
    variables = {"query": search}
    json = requests.post(
        url,
        json={"query": character_query, "variables": variables},
    ).json()
    if "errors" in json.keys():
        update.effective_message.reply_text("ᴄʜᴀʀᴀᴄᴛᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ")
        return
    if json:
        json = json["data"]["Character"]
        msg = f"*{json.get('name').get('full')}* (`{json.get('name').get('native')}`)\n"
        description = f"{json['description']}".replace("~!", "").replace("!~", "")
        site_url = json.get("siteUrl")
        msg += shorten(description, site_url)
        if image := json.get("image", None):
            image = image.get("large")
            update.effective_message.reply_photo(
                photo=image,
                caption=msg.replace("<b>", "</b>"),
                parse_mode=ParseMode.MARKDOWN,
            )
        else:
            update.effective_message.reply_text(
                msg.replace("<b>", "</b>"),
                parse_mode=ParseMode.MARKDOWN,
            )


def manga(update: Update, context: CallbackContext):
    message = update.effective_message
    search = extract_arg(message)
    if not search:
        update.effective_message.reply_text("ғᴏʀᴍᴀᴛ : /manga < manga name >")
        return
    variables = {"search": search}
    json = requests.post(
        url,
        json={"query": manga_query, "variables": variables},
    ).json()
    msg = ""
    if "errors" in json.keys():
        update.effective_message.reply_text("Manga not found")
        return
    if json:
        json = json["data"]["Media"]
        title, title_native = json["title"].get("romaji", False), json["title"].get(
            "native",
            False,
        )
        start_date, status, score = (
            json["startDate"].get("year", False),
            json.get("status", False),
            json.get("averageScore", False),
        )
        if title:
            msg += f"*{title}*"
            if title_native:
                msg += f"(`{title_native}`)"
        if start_date:
            msg += f"\n*sᴛᴀʀᴛ ᴅᴀᴛᴇ* - `{start_date}`"
        if status:
            msg += f"\n*sᴛᴀᴛᴜs* - `{status}`"
        if score:
            msg += f"\n*sᴄᴏʀᴇ* - `{score}`"
        msg += "\n*ɢᴇɴʀᴇs* - "
        for x in json.get("genres", []):
            msg += f"{x}, "
        msg = msg[:-2]
        info = json["siteUrl"]
        buttons = [[InlineKeyboardButton("ᴍᴏʀᴇ ɪɴғᴏ", url=info)]]
        image = json.get("bannerImage", False)
        msg += f"\n_{json.get('description', None)}_"
        if image:
            try:
                update.effective_message.reply_photo(
                    photo=image,
                    caption=msg,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
            except:
                msg += f" [〽️]({image})"
                update.effective_message.reply_text(
                    msg,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
        else:
            update.effective_message.reply_text(
                msg,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(buttons),
            )


def upcoming(update: Update, context: CallbackContext):
    jikan = jikanpy.jikan.Jikan()
    upcomin = jikan.top("anime", page=1, subtype="upcoming")

    upcoming_list = [entry["title"] for entry in upcomin["top"]]
    upcoming_message = ""

    for entry_num in range(len(upcoming_list)):
        if entry_num == 10:
            break
        upcoming_message += f"{entry_num + 1}. {upcoming_list[entry_num]}\n"

    update.effective_message.reply_text(upcoming_message)


def site_search(update: Update, context: CallbackContext, site: str):
    message = update.effective_message
    search_query = extract_arg(message)
    more_results = True

    if not search_query:
        message.reply_text("ɢɪᴠᴇ sᴏᴍᴇᴛʜɪɴɢ ᴛᴏ sᴇᴀʀᴄʜ")
        return

    if site == "kaizoku":
        search_url = f"https://animekaizoku.com/?s={search_query}"
        html_text = requests.get(search_url).text
        soup = bs4.BeautifulSoup(html_text, "html.parser")
        if search_result := soup.find_all("h2", {"class": "post-title"}):
            result = f"<b>sᴇᴀʀᴄʜ ʀᴇsᴜʟᴛs ғᴏʀ</b> <code>{html.escape(search_query)}</code> <b>on</b> @Anime_Campus: \n\n"
            for entry in search_result:
                post_link = "https://animekaizoku.com/" + entry.a["href"]
                post_name = html.escape(entry.text)
                result += f"• <a href='{post_link}'>{post_name}</a>\n"
        else:
            more_results = False
            result = f"<b>ɴᴏ ʀᴇsᴜʟᴛ ғᴏᴜɴᴅ ғᴏʀ</b> <code>{html.escape(search_query)}</code> <b>on</b> @Anime_Campus"

            post_link = entry.a["href"]
            post_name = html.escape(entry.text.strip())
            result += f"• <a href='{post_link}'>{post_name}</a>\n"

    buttons = [[InlineKeyboardButton("sᴇᴇ ᴀʟʟ ʀᴇsᴜʟᴛs", url=search_url)]]

    if more_results:
        message.reply_text(
            result,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True,
        )
    else:
        message.reply_text(
            result,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
        )


def kaizoku(update: Update, context: CallbackContext):
    site_search(update, context, "kaizoku")


__help__ = """
ɢᴇᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴀɴɪᴍᴇ, ᴍᴀɴɢᴀ ᴏʀ ᴄʜᴀʀᴀᴄᴛᴇʀs ғʀᴏᴍ [ᴀɴɪʟɪsᴛ](anilist.co) ᴀɴᴅ [ᴍᴀʟ](https://myanimelist.net/)

*ᴀɴɪʟɪsᴛ ᴄᴏᴍᴍᴀɴᴅs:*

• /anime <anime>*:* `ʀᴇᴛᴜʀɴs ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴛʜᴇ ᴀɴɪᴍᴇ ғʀᴏᴍ ᴀɴɪʟɪsᴛ `

• /character <character>*:* `ʀᴇᴛᴜʀɴs ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴛʜᴇ ᴄʜᴀʀᴀᴄᴛᴇʀ ғʀᴏᴍ ᴀɴɪʟɪsᴛ `
  
• /manga <manga>*:* `ʀᴇᴛᴜʀɴs ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴛʜᴇ ᴍᴀɴɢᴀ ғʀᴏᴍ ᴀɴɪʟɪsᴛ `
  
• /airing <anime>*:* `ʀᴇᴛᴜʀɴs ᴀɴɪᴍᴇ ᴀɪʀɪɴɢ ɪɴғᴏ ғʀᴏᴍ ᴀɴɪʟɪsᴛ `
 
*ᴀɴɪᴍᴇ sᴇᴀʀᴄʜ ᴄᴏᴍᴍᴀɴᴅs:*

• /anime <anime>*:* `ʀᴇᴛᴜʀɴs ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴛʜᴇ ᴀɴɪᴍᴇ ғʀᴏᴍ ᴀɴɪʟɪsᴛ `

• /animequotes*:* `ɢᴇᴛ ǫᴜᴏᴛᴇs ɪɴ ᴘɪᴄᴛᴜʀᴇ`

• /quote*:* `ɢᴇᴛ ᴛᴇxᴛ ǫᴜᴏᴛᴇs`

• /whatanime*:* `ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ɪᴛ ᴛᴏ ᴀ ᴘʜᴏᴛᴏ ᴏʀ ɢɪғ ᴏʀ ᴠɪᴅᴇᴏ ᴛᴏ ᴡᴏʀᴋ `
     
"""


ANIME_HANDLER = DisableAbleCommandHandler("anime", anime, run_async=True)
AIRING_HANDLER = DisableAbleCommandHandler("airing", airing, run_async=True)
CHARACTER_HANDLER = DisableAbleCommandHandler("character", character, run_async=True)
MANGA_HANDLER = DisableAbleCommandHandler("manga", manga, run_async=True)
##USER_HANDLER = DisableAbleCommandHandler("user", user, run_async=True)
UPCOMING_HANDLER = DisableAbleCommandHandler("upcoming", upcoming, run_async=True)
##KAIZOKU_SEARCH_HANDLER = DisableAbleCommandHandler("kaizoku", kaizoku, run_async=True)
##KAYO_SEARCH_HANDLER = DisableAbleCommandHandler("kayo", kayo, run_async=True)

dispatcher.add_handler(ANIME_HANDLER)
dispatcher.add_handler(CHARACTER_HANDLER)
dispatcher.add_handler(MANGA_HANDLER)
dispatcher.add_handler(AIRING_HANDLER)
# dispatcher.add_handler(USER_HANDLER)
# dispatcher.add_handler(KAIZOKU_SEARCH_HANDLER)
# dispatcher.add_handler(KAYO_SEARCH_HANDLER)
dispatcher.add_handler(UPCOMING_HANDLER)

__mod_name__ = "𝙰ɴɪᴍᴇ"
__command_list__ = [
    "anime",
    "manga",
    "character",
    "user",
    "upcoming",
    "airing",
    "kayo",
]
__handlers__ = [
    ANIME_HANDLER,
    CHARACTER_HANDLER,
    MANGA_HANDLER,
    #   USER_HANDLER,
    UPCOMING_HANDLER,
    # KAYO_SEARCH_HANDLER,
    AIRING_HANDLER,
    # KAIZOKU_SEARCH_HANDLER,
]
