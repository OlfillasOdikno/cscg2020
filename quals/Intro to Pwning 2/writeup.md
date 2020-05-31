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

# Intro to Pwning 2 - localo

**Category:** Pwn       
**Difficulty:** Baby        
**Author:** LiveOverflow      
**Dependencies:** Intro to Pwning 1      

## Description
>This is a introductory challenge for exploiting Linux binaries with memory corruptions. Nowodays there are quite a few mitigations that make it not as straight forward as it used to be. So in order to introduce players to pwnable challenges, LiveOverflow created a video walkthrough of the first challenge. An alternative writeup can also be found by 0x4d5a. More resources can also be found here.
>
>Service running at: hax1.allesctf.net:9101

## Summery
This is the writeup for the second part of the `Intro to Pwning` series. This writeup depends on my writeup for `Intro to Pwning 1`.
The code for the second part is the same as for the first part, except that we are now a `Ravenclaw` and the program asks for the flag of the first part. But more important it has stack-protector enabled, this is the first mitigation I suggested. 

## Solution
With the preparation done in the last writeup the only thing that is needed is to leak the stack cookie and use that in the buffer-overflow.

We can again use `telescope` to get the right offset.
<style>
.ansi2html-content{
	background-color: transparent !important;
	padding: 0;
}
body > div > div{
	background-color: #323232;
	padding: 1em;
}
</style>
@import "telescope.html"

The stack cookie is the random looking thing (*22*)

We can leak it like we leak `__libc_start_main+231`

Our payload should be something like `%45$p %39$p` the first one will leak `__libc_start_main+231` (`0x05+0x28=45`) and the second one will leak the stack cookie (`0x05+0x22=39`)

With minimal changes to the exploit of `Intro to Pwning 1` the exploit just works.
**Caution: The flag in the C code does not match the flag in the binary, use `strings` to get it**

@import "flag.html"

## Code
@import "rop.py"

## Mitigation
- use safe functions like `read` to prevent buffer overflows
- never use printf on user controlled data, use `puts` or `printf("%s",data)`

## Flag
CSCG{NOW_GET_VOLDEMORT}