---
title: "2FA simple bypass"
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
      url: "https://portswigger.net/web-security/learning-paths/server-side-vulnerabilities-apprentice/authentication-apprentice/authentication/multi-factor/lab-2fa-simple-bypass"
classes: wide
---

У нас есть наши креды `wiener:peter`, и креды жертывы `carlos:montoya`. Нужно обойти двухфакторную аутентификацию.

```
https://0a84007303189a6280c7302a00a200ac.web-security-academy.net/
```

## Solution

Залогинимся в наш аккаунт. 

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_2FA_simple_bypass/1.png){: height="200" .align-center}

Нас просят ввести четырехзначный код с почты. Сделаем это.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_2FA_simple_bypass/2.png){: height="200" .align-center}

Обратим внимание на `url`: `https://0a84007303189a6280c7302a00a200ac.web-security-academy.net/my-account`. Можно сказать, что обычный путь для входа в аккаунт у нас выглядит следующим образом: `login`-> `login2` -> `my-account`. Проверим, есть ли у нас проверка на успешное завершение шага 2. Для этого залогинимся с помощью кред жертвы и в url `login2` заменим на `my-account`.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_2FA_simple_bypass/3.png){: height="200" .align-center}
