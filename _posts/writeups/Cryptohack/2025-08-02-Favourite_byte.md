---
title: "CryptoHack Lab. Favourite byte"
date: 2025-08-02
tags: [crypto, writeup]  
categories: [Crypto]
tagline: ""
header:
  overlay_image: /assets/images/IMG_writeups/IMG_Cryptohack/cryptohack_logo.webp
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "СryptoHack Lab"
      url: "https://cryptohack.org/courses/intro/xorkey0/"
---

Для решения нужно расшифровать строку, которая зашифрована с помощью операции `XOR` с одним байтом. Но ключ неизвестен.

```
73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d
```

## Solution

Значения ключа могут быть от `0` до `255`. Без брутфорса тут не обойтись. Но у нас есть подсказка: флаг начинается с `crypto{`. Значит нужно найти такой ключ, при `XOR` с которым `73626960647f6b` превратится в `crypto{`.

Погнали:

```python
flag = '73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d'
prefix = '73626960647f6b'


def xor(s: bytes, key: int) -> bytes:
   return bytes([s[i] ^ key for i in range(len(s))])


prefix = bytes.fromhex(prefix)
flag = bytes.fromhex(flag)
for key in range(0xff):
    s = xor(prefix, key)
    if s.startswith(b'crypto{'):
        print('Key is', key)
        print(xor(flag, key).decode())
```

Ключ — `16`. Флаг:

```
crypto{0x10_15_my_f4v0ur173_by7e}
```
