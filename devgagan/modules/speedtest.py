
#GitHub/devgaganin

from time import time
from speedtest import Speedtest
import math
from telethon import events
from devgagan import botStartTime
from devgagan import sex as gagan

SIZE_UNITS = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']

def get_readable_time(seconds: int) -> str:
    result = ''
    (days, remainder) = divmod(seconds, 86400)
    days = int(days)
    if days != 0:
        result += f'{days}d'
    (hours, remainder) = divmod(remainder, 3600)
    hours = int(hours)
    if hours != 0:
        result += f'{hours}h'
    (minutes, seconds) = divmod(remainder, 60)
    minutes = int(minutes)
    if minutes != 0:
        result += f'{minutes}m'
    seconds = int(seconds)
    result += f'{seconds}s'
    return result

def get_readable_file_size(size_in_bytes) -> str:
    if size_in_bytes is None:
        return '0B'
    index = 0
    while size_in_bytes >= 1024:
        size_in_bytes /= 1024
        index += 1
    try:
        return f'{round(size_in_bytes, 2)}{SIZE_UNITS[index]}'
    except IndexError:
        return 'File too large'


@gagan.on(events.NewMessage(incoming=True, pattern='/speedtest'))
async def speedtest(event):
    speed = await event.reply("Tezlik testi bajarilmoqda. Bir necha soniya kuting.")  #edit telethon
    test = Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    test.results.share()
    result = test.results.dict()
    path = (result['share'])
    currentTime = get_readable_time(time() - botStartTime)
    string_speed = f'''
╭─《 🚀 TEZLIK TEST MA'LUMOTI 》
├ <b>Yuborish:</b> <code>{speed_convert(result['upload'], False)}</code>
├ <b>Yuklab olish:</b>  <code>{speed_convert(result['download'], False)}</code>
├ <b>Ping:</b> <code>{result['ping']} ms</code>
├ <b>Vaqt:</b> <code>{result['timestamp']}</code>
├ <b>Yuborilgan ma'lumot:</b> <code>{get_readable_file_size(int(result['bytes_sent']))}</code>
╰ <bQabul qilingan ma'lumot:</b> <code>{get_readable_file_size(int(result['bytes_received']))}</code>
╭─《 🌐 TEZLIK TEST SERVERI 》
├ <b>Nomi:</b> <code>{result['server']['name']}</code>
├ <b>Mamlakat:</b> <code>{result['server']['country']}, {result['server']['cc']}</code>
├ <b>Sponsor:</b> <code>{result['server']['sponsor']}</code>
├ <b>Kechikish:</b> <code>{result['server']['latency']}</code>
├ <b>Kenglik:</b> <code>{result['server']['lat']}</code>
╰ <b>Uzunlik:</b> <code>{result['server']['lon']}</code>
╭─《 👤 MIJOZ MA'LUMOTLARI 》
├ <b>IP Address:</b> <code>{result['client']['ip']}</code>
├ <b>Kenglik:</b> <code>{result['client']['lat']}</code>
├ <b>Uzunlik:</b> <code>{result['client']['lon']}</code>
├ <b>Mamlakat:</b> <code>{result['client']['country']}</code>
├ <b>ISP:</b> <code>{result['client']['isp']}</code>
├ <b>ISP baholash:</b> <code>{result['client']['isprating']}</code>
╰ <b>Powered by @jonathanfrky</b> 
'''
    try:
        await event.reply(string_speed,file=path,parse_mode='html')
        await speed.delete()
    except Exception as g:
        await speed.delete()
        await event.reply(string_speed,parse_mode='html' )

def speed_convert(size, byte=True):
    if not byte: size = size / 8
    power = 2 ** 10
    zero = 0
    units = {0: "B/s", 1: "KB/s", 2: "MB/s", 3: "GB/s", 4: "TB/s"}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"
