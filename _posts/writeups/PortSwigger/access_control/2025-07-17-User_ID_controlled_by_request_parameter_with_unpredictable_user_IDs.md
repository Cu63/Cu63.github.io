---
title: "User ID controlled by request parameter, with unpredictable user IDs"
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
      url: "https://portswigger.net/web-security/learning-paths/server-side-vulnerabilities-apprentice/access-control-apprentice/access-control/lab-user-id-controlled-by-request-parameter-with-unpredictable-user-ids#"
classes: wide
---

Для решения лабы нужно получить доступ к `GUID` пользователя `carlos` и украсть его `API`-ключ. У нас есть креды для аккаунта `wiener:peter`.

```
https://0a9400d7046948b081d190470089000a.web-security-academy.net/
```

## Solution

Давайте залогинимся в наш профиль.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_access_control/IMG_User_ID_controlled_by_request_parameter_with_unpredictable_user_IDs/1.png){: height="200" .align-center}

Так же в `url` мы можем увидеть `id` нашего аккаунта: `https://0a9400d7046948b081d190470089000a.web-security-academy.net/my-account?id=645d6706-c01e-4080-bb1e-3e28010f2947`.

На главной странице мы видим посты пользователей. Давайте откроем любой из них.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_access_control/IMG_User_ID_controlled_by_request_parameter_with_unpredictable_user_IDs/2.png){: height="200" .align-center}

Тут есть ссылка на наш профиль. Перейдем по ней.

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_access_control/IMG_User_ID_controlled_by_request_parameter_with_unpredictable_user_IDs/3.png){: height="200" .align-center}

Тут мы видим посты пользователя. Обратим внимание на `url`: `https://0a9400d7046948b081d190470089000a.web-security-academy.net/blogs?userId=645d6706-c01e-4080-bb1e-3e28010f2947`. В нем есть параметр `userID`, который совпадает со значением `id` со страницы нашего акаунта. Давайте попробуем найти это значения для другого пользователя. Для этого:

1. Найдем пост другого пользователя:

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_access_control/IMG_User_ID_controlled_by_request_parameter_with_unpredictable_user_IDs/4.png){: height="200" .align-center}

2. Перейдем в его профиль и возьмем значение `userId` из `url`: `https://0a9400d7046948b081d190470089000a.web-security-academy.net/blogs?userId=73952a23-74f9-46e5-90f6-55e412599380`;

3. Подставим полученное значение в качестве значения `id`: `https://0a9400d7046948b081d190470089000a.web-security-academy.net/my-account?id=73952a23-74f9-46e5-90f6-55e412599380`;

![IMG](/assets/images/IMG_writeups/IMG_PortSwigger/IMG_access_control/IMG_User_ID_controlled_by_request_parameter_with_unpredictable_user_IDs/5.png){: height="200" .align-center}

Мы получили доступ к `API`-ключу пользователя `carlos`.