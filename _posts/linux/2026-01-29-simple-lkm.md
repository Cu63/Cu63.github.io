---
title: "Простые LKM: фундамент для kernel-руткитов"
date: 2026-01-29
tags:
  - linux
  - kernel
  - lkm
  - rootkits
categories: [linux]
tagline: "Почему без hello world нельзя говорить о руткитах"
header:
  overlay_image: /assets/images/linux/simple_lkm/IMG_simple_lkm_header.jpeg
  overlay_filter: 0.5
  overlay_color: "#fff"
classes: half
layout: single
toc: true
toc_sticky: true
toc_label: "Оглавление"
---

# Простые LKM

Привет^3

Примерно год назад я увлекся темой руткитов под `Linux`. Это оказалось достаточно интересным и увлекательным приключением. Я даже реализовал модуль по их обнаружению. 

Вы можете сопротивляться, жаловаться или бежать, но я все равно расскажу вам про руткиты. Снова... Я пытался ранее... Ну да ладно.

В этой статье мы с тобой разберем, что это за модули, напишем `hello, world`. Без этого про руткиты не рассказать. Так что вперед.

## Loadable Kernel Module, LKM

Это код, который может быть загружен в адресное пространство ядра без перезагрузки системы. Они позволяют расширять функциональность ядра динамически.

Классический пример такого модуля - драйвер устройства.

## Команды для работы с модулями

- `lsmod` - показать список загруженных модулей;
- `modinfo module.ko` - показать информацию о модуле;
- `insmod module.ko` - загрузка модуля в ядро;
- `rmmod module_name` - удаление модуля из ядра;
- `sudo journalctl --since "1 hour ago" | grep kernel` - просмотр сообщений ядра.

## Установка окружения

### Пакеты

```bash
sudo apt-get update
````

### Заголовочные файлы ядра

Для `Ubuntu / Debian`:

```bash
apt-cache search linux-headers-$(uname -r)
sudo apt-get install kmod linux-headers-$(uname -r)
```

## Структура LKM-модуля

### Базовая модель

Модуль ядра должен иметь как минимум две точки входа.

До версии ядра `2.3.13`:

* `init_module()` - вызывается при загрузке модуля;
* `cleanup_module()` - вызывается перед выгрузкой модуля.

В современных ядрах используются макросы `module_init()` и `module_exit()`, которые позволяют указать **произвольные функции** инициализации и завершения.

## Hello, world на руткитском

`hello-1.c`:

```c
#include <linux/kernel.h>
#include <linux/module.h>

int init_module(void) {
	pr_info("Hello, world\n");
	return 0;
}

void cleanup_module(void) {
	pr_info("Goodbye, world.\n");
}

MODULE_LICENSE("GPL");
```

`Makefile`:

```make
obj-m += hello-1.o

all:
	make -C /lib/modules/$(shell uname -r)/build M=$(shell pwd) modules
clean:
	make -C /lib/modules/$(shell uname -r)/build M=$(shell pwd) clean
```

Сборка и загрузка:

```bash
make
sudo insmod hello-1.ko
```

Проверяем:

```bash
lsmod | grep hello_1
sudo dmesg | tail -n 3
```

Удаление модуля:

```bash
sudo rmmod hello_1
sudo dmesg | tail -n 3
```

### `module_init()` и `module_exit()`

Аналогичный пример с макросами:

```c
#include <linux/init.h>
#include <linux/kernel.h>
#include <linux/module.h>

static int __init hello_init(void) {
	pr_info("Hello, world\n");
	return 0;
}

static void __exit hello_exit(void) {
	pr_info("Goodbye, world.\n");
}

module_init(hello_init);
module_exit(hello_exit);

MODULE_LICENSE("GPL");
```

Макросы:

* `__init` - позволяет освободить память, занятую кодом инициализации, после её выполнения;
* `__exit` - указывает, что функция завершения не используется для встроенных в ядро модулей.

## Вывод

Мы написали и загрузили простой модуль ядра.
Это минимальный строительный блок, без которого невозможно говорить о LKM-руткитах.

В следующем посте мы начнём смотреть, как LKM могут скрываться от `lsmod`.
