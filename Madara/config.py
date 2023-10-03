import json
import os
from os import getenv

from dotenv import load_dotenv

load_dotenv()


def get_user_list(config, key):
    with open("{}/Madara/{}".format(os.getcwd(), config), "r") as json_file:
        return json.load(json_file)[key]


class Config(object):
    LOGGER = True
    # ᴀᴅᴅ ʏᴏᴜʀ ᴠᴇʀs  (ᴍᴀɪɴ ᴠᴇʀs)
    API_ID = int(getenv("API_ID", "16743442"))
    API_HASH = getenv("API_HASH", "12bbd720f4097ba7713c5e40a11dfd2a")
    EVENT_LOGS = int(getenv("EVENT_LOGS", "-1001922732593"))
    DATABASE_URL = getenv(
        "DATABASE_URL",
        "postgres://pjwfzthq:eGF0tslmouCIz1S-FtDs1WGFW0DrIOi8@arjuna.db.elephantsql.com/pjwfzthq",
    )  # elephantsql.com
    REDIS_URL = "redis://default:neko69@redis-18084.c289.us-west-1-2.ec2.cloud.redislabs.com:18084/Neko-Free-db"  # redis.os
    MONGO_DB_URL = getenv(
        "MONGO_DB_URL",
        "mongodb+srv://vortex:yNNrzMsR0BAiI4iY@cluster0.8sizo.mongodb.net/?retryWrites=true&w=majority",
    )
    TOKEN = getenv("TOKEN", "6330964987:AAGGGM2iz-2hTmZLkiigTQgTCHMPePRC6AY")
    OWNER_USERNAME = getenv("OWNER_USERNAME", "SexyNano")
    OWNER_ID = int(getenv("OWNER_ID", "6198858059"))
    SUPPORT_CHAT = getenv("SUPPORT_CHAT", "JHBots")

    # ɴᴏᴛ ɪᴍᴘᴏʀᴛᴀɴᴛ ᴢᴏɴᴇ, ɴᴏ ɴᴇᴇᴅ ᴛᴏ ᴇᴅɪᴛ
    MONGO_DB = "Madara"  # ⚠️ ᴅᴏɴ'ᴛ ᴇᴅɪᴛ
    ARQ_API_URL = "arq.hamker.dev"  # ⚠️ ᴅᴏɴ'ᴛ ᴇᴅɪᴛ
    ARQ_API_KEY = "YZXQNZ-TPCRLZ-HKWWKY-SPPYAL-ARQ"
    DONATION_LINK = "t.me/SexyNano"
    HELP_IMG = "https://graph.org/file/9b8b09ce1d5d48f8004f3.jpg"
    START_VIDEO = "https://graph.org/file/2904688233933fd7e64fc.mp4"
    UPDATES_CHANNEL = "JujutsuHighNetwork"
    INFOPIC = False
    GENIUS_API_TOKEN = (
        "gIgMyTXuwJoY9VCPNwKdb_RUOA_9mCMmRlbrrdODmNvcpslww_2RIbbWOB8YdBW9"
    )
    SPAMWATCH_API = "tBIAzON4MiJmj_WwVbcI3HSXv03xoOZLgQqcZXgQD~6mvM_Gl0fresvC~FoROHKP"
    REM_BG_API_KEY = None
    OPENWEATHERMAP_ID = None
    WALL_API = None
    TIME_API_KEY = None
    NO_LOAD = ["rss"]
    TEMP_DOWNLOAD_DIRECTORY = "./"  # ⚠️ ᴅᴏɴ'ᴛ ᴇᴅɪᴛ
    LOAD = []  # ⚠️ ᴅᴏɴ'ᴛ ᴇᴅɪᴛ
    DEL_CMDS = True
    BAN_STICKER = None
    WORKERS = 8
    STRICT_GBAN = True
    WEBHOOK = False
    URL = None
    PORT = []
    ALLOW_EXCL = []
    ALLOW_CHATS = True
    CERT_PATH = []
    SPAMWATCH_SUPPORT_CHAT = "Anime_Krew"
    BOT_API_URL = "https://api.telegram.org/bot"  # ⚠️ ᴅᴏɴ'ᴛ ᴇᴅɪᴛ
    DRAGONS = get_user_list("elevated_users.json", "sudos")  # ⚠️ ᴅᴏɴ'ᴛ ᴇᴅɪᴛ
    DEV_USERS = get_user_list("elevated_users.json", "devs")  # ⚠️ ᴅᴏɴ'ᴛ ᴇᴅɪᴛ
    REQUESTER = get_user_list("elevated_users.json", "whitelists")  # ⚠️ ᴅᴏɴ'ᴛ ᴇᴅɪᴛ
    DEMONS = get_user_list("elevated_users.json", "supports")  # ⚠️ ᴅᴏɴ'ᴛ ᴇᴅɪᴛ
    INSPECTOR = get_user_list("elevated_users.json", "sudos")  # ⚠️ ᴅᴏɴ'ᴛ ᴇᴅɪᴛ
    TIGERS = get_user_list("elevated_users.json", "tigers")  # ⚠️ ᴅᴏɴ'ᴛ ᴇᴅɪᴛ
    WOLVES = get_user_list("elevated_users.json", "whitelists")  # ⚠️ ᴅᴏɴ'ᴛ ᴇᴅɪᴛ


class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True


# ENJOY
