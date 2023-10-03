import nekos
import requests
from telegram.ext import run_async

from Madara import dispatcher
from Madara.modules.disable import DisableAbleCommandHandler

url_sfw = "https://api.waifu.pics/sfw/"


@run_async
def wallpaper(update, context):
    msg = update.effective_message
    target = "wallpaper"
    msg.reply_photo(nekos.img(target))


@run_async
def waifu(update, context):
    msg = update.effective_message
    url = f"{url_sfw}waifu"
    result = requests.get(url).json()
    img = result["url"]
    msg.reply_photo(photo=img)


@run_async
def neko(update, context):
    msg = update.effective_message
    url = f"{url_sfw}neko"
    result = requests.get(url).json()
    img = result["url"]
    msg.reply_photo(photo=img)


@run_async
def shinobu(update, context):
    msg = update.effective_message
    url = f"{url_sfw}shinobu"
    result = requests.get(url).json()
    img = result["url"]
    msg.reply_photo(photo=img)


@run_async
def megumin(update, context):
    msg = update.effective_message
    url = f"{url_sfw}megumin"
    result = requests.get(url).json()
    img = result["url"]
    msg.reply_photo(photo=img)


@run_async
def bully(update, context):
    msg = update.effective_message
    url = f"{url_sfw}bully"
    result = requests.get(url).json()
    img = result["url"]
    msg.reply_animation(img)


@run_async
def cuddle(update, context):
    msg = update.effective_message
    url = f"{url_sfw}cuddle"
    result = requests.get(url).json()
    img = result["url"]
    msg.reply_animation(img)


@run_async
def cry(update, context):
    msg = update.effective_message
    url = f"{url_sfw}cry"
    result = requests.get(url).json()
    img = result["url"]
    msg.reply_animation(img)


@run_async
def hug(update, context):
    msg = update.effective_message
    url = f"{url_sfw}hug"
    result = requests.get(url).json()
    img = result["url"]
    msg.reply_animation(img)


@run_async
def awoo(update, context):
    msg = update.effective_message
    url = f"{url_sfw}awoo"
    result = requests.get(url).json()
    img = result["url"]
    msg.reply_animation(img)


@run_async
def kiss(update, context):
    msg = update.effective_message
    url = f"{url_sfw}kiss"
    result = requests.get(url).json()
    img = result["url"]
    msg.reply_animation(img)


@run_async
def lick(update, context):
    msg = update.effective_message
    url = f"{url_sfw}lick"
    result = requests.get(url).json()
    img = result["url"]
    msg.reply_animation(img)


@run_async
def pat(update, context):
    msg = update.effective_message
    url = f"{url_sfw}pat"
    result = requests.get(url).json()
    img = result["url"]
    msg.reply_animation(img)


@run_async
def smug(update, context):
    msg = update.effective_message
    url = f"{url_sfw}smug"
    result = requests.get(url).json()
    img = result["url"]
    msg.reply_animation(img)


@run_async
def bonk(update, context):
    msg = update.effective_message
    url = f"{url_sfw}bonk"
    result = requests.get(url).json()
    img = result["url"]
    msg.reply_animation(img)


@run_async
def yeet(update, context):
    msg = update.effective_message
    url = f"{url_sfw}yeet"
    result = requests.get(url).json()
    img = result["url"]
    msg.reply_animation(img)


@run_async
def blush(update, context):
    msg = update.effective_message
    url = f"{url_sfw}blush"
    result = requests.get(url).json()
    img = result["url"]
    msg.reply_animation(img)


@run_async
def smile(update, context):
    msg = update.effective_message
    url = f"{url_sfw}smile"
    result = requests.get(url).json()
    img = result["url"]
    msg.reply_animation(img)


@run_async
def wave(update, context):
    msg = update.effective_message
    url = f"{url_sfw}wave"
    result = requests.get(url).json()
    img = result["url"]
    msg.reply_animation(img)


@run_async
def highfive(update, context):
    msg = update.effective_message
    url = f"{url_sfw}highfive"
    result = requests.get(url).json()
    img = result["url"]
    msg.reply_animation(img)


@run_async
def handhold(update, context):
    msg = update.effective_message
    url = f"{url_sfw}handhold"
    result = requests.get(url).json()
    img = result["url"]
    msg.reply_animation(img)


@run_async
def nom(update, context):
    msg = update.effective_message
    url = f"{url_sfw}nom"
    result = requests.get(url).json()
    img = result["url"]
    msg.reply_animation(img)


@run_async
def bite(update, context):
    msg = update.effective_message
    url = f"{url_sfw}bite"
    result = requests.get(url).json()
    img = result["url"]
    msg.reply_animation(img)


@run_async
def glomp(update, context):
    msg = update.effective_message
    url = f"{url_sfw}glomp"
    result = requests.get(url).json()
    img = result["url"]
    msg.reply_animation(img)


@run_async
def slap(update, context):
    msg = update.effective_message
    url = f"{url_sfw}slap"
    result = requests.get(url).json()
    img = result["url"]
    msg.reply_animation(img)


@run_async
def killgif(update, context):
    msg = update.effective_message
    url = f"{url_sfw}kill"
    result = requests.get(url).json()
    img = result["url"]
    msg.reply_animation(img)


@run_async
def kickgif(update, context):
    msg = update.effective_message
    url = f"{url_sfw}kick"
    result = requests.get(url).json()
    img = result["url"]
    msg.reply_animation(img)


@run_async
def happy(update, context):
    msg = update.effective_message
    url = f"{url_sfw}happy"
    result = requests.get(url).json()
    img = result["url"]
    msg.reply_animation(img)


@run_async
def wink(update, context):
    msg = update.effective_message
    url = f"{url_sfw}wink"
    result = requests.get(url).json()
    img = result["url"]
    msg.reply_animation(img)


@run_async
def poke(update, context):
    msg = update.effective_message
    url = f"{url_sfw}poke"
    result = requests.get(url).json()
    img = result["url"]
    msg.reply_animation(img)


@run_async
def dance(update, context):
    msg = update.effective_message
    url = f"{url_sfw}dance"
    result = requests.get(url).json()
    img = result["url"]
    msg.reply_animation(img)


@run_async
def cringe(update, context):
    msg = update.effective_message
    url = f"{url_sfw}cringe"
    result = requests.get(url).json()
    img = result["url"]
    msg.reply_animation(img)


################
@run_async
def tickle(update, context):
    msg = update.effective_message
    target = "tickle"
    msg.reply_video(nekos.img(target))


@run_async
def ngif(update, context):
    msg = update.effective_message
    target = "ngif"
    msg.reply_video(nekos.img(target))


@run_async
def feed(update, context):
    msg = update.effective_message
    target = "feed"
    msg.reply_video(nekos.img(target))


@run_async
def gasm(update, context):
    msg = update.effective_message
    target = "gasm"
    msg.reply_photo(nekos.img(target))


@run_async
def avatar(update, context):
    msg = update.effective_message
    target = "avatar"
    msg.reply_photo(nekos.img(target))


@run_async
def foxgirl(update, context):
    msg = update.effective_message
    target = "fox_girl"
    msg.reply_photo(nekos.img(target))


@run_async
def gecg(update, context):
    msg = update.effective_message
    target = "gecg"
    msg.reply_photo(nekos.img(target))


@run_async
def lizard(update, context):
    msg = update.effective_message
    target = "lizard"
    msg.reply_photo(nekos.img(target))


@run_async
def spank(update, context):
    msg = update.effective_message
    target = "spank"
    msg.reply_video(nekos.img(target))


@run_async
def goose(update, context):
    msg = update.effective_message
    target = "goose"
    msg.reply_photo(nekos.img(target))


@run_async
def woof(update, context):
    msg = update.effective_message
    target = "woof"
    msg.reply_photo(nekos.img(target))


WALLPAPER_HANDLER = DisableAbleCommandHandler("wallpaper", wallpaper)
TICKLE_HANDLER = DisableAbleCommandHandler("tickle", tickle)
FEED_HANDLER = DisableAbleCommandHandler("feed", feed)
GASM_HANDLER = DisableAbleCommandHandler("gasm", gasm)
AVATAR_HANDLER = DisableAbleCommandHandler("avatar", avatar)
FOXGIRL_HANDLER = DisableAbleCommandHandler("foxgirl", foxgirl)
GECG_HANDLER = DisableAbleCommandHandler("gecg", gecg)
LIZARD_HANDLER = DisableAbleCommandHandler("lizard", lizard)
GOOSE_HANDLER = DisableAbleCommandHandler("goose", goose)
WOOF_HANDLER = DisableAbleCommandHandler("woof", woof)
NGIF_HANDLER = DisableAbleCommandHandler("ngif", ngif)

WAIFUS_HANDLER = DisableAbleCommandHandler("waifus", waifu)
NEKO_HANDLER = DisableAbleCommandHandler("neko", neko)
SHINOBU_HANDLER = DisableAbleCommandHandler("shinobu", shinobu)
MEGUMIN_HANDLER = DisableAbleCommandHandler("megumin", megumin)
BULLY_HANDLER = DisableAbleCommandHandler("bully", bully)
CUDDLE_HANDLER = DisableAbleCommandHandler("cuddle", foxgirl)
CRY_HANDLER = DisableAbleCommandHandler("cry", cry)
HUG_HANDLER = DisableAbleCommandHandler("hug", hug)
AWOO_HANDLER = DisableAbleCommandHandler("awoo", awoo)
KISS_HANDLER = DisableAbleCommandHandler("kiss", kiss)
LICK_HANDLER = DisableAbleCommandHandler("lick", lick, run_async=True)
PAT_HANDLER = DisableAbleCommandHandler("pat", pat)


SMUG_HANDLER = DisableAbleCommandHandler("smug", smug)
BONK_HANDLER = DisableAbleCommandHandler("bonk", bonk)
YEET_HANDLER = DisableAbleCommandHandler("yeet", yeet)
BLUSH_HANDLER = DisableAbleCommandHandler("blush", blush)
SMILE_HANDLER = DisableAbleCommandHandler("smile", smile)
WAVE_HANDLER = DisableAbleCommandHandler("wave", wave)
HIGHFIVE_HANDLER = DisableAbleCommandHandler("highfive", highfive)
HANDHOLD_HANDLER = DisableAbleCommandHandler("handhold", handhold)
NOM_HANDLER = DisableAbleCommandHandler("nom", nom)
BITE_HANDLER = DisableAbleCommandHandler("bite", bite)
GLOMP_HANDLER = DisableAbleCommandHandler("glomp", glomp)


SLAP_HANDLER = DisableAbleCommandHandler("slap", slap)
KILLGIF_HANDLER = DisableAbleCommandHandler("killgif", killgif)
HAPPY_HANDLER = DisableAbleCommandHandler("happy", happy)
WINK_HANDLER = DisableAbleCommandHandler("wink", wink)
POKE_HANDLER = DisableAbleCommandHandler("poke", poke)
DANCE_HANDLER = DisableAbleCommandHandler("dance", dance)
CRINGE_HANDLER = DisableAbleCommandHandler("cringe", cringe)


dispatcher.add_handler(SLAP_HANDLER)
dispatcher.add_handler(KILLGIF_HANDLER)
dispatcher.add_handler(HAPPY_HANDLER)
dispatcher.add_handler(WINK_HANDLER)
dispatcher.add_handler(POKE_HANDLER)
dispatcher.add_handler(DANCE_HANDLER)
dispatcher.add_handler(CRINGE_HANDLER)


dispatcher.add_handler(SMUG_HANDLER)
dispatcher.add_handler(BONK_HANDLER)
dispatcher.add_handler(YEET_HANDLER)
dispatcher.add_handler(BLUSH_HANDLER)
dispatcher.add_handler(SMILE_HANDLER)
dispatcher.add_handler(WAVE_HANDLER)
dispatcher.add_handler(HIGHFIVE_HANDLER)
dispatcher.add_handler(HANDHOLD_HANDLER)
dispatcher.add_handler(NOM_HANDLER)
dispatcher.add_handler(BITE_HANDLER)
dispatcher.add_handler(GLOMP_HANDLER)


dispatcher.add_handler(AWOO_HANDLER)
dispatcher.add_handler(PAT_HANDLER)
dispatcher.add_handler(KISS_HANDLER)
dispatcher.add_handler(LICK_HANDLER)
dispatcher.add_handler(CRY_HANDLER)
dispatcher.add_handler(HUG_HANDLER)
dispatcher.add_handler(WAIFUS_HANDLER)
dispatcher.add_handler(NEKO_HANDLER)
dispatcher.add_handler(SHINOBU_HANDLER)
dispatcher.add_handler(MEGUMIN_HANDLER)
dispatcher.add_handler(BULLY_HANDLER)
dispatcher.add_handler(CUDDLE_HANDLER)

dispatcher.add_handler(LIZARD_HANDLER)
dispatcher.add_handler(NGIF_HANDLER)
dispatcher.add_handler(GOOSE_HANDLER)
dispatcher.add_handler(WOOF_HANDLER)
dispatcher.add_handler(GECG_HANDLER)
dispatcher.add_handler(WALLPAPER_HANDLER)
dispatcher.add_handler(TICKLE_HANDLER)
dispatcher.add_handler(FEED_HANDLER)
dispatcher.add_handler(GASM_HANDLER)
dispatcher.add_handler(AVATAR_HANDLER)
dispatcher.add_handler(FOXGIRL_HANDLER)

__handlers__ = [
    SLAP_HANDLER,
    LIZARD_HANDLER,
    GOOSE_HANDLER,
    WOOF_HANDLER,
    WALLPAPER_HANDLER,
    TICKLE_HANDLER,
    FEED_HANDLER,
    GASM_HANDLER,
    AVATAR_HANDLER,
    GECG_HANDLER,
    FOXGIRL_HANDLER,
]


__mod_name__ = "𝚂ғᴡ"
__help__ = """
*Commands* *:*  

• `/neko`*:* sᴇɴᴅs ʀᴀɴᴅᴏᴍ sғᴡ ɴᴇᴋᴏ sᴏᴜʀᴄᴇ ɪᴍᴀɢᴇs.
• `/ngif`*:* sᴇɴᴅs ʀᴀɴᴅᴏᴍ ɴᴇᴋᴏ ɢɪғs.
• `/tickle`*:* sᴇɴᴅs ʀᴀɴᴅᴏᴍ ᴛɪᴄᴋʟᴇ ɢɪғs.
• `/feed`*:* sᴇɴᴅs ʀᴀɴᴅᴏᴍ ғᴇᴇᴅɪɴɢ ɢɪғs.
• `/gasm`*:* sᴇɴᴅs ʀᴀɴᴅᴏᴍ ᴏʀɢᴀsᴍ sᴛɪᴄᴋᴇʀs.
• `/avatar`*:* sᴇɴᴅs ʀᴀɴᴅᴏᴍ ᴀᴠᴀᴛᴀʀ sᴛɪᴄᴋᴇʀs.
• `/waifus`*:* sᴇɴᴅs ʀᴀɴᴅᴏᴍ ᴡᴀɪғᴜ sᴛɪᴄᴋᴇʀs.
• `/kiss`*:* sᴇɴᴅs ʀᴀɴᴅᴏᴍ ᴋɪssɪɴɢ ɢɪғs.
• `/cuddle`*:* sᴇɴᴅs ʀᴀɴᴅᴏᴍ ᴄᴜᴅᴅʟᴇ ɢɪғs.
• `/foxgirl`*:* sᴇɴᴅs ʀᴀɴᴅᴏᴍ ғᴏxɢɪʀʟ sᴏᴜʀᴄᴇ ɪᴍᴀɢᴇs.
• `/smug`*:* sᴇɴᴅs ʀᴀɴᴅᴏᴍ sᴍᴜɢ ɢɪғs.
• `/gecg`*:* IDK
• `/slap`*:* sᴇɴᴅs ʀᴀɴᴅᴏᴍ sʟᴀᴘ ɢɪғs.
• `/hug`*:* ɢᴇᴛ ʜᴜɢɢᴇᴅ, ʜᴜɢs ᴀ ᴜsᴇʀ.
• `/pat`*:* ᴘᴀᴛs ᴀ ᴜsᴇʀ, ᴏʀ ɢᴇᴛ ᴘᴀᴛᴛᴇᴅ.
   
*Some more SFW commands :*

• `/shinobu`
• `/megumin`
• `/bully`
• `/cry`
• `/awoo`
• `/lick`
• `/bonk`
• `/yeet`
• `/blush`
• `/smile`
• `/wave`
• `/highfive`
• `/handhold`
• `/nom`
• `/bite`
• `/glomp`
• `/slapgif`
• `/kill`
• `/kick`
• `/happy`
• `/wink`
• `/poke`
• `/dance`
• `/cringe`
"""
