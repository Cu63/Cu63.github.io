---
title: "CryptoHack Lab. XOR-1. Starter"
date: 2025-08-25
tags: [crypto, writeup]  
categories: [Crypto]
tagline: ""
header:
  overlay_image: /assets/images/IMG_writeups/IMG_Cryptohack/cryptohack_logo.webp
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "СryptoHack Lab"
      url: "https://cryptohack.org/courses/intro/xor0/"
---

Для решения лабы необходимо зашифровать строку `label` с ключом `13` и подставить это значение в  `crypto{new_string}`.

```
label
```

## Solution

**XOR** (Исключа́ющее «или») — булева функция, а также логическая и битовая операция, в случае двух переменных результат выполнения операции истинен тогда и только тогда, когда один из аргументов истинен, а другой — ложен.

Таблица истиности:

<table align="center">
  <tr>
    <th align="center">a</th>
    <th align="center">b</th>
    <th align="center">a XOR b</th>
  </tr>
  <tr>
    <td align="center">0</td>
    <td align="center">0</td>
    <td align="center">0</td>
  </tr>
  <tr>
    <td align="center">0</td>
    <td align="center">1</td>
    <td align="center">1</td>
  </tr>
  <tr>
    <td align="center">1</td>
    <td align="center">0</td>
    <td align="center">1</td>
  </tr>
  <tr>
    <td align="center">1</td>
    <td align="center">1</td>
    <td align="center">0</td>
  </tr>
</table>

Результат `XOR` обратим. Повторное использование операции между теми же операндами, вернет к первоначальному значению. Т.е. `123 ^ 13 ^ 13 = 123`. Благодаря этому `XOR` часто используют в криптографии. Операция легко реализуется и достаточно быстро выполняется.

Реализую алгоритм на языке `Python`:

```python
key = 'label'
flag = []

for c in key: 
    n = ord(c) ^ 13
    flag.append(chr(n))

print('crypto{'+ ''.join(flag) + '}')
```

Флаг:

```
crypto{aloha}
```
