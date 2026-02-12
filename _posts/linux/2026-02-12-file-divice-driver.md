---
title: "Драйверы файловых устройств"
date: 2026-02-12
tags: [Linux, LKM, Rootkits, Kernel]
categories: [Linux, Security]
tagline: ""
header:
  overlay_image: /assets/images/linux/file-device-drivers/IMG_file-device-drivers_header.jpeg
  overlay_filter: 0.5
  overlay_color: "#000"
classes: wide
layout: single
toc: true
toc_sticky: true
toc_label: "Оглавление"
---

**Привет^3**

В продолжение серии постов про `LKM` и руткиты мы поговорим о драйверах файловых устройств. Их удобно использовать для передачи команд в `kernel space` без лишних заморочек. А это нам сильно пригодится при отладке и разборе руткитов.

Так что в путь.

## Who is драйвер файлового устройства

Это модуль программного кода ядра, который реализует набор операций ввода-вывода. Говоря проще, мы пишем код, который обрабатывает определенные действия с устройством.

Каждый элемент оборудования в `Unix` представлен **файлом устройства** и расположен в `/dev`.

Все доступные операции описываются структурой `file_operations`.

## Структура `file_operations`

Эта структура находится в `linux/fs.h` и содержит указатели на функции, реализованные драйвером. Они выполняют различные действия с устройством. Нереализованные операции устанавливаются в `NULL`. Их там много, поэтому покажу только те, что буду использовать дальше в посте:

```c
struct file_operations {
    struct module *owner;
    ...
    ssize_t (*read) (struct file *, char __user *, size_t, loff_t *);
    ssize_t (*write) (struct file *, const char __user *, size_t, loff_t *);
    int (*open) (struct inode *, struct file *);
    int (*release) (struct inode *, struct file *);
    ...
} __randomize_layout;
````

Такую громадину заполнять не очень удобно, поэтому в `gcc` есть расширение, которое упрощает инициализацию структуры:

```c
struct file_operations fops = {
	read: device_read,
	write: device_write,
	open: device_open,
	release: device_release
};
```

Можно также использовать стандарт `C99`:

```c
struct file_operations fops = {
	.read = device_read,
	.write = device_write,
	.open = device_open,
	.release = device_release
};
```

## Регистрация устройства

Обычно обращение к файловым устройствам происходит через `/dev`.

Старший номер (`major`) сообщает, какой драйвер обслуживает устройство.
Младший номер (`minor`) используется драйвером для определения конкретного устройства.

При добавлении драйвера происходит его регистрация в ядре. Это можно сделать с помощью `register_chrdev()`. Однако этот вызов занимает диапазон `minor`-номеров.

## Отмена регистрации устройства

Чтобы модуль не был выгружен во время использования другим процессом, существует счетчик ссылок. Его можно посмотреть через `cat /proc/modules` или `lsmod`.

Если значение счетчика не равно `0`, `rmmod` завершится с ошибкой.

Обычно вручную работать с этим счетчиком не требуется, но существуют функции:

* `try_module_get(THIS_MODULE)` - увеличивает счетчик ссылок
* `module_put(THIS_MODULE)` - уменьшает счетчик ссылок
* `module_refcount(THIS_MODULE)` - возвращает текущее значение

## Пример

`chardev.c`:

```c
#include <linux/cdev.h>
#include <linux/delay.h>
#include <linux/device.h>
#include <linux/fs.h>
#include <linux/init.h>
#include <linux/irq.h>
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/poll.h>
#include <linux/version.h>

static int device_open(struct inode *, struct file *);
static int device_release(struct inode *, struct file *);
static ssize_t device_read(struct file *, char __user *, size_t, loff_t *);
static ssize_t device_write(struct file *, const char __user *, size_t, loff_t *);

#define SUCCESS 0
#define DEVICE_NAME "chardev"
#define BUF_LEN 80

static int major;

enum {
	CDEV_NOT_USED = 0,
	CDEV_EXCLUSIVE_OPEN = 1
};

static atomic_t already_open = ATOMIC_INIT(CDEV_NOT_USED);
static char msg[BUF_LEN];
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
	pr_info("I was assigned major number %d.\n", major);

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
	/* Cancel device registration */
	unregister_chrdev(major, DEVICE_NAME);
}

module_init(chardev_init);
module_exit(chardev_exit);

/*
 * Called when a process tries to open the device file.
 */
static int device_open(struct inode *inode, struct file *file) {
	static int counter = 0;

	if (atomic_cmpxchg(&already_open, CDEV_NOT_USED, CDEV_EXCLUSIVE_OPEN))
		return -EBUSY;

	sprintf(msg, "I already told you %d times Hello\n", counter++);
	try_module_get(THIS_MODULE);
	return SUCCESS;
}

/*
 * Called when a process closes the device file.
 */
static int device_release(struct inode *inode, struct file *file) {
	atomic_set(&already_open, CDEV_NOT_USED);
	module_put(THIS_MODULE);
	return SUCCESS;
}

/*
 * Called when a process tries to read from the device file.
 */
static ssize_t device_read(struct file *filp,
			   char __user *buffer,
			   size_t length,
			   loff_t *offset) {
	int bytes_read = 0;
	const char *msg_ptr = msg;

	if (!*(msg_ptr + *offset)) {
		*offset = 0;
		return 0;
	}

	msg_ptr += *offset;

	while (length && *msg_ptr) {
		if (put_user(*(msg_ptr++), buffer++))
			return -EFAULT;
		length--;
		bytes_read++;
	}

	*offset += bytes_read;
	return bytes_read;
}

static ssize_t device_write(struct file *filp,
			    const char __user *buff,
			    size_t len,
			    loff_t *off) {
	pr_alert("Sorry, this operation is not supported\n");
	return -EINVAL;
}

MODULE_LICENSE("GPL");
MODULE_AUTHOR("cu63");
```

`Makefile`:

```makefile
NAME := chardev
obj-m += $(NAME).o
VER := $(shell uname -r)

all:
	make -C /lib/modules/$(VER)/build M=$(shell pwd) modules
clean:
	make -C /lib/modules/$(VER)/build M=$(shell pwd) clean
ins:
	sudo insmod $(NAME).ko
rm:
	sudo rmmod $(NAME)
log:
	sudo journalctl --since "30 seconds ago"
```

Скомпилирую и запущу модуль:

```bash
[cu63@fedora chardev]$ make
make -C /lib/modules/5.17.5-300.fc36.x86_64/build M=/home/cu63/rootkits/chardev modules
make[1]: вход в каталог «/usr/src/kernels/5.17.5-300.fc36.x86_64»
warning: the compiler differs from the one used to build the kernel
  The kernel was built by: gcc (GCC) 12.0.1 20220413 (Red Hat 12.0.1-0)
  You are using:           gcc (GCC) 12.2.1 20221121 (Red Hat 12.2.1-4)
  CC [M]  /home/cu63/rootkits/chardev/chardev.o
  MODPOST /home/cu63/rootkits/chardev/Module.symvers
  CC [M]  /home/cu63/rootkits/chardev/chardev.mod.o
  LD [M]  /home/cu63/rootkits/chardev/chardev.ko
  BTF [M] /home/cu63/rootkits/chardev/chardev.ko
Skipping BTF generation for /home/cu63/rootkits/chardev/chardev.ko due to unavailability of vmlinux
make[1]: выход из каталога «/usr/src/kernels/5.17.5-300.fc36.x86_64»
[cu63@fedora chardev]$ make ins
[cu63@fedora chardev]$ lsmod | grep chardev
chardev                16384  0
[cu63@fedora chardev]$ sudo cat /dev/chardev
I already told you 0 times Hello
[cu63@fedora chardev]$ sudo cat /dev/chardev
I already told you 1 times Hello
```

## Вывод

Мы написали простой драйвер файлового устройства. Теперь мы морально готовы разбираться с руткитами. С чем я вас и поздравляю.

В следующем посте перейдем уже к ним.
