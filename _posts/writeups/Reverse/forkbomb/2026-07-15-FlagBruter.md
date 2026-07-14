---
title: "FlagBruter"
date: 2026-07-15
tags: [reverse, writeup]
categories: [Reverse]
tagline: "ltrace ловит memcpy с флагом"
header:
  overlay_image: /assets/images/IMG_writeups/IMG_Reverse/IMG_forkbomb/forkbomb_logo.jpg
  overlay_filter: 0.5
  overlay_color: "#fff"
  actions:
    - label: "Lab forkbomb"
      url: "https://rev-kids20.forkbomb.ru/tasks/RE5_flagbruter"
classes: wide
layout: single
toc: true
toc_sticky: true
toc_label: "Оглавление"
---

- [flagbruter.elf](https://rev-kids20.forkbomb.ru/files/rev/re5/flagbruter.elf)

Sometimes the string variable contains flag. Most of times not.

# Solution

## Анализ

```c
int32_t main(int32_t argc, char** argv, char** envp)
{
    int64_t var_78;
    __builtin_memcpy(&var_78, "\xe8\xc0\x6c\x66...", 0x18);
    char var_58;
    
    for (int32_t i = 0; i <= 0x1869f; i += 1)
    {
        void* rax_1 = malloc(0x18);
        sprintf(&s, "%d", (uint64_t)i);
        hooyeah(&s, 6);
        
        while (var_94_1 < 0x17)
        {
            *(uint8_t*)(var_94_1 + rax_1) = yahooo() ^ *(uint8_t*)(&var_78 + var_94_1);
            var_94_1 += 1;
        }
        
        memcpy(&var_58, rax_1, 0x17);
        free(rax_1);
    }
    
    return (int32_t)var_58;
}
```

Цикл перебирает 100 000 вариантов: XOR-ит байты с результатом `yahooo()` и складывает в буфер через `memcpy`. Статически разбирать это долго — `memcpy` вызывается на каждой итерации, в какой-то момент там окажется флаг.

## ltrace

Запускаю `ltrace` и перенаправляю в файл — вывод большой:

```bash
$ ltrace -o trace ./flagbruter.elf
```

Ищу `memcpy` без экранированных байт (т.е. где значение читаемое):

```bash
$ grep memcpy trace | grep -v '\\'
memcpy(0x7ffd2400b670, "FLAGus_flagus_asparagus", 23) = 0x7ffd2400b670
```

```
FLAGus_flagus_asparagus
```
