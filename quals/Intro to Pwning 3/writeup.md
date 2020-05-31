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

# Intro to Pwning 3 - localo


**Category:** Pwn       
**Difficulty:** Baby        
**Author:** LiveOverflow      
**Dependencies:** Intro to Pwning 2      

## Description
>This is a introductory challenge for exploiting Linux binaries with memory corruptions. Nowodays there are quite a few mitigations that make it not as straight forward as it used to be. So in order to introduce players to pwnable challenges, LiveOverflow created a video walkthrough of the first challenge. An alternative writeup can also be found by 0x4d5a. More resources can also be found here.
>
>Service running at: hax1.allesctf.net:9102

## Summery
This is the writeup for the third part of the `Intro to Pwning` series. This writeup depends on my writeup for `Intro to Pwning 2`.
The code for the third part is the same as for the second part, except that we are now a `Gryffindor` and the program asks for the flag of the second part. 

## Solution
The exploit of the writeup for the last part works after changing the flag and pointing it to the right server. This writeup would have close to no content and that's why I decided to omit one detail in the other writeups. 
The code contains a function that is never called: `WINgardium_leviosa`

<style>
.code1 .line-numbers-rows > span:nth-child(1){
	counter-reset: linenumber 51;
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
The one from `pwn2.c` and `pwn1.c`
@import "pwn2.c" {as="c" class="line-numbers code1" line_begin=51 line_end=57}


And the one from `pwn3.c`
@import "pwn3.c" {as="c" class="line-numbers code1" line_begin=51 line_end=57}

As I mentioned in my writeup for `Intro to Pwning 3` I wanted to speedrun the challenges. Therefore I took a look at all three parts before starting.
The first two parts had a `gadget` that calls `system("/bin/sh")` for us, therefore it would have been possible to leak the return address of `welcome` and calculate the base address of the `pwn1/2` instead. The buffer overflow would have written the address of `WINgardium_leviosa` and it would spawn a shell.

For part three this gadget is not anymore. But there is no need for ROP, we could have jumped back to `welcome` and written the address of `system` in the `got` entry for `printf` using the `%n` format specifier, returned back to `welcome` again and used `/bin/sh` as our name to spawn a shell. But the use of `printf` to write addresses can result in many chars to print to `stdout` and involves more math than just `leak-offset`.
And that is why I decided to go for ROP.

@import "flag.html"

## Code
@import "rop.py"

## Mitigation
- use safe functions like `read` to prevent buffer overflows
- never use printf on user controlled data, use `puts` or `printf("%s",data)`

## Flag
CSCG{VOLDEMORT_DID_NOTHING_WRONG}