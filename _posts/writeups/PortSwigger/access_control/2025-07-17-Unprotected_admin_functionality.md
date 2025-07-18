---
title: "Unprotected admin functionality"
date: 2025-07-17
tags: [web, writeup]  
categories: [PortSwigger]
tagline: ""
header:
  overlay_image: /assets/images/IMG_writeups/IMG_PortSwigger/ps_logo.webp
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "Lab PortSwigger"
      url: "https://portswigger.net/web-security/learning-paths/server-side-vulnerabilities-apprentice/access-control-apprentice/access-control/lab-unprotected-admin-functionality"
classes: wide
---

Для решения лабы нужно зайти в админ-панель и удалить пользователя `carlos`.

## Solution

На сайте есть страница авторизации:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_access_control/IMG_Unprotected_admin_functionality/1.png){: height="200" .align-center}

Можно поискать, есть ли у нас доступ к админ-панели. Попробуем зайти на страницу `admin`.

Взгляну на `robots.txt`:

```html
User-agent: *
Disallow: /administrator-panel
```

Нашли адрес админ панели. Попробуем зайти на нее:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_access_control/IMG_Unprotected_admin_functionality/2.png){: height="200" .align-center}

Для решения лабы удалим пользователя `carlos` (за кадром).