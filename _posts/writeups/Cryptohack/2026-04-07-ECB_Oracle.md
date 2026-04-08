---
title: "Cryptohack Lab. ECB Oracle"
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
      url: "https://cryptohack.org/courses/symmetric/ecb_oracle/"
---

ECB — самый простой режим: каждый блок открытого текста шифруется полностью независимо от других.

В этом случае твой ввод добавляется **перед** секретным флагом, после чего всё шифруется — и на этом всё. Функция расшифрования даже не предоставляется. Возможно, тебе и не нужен `padding oracle`, если у тебя есть `ECB oracle`?

## Исходный код

```python
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


KEY = ?
FLAG = ?


@chal.route('/ecb_oracle/encrypt/<plaintext>/')
def encrypt(plaintext):
    plaintext = bytes.fromhex(plaintext)

    padded = pad(plaintext + FLAG.encode(), 16)
    cipher = AES.new(KEY, AES.MODE_ECB)
    try:
        encrypted = cipher.encrypt(padded)
    except ValueError as e:
        return {"error": str(e)}

    return {"ciphertext": encrypted.hex()}
```

## ECB

Алгоритм применяется к каждому блоку фиксированной длины. Открытый текст делится на отдельные блоки, и к каждому из них применяется алгоритм шифрования. Каждый блок шифруется независимо.

![ECB scheme](/assets/images/IMG_writeups/IMG_Cryptohack/IMG_ECB_Oracle/ecb_scheme.png)

Что это нам даёт? Каждый блок шифруется независимо. Значит, если мы подадим на вход 2 одинаковых блока открытого текста, то шифротекст у них будет одинаковым.

## Дополнение (padding)

Используется в блоках, которые имеют размер меньше необходимого. Может заполняться нулями, единицами, чередующимися нулями и единицами. При необходимости удалить дополнение после расшифровки количество байтов дополнения записывается в последний байт последнего блока.

## Атака

Стоит обратить внимание вот на эту строку:

```python
padded = pad(plaintext + FLAG.encode(), 16)
```

В ней происходит дополнение нашего открытого текста до нужного размера. Также наш текст добавляется в начало открытого текста. Более того, нам известна часть открытого текста, а именно `crypto{`.

А теперь время подумать. Размер блока — 16 байт. Если мы передадим 15 одинаковых символов, то в первый блок шифротекста попадёт первый символ нашего флага. Давай это проверим:

```
hex('000000000000000c') -> 65caee23eddec29b6643ec34a9c7cc05|f67f5f7fad4f00797f4e2e678d61893f|6f791fa103157b44ccfea4c321ad93f9
hex('000000000000000')  -> 65caee23eddec29b6643ec34a9c7cc05|5cd9e17683b81d63d60e0d89a2b776b3|d4f1cc43ded09a65141ac5b63b7b275e
```

Первые блоки совпали, а значит, мы убедились в том, что первый символ искомого открытого текста — `c`. Давай повторим это для `r`. Должно выйти также:

```
hex('00000000000000cr') -> 0d62c22d39b5e76d428dcdc383ef7a48|f67f5f7fad4f00797f4e2e678d61893f|6f791fa103157b44ccfea4c321ad93f9
hex('00000000000000')   -> 0d62c22d39b5e76d428dcdc383ef7a48|494e9c82d232787f01ff7fa91213e4e1|ea2d6aef1b57ad3575c8762424a510cf
```

Блоки опять совпали. Теперь нужно повторить данную операцию для каждой буквы искомого открытого текста.

## Автоматизация атаки

При передаче `16` символов на выходе мы имеем 3 блока шифротекста. Значит, флаг длиннее 16 символов. Поэтому в качестве пейлоада буду использовать 32 символа.

Логика работы будет такая же. Мы отправляем строку из 32 символов, где крайние правые — это уже найденные буквы. Нам известен префикс `crypto{`, поэтому первый вариант может быть такой:

```
000000000000000000000000crypto{*
```

Но вместо `*` мы подставляем символ-кандидат. Полученный шифротекст мы сравниваем с оригинальным шифротекстом, который можем получить, отправив вот эту строку:

```
000000000000000000000000
```

И так мы делаем для каждого символа, пока в итоге не получим флаг. Флаг заканчивается символом `}`.

Вот моё решение на `Python`:

```python
import requests


def encrypt(plaintext):
    text = plaintext.encode().hex()
    url = f'http://aes.cryptohack.org/ecb_oracle/encrypt/{text}/'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['ciphertext']

    return None


def main():
    flag = list('crypto{')
    max_flag_len = 32
    while True:
        plaintext = ''.rjust(max_flag_len - len(flag) - 1, '0')
        original = encrypt(plaintext)[:64]
        print(original)
        for c in range(0x20, 0x7f):
            plaintext = ''.join([*flag, chr(c)]).rjust(max_flag_len, '0')
            candidate = encrypt(plaintext)
            if original == candidate[:64]:
                flag.append(chr(c))
                if chr(c) == '}':
                    print(''.join(flag))
                    return 0
                break

        print(''.join(flag))
    return 1


if __name__ == '__main__':
    main()
```

Ход решения:

```
e26797a6483c5f43bf2cf28a961ffce995cdbce954bd9da88433a81d3a32d02c
crypto{p
e26797a6483c5f43bf2cf28a961ffce9f378143c5c6f2811f00f333776c83fda
crypto{p3
e26797a6483c5f43bf2cf28a961ffce92c09efdcf82b6e0061211595d64ad2c1
crypto{p3n
e26797a6483c5f43bf2cf28a961ffce9f22cd1771056f4cdf4b7e2accc4e0473
crypto{p3n6
e26797a6483c5f43bf2cf28a961ffce94ef2e6bcfba809445f3b411df5157cfd
crypto{p3n6u
e26797a6483c5f43bf2cf28a961ffce9e5d700d3ab9a7f4637f89a35537de5de
crypto{p3n6u1
e26797a6483c5f43bf2cf28a961ffce99651442ed41b3df3535305a1b7e3f3e9
crypto{p3n6u1n
e26797a6483c5f43bf2cf28a961ffce94c401926e12ebb6f9da9deab9dd6db9f
crypto{p3n6u1n5
e26797a6483c5f43bf2cf28a961ffce9f67f5f7fad4f00797f4e2e678d61893f
crypto{p3n6u1n5_
65caee23eddec29b6643ec34a9c7cc055cd9e17683b81d63d60e0d89a2b776b3
crypto{p3n6u1n5_h
0d62c22d39b5e76d428dcdc383ef7a48494e9c82d232787f01ff7fa91213e4e1
crypto{p3n6u1n5_h4
184602c9ab1658011054cc8013b38c58d7afbcd0c0dc7e7b6cf56af202ec9422
crypto{p3n6u1n5_h47
9b89e00b25fcaf65119e899d46bf3e5e5c30fd6a6247f6d542e46ed3088e421f
crypto{p3n6u1n5_h473
1e55ccefd70218ef86b7cab97443cbf355ef8fee4629552d321b15298396e4c9
crypto{p3n6u1n5_h473_
d03570da4ed6785df86997a09d82d3911f0d066726d2e552f1976e33c28760ba
crypto{p3n6u1n5_h473_3
ff67de510a753c247b31f1172437ee9ebcdc63c3c48823b1c258b1ea96cc22a3
crypto{p3n6u1n5_h473_3c
95cdbce954bd9da88433a81d3a32d02c67a6abb5cea5be9ee727f0252702cd0f
crypto{p3n6u1n5_h473_3cb
f378143c5c6f2811f00f333776c83fda32e3e96a187478a43ae626ed011c7b2c
crypto{p3n6u1n5_h473_3cb}
```
