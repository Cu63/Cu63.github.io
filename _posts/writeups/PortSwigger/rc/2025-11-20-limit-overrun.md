---
title: "Limit overrun race conditions"
date: 2025-11-20
tags: [web, writeup, race-conditions]  
categories: [PortSwigger]
tagline: ""
header:
  overlay_image: /assets/images/IMG_writeups/IMG_PortSwigger/ps_logo.webp
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "Lab PortSwigger"
      url: "https://portswigger.net/web-security/race-conditions/lab-race-conditions-limit-overrun"
classes: wide
---		

Лаба содержит уязвимость типа `Race condition`. Для решения необходимо купить `Lightweight L33t Leather Jacket`. Для входа доступны креды `winere`:`peter`.

```
https://0a30007f04cd108d814b48510086008f.web-security-academy.net/
```

# Solution

Мммм... Скидка

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_rc/IMG_limit-overrun/1.png){: height="200" .align-center}

Ладно, нужно хотя бы зайти в аккаунт) У меня даже есть 50$. Добавлю нужный товар в корзину. 

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_rc/IMG_limit-overrun/2.png){: height="200" .align-center}

Вижу поля для ввода купона. Попробую ввести что-то рандомное, чтобы получить сам запрос:

```http
POST /cart/coupon HTTP/2
Host: 0a30007f04cd108d814b48510086008f.web-security-academy.net
Cookie: session=BKim35Hz5P2eYaCmeLCD3TpoOSB09yq3
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:139.0) Gecko/20100101 Firefox/139.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a30007f04cd108d814b48510086008f.web-security-academy.net/cart
Content-Type: application/x-www-form-urlencoded
Content-Length: 51
Origin: https://0a30007f04cd108d814b48510086008f.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

csrf=OIuypoh9kWVUNuxpjxiRErXjIfio43od&coupon=random
```

Теперь введу нужный купон, но отправлю его множество раз. Для этого создам группу запросов в `Repeater`, выберу параллельную отправку и накопирую запросов:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_rc/IMG_limit-overrun/3.png){: height="200" .align-center}

Через нескольно попыток у меня получилось добиться выгодной цены)))

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_rc/IMG_limit-overrun/4.png){: height="200" .align-center}

Покупаю)

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_rc/IMG_limit-overrun/5.png){: height="200" .align-center}

~~Безумные скидки~~ Лаба решена

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_rc/IMG_limit-overrun/6.png){: height="200" .align-center}
