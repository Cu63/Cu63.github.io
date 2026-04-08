---
title: "Cryptohack Lab. Passwords as Keys"
date: 2026-04-07
tags: [crypto, writeup]
categories: [Crypto]
tagline: ""
header:
  overlay_image: /assets/images/IMG_writeups/IMG_Cryptohack/cryptohack_logo.webp
  overlay_filter: 0.5
  overlay_color: "#fff"
  actions:
    - label: "Сryptohack Lab"
      url: "https://cryptohack.org/courses/symmetric/passwords_as_keys/"
---

Крайне важно, чтобы ключи в симметричных алгоритмах были **случайными байтами**, а не паролями или другими предсказуемыми данными. Эти случайные байты должны генерироваться с помощью криптографически стойкого генератора псевдослучайных чисел (CSPRNG). Если ключи хоть как-то предсказуемы, уровень безопасности шифра снижается, и злоумышленник, получивший доступ к шифротексту, может расшифровать его.

То, что ключ выглядит как набор случайных байтов, ещё не означает, что он действительно случайный. В данном случае ключ получен из простого пароля с помощью хеш-функции, что делает шифротекст уязвимым для взлома.

## Исходный код

```python
from Crypto.Cipher import AES
import hashlib
import random


# /usr/share/dict/words from
# https://gist.githubusercontent.com/wchargin/8927565/raw/d9783627c731268fb2935a731a618aa8e95cf465/words
with open("/usr/share/dict/words") as f:
    words = [w.strip() for w in f.readlines()]
keyword = random.choice(words)

KEY = hashlib.md5(keyword.encode()).digest()
FLAG = ?


@chal.route('/passwords_as_keys/decrypt/<ciphertext>/<password_hash>/')
def decrypt(ciphertext, password_hash):
    ciphertext = bytes.fromhex(ciphertext)
    key = bytes.fromhex(password_hash)

    cipher = AES.new(key, AES.MODE_ECB)
    try:
        decrypted = cipher.decrypt(ciphertext)
    except ValueError as e:
        return {"error": str(e)}

    return {"plaintext": decrypted.hex()}


@chal.route('/passwords_as_keys/encrypt_flag/')
def encrypt_flag():
    cipher = AES.new(KEY, AES.MODE_ECB)
    encrypted = cipher.encrypt(FLAG.encode())

    return {"ciphertext": encrypted.hex()}
```

Зашифрованный флаг:

```
c92b7734070205bdf6c0087a751466ec13ae15e6f1bcdd3f3a535
```

## Решение

У нас есть исходный текст того, как выбирался ключ и происходило шифрование. Также мы знаем, что использовался `AES`.

В качестве ключа используется случайный пароль из [словаря](https://gist.githubusercontent.com/wchargin/8927565/raw/d9783627c731268fb2935a731a618aa8e95cf465/words):

```python
with open("/usr/share/dict/words") as f:
    words = [w.strip() for w in f.readlines()]
keyword = random.choice(words)

KEY = hashlib.md5(keyword.encode()).digest()
```

Скачаю его через `wget`. Далее мне нужно перебрать все пароли, чтобы найти нужный:

```python
from Crypto.Cipher import AES
import hashlib


CIPHERTEXT = bytes.fromhex(
    'c92b7734070205bdf6c0087a751466ec13ae15e6f1bcdd3f3a535ec0f4bbae66'
)

def try_decrypt(key: bytes) -> str | None:
    plaintext = AES.new(key, AES.MODE_ECB).decrypt(CIPHERTEXT)
    try:
        text = plaintext.decode('ascii')
    except UnicodeDecodeError:
        return None
    return text if text.startswith('crypto{') else None

def main():
    with open('words') as f:
        for word in f:
            key = hashlib.md5(word.strip().encode()).digest()
            if flag := try_decrypt(key):
                print(flag)
                break

if __name__ == '__main__':
    main()
```

Логика работы простая. У нас есть зашифрованный текст, есть варианты ключей, а также начало открытого текста `crypto{`. Если после попытки расшифровки мы получим строку, начало которой совпадает с `crypto{`, то мы нашли наш ключ. Запущу:

```
cu63:Passwords as Keys/ $ python solver.py
crypto{k3y5__r__n07__p455w0rdz?}
```

Ключ найден.
