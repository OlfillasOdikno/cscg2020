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

# Intro to Pwning 1 - localo

**Category:** Pwn       
**Difficulty:** Baby        
**Author:** LiveOverflow      

## Description
>This is a introductory challenge for exploiting Linux binaries with memory corruptions. Nowodays there are quite a few mitigations that make it not as straight forward as it used to be. So in order to introduce players to pwnable challenges, LiveOverflow created a video walkthrough of the first challenge. An alternative writeup can also be found by 0x4d5a. More resources can also be found here.
>
>Service running at: hax1.allesctf.net:9100

## Summery
This is the writeup for the first part of the `Intro to Pwning` series. The author provided a Docker-Compose setup for all three challenges. 
The program asks the user for a name and for a spell using a personalized message for the user and says that we are a `Hufflepuff`. If the spell is `Expelliarmus` the program returns `~ Protego!` otherwise it tells us that we loose 10 Points.

## Solution
@import "pwn.png"
I tried to speedrun the three pwn challenges therefore I tried to solve them with minimal effort. I wrote a handy ROP template some time ago so that I just have to get the offsets right. 

We have the source code to all challenges.

The code  has two vulnerable functions:
<style>
.code1 .line-numbers-rows > span:nth-child(1){
	counter-reset: linenumber 37;
}

.code2 .line-numbers-rows > span:nth-child(1){
	counter-reset: linenumber 47;
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
@import "pwn1.c" {as="c" class="line-numbers code1" line_begin=37 line_end=46}
The code above is actually vulnerable to two attacks, a stack-buffer overflow using the `gets` function on the `read_buf` buffer. This alone would be enough for an exploit, but due to `ASLR` the chance of success is quite low, because we need to hit the right address when overwriting the return pointer which we can just guess. Luckily the code is vulnerable to another attack which allows us leak some data. 

### Format String

The **format string** attack abuses the way formatting works in function like `printf, snprintf, fprintf, ...` those functions take a format specifier as their first argument and use this to represent the next arguments. We can lookup the calling convention on wikipedia. 

#### System V AMD64 ABI
The calling convention of the System V AMD64 ABI is followed on Solaris, Linux, FreeBSD, macOS, and is the de facto standard among Unix and Unix-like operating systems. The `first six integer or pointer arguments are passed in registers RDI, RSI, RDX, RCX, R8, R9` (R10 is used as a static chain pointer in case of nested functions, while XMM0, XMM1, XMM2, XMM3, XMM4, XMM5, XMM6 and XMM7 are used for the first floating point arguments. As in the Microsoft x64 calling convention, `additional arguments are passed on the stack`. 
**Source**: [wikipedia](
https://en.wikipedia.org/w/index.php?title=X86_calling_conventions&oldid=947471460#System_V_AMD64_ABI)

Using this attack we can read the contents of those Registers (except for RDI which is used for the format specifier) and we can read the content of the stack. 

Here is the output of `telescope` (which prints a fancy back-trace) inside of `printf`.
@import "telescope.html" {class="telescope"}

As you can see there are many interesting addresses to leak, we could leak the return address of `welcome` (*22*) and calculate the base address of `pwn1`, but I decided to go for `__libc_start_main+231` (*26*) as the address can be used to calculate the base address for libc, which in return we can use to build a ROP chain which does not depend on the program and therefore use for the other `pwnintro` challenges.
We can find the right offset by using `%(0x5+0xn)$p` where `n` is the offset of the `telescope output`. Which results in `%43$p`.

```
Enter your witch name:
%43$p
┌───────────────────────┐
│ You are a Hufflepuff! │
└───────────────────────┘
0x7f1b0a12db97 enter your magic spell:

-10 Points for Hufflepuff!
```

We have address `0x7f1b0a12db97` for `__libc_start_main+231` and if we take a look at the virtual memory map:
@import "vmmap.html"

we can see that libc is loaded at `0x7f1b0a10c000`

which results in the offset `0x7f1b0a12db97-0x7f1b0a10c000=0x21b97`

Before I continue we should take a look at the second vulnerable function:
@import "pwn1.c" {as="c" class="line-numbers code2" line_begin=47 line_end=59}

Here we have the the same vulnerability, `gets` on a stack-buffer.

Here is a part of the man entry:

---

##### DESCRIPTION 

*Never use this function.*
`gets()` reads a line from stdin into the buffer pointed to by s until either a `terminating newline or EOF`, which it replaces with a null byte ('\0').  **No check for buffer overrun is performed** (see BUGS below).
[Source](http://man7.org/linux/man-pages/man3/gets.3.html#DESCRIPTION)

---

We just have to make sure our input does not contain newlines and `gets` will read it into and over the buffer. This comes quite handy as we have to pass the `strcmp(read_buf, "Expelliarmus")` check, because `_exit(0)` would not do a `ret`. The function tests if two char arrays match until the first nullbyte. Therefore our payload has to start with `Expelliarmus\x00`. 

I won't go too much into the details of `ROP`, basically it is a code reuse attack where code snippets end with a `ret` instruction. It is a bit more useful than `ret-2-libc`, because it can be used to do more complex stuff. For most pwn challenges it is enough to pop the address of `/bin/sh\x00` in `RDI` and call `system`.

`pwntools` has a function to search for gadgets.

With all this combined a script can be written to do the work for us.

I used my local libc for this, for the remote exploit we just have to adjust the offsets to the libc in the Docker container.

The padding can be calculated by using `cyclic` in the overflow , get the value of the return pointer and `cyclic_find` to get the offset. 

```shell
$ ./rop.py debug buffer_overflow
[...]
cyclic: 0x61616e63
```

@import "flag.html"

## Code
@import "rop.py"

## Mitigation
To mitigate this problem the following changes should be made:
- use `stack cookies`
- use safe functions like `read` to prevent buffer overflows
- never use printf on user controlled data, use `puts` or `printf("%s",data)`

## Flag
CSCG{NOW_PRACTICE_MORE}