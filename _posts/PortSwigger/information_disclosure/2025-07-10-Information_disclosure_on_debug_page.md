---
title: "Information disclosure on debug page"
date: 2025-07-10
tags: [web, writeup]  
categories: [PortSwigger]
tagline: ""
header:
  overlay_image: /assets/images/ps_logo.webp
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "Lab PortSwigger"
      url: "https://portswigger.net/web-security/information-disclosure/exploiting/lab-infoleak-on-debug-page"
classes: wide
---

Для прохождения лабораторной работы необходимо найти значение переменной окружения `SECRET_KEY` из логов сайта.

```
https://0a31001404865bf080223a07000f001f.web-security-academy.net/
```

## Solution

Осмотрю сайт. Выглядит он пустовато. Попробую поискать интересные страницы с помощью `ffuf`:

```bash
cu63:~/ $ ffuf -u https://0a31001404865bf080223a07000f001f.web-security-academy.net/FUZZ -w ~/wordlists/common.txt

        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : https://0a31001404865bf080223a07000f001f.web-security-academy.net/FUZZ
 :: Wordlist         : FUZZ: /Users/cu63/wordlists/common.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

analytics               [Status: 200, Size: 0, Words: 1, Lines: 1, Duration: 67ms]
cgi-bin                 [Status: 200, Size: 410, Words: 126, Lines: 17, Duration: 74ms]
cgi-bin/                [Status: 200, Size: 410, Words: 126, Lines: 17, Duration: 72ms]
favicon.ico             [Status: 200, Size: 15406, Words: 11, Lines: 1, Duration: 61ms]
filter                  [Status: 200, Size: 10960, Words: 5122, Lines: 201, Duration: 72ms]
:: Progress: [4686/4686] :: Job [1/1] :: 46 req/sec :: Duration: [0:01:27] :: Errors: 0 ::
```

Интересненько, посмотрю, что там есть.

`cgi-bin`:

![IMG](/assets/images/PortSwigger/IMG_information_disclosure/IMG_Information_disclosure_on_debug_page/1.png){: height="200" .align-center}

Любопытно, открою:

![IMG](/assets/images/PortSwigger/IMG_information_disclosure/IMG_Information_disclosure_on_debug_page/2.png){: height="200" .align-center}

Похоже на информацию о сервере. Поищу нужный мне ключ `SECRET_KEY`:

![IMG](/assets/images/PortSwigger/IMG_information_disclosure/IMG_Information_disclosure_on_debug_page/3.png){: height="200" .align-center}

А вот и он — `SECRET_KEY`:`oyo444i8qp9e3zew2darg7zuyxrsfh25`.

![IMG](/assets/images/PortSwigger/IMG_information_disclosure/IMG_Information_disclosure_on_debug_page/4.png){: height="200" .align-center}
