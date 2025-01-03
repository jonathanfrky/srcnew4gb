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
STRING = getenv("STRING", "1ApWapzMBuwosoU4sQg8vG_4xs17Tu_VAygbZ73k8okmbrBHa3Yh81GJnHJnFJn6X67x6C8GHmGYKXogGLIlFjOrXFZyIsL_PmlZJxe2KEK1bV50SRNGcIJhpDKy3fwPwwhJ8rL7qw5lyPR19uy5iuA8oVp6yGZgJiIfPc6nr9b0FEVJFOb7Q2OobUn0V_HIbezZfslyQ20Xn4cJdcjU8tnR3uyWT8zeOpelpAK5DhG28V0WhN9vv1naUz2uwJaVZ7H3DJ0168j8vPtPtje5GqU9g-QrmwuQ1oqQmHuS1oTNq1fRjLDz8hJwq-AMLEubp12JSO8YaprfEW0mBr1OknEdYdycDg58=")
YT_COOKIES = getenv("YT_COOKIES", None)
INSTA_COOKIES = getenv("INSTA_COOKIES", None)
