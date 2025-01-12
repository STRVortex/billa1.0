import re
from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

# Get this value from my.telegram.org/apps
API_ID = "23539804"
API_HASH = "a174f115853c3cc48b9d571329dd32f3"

# Get your token from @BotFather on Telegram.
BOT_TOKEN = "7127577382:AAHjGrAwFVH364gg9KUyM-clEx1vPoW7JaA"

# Get your mongo url from cloud.mongodb.com
MONGO_DB_URI = "mongodb+srv://github9210:ieMwBAIuNl2NEMRO@cluster0.lcwkg5r.mongodb.net/?retryWrites=true&w=majority"

DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 6000))

# Chat id of a group for logging bot's activities
LOGGER_ID = -1002064111110

# Get this value from @FallenxBot on Telegram by /id
OWNER_ID = 5960968099

## Fill these variables if you're deploying on heroku.
# Your heroku app name
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
# Get it from http://dashboard.heroku.com/account
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

UPSTREAM_REPO = getenv(
    "UPSTREAM_REPO",
    "https://github.com/koreansmu/billamusic2.0",
)
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "master")
GIT_TOKEN = "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"  # Fill this variable if your upstream repository is private

SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/STORM_TECHH")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/STORM_CORE")

# Set this to True if you want the assistant to automatically leave chats after an interval
AUTO_LEAVING_ASSISTANT = bool(getenv("AUTO_LEAVING_ASSISTANT", False))

# Get this credentials from https://developer.spotify.com/dashboard
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "2d3fd5ccdd3d43dda6f17864d8eb7281")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", "48d311d8910a4531ae81205e1f754d27")


# Maximum limit for fetching playlist's track from youtube, spotify, apple links.
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", 70))


# Telegram audio and video file size limit (in bytes)
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", 104857600))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", 1073741824))
# Checkout https://www.gbmb.org/mb-to-bytes for converting mb to bytes


# Get your pyrogram v2 session from @StringFatherBot on Telegram
STRING1 = "BQAf70YAcmT_XLFtOnNBDeUP8LeIxyn5n1rEDAqBQ3L9nbHm5yJGZbiOZt9y1HrRJewfQbFGTLlBb_3TanXwbz-Jw91J5EFKGLVd9Sx5WIq2duVvjVbnd73p6UrZAISnm92z8eCcdaRds4lwLfqPqxEFObTWoWMyMxTDu2ffKLqn2O4TTUWfiNcZVgbSxm55J7V5C0suqF4f1fStYVvgIt3F6vUaOIDBBqi-HsxPB004vHGaKL4ScZdCTB79ymO7TEn78Dm9YW5Zyl_rfLUA3fljB-sgcVyK-sWxpmP36H3hkgNX5IoqcVMy43OrrB76GSw0_YKvZb19RXaidzTA36skk0kYfQAAAAHoeEM3AA"
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)


BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}


START_IMG_URL = getenv(
    "START_IMG_URL", "https://graph.org/file/8e3acca08b3ecce1dd1d9-4bbbbf3c17511d79aa.jpg"
)
PING_IMG_URL = getenv(
    "PING_IMG_URL", "https://graph.org/file/2398b367e4372d20ee6c0-4273e6d34c37115326.jpg"
)
PLAYLIST_IMG_URL = "https://graph.org/file/0152d3a7c0de056fe76df-f8dab610c650f0ad31.jpg"
STATS_IMG_URL = "https://graph.org/file/999be18d2ae22977571f3-f93222d713f41b0146.jpg"
TELEGRAM_AUDIO_URL = "https://graph.org/file/002dc32a43f463fbfed8e-e04d6df2456227531b.jpg"
TELEGRAM_VIDEO_URL = "https://graph.org/file/f4e010d4a88b63d1f6258-dac28211d4296ff886.jpg"
STREAM_IMG_URL = "https://graph.org/file/d6d0d0b2328e9916de696-b5fb5dd3091cbab13e.jpg"
SOUNCLOUD_IMG_URL = "https://te.legra.ph/file/bb0ff85f2dd44070ea519.jpg"
YOUTUBE_IMG_URL = "https://te.legra.ph/file/6298d377ad3eb46711644.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://te.legra.ph/file/37d163a2f75e0d3b403d6.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://te.legra.ph/file/b35fd1dfca73b950b1b05.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://te.legra.ph/file/95b3ca7993bbfaf993dcb.jpg"


def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))


DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))


if SUPPORT_CHANNEL:
    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHANNEL url is wrong. Please ensure that it starts with https://"
        )

if SUPPORT_CHAT:
    if not re.match("(?:http|https)://", SUPPORT_CHAT):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHAT url is wrong. Please ensure that it starts with https://"
        )
