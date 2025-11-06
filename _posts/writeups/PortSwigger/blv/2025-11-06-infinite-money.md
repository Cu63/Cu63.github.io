---
title: "Flawed enforcement of business rules"
date: 2025-11-06
tags: [web, writeup]  
categories: [PortSwigger]
tagline: ""
header:
  overlay_image: /assets/images/IMG_writeups/IMG_PortSwigger/ps_logo.webp
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "Lab PortSwigger"
      url: "https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-infinite-money"
classes: wide
---

Для прохождения лабы нужно купить `Lightweight l33t leather jacket`. 

Для входа в учетную запись даны креды `wiener`:`peter`.

```
0acc0042047fc9a08282d9e8005e00a2.web-security-academy.net
```

# Solution

Как обычно, зайду в учетную запись.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_infinite-money/1.png){: height="200" .align-center}

Как много всего. Если есть окно для ввода кода гифткарты, то стоит поискать ее на сайте. За заполнение почты я получил следующий купон:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_infinite-money/2.png){: height="200" .align-center}

Он дает скидку в 30%. Хммм... А в товарах есть подарочная карта на 10$. А что если...

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_infinite-money/3.png){: height="200" .align-center}

Хех)

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_infinite-money/4.png){: height="200" .align-center}

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_infinite-money/5.png){: height="200" .align-center}

Погнали)

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_infinite-money/6.jpg){: height="200" .align-center}

Чтобы упростить себе жизнь я закинул запрос в `Intruder`:

```http
POST /gift-card HTTP/2
Host: 0a6900e8030b88d6828456cb00c4006c.web-security-academy.net
Cookie: session=CH8BGA3L5FG4ZummVnAoq3356HphD317
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:144.0) Gecko/20100101 Firefox/144.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a6900e8030b88d6828456cb00c4006c.web-security-academy.net/my-account
Content-Type: application/x-www-form-urlencoded
Content-Length: 58
Origin: https://0a6900e8030b88d6828456cb00c4006c.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

csrf=1S3wY4RdFNWXxTJcPyYK0kwi303JMNEd&gift-card=§code§
```

Далее подставляю номера карт в `Sniper` пейлоад.

Наконец-то:
 
![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_infinite-money/7.png){: height="200" .align-center}

Done!

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_infinite-money/8.png){: height="200" .align-center}