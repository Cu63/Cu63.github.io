---
title: "Cryptohack Lab. Stream of Consciousness"
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
      url: "https://cryptohack.org/challenges/aes/"
---

Поговори со мной и услышь предложение из моего зашифрованного потока сознания.

## Исходный код

```python
from Crypto.Cipher import AES
from Crypto.Util import Counter
import random


KEY = ?
TEXT = ['???', '???', ..., FLAG]


@chal.route('/stream_consciousness/encrypt/')
def encrypt():
    random_line = random.choice(TEXT)

    cipher = AES.new(KEY, AES.MODE_CTR, counter=Counter.new(128))
    encrypted = cipher.encrypt(random_line.encode())

    return {"ciphertext": encrypted.hex()}
```

## Анализ

Уже знакомый нам потоковый шифр в режиме `CTR` (см. [Bean Counter]({% post_url writeups/Cryptohack/2026-04-14-Bean_Counter %})).

![CTR scheme](/assets/images/IMG_writeups/IMG_Cryptohack/IMG_Stream_of_Consciousness/ctr_scheme.png)

Ключ статичен. Для шифрования выбирается случайная строка из `TEXT`. Далее задаётся `AES` со счётчиком.

Но есть проблема. Для шифрования используется пара `(nonce, counter)`. Причём каждая пара должна использоваться один раз. А счётчик у нас обнуляется каждый раз. Это значит, что каждый текст зашифрован одной гаммой (keystream). Мы можем найти части гаммы, так как знаем часть открытого текста — `crypto{`.

## Реализация

Для начала нам нужно собрать набор шифротекстов. При этом нам не нужны повторяющиеся части. И для удобства их лучше сохранить в файл, чтобы не собирать набор каждый раз заново:

```python
import requests
import time

URL = 'http://aes.cryptohack.org'


def encrypt():
    url = f'{URL}/stream_consciousness/encrypt/'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['ciphertext']

    return ''


def xor(a: bytes, b: bytes) -> bytes:
    return bytes([i ^ j for i, j in zip(a, b)])


def crib_dragging(a: bytes, b: bytes, crib: str):
    crib = bytes(crib, 'utf-8')

    xored = list(xor(a, b))
    xored[:len(crib)] = xor(xored[:len(crib)], crib)

    xored = bytes(xored)
    return xored


def collect():
    ciphertexts = set()

    for i in range(30):
        ciphertexts.add(encrypt())
        time.sleep(1)

    with open('collection', 'w') as f:
        for c in ciphertexts:
            f.write(c + '\n')

if __name__ == '__main__':
    collect()
```

После запуска получилось собрать вот такой набор шифротекстов:

```
b7db633044ae648a883b0b6a495b587dc1ed047557188f999c5487b46d4804dfcf3733617b8a110a09f626bc
aac7267351a5318cc13b022f1d40427a8fe55168081899848900ceb4254e45c18e262261718c11420fb320f7a15fa1c1d388a5febf013933993b500f087c8d8b5345d3
bcda37736ce03497c4354e39555b5d3389eb1c2f
bfdc633a43e00adec0380a6a5c5a533396eb02695b4c82cc8a11cea9230b11d98a75242875850b445bda62f1e045e9c79c
aac7262040e02b91da2a0b3911145e7b88f151621a4a9f8589138be0600b0dde98751f617e821e1113f662fff858abdfdb88a3e5eb553323ca72471d5a7c8b854053dd9082fa64a3b61db7d5c9e0f3a81aeaab58c56caea30422bb3a2be380974e50f324ed99676da765690cacd91c6d84f8d3fac94c45
bac02f3f5ce03497c4354e3e555d4478c1f619600f18a4cb855482a52c5d0cdf8875376161881c0a15f762faf458acd2d3cceaeaa5457b3ed133505c5c668796425092cfc7ae45e6a24fb6c4c9f2eab65feebb0b9c29ecbf1e2286723dab96894d1efa6f
a9c7222705a16390c92a1a331d4747768dee517513519ecc981587ae390b0dd08b7b
b2c0353609e0338cc73b0f28514d1533b5ea14785b5c8282cf00ceab23441291873a2161769f1a0409ea62fbf50ba7c09188a2e4bc01333fd43b4815497a8b8a4018d39382fa64a3ef7bb3d587f4fae45beca60b9d24a5ba1470977476
aac7313640e02191d12a4e38485a447a8fe55d210b548c95811a89e02c5f45d98027252461c15f361ee13bfdfb43af92
bfc127736ce03096c935026a5453447c93e751680f16
aeca313b44b030dec03c4e225c470a7e88f102641f1899848d549ab22c420b918e3b32617b9e5f071af029b2e352eeddd2dfe4ab9c40353e993f4b0e4d2e8a914a5f91d4c3fa65a9a11b
b78f303b44ac2fdec4361d2f1d515c7693fb056912568acc891a8ae023441191883022617a84124519f221f9af
b7882e7350ae2b9fd82917661d7d0a7784f114730d5dcd859c58ceb4254e45d78e203a35359e5f0812fd27bea149bbc79de1ede6eb543522d8225405086f8e88074295d882fd6dabaa16e5d88cedefe457e7ec
9ddd3a2351af38959b205b7d4f071e7ebef042744e0bb2dddd2b88f47a1f09cc
b0c06f736ce72f92883e016a545a0a678ea2356e175494cc891a8ae0394e09ddcf3d3333329e0b171afa25faf50ba1c6c9
```

Что-то из этого должно начинаться на `crypto{`. Наверное... Если нет, то нужно будет собрать больше шифротекстов. Как же нам найти нужное начало keystream? Можно брутфорсить для каждого шифротекста. Но это долго и сложно. Есть способ лучше — `crib dragging`.

## Crib dragging

Мы знаем, что гамма (keystream) у нас одна. Значит, если мы возьмём 2 шифротекста `C_a` и `C_b`, где каждый из них — это `KS ^ P_*`, и произведём `XOR`, то получим: `P_a ^ KS ^ KS ^ P_b = P_a ^ P_b` (вспоминаем [свойства XOR]({% post_url writeups/Cryptohack/2025-08-25-XOR_2_Properties %})). То есть результат XOR двух открытых текстов, гамма сократилась.

Мы знаем часть открытого текста: `crypto{`. Попробуем произвести `XOR` с результатом `P_a ^ P_b`. В той паре, где мы получим осмысленный текст, и находится наш флаг.

Давай это реализуем:

```python
def xor(a: bytes, b: bytes) -> bytes:
    return bytes([i ^ j for i, j in zip(a, b)])


def crib_dragging(a: bytes, b: bytes, crib: str):
    crib = bytes(crib, 'utf-8')

    xored = list(xor(a, b))
    xored[:len(crib)] = xor(xored[:len(crib)], crib)

    xored = bytes(xored)
    return xored


def main():
    ciphertexts = []
    with open('collection', 'r') as f:
        for c in f:
            ciphertexts.append(c[:-1])

    for i in range(len(ciphertexts)):
        a = bytes.fromhex(ciphertexts[i])
        for j in range(1, len(ciphertexts)):
            b = bytes.fromhex(ciphertexts[j])
            if i == j:
                continue

            print(i, j)
            cribs = [
                'crypto{',
            ]
            for crib in cribs:
                print(crib_dragging(a, b, crib))
    return
```

Запущу. Покажу только часть вывода:

```bash
...
13 1
b'The ter\x19Z\x1bYRRG\\\x041\x15\x13\x1cF\x13+YT+F@_QL\r'
13 2
b'But I w\x02_\x15\x15D\x1a\\CM7\x1b^['
13 3
b'As if IK[\x18Q\x17\x13]MM(\x1b@\x1d\x15G0\x11W:F]Y\x14\x18\x15'
13 4
b'These h\x04A\nPD^\x13@\x056\x01\x13\x16TA-XT8\x03\x14\x1a\x14\x04\x12'
13 5
b'Dolly w\x02_\x15\x15C\x1aZZ\x06\x7f\x06[\x14A\x13\x16\x16X\x7f\nQVB\x05\x13'
13 6
b'What a \x05R\nANR@Y\x083\x1e\x13\x01]Z,\x11E>\x0fZC\x14\x04\x1c'
13 7
b'Love, p\x19\\\x1bTU\x1eJ\x0bM\x0b\x1aV\x0c\x15W0_\x12+F_Y[\x1b]'
13 8
b'Three b\x04J\n\x15E\x07]Z\x041\x15\x1fUE_>H\\1\x01\x14V@L\x15'
13 9
b'And I s\x03R\x15Y\x17\x1bTZ\x02-\x17\x13\x1cA\x1d'
13 10
b'PerhapsK[\x1c\x15_\x13@\x14\x006\x01@\x10Q\x13+YP\x7f\x12FV]\x02]'
13 11
b'I shallK_\x16FRRVB\x08-\x0bG\x1d\\]8\x11T1\x02\x14Y[\x18]'
13 12
b"I'm unh\nC\tL\x1bRz\x14\t:\x01V\x07CV\x7fXAsF@_QL\x1b"
13 14
b"No, I'l\x07\x13\x1eZ\x17\x1b]\x14\x190Rw\x1aY_&\x11T1\x02\x14CQ\x00\x11"
...
```

Можно увидеть, что все пары с 13 содержат текст, похожий на английский. Значит наш флаг находится в 13-й строке. Теперь через `XOR` получим часть гаммы и будем расширять её дальше:

```python
def main():
    ciphertexts = []
    with open('collection', 'r') as f:
        for c in f:
            ciphertexts.append(c[:-1])

    i = 13
    keystream = xor(b'crypto{', bytes.fromhex(ciphertexts[i]))
    print('cribs = [')
    for i in range(len(ciphertexts)):
        a = bytes.fromhex(ciphertexts[i])
        xored = xor(a, keystream)
        print(7 * ' ', xored, f', # {i}')
    print('    ]')
```

Запущу:

```bash
cu63:Stream of Consciousness/ $ python solver.py
cribs = [
        b"It can'" , # 0
        b'The ter' , # 1
        b'But I w' , # 2
        b'As if I' , # 3
        b'These h' , # 4
        b'Dolly w' , # 5
        b'What a ' , # 6
        b'Love, p' , # 7
        b'Three b' , # 8
        b'And I s' , # 9
        b'Perhaps' , # 10
        b'I shall' , # 11
        b"I'm unh" , # 12
        b'crypto{' , # 13
        b"No, I'l" , # 14
    ]
```

У нас есть начала английских предложений. Теперь мы можем предполагать, как продолжается строка, подставлять предположение как новый crib, получать от него больше байт гаммы и проверять результат. Если все строки выглядят осмысленно — сохраняем и делаем следующий шаг.

## Итеративное расширение keystream

Логика такая: берём строку с очевидным продолжением, подставляем — получаем больше байт keystream — применяем ко всем строкам — ищем следующее продолжение.

Покажу пару итераций для наглядности. 12-я строка похожа на `I'm unhappy`. Подставлю:

```python
cribs = [
    b"It can't be" , # 0
    b'The terribl' , # 1
    b'But I will ' , # 2
    b'As if I had' , # 3
    b'These horse' , # 4
    b'Dolly will ' , # 5
    b'What a nast' , # 6
    b'Love, proba' , # 7
    b'Three boys ' , # 8
    b'And I shall' , # 9
    b'Perhaps he ' , # 10
    b'I shall los' , # 11
    b"I'm unhappy" , # 12
    b'crypto{k3y5' , # 13
    b"No, I'll go" , # 14
]
```

Похоже на нормальный текст. Продолжим. 7-я строка похожа на `Love, probably`. Подставлю:

```python
cribs = [
    b"It can't be to" , # 0
    b'The terrible t' , # 1
    b'But I will sho' , # 2
    b'As if I had an' , # 3
    b'These horses, ' , # 4
    b'Dolly will thi' , # 5
    b'What a nasty s' , # 6
    b'Love, probably' , # 7
    b'Three boys run' , # 8
    b'And I shall ig' , # 9
    b'Perhaps he has' , # 10
    b'I shall lose e' , # 11
    b"I'm unhappy, I" , # 12
    b'crypto{k3y57r3' , # 13
    b"No, I'll go in" , # 14
]
```

Похоже на правду. И далее таким способом мы перебираем разные слова, чтобы получить полный keystream. Итоговый список:

```python
cribs = [
    b"It can't be torn out, but it can " , # 0
    b'The terrible thing is that the pa' , # 1
    b'But I will show him.' , # 2
    b'As if I had any wish to be in the' , # 3
    b'These horses, this carriage - how' , # 4
    b"Dolly will think that I'm leaving" , # 5
    b'What a nasty smell this paint had' , # 6
    b"Love, probably? They don't know h" , # 7
    b'Three boys running, playing at ho' , # 8
    b'And I shall ignore it.' , # 9
    b'Perhaps he has missed the train a' , # 10
    b'I shall lose everything and not g' , # 11
    b"I'm unhappy, I deserve it, the fa" , # 12
    b'crypto{k3y57r34m_r3u53_15_f474l}' , # 13
    b"No, I'll go in to Dolly and tell " , # 14
]
```

>Тексты оказались цитатами из «Анны Карениной» Толстого.

Флаг:

```
crypto{k3y57r34m_r3u53_15_f474l}
```
