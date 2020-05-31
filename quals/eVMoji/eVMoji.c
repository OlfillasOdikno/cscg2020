#include "eVMoji.h"

context con;

ulong read_operands(char *param_1)

{
  undefined8 uVar1;
  uint local_c;
  
  if (*param_1 < '\0') {
    local_c = 2;
    while ((int)local_c < 5) {
      if ((0x80 >> ((byte)local_c & 0x1f) & (int)*param_1) == 0) {
        return (ulong)local_c;
      }
      local_c = local_c + 1;
    }
    uVar1 = 0xffffffff;
  }
  else {
    uVar1 = 1;
  }
  return uVar1;
}



ulong read_opcode(char *param_1)

{
  uint uVar1;
  uint local_18;
  uint local_14;
  
  uVar1 = read_operands(param_1);
  local_18 = 0;
  local_14 = 0;
  while (local_14 < uVar1) {
    local_18 = local_18 |
               0xff << ((byte)(local_14 << 3) & 0x1f) &
               (int)param_1[(int)local_14] << ((byte)(local_14 << 3) & 0x1f);
    local_14 = local_14 + 1;
  }
  return (ulong)local_18;
}



ulong FUN_00100a26(char *code,char *param_2)

{
  char cVar1;
  int iVar2;
  int iVar3;
  
  cVar1 = read_opcode(code);
  *param_2 = cVar1 + -0x30;
  iVar2 = read_operands(code + 1);
  iVar3 = read_operands(code + (iVar2 + 1));
  return (ulong)(uint)(iVar2 + 1 + iVar3);
}



ulong read_registers(char *code,uint *param_2)

{
  char cVar1;
  double dVar2;
  char local_1a;
  char local_19;
  uint local_18;
  int local_14;
  long local_10;
  
  *param_2 = 0;
  local_18 = 0;
  local_14 = 0;
  while (local_14 < 3) {
    cVar1 = FUN_00100a26(code + (int)local_18,&local_1a);
    local_18 = local_18 + (int)cVar1;
    cVar1 = FUN_00100a26(code + (int)local_18,&local_19);
    local_18 = local_18 + (int)cVar1;
    dVar2 = pow((double)(int)local_19,(double)(int)local_1a);
    *param_2 = (uint)(long)((double)(ulong)*param_2 + dVar2);
    local_14 = local_14 + 1;
  }
  return (ulong)local_18;
}



ulong pop(context *con)

{
  con->sp = con->sp - 1;
  return (ulong)*(uint *)(con->stack + (long)(int)con->sp * 4);
}



void vm_main(context *con)

{
  char cVar1;
  char *pcVar2;
  int op_length;
  int iVar3;
  uint uVar4;
  uint uVar5;
  uint uVar6;
  uint local_2c;
  uint local_28;
  uint opcode;
  int should_log;
  should_log=0;
  local_2c = 0;
  local_28 = 0;
LAB_00100bf0:
  opcode = read_opcode(con->code + (int)con->pc);
  op_length = read_operands(con->code + (int)con->pc);
  con->pc = op_length + con->pc;
  if (opcode == 0x80929ff0) {
                    // WARNING: Subroutine does not return
    exit(-1);
  }
  if (opcode < 0x80929ff1) {
    if (opcode == 0x959ee2) {
      local_2c = pop(con);
      //printf("lsb %x = %x\n",local_2c,local_2c & 1);
      //printf("lsb %x = %x\n",local_2c,local_2c & 1);
      local_2c = local_2c & 1;
      uVar5 = con->sp;
      con->sp = uVar5 + 1;
      *(uint *)(con->stack + (long)(int)uVar5 * 4) = local_2c;
      goto LAB_00100bf0;
    }
    if (opcode < 0x959ee3) {
      if (opcode == 0x859ce2) {
        uVar6 = pop(con);
        uVar4 = pop(con);
        uVar5 = con->sp;
        con->sp = uVar5 + 1;
        if(should_log || 1){
            //printf("%x | %x = %x \n",uVar6 , uVar4,uVar6 | uVar4);
            printf("%c",uVar6);
        }
        *(uint *)(con->stack + (long)(int)uVar5 * 4) = uVar6 | uVar4;
        goto LAB_00100bf0;
      }
      if (opcode == 0x8f9ce2) {
        uVar5 = pop(con);
        pcVar2 = con->mem;
        uVar6 = pop(con);
        //write(1,pcVar2 + uVar6,(ulong)uVar5);
        op_length = read_operands(con->code + (int)con->pc);
        con->pc = op_length + con->pc;
        goto LAB_00100bf0;
      }
    }
    else {
      if (opcode == 0xa19ee2) {
        op_length = read_operands(con->code + (int)con->pc);
        con->pc = op_length + con->pc;
        op_length = read_registers(con->code + (int)con->pc,&local_2c);
        con->pc = op_length + con->pc;
        local_28 = pop(con);
        if(should_log){
          printf("%x >> %d = %x\n", local_28,(byte)local_2c & 0x1f,local_28 >> ((byte)local_2c & 0x1f));
        }
        local_28 = local_28 >> ((byte)local_2c & 0x1f);
        uVar5 = con->sp;
        con->sp = uVar5 + 1;
        *(uint *)(con->stack + (long)(int)uVar5 * 4) = local_28;
        goto LAB_00100bf0;
      }
      if (opcode == 0xbc80e2) {
        op_length = read_operands(con->code + (int)con->pc);
        con->pc = op_length + con->pc;
        local_2c = pop(con);
        if(should_log){
            //printf("dup %x\n",local_2c);
        }
        uVar5 = con->sp;
        con->sp = uVar5 + 1;
        *(uint *)(con->stack + (long)(int)uVar5 * 4) = local_2c;
        uVar5 = con->sp;
        con->sp = uVar5 + 1;
        *(uint *)(con->stack + (long)(int)uVar5 * 4) = local_2c;
        goto LAB_00100bf0;
      }
    }
  }
  else {
    if (opcode == 0x96939ff0) {
      uVar5 = pop(con);
      pcVar2 = con->mem;
      uVar6 = pop(con);
      printf("read: %d\n",uVar5);
      read(0,pcVar2 + uVar6,(ulong)uVar5);
      goto LAB_00100bf0;
    }
    if (opcode < 0x96939ff1) {
      if (opcode == 0x80949ff0) {
        uVar6 = pop(con);
        uVar4 = pop(con);
        uVar5 = con->sp;
        if(should_log){
            printf("%x ^ %x = %x\n", uVar6 , uVar4, uVar6 ^ uVar4);
        }
        con->sp = uVar5 + 1;
        *(uint *)(con->stack + (long)(int)uVar5 * 4) = uVar6 ^ uVar4;
      }
      else {
        if (opcode != 0x94a49ff0) goto LAB_00101147;
        op_length = read_registers(con->code + (int)con->pc,&local_2c);
        con->pc = op_length + con->pc;
        op_length = pop(con);
        iVar3 = pop(con);
        should_log=1;

        if(should_log){
            printf("%x == %x\n",op_length,iVar3);
            //printf("%x\n",op_length==iVar3);
        }
        if (op_length == iVar3) {
          con->pc = local_2c + con->pc;
        }
      }
      goto LAB_00100bf0;
    }
    if (opcode == 0xaa929ff0) {
      op_length = read_registers(con->code + (int)con->pc,&local_2c);
      con->pc = op_length + con->pc;
      uVar5 = con->sp;
      con->sp = uVar5 + 1;
      //printf("copy to stack: %x\n", local_2c);
      *(uint *)(con->stack + (long)(int)uVar5 * 4) = local_2c;
      goto LAB_00100bf0;
    }
    if (opcode == 0xbea69ff0) {
      op_length = read_registers(con->code + (int)con->pc,&local_2c);
      con->pc = op_length + con->pc;
      cVar1 = con->mem[local_2c];
      uVar5 = con->sp;
      con->sp = uVar5 + 1;
      if(should_log){
        //printf("copy to stack: %x\n",cVar1);
      }
      *(int *)(con->stack + (long)(int)uVar5 * 4) = (int)cVar1;
      goto LAB_00100bf0;
    }
    if (opcode == 0xa08c9ff0) {
      op_length = read_registers(con->code + (int)con->pc,&local_2c);
      con->pc = op_length + con->pc;
      uVar5 = con->sp;
      con->sp = uVar5 + 1;
      if(should_log){
        //printf("copy to stack: %x\n", *(undefined4 *)(con->mem + local_2c));
      }
      *(undefined4 *)(con->stack + (long)(int)uVar5 * 4) = *(undefined4 *)(con->mem + local_2c);
      goto LAB_00100bf0;
    }
  }
LAB_00101147:
  printf("Unknown opcode: %x",(ulong)opcode);
  goto LAB_00100bf0;
}



int main(int argc,char **argv)

{
  FILE *__stream;
  
  if (argc < 2) {
    puts("Usage: ./eVMoji <code.bin>");
  }
  con.pc = 0;
  con.sp = 0;
  con.mem = (char *)malloc(0x400);
  con.stack = (char *)malloc(0x400);
  con.code = (char *)malloc(0x10000);
  __stream = fopen(argv[1],"rb");
  if (__stream == (FILE *)0x0) {
    printf("File not found: %s",argv[1]);
  }
  fread(con.mem,0x200,1,__stream);
  fread(con.code,0x10000,1,__stream);
  fclose(__stream);
  vm_main(&con);
  return 0;
}
