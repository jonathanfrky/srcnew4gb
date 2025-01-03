# devgagan
# Note if you are trying to deploy on vps then directly fill values in ("")

from os import getenv

API_ID = int(getenv("API_ID", "18037098"))
API_HASH = getenv("API_HASH", "c4905ea7f50b335b9e792a193898ce1b")
BOT_TOKEN = getenv("BOT_TOKEN", "7767489346:AAEpm557wbEfAwo1J401j2PoWodObThFN6s")
OWNER_ID = list(map(int, getenv("OWNER_ID", "1027418759").split()))
MONGO_DB = getenv("MONGO_DB", "mongodb+srv://azikfaylyukla:azikfaylyukla@cluster0.pqs27.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
LOG_GROUP = getenv("LOG_GROUP", "-1004741374600")
CHANNEL_ID = int(getenv("CHANNEL_ID", "-1001425340692"))
FREEMIUM_LIMIT = int(getenv("FREEMIUM_LIMIT", "30"))
PREMIUM_LIMIT = int(getenv("PREMIUM_LIMIT", "500"))
WEBSITE_URL = getenv("WEBSITE_URL", "")
AD_API = getenv("AD_API", "")
STRING = getenv("STRING", "AgETOWoACP3DA27pg3gatC5jLdoO1JaWyco5YeeB-Rdnh1EV8bYWv8kz0odQfVLohtsO1YtjTC5t2Riq8CrPnDv7S9ZtlBGOYePV-BDPuCxjHovQDX-XkkFWqudfE_3_9Y3G7ev4In4ASVFJvmI8LP9x4VKML05-o6TYj0qoVfCEmQjK_jtYp7-b9ndynrTgjfeJ4taS1K1IH11Jy9fPYVTonQ9xZEGw8mUGcYdn6dH5bJ2P38fBOrLVdHhp3JF5XmxeebBtyEPd4gYQwDXFIM4ads1UtqjA99pkD7P5qyKJeA4srw-sb7SNrs1jF3LRxFfb5AD0JTFOhNsM04sz-pXA5YYHxwAAAAA9PSqHAA")
YT_COOKIES = getenv("YT_COOKIES", None)
INSTA_COOKIES = getenv("INSTA_COOKIES", None)
