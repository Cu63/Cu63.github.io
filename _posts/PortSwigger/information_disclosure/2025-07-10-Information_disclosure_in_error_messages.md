---
title: "Information disclosure in error messages"
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
      url: "https://portswigger.net/web-security/information-disclosure/exploiting/lab-infoleak-in-error-messages"
classes: wide
---
В лабораторной работе выводится ошибка, которая приводит к раскрытию информации. Для решения нужно определить версию используемого фреймворка.

```
https://0a9f007c036c9dd181121624006b0011.web-security-academy.net
```

## Solution

Прогуляюсь по сайту в поисках чего-нибудь интересного.

Мда...  Ничего, кроме постов, я не нашел. Попробую поковырять параметр в `GET`-запросе:

```
https://0a9f007c036c9dd181121624006b0011.web-security-academy.net/product?productId=3
```

Попробую использовать разные типы данных для этого параметра:

```
0 - error
-1 - errro
aeouaeou - error messag
```

Нашел что-то интересное:

```
Internal Server Error: java.lang.NumberFormatException: For input string: "aeouaeou"
	at java.base/java.lang.NumberFormatException.forInputString(NumberFormatException.java:67)
	at java.base/java.lang.Integer.parseInt(Integer.java:661)
	at java.base/java.lang.Integer.parseInt(Integer.java:777)
	at lab.b.d.m.c.y(Unknown Source)
	at lab.n.q.y.j.o(Unknown Source)
	at lab.n.q.p.m.q.O(Unknown Source)
	at lab.n.q.p.n.lambda$handleSubRequest$0(Unknown Source)
	at j.h.r.i.lambda$null$3(Unknown Source)
	at j.h.r.i.o(Unknown Source)
	at j.h.r.i.lambda$uncheckedFunction$4(Unknown Source)
	at java.base/java.util.Optional.map(Optional.java:260)
	at lab.n.q.p.n.L(Unknown Source)
	at lab.server.p.b.w.l(Unknown Source)
	at lab.n.q.j.P(Unknown Source)
	at lab.n.q.j.l(Unknown Source)
	at lab.server.p.b.o.c.g(Unknown Source)
	at lab.server.p.b.o.q.lambda$handle$0(Unknown Source)
	at lab.b.z.x.a.r(Unknown Source)
	at lab.server.p.b.o.q.Z(Unknown Source)
	at lab.server.p.b.h.W(Unknown Source)
	at j.h.r.i.lambda$null$3(Unknown Source)
	at j.h.r.i.o(Unknown Source)
	at j.h.r.i.lambda$uncheckedFunction$4(Unknown Source)
	at lab.server.am.W(Unknown Source)
	at lab.server.p.b.h.I(Unknown Source)
	at lab.server.p.w.y.c(Unknown Source)
	at lab.server.p.z.K(Unknown Source)
	at lab.server.p.k.K(Unknown Source)
	at lab.server.a4.R(Unknown Source)
	at lab.server.a4.I(Unknown Source)
	at lab.m.j.lambda$consume$0(Unknown Source)
	at java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1144)
	at java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:642)
	at java.base/java.lang.Thread.run(Thread.java:1583)

Apache Struts 2 2.3.31
```

Возникал ошибка при обработке строки и из-за этого выпала ошибка. А вот и ответ: `2.3.31`)

![IMG](/assets/images/PortSwigger/IMG_information_disclosure/IMG_Information_disclosure_in_error_messages/1.png){: height="200" .align-center}
