---
title: "Cryptohack Lab. Encoding Challenge"
date: 2025-09-29
tags: [crypto, writeup]  
categories: [Crypto]
tagline: ""
header:
  overlay_image: /assets/images/IMG_writeups/IMG_Cryptohack/cryptohack_logo.webp
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "Сryptohack Lab"
      url: "https://cryptohack.org/challenges/general/"
---

{% raw %}

Нужно подключиться к `socket.cryptohack.org 13377` и получить флаг. Дан исходный код [13377.py](https://cryptohack.org/static/challenges/13377_86793614535c47dea371d2f0e406dbd9.py) и шаблон для подключения [pwntools_example.py](https://cryptohack.org/static/challenges/pwntools_example_f93ca6ccef2def755aa8f6d9aa6e9c5b.py).

```
socket.cryptohack.org 13377
```

## Solution

Так-с. Нужно разбираться в задаче. Дан исходный код приложения в `13377.py`. Этот код запущен на сервере. Для подключения есть адрес `socket.cryptohack.org 13377`. Попробую подключиться через `netcat`:

```bash
nc socket.cryptohack.org 13377
```

А вот ответы от сервера:

![IMG](/assets/images/IMG_writeups/IMG_Cryptohack/IMG_Encoding_Challenge/1.png){: height="200" .align-center}

Посмотрю исходник кода:

```python
#!/usr/bin/env python3

from Crypto.Util.number import bytes_to_long, long_to_bytes
from utils import listener # this is cryptohack's server-side module and not part of python
import base64
import codecs
import random

FLAG = "crypto{????????????????????}"
ENCODINGS = [
    "base64",
    "hex",
    "rot13",
    "bigint",
    "utf-8",
]
with open('/usr/share/dict/words') as f:
    WORDS = [line.strip().replace("'", "") for line in f.readlines()]


class Challenge():
    def __init__(self):
        self.no_prompt = True # Immediately send data from the server without waiting for user input
        self.challenge_words = ""
        self.stage = 0

    def create_level(self):
        self.stage += 1
        self.challenge_words = "_".join(random.choices(WORDS, k=3))
        encoding = random.choice(ENCODINGS)

        if encoding == "base64":
            encoded = base64.b64encode(self.challenge_words.encode()).decode() # wow so encode
        elif encoding == "hex":
            encoded = self.challenge_words.encode().hex()
        elif encoding == "rot13":
            encoded = codecs.encode(self.challenge_words, 'rot_13')
        elif encoding == "bigint":
            encoded = hex(bytes_to_long(self.challenge_words.encode()))
        elif encoding == "utf-8":
            encoded = [ord(b) for b in self.challenge_words]

        return {"type": encoding, "encoded": encoded}

    #
    # This challenge function is called on your input, which must be JSON
    # encoded
    #
    def challenge(self, your_input):
        if self.stage == 0:
            return self.create_level()
        elif self.stage == 100:
            self.exit = True
            return {"flag": FLAG}

        if self.challenge_words == your_input["decoded"]:
            return self.create_level()

        return {"error": "Decoding fail"}


import builtins; builtins.Challenge = Challenge # hack to enable challenge to be run locally, see https://cryptohack.org/faq/#listener
listener.start_server(port=13377)
```

В списке `ENCODINGS` можно увидеть используемыe кодировки. В методе `create_level` класса `Challenge` можно увидеть создание уровня. По строке `self.challenge_words = "_".join(random.choices(WORDS, k=3))` можно понять, что слова подбираются рандомно, кодировка — тоже — `encoding = random.choice(ENCODINGS)`.

Можно пройти это руками... GL HF.

Либо же написать автоматизацию. Сайт `CryptoChallenge` предлагает сделать это с помощью `pwntools`. Вполне себе хорошее решение. Но предварительно разберемся со всеми алгоритмами кодирования. Про [`base64`](https://cu63.github.io/crypto/base64/), [`hex`](https://cu63.github.io/crypto/hex/), [`bigint`](https://cu63.github.io/crypto/Bytes_and_Big_Integers/), [`utf-8`(`ascii`)](https://cu63.github.io/crypto/ascii/) я уже рассказывал. Посмотрим на `rot13`.

## ROT-13

`ROT-13` — это простейший метод шифрования, относящийся к семейству [шифров Цезаря](https://ru.wikipedia.org/wiki/%D0%A8%D0%B8%D1%84%D1%80_%D0%A6%D0%B5%D0%B7%D0%B0%D1%80%D1%8F). Он работает путем сдвига каждой буквы латинского алфавита на **13 позиций**:

![IMG](/assets/images/IMG_writeups/IMG_Cryptohack/IMG_Encoding_Challenge/2.png){: height="200" .align-center}

Оригинальная строка — `ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz`, строка для перестановок — `NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm`. Напишу простую реализацию на `Python`:

```python
orig = 'abcdefghijklmnopqrstuvwxyz'

def encode(s: str, shift: int = 13) -> str: 
    encoded_str = []

    shift = shift % 26
    for c in s:
        if 'a' <= c <= 'z':
            pos = ord(c) - ord('a')
            pos += shift
            pos %= 26
            c = chr(ord('a') + pos)
        elif 'A' <= c <= 'Z':
            pos = ord(c) - ord('A')
            pos += shift
            pos %= 26
            c = chr(ord('A') + pos)
        encoded_str.append(c)
    return ''.join(encoded_str)


def decode(s: str, shift: int = 13) -> str:
    decoded_str = []

    shift = shift % 26
    for c in s:
        if 'a' <= c <= 'z':
            pos = ord(c) - ord('a')
            pos -= shift
            pos %= 26
            c = chr(ord('a') + pos)
        elif 'A' <= c <= 'Z':
            pos = ord(c) - ord('A')
            pos -= shift
            pos %= 26
            c = chr(ord('A') + pos)
        decoded_str.append(c)

    return ''.join(decoded_str)


if __name__ == '__main__':
    s = 'Coffee Cube' 
    for i in range(-26, 26):
        encoded_s = encode(s, i)
        decoded_s = decode(encoded_s, i)
        print(i, encoded_s, decoded_s)
```

С алгоритмом мы разобрались. Теперь можно с чистой совестью использовать готовые решения)

## pwntools

Это удобная [Python-библиотека](https://github.com/Gallopsled/pwntools), предназначенная для **эксплуатации уязвимостей**, **CTF-задач** и **автоматизации взаимодействия с бинарями**.

Тула действительно удобная. Поэтому начнем с ней знакомство. Шаблон для работы с сервером уже есть. Разберу его:

```python
from pwn import * # pip install pwntools
import json

r = remote('socket.cryptohack.org', 13377, level = 'debug') # Указывается удаленный сервер для взаимодействия

def json_recv():
    line = r.recvline() # Получение строки до символа `\0` или `\n`
    return json.loads(line.decode())

def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request) # Отправить строку


received = json_recv()

print("Received type: ")
print(received["type"])
print("Received encoded value: ")
print(received["encoded"])

to_send = {
    "decoded": "changeme"
}
json_send(to_send)

json_recv()
```

Запущу шаблон:

![IMG](/assets/images/IMG_writeups/IMG_Cryptohack/IMG_Encoding_Challenge/3.png){: height="200" .align-center}

Видно, что код уже корректно парсит приходящие данные. Напишу автоматизацию. Можно использовать реализации из [предыдущих разборов](https://cu63.github.io/categories/#crypto). Я буду использовать и то, и другое.

```python
from pwn import * # pip install pwntools
import json

import base64


r = remote('socket.cryptohack.org', 13377, level = 'info')


def json_recv():
    line = r.recvline()
    return json.loads(line.decode())


def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)


def decode_utf(s: bytes):
    return ''.join([chr(c) for c in s])


def decode_hex(s: bytes):
    return bytes.fromhex(s).decode()


def decode_base64(s: str):
    s = base64.b64decode(s).decode()
    return s

def decode_bigint(s: str):
    ans = []

    for i in range(2, len(s), 2):
        ans.append(chr(int(s[i:i+2], 16)))

    return ''.join(ans)


def decode_rot(s: str, shift: int = 13) -> str:
    orig = 'abcdefghijklmnopqrstuvwxyz'
    decoded_str = []

    shift = shift % 26
    for c in s:
        if 'a' <= c <= 'z':
            pos = ord(c) - ord('a')
            pos -= shift
            pos %= 26
            c = chr(ord('a') + pos)
        elif 'A' <= c <= 'Z':
            pos = ord(c) - ord('A')
            pos -= shift
            pos %= 26
            c = chr(ord('A') + pos)
        decoded_str.append(c)

    return ''.join(decoded_str)


ENCODINGS = {
        "base64": decode_base64,
        "hex": decode_hex,
        "rot13": decode_rot,
        "bigint": decode_bigint,
        "utf-8": decode_utf,
}

for _ in range(100):
    received = json_recv()

    encode_type = received["type"]
    s = received["encoded"]
    print("Received type:", encode_type)

    print("Received encoded value:", s)

    f = ENCODINGS[encode_type]
    decoded = f(s)
    print(decoded)
    to_send = {
        "decoded": decoded
    }
    json_send(to_send)

print('\nFlag is:', json_recv()['flag'])
```

Запустил скрипт.

![IMG](/assets/images/IMG_writeups/IMG_Cryptohack/IMG_Encoding_Challenge/4.png){: height="200" .align-center}

Чтобы убрать кучу отладочных сообщений, можно включить другой режим вот тут:

```python
r = remote('socket.cryptohack.org', 13377, level = 'info')
```

```
Flag is: crypto{3nc0d3_d3c0d3_3nc0d3}
```

{% endraw %}
