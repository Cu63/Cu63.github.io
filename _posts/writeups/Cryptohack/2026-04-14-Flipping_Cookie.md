---
title: "Cryptohack Lab. Flipping Cookie"
date: 2026-04-14
tags: [crypto, writeup]
categories: [Crypto]
tagline: ""
header:
  overlay_image: /assets/images/IMG_writeups/IMG_Cryptohack/cryptohack_logo.webp
  overlay_filter: 0.5
  overlay_color: "#fff"
  actions:
    - label: "Сryptohack Lab"
      url: "https://cryptohack.org/courses/symmetric/flipping_cookie/"
---

Ты можешь получить cookie для моего сайта, но это не поможет тебе прочитать флаг... наверное.

## Исходный код

```python
from Crypto.Cipher import AES
import os
from Crypto.Util.Padding import pad, unpad
from datetime import datetime, timedelta


KEY = ?
FLAG = ?


@chal.route('/flipping_cookie/check_admin/<cookie>/<iv>/')
def check_admin(cookie, iv):
    cookie = bytes.fromhex(cookie)
    iv = bytes.fromhex(iv)

    try:
        cipher = AES.new(KEY, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(cookie)
        unpadded = unpad(decrypted, 16)
    except ValueError as e:
        return {"error": str(e)}

    if b"admin=True" in unpadded.split(b";"):
        return {"flag": FLAG}
    else:
        return {"error": "Only admin can read the flag"}


@chal.route('/flipping_cookie/get_cookie/')
def get_cookie():
    expires_at = (datetime.today() + timedelta(days=1)).strftime("%s")
    cookie = f"admin=False;expiry={expires_at}".encode()

    iv = os.urandom(16)
    padded = pad(cookie, 16)
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(padded)
    ciphertext = iv.hex() + encrypted.hex()

    return {"cookie": ciphertext}
```

## Анализ

Напишу код, чтобы автоматизировать получение cookie:

```python
def get_cookie() -> str:
    url = f'{URL}/get_cookie/'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['cookie']

    return ''
```

Ответ:

```
4ce53aac2104003af6a068bfccadc063f1251cf2b4691db99963a6e558a5801a11645386b3c4b8d0dda55d3733019bcc
```

Теперь нужно разобрать алгоритм генерации cookie. Меня очень радует вот эта строка:

```python
ciphertext = iv.hex() + encrypted.hex()
```

Она означает, что первые 32 символа — это наш `iv`. Брутфорсить его было бы сложно. А нам его просто подарили.

Также у нас есть часть открытого текста `admin=False;expiry=`. Посмотрим внимательнее на проверку cookie:

```python
if b"admin=True" in unpadded.split(b";"):
    return {"flag": FLAG}
else:
    return {"error": "Only admin can read the flag"}
```

Для того чтобы получить флаг, нам нужно, чтобы в cookie было значение `admin=True`. При расшифровке в режиме `CBC` (как мы разбирали в [лабе ECB CBC WTF]({% post_url writeups/Cryptohack/2026-04-07-ECB_CBC_WTF %})) последним шагом является `XOR` расшифрованного блока с `iv`. Нам не нужно знать ключ. Достаточно сделать так, чтобы после `XOR` мы получили нужную нам строку.

Чтобы это сделать, нам нужно заменить часть `iv` так, чтобы на выходе было `admin=True` вместо `admin=False`. Изменить нужно только 5 символов начиная с позиции 6 (`admin=` — 6 байт, дальше идёт `False`). Для каждого из символов формула такая:

```python
new_iv[i] = old_iv[i] ^ ord(old_char) ^ ord(target_char)
```

Это работает благодаря [свойствам XOR]({% post_url writeups/Cryptohack/2025-08-25-XOR_2_Properties %}) — коммутативности и обратимости.

>`False` (5 символов) заменяется на `True;` (тоже 5 символов). После подмены строка станет `admin=True;;expiry=...` — двойная `;`. Это не мешает, потому что `split(b";")` просто создаст пустой элемент, а проверяется наличие `admin=True` в списке.

## Реализация

Для подмены напишу функцию `flip_iv`:

```python
def flip_iv(iv: bytes, offset: int, old: str, new: str) -> bytes:
    iv = list(iv)
    for i in range(len(old)):
        iv[offset + i] ^= ord(old[i]) ^ ord(new[i])
    return bytes(iv)
```

Полный код решения:

```python
import requests


URL = 'http://aes.cryptohack.org/flipping_cookie'


def get_cookie() -> str:
    url = f'{URL}/get_cookie/'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['cookie']

    return ''


def check_admin(cookie: bytes, iv: bytes) -> str:
    url = (
        f'{URL}/check_admin/{cookie.hex()}/{iv.hex()}/'
    )
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()

    return ''


def flip_iv(iv: bytes, offset: int, old: str, new: str) -> bytes:
    iv = list(iv)
    for i in range(len(old)):
        iv[offset + i] ^= ord(old[i]) ^ ord(new[i])
    return bytes(iv)


def main():
    raw = bytes.fromhex(get_cookie())
    iv, ciphertext = raw[:16], raw[16:]

    iv = flip_iv(iv, offset=6, old='False', new='True;')

    result = check_admin(ciphertext, iv)
    print(result.get('flag', result.get('error')))


if __name__ == '__main__':
    main()
```

Запущу, чтобы получить флаг:

```bash
cu63:Flipping Cookie/ $ python solver.py
crypto{4u7h3n71c4710n_15_3553n714l}
```
