#include <stdio.h>
#include <math.h>
#include <unistd.h>
#include <stdlib.h>

typedef unsigned char   undefined;

typedef unsigned char    byte;
typedef unsigned char    dwfenc;
typedef unsigned int    dword;
typedef unsigned long    qword;
typedef unsigned int    uint;
typedef unsigned long    ulong;
typedef unsigned char    undefined1;
typedef unsigned int    undefined4;
typedef unsigned long    undefined8;
typedef unsigned short    ushort;
typedef unsigned short    word;

typedef ulong uint64_t;

typedef struct context context;

struct context {
    uint pc;
    undefined field_0x4;
    undefined field_0x5;
    undefined field_0x6;
    undefined field_0x7;
    char * mem;
    char * stack;
    uint sp;
    undefined field_0x1c;
    undefined field_0x1d;
    undefined field_0x1e;
    undefined field_0x1f;
    char * code;
};
ulong read_operands(char *param_1);
ulong read_opcode(char *param_1);
ulong FUN_00100a26(char *code,char *param_2);
ulong read_registers(char *code,uint *param_2);
ulong pop(context *con);
void vm_main(context *con);
int main(int param_1,char ** param_2);
