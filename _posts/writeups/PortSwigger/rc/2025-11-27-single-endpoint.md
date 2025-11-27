---
title: "Single-endpoint race conditions"
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
      url: "https://portswigger.net/web-security/race-conditions/lab-race-conditions-single-endpoint"
classes: wide
---	

В лабе содержится уязвимость `Race condition` в функционале смены почты. Пользователя с почтой `carlos@ginandjuice.shop` повысили до администратора, но он еще не успел зарегистрировать аккаунт. Для решение необходимо:

1. Найти уязвимость, которая позволит получить любой почтовый адрес;
2. Изменить свою почту на `carlos@ginandjuice.shop`;
3. Получить доступ к панели админа;
4. Удалить пользователя `carlos`;

Для входа в учетную запись можно использовать `wiener`:`peter`.

```
https://0aea008803f9155b9f29310d00f0009c.web-security-academy.net/
```

# Solution

Зайду в аккаунт, чтобы посмотреть внутренний функционал. В лк есть функция замены почтового адреса. Попробую изменить его, чтобы собрать запрос:

```http
POST /my-account/change-email HTTP/2
Host: 0aea008803f9155b9f29310d00f0009c.web-security-academy.net
Cookie: session=pzVsH2eECiZjdKPI8R47BJP7ssFyTjWX
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0aea008803f9155b9f29310d00f0009c.web-security-academy.net/my-account
Content-Type: application/x-www-form-urlencoded
Content-Length: 114
Origin: https://0aea008803f9155b9f29310d00f0009c.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
Connection: keep-alive

email=new_mail%40exploit-0a24006503c415409f72303601bc00ea.exploit-server.net&csrf=znxJFlNk9HvwwWClA1GNttvERFmb1mDP
```

Для смены почты необходимо подтвердить ее:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_rc/IMG_single-endpoint/1.png){: height="200" .align-center}

Интересно. Попробую отправить несколько запросов параллельно. Один из пакетов будет содержать текущую почту, второй - `carlos@ginandjuice.shop`. Разберу на примере:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_rc/IMG_single-endpoint/2.png){: height="200" .align-center}

Первый запрос содержит подконтрольный мной почтовый адрес. Если он сохраняет новый адрес в переменную, а затем отправляет запрос на подтверждение, то есть возможность изменить эту переменную с помощью второго запроса. Отправлю второй запрос параллельно с первым. Если произойдет такая же ситуация, как и на картинке выше, то значение в переменной с новой почтой изменится на `carlos@ginandjuice.shop`, но подтверждение будет отправлено на мой почтовый ящик. Что собственно и произошло:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_rc/IMG_single-endpoint/3.png){: height="200" .align-center}

Подтверждаю и проверю ЛК:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_rc/IMG_single-endpoint/4.png){: height="200" .align-center}

Зайду в админ панель и удалю пользователя:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_rc/IMG_single-endpoint/5.png){: height="200" .align-center}

Лаба решена:3

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_rc/IMG_single-endpoint/6.png){: height="200" .align-center}