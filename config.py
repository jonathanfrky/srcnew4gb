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
STRING = getenv("STRING", "AgETOWoAJ4fYuc-l8MBh5brKbHN6Kjgad8qpmHjTJX4DAO5yHiMk6cKkkebsjzooSjbksKoCJH1OBMvxer9rGATiOZZf1LpgbAsM3KLxdVlBwQcDbQp7QzPgs5_BTLnZaa4YBCD6yBSmOm55nznIiOptGh4pqfPdRdOfpW6QWDn3qwVcB8HO6m0sNr-oQSPUdYA-6orP85_DkPrc2ACs-9W4pFjNqf3UZkaHrJN1X9TDmW4UKsBvUqXOeEp6r7ZmSJoZY8uVCVmPM5wgjDmz6JJfvWRUxuBDXoZZUiqUUPwLl8q5vh82937jmxqlwuSjbqCwGCwVi-e7UAXUyTdT8qSqeqsqsgAAAAA9PSqHAA")
YT_COOKIES = getenv("YT_COOKIES", None)
INSTA_COOKIES = getenv("INSTA_COOKIES", None)
