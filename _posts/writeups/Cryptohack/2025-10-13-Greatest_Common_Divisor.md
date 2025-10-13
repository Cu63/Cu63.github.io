---
title: "Cryptohack Lab. Greatest Common Divisor"
date: 2025-10-13
tags: [crypto, writeup]  
categories: [Crypto]
tagline: ""
header:
  overlay_image: /assets/images/IMG_writeups/IMG_Cryptohack/cryptohack_logo.webp
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "Сryptohack Lab"
      url: "https://cryptohack.org/courses/modular/gcd/"
---

Для решения нужно вычислить `НОД` чисел `66528` и `52920`.

## Sulution

Подобная задача часто встречается в криптографии, поэтому глупо будет про нее не рассказать. Одним из способов вычисления `НОД` (наибольшего общего делителя) является алгоритм Евклида.

### Алгоритм Евклида 

Алгоритм для поиска наибольшего общего делителя. 

Если у нас есть два числа `a` и `b`, то:

```
НОД(a, b) = НОД(b, a mod b)
```

где `a mod b` — остаток от деления `a` на `b`.  

Это работает, потому что общий делитель двух чисел также делит их разность и остаток от деления. Реализуем решение на `Python`:

```python
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


if __name__ == '__main__':
    print(gcd(66528, 52920))
```

Ответ: `1512`