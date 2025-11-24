---
title: "Want the flag"
date: 2025-11-24
tags: [pwn, writeup]  
categories: [Reverse]
tagline: ""
header:
  overlay_image: /assets/images/IMG_writeups/IMG_Reverse/IMG_Pwn_Season/Pwn_Season_logo.jpg
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "Pwn Season"
      url: "https://pwn.spbctf.ru/tasks/pwn1_mc2_2"
classes: wide
---

Убедите бинарник, что ХОТИТЕ флаг.

- [ELF](https://pwn.spbctf.ru/files/overflow/mc2)

# Solution

Бинарь тот же. Ладно. Теперь нужно уговорить его выдать нам флаг.

```c
00400590    int32_t main(int32_t argc, char** argv, char** envp)

00400598        int32_t var_c = 0
0040059f        int64_t rax
0040059f        rax.b = 0
004005a1        obfuscated_prepare_memory()
004005b0        void* rax_1
004005b0        rax_1.b = 0
004005c1        int32_t var_10 = printf(format: "Hope you got what you wanted!\n")
004005c4        int32_t rax_2
004005c4        rax_2.b = 0
004005d5        int32_t var_14 = printf(format: "Checking... ")
004005e0        int32_t rax_4
004005e0        
004005e0        if (strcmp("dont_give_flag", "I_WANT_THE_FLAG!") == 0)
00400606            rax_4.b = 0
0040060d            int32_t var_18_1 = printf(format: "okok, giving you the flag..\n")
00400610            int32_t rax_5
00400610            rax_5.b = 0
00400612            obfuscated_give_flag()
004005e0        else
004005f0            rax_4.b = 0
004005f2            printf(format: "looks like you don't want flag\n")
0040061f        return 0
```

Нам мешает проверка `strcmp`. Запатчим?

## Патчинг

Использую для этого встроенные возможности `Binary Ninja`:

![IMG](/assets/images/IMG_writeups/IMG_Reverse/IMG_Pwn_Season/IMG_want-the-flag/1.png){: height="200" .align-center}

На выходе я имею следующую функцию:

![IMG](/assets/images/IMG_writeups/IMG_Reverse/IMG_Pwn_Season/IMG_want-the-flag/2.png){: height="200" .align-center}

Запускаю.

![IMG](/assets/images/IMG_writeups/IMG_Reverse/IMG_Pwn_Season/IMG_want-the-flag/3.png){: height="200" .align-center}

Внезапно.

![IMG](/assets/images/IMG_writeups/IMG_Reverse/IMG_Pwn_Season/IMG_want-the-flag/4.jpg){: height="200" .align-center}

Поиск строки в файле мне ничего не дал.

![IMG](/assets/images/IMG_writeups/IMG_Reverse/IMG_Pwn_Season/IMG_want-the-flag/5.png){: height="200" .align-center}

Пропатчу саму строку. Для этого использую команду `Binary Ninja API` - `bv.write(0x60b040, 'I_WANT_THE_FLAG!')`.

![IMG](/assets/images/IMG_writeups/IMG_Reverse/IMG_Pwn_Season/IMG_want-the-flag/6.png){: height="200" .align-center}

Запущу:

![IMG](/assets/images/IMG_writeups/IMG_Reverse/IMG_Pwn_Season/IMG_want-the-flag/7.png){: height="200" .align-center}

![IMG](/assets/images/IMG_writeups/IMG_Reverse/IMG_Pwn_Season/IMG_want-the-flag/8.png){: height="200" .align-center}

Ладно. Полез в отладчик.

##  Отладка.

Чтобы убедиться в своей адекватности, я поставлю брейкпоинт на `main` и через `strcmp`, чтобы проверить, что подается правильная строка для сравнения:

![IMG](/assets/images/IMG_writeups/IMG_Reverse/IMG_Pwn_Season/IMG_want-the-flag/9.png){: height="200" .align-center}

Начало `main`:

![IMG](/assets/images/IMG_writeups/IMG_Reverse/IMG_Pwn_Season/IMG_want-the-flag/10.png){: height="200" .align-center}

Перед сравнением:

![IMG](/assets/images/IMG_writeups/IMG_Reverse/IMG_Pwn_Season/IMG_want-the-flag/11.png){: height="200" .align-center}

Замечательно. С головой все в порядке. Ну так уж и быть. Пропатчу строку перед вызовом `strcmp`. Делов-то:

- Дойду до нужного брейкпоинта:

![IMG](/assets/images/IMG_writeups/IMG_Reverse/IMG_Pwn_Season/IMG_want-the-flag/12.png){: height="200" .align-center}

- Изменю память командой `set {char[0x11]} 0x60b040 = "I_WANT_THE_FLAG!"`:

![IMG](/assets/images/IMG_writeups/IMG_Reverse/IMG_Pwn_Season/IMG_want-the-flag/13.png){: height="200" .align-center}

- Продолжу нормальное выполнение программы с помощью `continue/c`:

![IMG](/assets/images/IMG_writeups/IMG_Reverse/IMG_Pwn_Season/IMG_want-the-flag/14.png){: height="200" .align-center}

А вот и флаг:

```
spbctf{ed1t1ng_t3h_memory_l1ke_a_PRO}
```
