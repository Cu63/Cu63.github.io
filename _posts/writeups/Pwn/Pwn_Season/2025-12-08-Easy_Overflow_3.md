---
title: "Easy Overflow 3"
date: 2025-12-08
tags: [pwn, writeup]  
categories: [Pwn]
tagline: ""
header:
  overlay_image: /assets/images/IMG_writeups/IMG_Pwn/IMG_Pwn_Season/Pwn_Season_logo.jpg
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "Pwn Season"
      url: "https://pwn.spbctf.ru/tasks/pwn1_mc6"
classes: half
layout: single
toc: true
toc_sticky: true
toc_label: "Оглавление"
---

Переполните, чтобы получить флаг.

- [ELF](https://pwn.spbctf.ru/files/overflow/mc6_censored)

```
nc 109.233.56.90 11586
```

# Solution

Нужно найти переполнение буфера, чтобы получить флаг. Значит реверсим.

## Анализ `main`

А вот и код:

```c
  int32_t main()
  {
      int32_t result = 0;
      int32_t num = 666;
      int64_t rax;
      (uint8_t)rax = 0;
      int32_t var_3c = printf("Give me your input: ");
      char buf[0x28];
      char* var_48 = gets(&buf);
      char* rax_2;
      (uint8_t)rax_2 = 0;
      printf("The check number is %d\n", (uint64_t)num);
      int64_t rax_3;
      
      if (num != 13371337)
      {
          (uint8_t)rax_3 = 0;
          printf("Bad luck!\n");
      }
      else
      {
          (uint8_t)rax_3 = 0;
          printf("Flag is: spbctf{*************************}\n");
      }
      return result;
  }
```

Ввод совершается через не безопасный `gets`. Для прохождения нужно заменять `num` на `13371337`. 

## Подбор пейлоада

Как всегда, нам нужен стек:

![IMG](/assets/images/IMG_writeups/IMG_Pwn/IMG_Pwn_Season/IMG_Easy_Overflow_3/1.png){: height="200" .align-center}

Число 32-х битное. Значит нужно будет 4 символа, чтобы его переписать. В бинже я представил строку в виде символов, получилось вот это чудо: `\xc9\x07\xcc`.

Значит пейлоад будет 40 рандомных символов и вот это:

```
qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq\xC9\x07\xCC
```

Другая проблема - это ввод неотображаемых символов. Для этого использую перенаправление потока вывода и `printf`:

![IMG](/assets/images/IMG_writeups/IMG_Pwn/IMG_Pwn_Season/IMG_Easy_Overflow_3/2.png){: height="200" .align-center}

Теперь нужно получить флаг. 

![IMG](/assets/images/IMG_writeups/IMG_Pwn/IMG_Pwn_Season/IMG_Easy_Overflow_3/3.png){: height="200" .align-center}

Для того, чтобы все получилось, я добавил `\n` в конец пейлоада.