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

# Intro to Reversing 1 - localo


**Category:** Reverse Engineering       
**Difficulty:** Baby        
**Author:** 0x4d5a      

## Description
>This is a introductory challenge for beginners which are eager to learn reverse engineering on linux. The three stages of this challenge will increase in difficulty. But for a gentle introduction, we have you covered: Check out the video of LiveOverflow or follow the authors step by step guide to solve the first part of the challenge.
>
>Once you solved the challenge locally, grab your real flag at: nc hax1.allesctf.net 9600
>
>Note: Create a dummy flag file in the working directory of the rev1 challenge. The real flag will be provided on the server

## Summery
The author provided a simple password checker. If the password is correct we get the flag. 

## Solution
1. Just use `strings` on the binary and grab the password.
```shell
$ strings rev1
/lib64/ld-linux-x86-64.so.2
libc.so.6
exit
fopen
puts
__stack_chk_fail
printf
[...]
Give me your password:
y0u_5h3ll_p455
Thats the right password!
Flag: %s
Thats not the password!
./flag
[...]
```
2. Use the string that is most 1337:
`y0u_5h3ll_p455`
3. Get the flag:
```shell
$ nc hax1.allesctf.net 9600
Give me your password:
y0u_5h3ll_p455
Thats the right password
Flag: CSCG{ez_pz_reversing_squ33zy}
```
4. write a writeup
## Mitigation
- check the hash of the password and use the plaintext as a decryption key for the program or something similar

## Flag
CSCG{ez_pz_reversing_squ33zy}