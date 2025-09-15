---
title: "CryptoHack Lab. You either know, XOR you don't"
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
      url: "https://cryptohack.org/courses/intro/xorkey1/"
---
{% raw %}

Для решения нужно расшифровать строку, которая зашифрована с помощью операции `XOR` с одним байтом. Но ключ неизвестен. Его длина также неизвестна.

```
0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104
```

## Solution

Для нахождения ключа будем использовать брутфорс. Если ключ равен длине строки — то будет грустно.

Известен формат строки `crypto{`. Попробуем найти ключ для этой части. Если он будет повторяться, то возможно получится расшифровать всю строку.

Попробую сделать это:

```python
flag = '0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104'
s = b'crypto{'

def xor(s: bytes, key: list[int]) -> bytes:
   return bytes([s[i] ^ key[i % len(key)] for i in range(len(s))])


flag = bytes.fromhex(flag)
key = [flag[i] ^ s[i] for i in range(len(s))]
print(key)
```

Для удобства написал `xor` для ключа разной длины. В `key[i % len(key)` мы всегда берем индекс по модулю его длины, так что не выйдем за границу списка.

Воть ключ:

```
[109, 121, 88, 79, 82, 107, 101]
```

Поксорим:

```
crypto{%r~n-LQCnAUaY6ifjtJJMvXeb_lGja
```

Получилась какая-то хрень. Но ключ подозрительно похож на отображаемые `ASCII` символы. Выведем его:

```
myXORke
```

Хмммм... Что-то это мне напоминает, может быть `myKORkebab`. Да не, бред какой-то. Пусть будет что-то безумное... Например `myXORkey`. Попробую расшифровать:

```python
flag = '0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104'
s = b'crypto{'
key = b'myXORkey'

def xor(s: bytes, key: list[int]) -> bytes:
   return bytes([s[i] ^ key[i % len(key)] for i in range(len(s))])

flag = bytes.fromhex(flag)
flag = xor(flag, key)

print(flag.decode())
```

А вот и флаг:

```
crypto{1f_y0u_Kn0w_En0uGH_y0u_Kn0w_1t_4ll}
```
{% endraw %}
