---
title: "Обнаружение отладчика"
date: 2025-09-22
tags: [reverse, malware]  
categories: [Reverse]
tagline: ""
header:
  overlay_image: /assets/images/IMG_writeups/IMG_Reverse/IMG_maldev/maldev_logo.jpg
  overlay_filter: 0.5 
  overlay_color: "#fff"
classes: wide
---
{% raw %}
Привет:3 Сегодня разберем одну из техник антиотладки.

При анализе вредоносов достаточно часто без ~~бутылки пива~~ динамического анализа не разобраться. Поэтому запустить бинарь под отладчиком — это база. Очевидно, что малварщики это тоже знают. Поэтому они используют различные методы защиты от отладки. Все это называется красивым словом — 🙌антиотладка🙌.

Одной из самых простых техник обнаружения отладчика является [Debugger Evasion](https://attack.mitre.org/techniques/T1622/). Обнаружив факт отладки, вредонос может изменить свое поведение, чтобы не палиться)

Сегодня рассмотрим простые примеры данной техники.

## Linux

У данного метода следующая логика — eсли к запущенному процессу есть подключение через `ptrace()`, значит к нему подключен дебаггер. Почему это работает? В `Linux` к одному процессу может подключиться для отслеживания только один процесс. Если при попытке подключения для отладки происходит ошибка, значит этот процесс уже был запущен под отладкой.

### ptrace()

`ptrace()` — это системный вызов, который позволяет трассировать или отлаживать выбранный процесс. 

```c
#include <sys/ptrace.h>

long ptrace(enum __ptrace_request request, pid_t pid, void *addr, void *data);
```

- `request` — это действие, которое необходимо осуществить;
- `pid` — PID;
- `addr` и `data` — зависят от `request`.

В поле `request` можно передать следующие команды:

- `PTRACE_SINGLESTEP` — позволяет запущенному процессу выполнить ровно одну инструкцию, а потом автоматически остановиться, чтобы отладчик мог проверить состояние;
- `PTRACE_SYSCALL` — продолжает выполнение процесса до того момента, когда он войдёт в системный вызов или выйдет из него, что даёт возможность посмотреть аргументы вызова или возвращаемое значение;
- `PTRACE_ATTACH` — отладчик присоединяется к уже работающему процессу, отправляет ему сигнал `SIGSTOP`, чтобы приостановить, и затем может управлять этим процессом;

```c
if (ptrace(PTRACE_ATTACH, pid, NULL, NULL) < 0) {
	perror("ptrace_attach");
    exit(EXIT_FAILURE);
}
```

- `PTRACE_PEEKTEXT` — позволяет прочитать данные из адресного пространства другого процесса;
- `PTRACE_POKETEXT` — позволяет записать данные в адресное пространство другого процесса;

```c
size_t data_len = strlen(data);
uint64_t *data_p = (uint64_t *)data;
for (size_t i = 0; i < data_len; i += 8, data_p++) {
    if (ptrace(PTRACE_POKETEXT, pid, address + i, *data_p) < 0) {
        perror("ptarce_poketext");
        exit(EXIT_FAILURE);
    }
}
```

- `PTRACE_GETREGS` — читает текущее состояние регистров процесса. Для хранения регистров используется структура [user_regs_struct](https://docs.huihoo.com/doxygen/linux/kernel/3.7/structuser__regs__struct.html);

```c
struct user_regs_struct old_regs;
if (ptrace(PTRACE_GETREGS, target_pid, NULL, &old_regs) < 0) {
	perror("ptrace_getregs");
	exit(EXIT_FAILURE);
}
```

- `PTRACE_SETREGS` — записывает состояние регистров процесса.

```c
struct user_regs_struct regs;
memcpy(&regs, &old_regs, sizeof(struct user_regs_struct));
regs.rip = target_address;

if (ptrace(PTRACE_SETREGS, target_pid, NULL, &regs) < 0) {
	perror("ptrace_setregs");
	exit(EXIT_FAILURE);
}
```

- `PTRACE_CONT` — продолжает выполнение отлаживаемого процесса;

```c
if (ptrace(PTRACE_CONT, pid, NULL, NULL) < 0) {
	perror("ptrace_cont");
	exit(EXIT_FAILURE);
}
```

### Пример

[`linux_ex.c`](/assets/files/FILE_writeups/FILE_Reverse/FILE_maldev/FILE_debugger_detection/linux_ex.c).

```c
#include <stdio.h>
#include <sys/ptrace.h>

int main()
{
	if (ptrace(PTRACE_TRACEME, 0, 1, 0) < 0) {
		printf("Debugging Dedected.\n");
		return 1;
	}
	ptrace(PTRACE_DETACH, 0, 1, 0);
	printf("Normal Execution.\n");
	return 0;
}
```

Запуск:

![IMG](/assets/images/IMG_writeups/IMG_Reverse/IMG_maldev/IMG_debugger_detection/1.png){: height="200" .align-center}

## Windows

В `Windows` существуют стандартные методы для проверки, запущен ли процесс под отладчиком. Среди них `IsDebuggerPresent()`, который проверяет текущий процесс, и `CheckRemoteDebuggerPresent()`, позволяющий определить, присутствует ли отладчик в другом процессе.

### `IsDebuggerPresent()`

`IsDebuggerPresent()` возвращает значение `True`, если к процессу подключен отладчик. Это позволяет программе самостоятельно определять, находится ли она под отладкой, и при необходимости изменять поведение или предпринимать защитные меры.

```c
#include <stdio.h>
#include <windows.h>

int main() {
	BOOL isDebuggerPresent = IsDebuggerPresent();

	if (isDebuggerPresent) {
		printf("Debugger detected\n");
	} else {
		printf("Debugger not detected\n");
	}
	return 0;
}
```

## `CheckRemoteDebuggerPresent`

`CheckRemoteDebuggerPresent()` — это расширенный вариант проверки отладки, который позволяет определить, подключён ли отладчик к другому процессу, а не только к текущему.

```c
#include <stdio.h>
#include <windows.h>

int main() {
	BOOL isDebuggerPresent = FALSE;
	HANDLE currentProcess = GetCurrentProcess();
	BOOL isRemoteDebuggerPresent = FALSE;

	CheckRemoteDebuggerPresent(currentProcess, &isRemoteDebuggerPresent);

	if (isRemoteDebuggerPresent) {
		printf("Debugger detected\n");
	} else {
		printf("Debugger not detected\n");
    }
	return 0;
}
```

## Практика

Для того, чтобы самим посмотреть на данную технику, можно попробовать решить следующую задачку: [`SimpleCrackMe.exe`](/assets/files/FILE_writeups/FILE_Reverse/FILE_maldev/FILE_debugger_detection/SimpleCrackMe.exe).
{% endraw %}
