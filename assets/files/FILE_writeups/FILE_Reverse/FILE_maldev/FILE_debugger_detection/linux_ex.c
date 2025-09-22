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
