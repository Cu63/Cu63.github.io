---
title: "Inconsistent security controls"
date: 2025-10-16
tags: [web, writeup]  
categories: [PortSwigger]
tagline: ""
header:
  overlay_image: /assets/images/IMG_writeups/IMG_PortSwigger/ps_logo.webp
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "Lab PortSwigger"
      url: "https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-inconsistent-security-controls"
classes: wide
---

В лабораторной работе предоставляются права админа всем сотрудникам компании. Для прохождения нужно удалить пользователя `carlos`.

```
https://0a77009b036ffd1f80d85dcf00ef0016.web-security-academy.net/
```

# Solution

Аккаунта у нас нет, так что нужно регистрировать. 

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_inconsistent-security-controls/1.png){: height="200" .align-center}

А вот и компания с админ правами. ~~Тряситесь в страхе, пока я иду за вами~~. 

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_inconsistent-security-controls/2.png){: height="200" .align-center}

Можно сменить почту. Попробую сделать это:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_inconsistent-security-controls/3.png){: height="200" .align-center}

Замечательно. Даже на почту не отправили подтверждение. Попробую поменять почту на новую, с доменом `@dontwannycry.com`. Внедрение прошло успешно:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_inconsistent-security-controls/4.png){: height="200" .align-center}

Удалю `carlos`:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_inconsistent-security-controls/5.png){: height="200" .align-center}