---
title: "Nostr 7"
date: 2025-10-06
tags: [reverse, writeup]  
categories: [Reverse]
tagline: ""
header:
  overlay_image: /assets/images/IMG_writeups/IMG_Reverse/IMG_forkbomb/forkbomb_logo.jpg
  overlay_filter: 0.5 
  overlay_color: "#fff"
  actions:
    - label: "Lab forkbomb"
      url: "https://rev-kids20.forkbomb.ru/tasks/RE2_nostr150"
classes: wide
---

Нужно найти флаг - верный серийный номер.

[ELF](https://rev-kids20.forkbomb.ru/files/rev/re2/s7.out)
[PE](https://rev-kids20.forkbomb.ru/files/rev/re2/s7.exe)

## Solution

Гляну файл:

```
Info:
    File name: /spbctf_rev/Nostr 7/s7.out
    Size: 7444
    File type: ELF32
    String: ELF(386)
    Extension: elf
    Operation system: Linux(ABI: 2.6.32)
    Architecture: 386
    Mode: 32-bit
    Type: EXEC
    Endianness: LE
```

А вот и функция `main`:

```c
int32_t main(int32_t argc, char** argv, char** envp)
{
    void* const __return_addr_1 = __return_addr;
    int32_t* var_c = &argc;
    int32_t var_14 = 0xb;
    printf("Enter serial number: ");
    void var_1f;
    scanf("%s", &var_1f);
    Check(&var_1f);
    return 0;
}
```

По `scanf` ясно, что `var_1f` - это строка. Перейду в функцию `Check`:

```c
int32_t Check(char* arg1)
{
    char eax = strlen(arg1);
    char var_d;
    
    if ((eax != 6 || arg1[5] != 'x'))
        var_d = 0;
    else
    {
        var_d = 1;
        
        for (int32_t i = 1; ((int32_t)eax) > i; i += 1)
        {
            if (((int32_t)arg1[i]) != (i + ((int32_t)arg1[(i - 1)])))
            {
                var_d = 0;
                break;
            }
        }
    }
    
    PrintOK(((uint32_t)var_d));
    return PrintError(((uint32_t)(var_d ^ 1)));
}
```

Давайте разбираться. `eax` - это длина нашего ключа.

```c
if ((eax != 6 || arg1[5] != 'x'))
    var_d = 0;
```

Значит ключ должен состоять из 6 символов, последний из которых - `x`. Ладно, погнали дальше. Вот эту кракозябру:

```c
if (((int32_t)arg1[i]) != (i + ((int32_t)arg1[(i - 1)])))
```

Можно привести к следующему виду:

```c
if (arg1[i] != i + arg1[i - 1])
```

Ну все ясно. Каждый последующий символ должен быть на `i` больше, чем предыдущий. Нам известен пятый символ `x`. Напишем код на `Python`:

```python
key = []

c = 'x'
for i in range(5, -1, -1):
    key.append(c)
    c = chr(ord(c) - i)

print(''.join(key[::-1]))
```

А вот и флаг:

```
ijlosx
```

Проверю:

![IMG](/assets/images/IMG_writeups/IMG_Reverse/IMG_forkbomb/IMG_Nostr_7/1.png){: height="200" .align-center}