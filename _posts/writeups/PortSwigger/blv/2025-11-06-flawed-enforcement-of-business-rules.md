---
title: "Flawed enforcement of business rules"
date: 2025-11-06
tags: [web, writeup]  
categories: [PortSwigger]
tagline: ""
header:
  overlay_image: /assets/images/IMG_writeups/IMG_PortSwigger/ps_logo.webp
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "Lab PortSwigger"
      url: "https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-flawed-enforcement-of-business-rules"
classes: wide
---

Для прохождения лабы нужно купить `Lightweight l33t leather jacket`. 

Для входа в учетную запись даны креды `wiener`:`peter`.

```
https://0ad900e30349a15980fd3f170062005a.web-security-academy.net/
```

# Solution

Сложно было не обратить внимание на вот эту надпись.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_flawed-enforcement-of-business-rules/1.png){: height="200" .align-center}

Что-ж... пойду логиниться. Купон я применил, но денег все еще не хватает.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_flawed-enforcement-of-business-rules/2.png){: height="200" .align-center}

Использовать его дважды у меня так же не получилось(

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_flawed-enforcement-of-business-rules/3.png){: height="200" .align-center}

Нашел еще вот такой купон за подписку на новостную рассылку:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_flawed-enforcement-of-business-rules/4.png){: height="200" .align-center}

Уже лучше)

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_flawed-enforcement-of-business-rules/5.png){: height="200" .align-center}

О как... Если купоны идут не подряд, то они работают)

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_flawed-enforcement-of-business-rules/6.png){: height="200" .align-center}

Немного копипасты, и я добился цели. Беру:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_flawed-enforcement-of-business-rules/7.png){: height="200" .align-center}

Лаба решена)

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_blv/IMG_flawed-enforcement-of-business-rules/8.png){: height="200" .align-center}