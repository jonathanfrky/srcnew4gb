# devgagan
# Note if you are trying to deploy on vps then directly fill values in ("")

from os import getenv

API_ID = int(getenv("API_ID", "18037098"))
API_HASH = getenv("API_HASH", "c4905ea7f50b335b9e792a193898ce1b")
BOT_TOKEN = getenv("BOT_TOKEN", "7767489346:AAEgPc-ZC3y8QwOBAziOMb_dOVy0o3yBCEE")
OWNER_ID = list(map(int, getenv("OWNER_ID", "1027418759").split()))
MONGO_DB = getenv("MONGO_DB", "mongodb+srv://azikfaylyukla:azikfaylyukla@cluster0.pqs27.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
LOG_GROUP = getenv("LOG_GROUP", "-1004741374600")
CHANNEL_ID = int(getenv("CHANNEL_ID", "-1001425340692"))
FREEMIUM_LIMIT = int(getenv("FREEMIUM_LIMIT", "30"))
PREMIUM_LIMIT = int(getenv("PREMIUM_LIMIT", "500"))
WEBSITE_URL = getenv("WEBSITE_URL", "")
AD_API = getenv("AD_API", "")
STRING = getenv("STRING", "AgE_wcoAAO9q4--b5oCpu6iQiMTC1muMwPqxzrXoNPwzltglv0brhQhansd72YUAjf7pZt6jm4XxHsTJvcBbouxhbJP0NucwUdYrLZHSqjU1xUMFUDYCxoOqhHpF7CiwHRJbi6TRUGVzGZ88OHDY8aa4Ujg-FJA1iEBRBVrb2uLgfj_qGNfmSoG6oAQy3y8pIBWnDlcaH11BlDnOFH-pam7OypBtYge8dt7hKKVvCmg5XaqgBLgSmeUujnRXCGGjRw-Xoavf-hdNs_JwSzg8r5OSUihHDU5DEqWf9tkX4ZKX1YVoTUy69zX2ioS9P78DkwePtsHdM0CNkZHHM0n3msFfw3r_hAAAAAA9PSqHAA")
YT_COOKIES = getenv("YT_COOKIES", None)
INSTA_COOKIES = getenv("INSTA_COOKIES", None)
