import re
import os
import binascii
from Crypto.Cipher import AES
import requests

os.system("cls")

def resolve_cookie(html):
    def hex_to_char(match):
        return chr(int(match.group(1), 16))

    page = re.sub(r'\\x([A-F0-9]{2})', hex_to_char, html)
    keys = re.findall(r'[a-f0-9]{32}', page)
    if not keys:
        raise ValueError('not bypassed')

    key, iv, cipher = [binascii.unhexlify(key) for key in keys]
    cookie_name_match = re.search(r'[a-z0-9]{32}","cookie","(?P<name>[^"=]+)', page, flags=re.IGNORECASE)
    cookie_name = cookie_name_match.group('name') if cookie_name_match else None
    cipher_bytes = AES.new(key, AES.MODE_CBC, iv=iv).decrypt(cipher)
    cookie_value = binascii.hexlify(cipher_bytes).decode()
    cookie_info_match = re.search(r'(?P<info>expires=[^"]+)', page, flags=re.IGNORECASE)
    cookie_info = cookie_info_match.group('info') if cookie_info_match else None

    if not cookie_name:
        raise ValueError('Cannot get cookieName')

    return cookie_value

#Создаем сессию
s=requests.Session()
s=requests.Session()

#Получаем хекс лист для обхода
html=s.get(
"https://forum.radmir.games/",
headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
).text

#Обходим
resolved_cookie = resolve_cookie(html)
print(resolved_cookie)
resolved_cookie = resolve_cookie(html)
print(resolved_cookie)

#Подставляем результат в куки
s.cookies.set("REACTLABSPROTECTION",resolved_cookie)

#Обходим react.su и получаем нужную нам страницу
html=s.get(
"https://forum.radmir.games/",
headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
).text
