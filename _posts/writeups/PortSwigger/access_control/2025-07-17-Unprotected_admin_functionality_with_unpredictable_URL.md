---
title: "Unprotected admin functionality with unpredictable URL"
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
      url: "https://portswigger.net/web-security/learning-paths/server-side-vulnerabilities-apprentice/access-control-apprentice/access-control/lab-unprotected-admin-functionality-with-unpredictable-url#"
classes: wide
---

Для решения задания нужно удалить пользователя `carlos`.

```
https://0a0200ac0463d70e804e8f93001000f4.web-security-academy.net/
```

## Solution

Из описания лабы понятно, что к странице панели администратора добавлен набор случайных символов, поэтому перебор займет большое время. Хорошей идеей будет изучить разметку страницы и `js`-скрипты на предмет интересных адресов.

Нашел встроенный скрипт, в котором есть ссылка на админ панель `/admin-ukz310`:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_access_control/IMG_Unprotected_admin_functionality_with_unpredictable_URL/1.png){: height="200" .align-center}

```js
var isAdmin = false;
if (isAdmin) {
   var topLinksTag = document.getElementsByClassName("top-links")[0];
   var adminPanelTag = document.createElement('a');
   adminPanelTag.setAttribute('href', '/admin-ukz310');
   adminPanelTag.innerText = 'Admin panel';
   topLinksTag.append(adminPanelTag);
   var pTag = document.createElement('p');
   pTag.innerText = '|';
   topLinksTag.appendChild(pTag);
}
```

Удаляю пользователя и решаю лабу:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_access_control/IMG_Unprotected_admin_functionality_with_unpredictable_URL/2.png){: height="200" .align-center}