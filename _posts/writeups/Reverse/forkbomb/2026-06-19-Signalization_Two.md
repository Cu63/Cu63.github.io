---
title: "Signalization Two"
date: 2026-06-19
tags: [reverse, writeup]
categories: [Reverse]
tagline: ""
header:
  overlay_image: /assets/images/IMG_writeups/IMG_Reverse/IMG_forkbomb/forkbomb_logo.jpg
  overlay_filter: 0.5
  overlay_color: "#fff"
  actions:
    - label: "Lab forkbomb"
      url: "https://rev-kids20.forkbomb.ru/tasks/RE3_signalization2"
classes: wide
layout: single
toc: true
toc_sticky: true
toc_label: "Оглавление"
---

- [signalization2.elf](https://rev-kids20.forkbomb.ru/files/rev/re3/signalization2.elf)

Программа принимает на вход строку. Нужно заставить её вывести флаг.

# Solution

## Анализ `main`

```c
int32_t main(int32_t argc, char** argv, char** envp)
{
    signal(sig: 2, handler);
    char buf[0x108];
    int32_t result = fgets(&buf, n: 0xa, fp: __TMC_END__);

    if (rax == *(fsbase + 0x28))
        return result;

    __stack_chk_fail();
}
```

`signal(2, handler)` — устанавливает свой обработчик на сигнал `SIGINT` (номер 2).

> Сигнал — программное прерывание. Поступление сигнала информирует процесс о возникновении события или исключительных условий.

`SIGINT` отправляется через `Ctrl+C` или `kill -2 <PID>`.

## Получение флага

Запускаем бинарь в фоне и отправляем сигнал:

```bash
root@db1e62f604a9:/rev# ./signalization2.elf &
[1] 22
root@db1e62f604a9:/rev# kill -2 22

[1]+  Stopped                 ./signalization2.elf
root@db1e62f604a9:/rev# fg
./signalization2.elf
Flag{T*is 14 Simple}
^CFlag{T*is 14 Simple}
^CFlag{T*is 14 Simple}
```

## Анализ `handler`

```c
int64_t handler()
{
    char str[0x15];
    __builtin_strncpy(dest: &str, src: "Flag{This Is Simple}", count: 0x15);
    str[0xa] = '1';
    str[0xb] = '4';
    str[6] = '*';
    puts(&str);
}
```

Обработчик берёт исходную строку `"Flag{This Is Simple}"`, заменяет несколько символов и выводит результат. Комментарии излишни.
