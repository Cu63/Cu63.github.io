---
title: "CryptoHack Lab. XOR-2. Properties"
date: 2025-07-19
tags: [crypto, writeup]  
categories: [Crypto]
tagline: ""
header:
  overlay_image: /assets/images/IMG_writeups/IMG_Cryptohack/cryptohack_logo.webp
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "СryptoHack Lab"
      url: "https://cryptohack.org/courses/intro/xor1/"
---

В данной лабе мы расcмотрим особенности работы с `XOR`. Для решения нужно получить значение `FLAG`.

```
KEY1 = a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313  
KEY2 ^ KEY1 = 37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e  
KEY2 ^ KEY3 = c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1  
FLAG ^ KEY1 ^ KEY3 ^ KEY2 = 04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf
```

## Solution

С `XOR` мы работали. Теперь же разберем его свойства:

1. **Коммутативность**: `A ^ B = B ^ A`  
2. **Ассоциативность**: `A ^ (B ^ C) = (A ^ B) ^ C`
3. **Идентичность**: `A ^ 0 = A`
4. **Обратимость (сам себе обратный)**: `A ^ A = 0`

Перейдем к решению задания:

1. `KEY1 = a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313`
2. `KEY2 ^ KEY1 = 37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e`
3. `KEY2 ^ KEY3 = c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1`
4. `FLAG ^ KEY1 ^ KEY3 ^ KEY2 = 04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf`

Для решения нам нужен `FLAG`. Его мы можем получить из `FLAG ^ KEY1 ^ KEY3 ^ KEY2` благодаря свойству обратимости.

Давайте подумаем. `KEY1 ^ KEY1 = 0`, в свою очередь `FLAG ^ 0 = FLAG`. Возьму выражения `4 ^ 1 ^ 3`. Мы получим следующее выражение:

```
FLAG ^ KEY1 ^ KEY3 ^ KEY2 ^ KEY1 ^ KEY2 ^ KEY3
```

Упростим, благодаря свойству обратимости:

```
FLAG ^ KEY1 ^ KEY1 ^ KEY2 ^ KEY2 ^ KEY3 ^ KEY3 = FLAG ^ (KEY1 ^ KEY1) ^ (KEY2 ^ KEY2) ^ (KEY3 ^ KEY3) = FLAG ^ 0 ^ 0 ^ 0 = FLAG
```

А вот и ответ. Напишу код на `Python`:

```python
a = 0x04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf
b = 0xa6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313
c = 0xc1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1

flag = hex(a ^ b ^ c)[2:]

print(bytes.fromhex(flag).decode())
```

Флаг:

```
crypto{x0r_i5_ass0c1at1v3}
```
