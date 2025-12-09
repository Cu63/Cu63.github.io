---
title: "Easy Overflow 2"
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
      url: "https://pwn.spbctf.ru/tasks/pwn1_mc5"
classes: half
layout: single
toc: true
toc_sticky: true
toc_label: "Оглавление"
---

Переполните, чтобы получить флаг.

- [ELF](https://pwn.spbctf.ru/files/overflow/mc5_censored)

```
nc 109.233.56.90 11585
```

# Solution

Тут тоже нужно переполнить буфер. Поэтому без реверса не обойтись. Гляну в статике, что там нужно переполнять. Заодно натравлю `LLM` на код.

## Анализ `main`

Анализ от `LLM`:

```
[Default] There are several potential security vulnerabilities in the provided code snippet. Here's a detailed analysis of each one, along with an explanation of why they're dangerous and how they could be exploited:
[Default]  
[Default] 1. Buffer overflow: The `strncpy` function is used to copy a string into a buffer that may not be large enough to hold it. This can lead to a buffer overflow if the string is longer than 9 characters,   which is the size of the buffer being copied into. An attacker could exploit this vulnerability by providing a specially crafted input that exceeds the buffer's capacity, allowing them to overwrite adjacent   memory locations.  
[Default] 2. Format string vulnerability: The `printf` function is used with a format string argument that contains user-supplied data. This can lead to a format string vulnerability if an attacker provides a     specially crafted input that exploits the format string's formatting logic. For example, they could provide a string like "%x%x%x%x" to overwrite adjacent memory locations with arbitrary values.      
[Default] 3. Use-after-free: The `scanf` function is used to read user-supplied data into an array of integers. However, the code does not properly check for errors when reading from standard input, which could  lead to a use-after-free vulnerability if an attacker provides a specially crafted input that causes the program to access previously freed memory locations.  
[Default] 4. Integer overflow: The `scanf` function is also used to read user-supplied data into an integer variable. However, the code does not properly check for errors when reading from standard input, which  could lead to an integer overflow if an attacker provides a specially crafted input that causes the program to store a large value in the integer variable.  
[Default] 5. Missing input validation: The code does not perform any input validation on the user-supplied data, which could lead to security vulnerabilities if an attacker provides malicious input. For example, they could provide a specially crafted input that exceeds the buffer's capacity, allowing them to overwrite adjacent memory locations.  
[Default] 6. Lack of error handling: The code does not properly handle errors when reading from standard input, which could lead to security vulnerabilities if an attacker provides malicious input. For example,  they could provide a specially crafted input that causes the program to crash or behave unexpectedly.
[Default] 7. Hardcoded flag: The code includes a hardcoded flag value that is not properly protected. An attacker could potentially discover this flag by reverse-engineering the binary or by analyzing the program's behavior.  
[Default] 8. No bounds checking: The `printf` function is used with a format string argument that contains user-supplied data, but no bounds checking is performed to ensure that the format string does not exceed the buffer's capacity. This could lead to a buffer overflow vulnerability if an attacker provides a specially crafted input.  
[Default] 9. No check for NULL: The `printf` function is used with a format string argument that contains user-supplied data, but no check is performed to ensure that the format string is not NULL. This could   lead to a null pointer dereference vulnerability if an attacker provides a specially crafted input.  
[Default] 10. No check for invalid characters: The `scanf` function is used with a format string argument that contains user-supplied data, but no check is performed to ensure that the format string does not   contain any invalid characters. This could lead to a format string vulnerability if an attacker provides a specially crafted input.  
[Default]   
[Default] Overall, the code snippet provided contains several potential security vulnerabilities that could be exploited by an attacker. It is important to thoroughly review and test the code to identify these   vulnerabilities and ensure that they are properly mitigated.  
```

```c
  int32_t main(int32_t argc, char** argv, char** envp)

  {
      int32_t ans;
      __builtin_strncpy(&ans, "NOPE", 9);
      int64_t rcx;
      (uint8_t)rcx = 0;
      int64_t rax;
      (uint8_t)rax = 0;
      int32_t var_34 = printf("How many numbers do you want to store (max. 5) ? ", argv, envp, rcx);
      int32_t rax_1;
      (uint8_t)rax_1 = 0;
      int32_t count;
      scanf("%d", &count);
      int32_t buf[0x5];
      int32_t rax_2;
      
      for (int32_t num = 0; num < count; num += 1)
      {
          (uint8_t)rax_2 = 0;
          int32_t var_38_1 = printf("Enter number # %d: ", (uint64_t)num);
          int32_t rax_3;
          (uint8_t)rax_3 = 0;
          scanf("%d", &buf[(int64_t)num]);
      }
      
      (uint8_t)rax_2 = 0;
      printf("Here are your numbers, well-kept: ");
      int32_t rax_6;
      
      for (int32_t i = 0; i < count; i += 1)
      {
          if (i > 0)
          {
              (uint8_t)rax_6 = 0;
              printf(", ");
          }
          
          int64_t rax_7;
          (uint8_t)rax_7 = 0;
          printf("%d", (uint64_t)buf[(int64_t)i]);
      }
      
      (uint8_t)rax_6 = 0;
      int32_t var_3c = printf("\n\n");
      int32_t rax_10;
      (uint8_t)rax_10 = 0;
      int32_t var_40 = printf("Now to the flag... Do you want flag - '%s'\n", &ans);
      int32_t rax_12;
      
      if (strcmp(&ans, "YEAH"))
      {
          (uint8_t)rax_12 = 0;
          printf("Good, i won't give you flag.\n");
      }
      else
      {
          (uint8_t)rax_12 = 0;
          printf("Flag is: spbctf{********************************}\n");
      }
      int32_t result;
      return result;
  }

```

Судя по коду мы можем записать свои числа в буфер. После чего нам эти числа покажут. Далее, если в `ans` будет лежать `YEAH`, то мы получим флаг.

## Подбор пейлоада

Запущу бинарный файл:

![IMG](/assets/images/IMG_writeups/IMG_Pwn/IMG_Pwn_Season/IMG_Easy_Overflow_2/1.png){: height="200" .align-center}

Проблема в том, что ответ захардкожен. Благо, что он в локальной переменной. В коде хоть и указано, что мы не можем хранить более 5 чисел, но это нигде не проверяется. Адресная арифметика в `c` работает следующим образом:

```
buf[i] = *(адрес buf + i * размер типа данных)
```

Давайте посмотрим на стек:

![IMG](/assets/images/IMG_writeups/IMG_Pwn/IMG_Pwn_Season/IMG_Easy_Overflow_2/2.png){: height="200" .align-center}

Можно увидеть, что между ответом и буфером есть еще 3 байт. Значит мне нужно записать на 6-ю и 7-ю позицию байты следующим образом:

```
| ** ** ** 'Y' | 'E' 'A' 'H' 00 |
```

В `Hex` это выглядит следующим образом:

```
59 45 41 48 00
```

Но есть нюанс. В памяти значения лежат в `Little Endian`. Это значит, что число `0x12345678` будет лежат так:

```
78 56 34 12
```

Таки образом, чтобы в памяти буквы лежали рядом, нам нужны следующие числа:

```
0x59000000 = 1493172224
```

и 

```
0x00484145 = 4735301
```

Проверю:

![IMG](/assets/images/IMG_writeups/IMG_Pwn/IMG_Pwn_Season/IMG_Easy_Overflow_2/3.png){: height="200" .align-center}

Осталось забрать флаг:

![IMG](/assets/images/IMG_writeups/IMG_Pwn/IMG_Pwn_Season/IMG_Easy_Overflow_2/4.png){: height="200" .align-center}

```
spbctf{0mgy3s_that_s_t3h_r34l_1337spe4k}
```
