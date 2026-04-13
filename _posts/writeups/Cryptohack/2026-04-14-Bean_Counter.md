---
title: "Cryptohack Lab. Bean Counter"
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
      url: "https://cryptohack.org/courses/symmetric/bean_counter/"
---

Я намучился с тем, чтобы режим счётчика (`CTR`) в `PyCrypto` работал так, как мне нужно, поэтому реализовал `CTR` сам поверх режима `ECB`. Мой счётчик может увеличиваться и уменьшаться, чтобы запутать криптоаналитиков! У них нет ни малейшего шанса прочитать моё изображение.

## Исходный код

```python
from Crypto.Cipher import AES


KEY = ?


class StepUpCounter(object):
    def __init__(self, step_up=False):
        self.value = os.urandom(16).hex()
        self.step = 1
        self.stup = step_up

    def increment(self):
        if self.stup:
            self.newIV = hex(int(self.value, 16) + self.step)
        else:
            self.newIV = hex(int(self.value, 16) - self.stup)
        self.value = self.newIV[2:len(self.newIV)]
        return bytes.fromhex(self.value.zfill(32))

    def __repr__(self):
        self.increment()
        return self.value


@chal.route('/bean_counter/encrypt/')
def encrypt():
    cipher = AES.new(KEY, AES.MODE_ECB)
    ctr = StepUpCounter()

    out = []
    with open("challenge_files/bean_flag.png", 'rb') as f:
        block = f.read(16)
        while block:
            keystream = cipher.encrypt(ctr.increment())
            xored = [a^b for a, b in zip(block, keystream)]
            out.append(bytes(xored).hex())
            block = f.read(16)

    return {"encrypted": ''.join(out)}
```

## Режим счётчика (CTR)

CTR превращает блочный шифр в потоковый. Вместо шифрования самого открытого текста шифруется значение счётчика, а результат `XOR`'ится с блоком данных:

```
keystream_i = AES_ECB(key, nonce || counter_i)
ciphertext_i = plaintext_i ^ keystream_i
```

Для каждого следующего блока счётчик инкрементируется, поэтому каждый блок получает уникальный `keystream`. Если счётчик не меняется — все блоки шифруются одной и той же гаммой (`keystream`), и шифр превращается в многоразовый одноразовый блокнот.

![CTR scheme](/assets/images/IMG_writeups/IMG_Cryptohack/IMG_Bean_Counter/ctr_scheme.png)

## Атака

Для понимания того, что нам делать, нужно разобрать код. А именно реализацию `StepUpCounter`:

```python
class StepUpCounter(object):
    def __init__(self, step_up=False):
        self.value = os.urandom(16).hex()
        self.step = 1
        self.stup = step_up

    def increment(self):
        if self.stup:
            self.newIV = hex(int(self.value, 16) + self.step)
        else:
            self.newIV = hex(int(self.value, 16) - self.stup)
        self.value = self.newIV[2:len(self.newIV)]
        return bytes.fromhex(self.value.zfill(32))
```

Тут генерируется `iv`. А далее для каждого последующего применения он должен изменяться. Для этого и реализован метод `increment`.

Но в нём допущена ошибка:

```python
if self.stup:
    self.newIV = hex(int(self.value, 16) + self.step)
else:
    self.newIV = hex(int(self.value, 16) - self.stup)
```

Если `self.stup == True`, то значение `iv` растёт. Но в противном случае значение не изменяется: `int(iv) - 0`. `False` равен 0. Счётчик, который не считает.

Рассмотрим шифрование:

```python
def encrypt():
    cipher = AES.new(KEY, AES.MODE_ECB)
    ctr = StepUpCounter()

    out = []
    with open("challenge_files/bean_flag.png", 'rb') as f:
        block = f.read(16)
        while block:
            keystream = cipher.encrypt(ctr.increment())
            xored = [a^b for a, b in zip(block, keystream)]
            out.append(bytes(xored).hex())
            block = f.read(16)

    return {"encrypted": ''.join(out)}
```

Для получения гаммы в нём шифруется `iv` (в режиме [ECB]({% post_url writeups/Cryptohack/2026-04-07-ECB_Oracle %})), а далее происходит `XOR` с открытым текстом. Но вот незадача. `iv` не изменяется, а значит каждый блок файла шифруется одной гаммой. Вот бы знать часть открытого текста...

А мы и знаем часть открытого текста. У форматов файлов часто есть единый формат заголовков. `PNG` — не исключение.

```bash
cu63:Downloads/ $ hexdump -C image.png | head
00000000  89 50 4e 47 0d 0a 1a 0a  00 00 00 0d 49 48 44 52  |.PNG........IHDR|
```

Попробую взять эти 16 байт заголовка, сделаю `XOR` с первым блоком шифротекста (о [свойствах XOR]({% post_url writeups/Cryptohack/2025-08-25-XOR_2_Properties %})). А далее попробую расшифровать весь файл полученной гаммой.

## Реализация

Как обычно, буду использовать `Python` для реализации:

```python
import requests

URL = 'http://aes.cryptohack.org'


def encrypt():
    url = f'{URL}/bean_counter/encrypt/'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['encrypted']

    return ''


def xor(a: bytes, b: bytes) -> bytes:
    return bytes([i ^ j for i, j in zip(a, b)])


def main():
    raw = bytes.fromhex(encrypt())
    png_header = bytes.fromhex('89504e470d0a1a0a0000000d49484452')

    keystream = xor(png_header, raw[:16])
    with open('flag.png', 'wb') as f:
        for i in range(0, len(raw), 16):
            f.write(xor(keystream, raw[i:i+16]))


if __name__ == '__main__':
    main()
```

Запущу и открою картинку:

![flag](/assets/images/IMG_writeups/IMG_Cryptohack/IMG_Bean_Counter/flag.png)

Флаг получен.
