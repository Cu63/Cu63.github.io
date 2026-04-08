---
title: "Cryptohack Lab. ECB CBC WTF"
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
      url: "https://cryptohack.org/courses/symmetric/ecbcbcwtf/"
---

Здесь ты можешь **шифровать в режиме CBC**, но **расшифровывать только в режиме ECB**. Казалось бы, это не должно быть уязвимостью, ведь это разные режимы работы… правда?

## Исходный код

```python
from Crypto.Cipher import AES


KEY = ?
FLAG = ?


@chal.route('/ecbcbcwtf/decrypt/<ciphertext>/')
def decrypt(ciphertext):
    ciphertext = bytes.fromhex(ciphertext)

    cipher = AES.new(KEY, AES.MODE_ECB)
    try:
        decrypted = cipher.decrypt(ciphertext)
    except ValueError as e:
        return {"error": str(e)}

    return {"plaintext": decrypted.hex()}


@chal.route('/ecbcbcwtf/encrypt_flag/')
def encrypt_flag():
    iv = os.urandom(16)

    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(FLAG.encode())
    ciphertext = iv.hex() + encrypted.hex()

    return {"ciphertext": ciphertext}
```

Зашифрованный флаг:

```
{"ciphertext":"45a0b258713724604831c4011bab47c6d394938e19fa93b5cb54544cce8ba6b361ed3cb7e39518a514ba86f591247f9e"}
```

## Режим сцепления блоков шифротекста (CBC)

Сцепление оснащает блочный шифротекст механизмом обратной связи: шифрование последующего блока зависит от значения предыдущего. К предыдущему зашифрованному блоку применяется `XOR` с текущим блоком, а затем — алгоритм шифрования. Выглядит это так:

![CBC scheme](/assets/images/IMG_writeups/IMG_Cryptohack/IMG_ECB_CBC_WTF/cbc_scheme.png)

Для первого блока используется вектор инициализации. Он задаётся вручную или генерируется.

Для дешифровки алгоритм применяется в обратном порядке. Блоки мы берём от конца к началу. Каждый блок шифротекста расшифровывается с помощью ключа, затем происходит `XOR` с предшествующим блоком.

## Решение

Режим работы `ECB` позволяет нам дешифровывать блоки независимо. Значит, нужно взять последний блок, дешифровать его, проксорить с предыдущим. Вот мы и получили открытый текст для этого блока.

Буду писать код на `Python`:

```python
import requests


def encrypt():
    url = 'http://aes.cryptohack.org/ecbcbcwtf/encrypt_flag/'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['ciphertext']

    return None



def decrypt(ciphertext):
    url = f'http://aes.cryptohack.org/ecbcbcwtf/decrypt/{ciphertext}/'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['plaintext']

    return None


def main():
    flag = []

    ciphertext = encrypt()
    blocks = [ciphertext[i:i+32] for i in range(0, len(ciphertext), 32)]
    for i in range(len(blocks)-1, 0, -1):
        xored = bytes.fromhex(decrypt(blocks[i]))
        prev_block = bytes.fromhex(blocks[i-1])
        plaintext = bytes(a ^ b for a, b in zip(xored, prev_block)).decode()
        flag.append(''.join(plaintext))

    print(''.join(flag[::-1]))
    return 1


if __name__ == '__main__':
    main()

```

`iv` для первого блока мне не известен. Угадать его будет сложно. Поэтому попробую посмотреть ту часть текста, что я точно могу расшифровать.

```
crypto{3cb_5uck5_4v01d_17_!!!!!}
```

Это и оказался флаг.
