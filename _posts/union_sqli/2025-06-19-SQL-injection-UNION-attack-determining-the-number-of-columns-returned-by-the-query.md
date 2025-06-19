---
title: "SQL injection UNION attack, determining the number of columns returned by the query"
date: 2025-06-19
tags: [sql, writeup]
---
**Source:** [Coffee Cube](https://t.me/coffee_cube)  
**Lab:** [PortSwigger](https://portswigger.net/web-security/learning-paths/sql-injection/sql-injection-determining-the-number-of-columns-required/sql-injection/union-attacks/lab-determine-number-of-columns)

## Scope

```
https://0a1600ed036880cd8c118c7100de00ed.web-security-academy.net/
```

В данной лабе есть уязвимый к **SQL injection** фильтр категории. Для решения необходимо выполнить атаку, которая должна вывести дополнительную строку с `NULL` значениями.

## Solution

Первым делом нужно найти фильтр категорий, который описан в задании. Это сделать достаточно легко, так как он находится на главной странице, и значения для фильтрации передаются через параметры `GET`-запроса.

![IMG](/assets/images/IMG_SQL-injection-UNION-attack-determining-the-number-of-columns-returned-by-the-query/1.png){: height="200" .align-center}

```
https://0a1600ed036880cd8c118c7100de00ed.web-security-academy.net/filter?category=Accessories
```


Теперь нужно найти символ обрамления для параметра. Предположим, что запрос выглядит следующим образом:

```sql
SELECT name, price FROM table WHERE category = 'Accessories'
```

Предположу, что для обрамления используется символ кавычки `'`, тогда я не должен получить никаких значений при следующем запросе:

```
https://0a1600ed036880cd8c118c7100de00ed.web-security-academy.net/filter?category=Accessories' and false-- -
```

Собственно это и произошло:

![IMG](/assets/images/IMG_SQL-injection-UNION-attack-determining-the-number-of-columns-returned-by-the-query/2.png){: height="200" .align-center}

Запрос к БД выглядел следующим образом:

```sql
SELECT name, price FROM table WHERE category = 'Accessories' and false -- -'
```

<details>
  <summary>Подробнее</summary>
  
  `-- -` - это комментарий в SQL, с помощью него я убрал всю последующую часть запроса. В данном случае это лишняя кавычка, которая ломала бы запрос.
</details>


Обрамления я нашел - это одинарные кавычки `'`. Теперь нужно найти количество элементов в запросе. Это можно сделать с помощью `ORDER BY`. Этот оператор используется для сортировки результата по номеру стоблца в БД. Если нужного столбца нет, то мы получим ошибку. Подставлю значение 100.

```
https://0a1600ed036880cd8c118c7100de00ed.web-security-academy.net/filter?category=Accessories%27%20ORDER%20BY%20100--%20-
```

Ошибка)

![IMG](/assets/images/IMG_SQL-injection-UNION-attack-determining-the-number-of-columns-returned-by-the-query/3.png){: height="200" .align-center}

Далее можно использовать бинарный поиск для нахождения нужного значения. То есть передать 50. В случае ошибки взять 25. Если же успех, то 75. И так далее. Можно так же ткнуть на обум. На сайте мы видим 3 колонки. Звучит логично, что они все заполняются из БД. Подставлю значение 4 (для сокращения буду писать только часть пейлоада).

```
Accessories' ORDER BY 4-- -
```

![IMG](/assets/images/IMG_SQL-injection-UNION-attack-determining-the-number-of-columns-returned-by-the-query/4.png){: height="200" .align-center}

Подставлю 3:

```
Accessories' ORDER BY 4-- -
```

![IMG](/assets/images/IMG_SQL-injection-UNION-attack-determining-the-number-of-columns-returned-by-the-query/5.png){: height="200" .align-center}

Супер. ~~Сбер теперь купер~~.

Я нашел количество столбцов. Попробую добавить `UNION` к своему пейлоаду, чтобы получить данные из БД.
  
```
Accessories' UNION SELECT 1,2,3-- -
```

Ошибка(

![IMG](/assets/images/IMG_SQL-injection-UNION-attack-determining-the-number-of-columns-returned-by-the-query/6.png){: height="200" .align-center}

Оберну значения в кавычки.

```
Accessories' and false UNION SELECT 1,2,3-- -
```

![IMG](/assets/images/IMG_SQL-injection-UNION-attack-determining-the-number-of-columns-returned-by-the-query/7.png){: height="200" .align-center}
<br>

Я вывел переданные значения в таблицу на сайте, что и требовалось для прохождения лабы.
