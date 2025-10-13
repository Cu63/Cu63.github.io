---
title: "Cryptohack Lab. Extended GCD"
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
      url: "https://cryptohack.org/courses/modular/egcd/"
---

{% raw %} 

Для решения лабы необходимо найти такие `u` и `v`, при данных `p` = `26513` и `q` = `32321`, что выполняется равенство:

```
p * u + q * v = gcd(p, q)
```

В качестве ответа используется наименьший из `u` и `v`.

## Sulution

[Алгоритм Евклида](https://cu63.github.io/crypto/Greatest_Common_Divisor/) мы уже рассматривали. Пришло время расширенного алгоритма Евклида.

### Расширенный алгоритм Евклида

Аналогично алгоритму Евклида находит `НОД` двух чисел `p` и `q`, но в дополнение находит коэффициенты `x` и `y` для [уравнения Безу](https://ru.wikipedia.org/wiki/%D0%A1%D0%BE%D0%BE%D1%82%D0%BD%D0%BE%D1%88%D0%B5%D0%BD%D0%B8%D0%B5_%D0%91%D0%B5%D0%B7%D1%83):

```
p * u + q * v = gcd(p, q)
```

Напишу его реализацию на `python`:

```python
def extended_gcd(p: int, q: int):
    if q == 0:
        return p, 1, 0
    gcd, x1, y1 = extended_gcd(q, p % q)
    return gcd, y1, x1 - (p // q) * y1


p = 26513
q = 32321
g, x, y = extended_gcd(p, q)
print(f"gcd = {g}, x = {x}, y = {y}")
```

Запущу код:

```
gcd = 1, x = 10245, y = -8404
```

Значит ответом будет `-8404`.

{% endraw %}