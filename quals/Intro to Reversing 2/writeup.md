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

# Intro to Reversing 2 - localo


**Category:** Reverse Engineering       
**Difficulty:** Baby        
**Author:** 0x4d5a
**Dependencies:** Intro to Reversing 1 

## Description
>This is a introductory challenge for beginners which are eager to learn reverse engineering on linux. The three stages of this challenge will increase in difficulty. But for a gentle introduction, we have you covered: Check out the video of LiveOverflow or follow the authors step by step guide to solve the first part of the challenge.
>
>Once you solved the challenge locally, grab your real flag at: nc hax1.allesctf.net 9601
>
>Note: Create a dummy flag file in the working directory of the rev1 challenge. The real flag will be provided on the server
## Summery
The author provided again a simple password checker. If the password is correct we get the flag. 

## Solution
1. Throw the binary in the `Ghidra-Decompiler`
```C
undefined8 main(void)
{
  int is_pass;
  ssize_t len;
  long in_FS_OFFSET;
  int i;
  char input [40];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  initialize_flag();
  puts("Give me your password: ");
  len = read(0,input,0x1f);
  input[(int)len + -1] = '\0';
  i = 0;
  while (i < (int)len + -1) {
    input[i] = input[i] + -0x77;
    i = i + 1;
  }
  is_pass = strcmp(input,&password);
  if (is_pass == 0) {
    puts("Thats the right password!");
    printf("Flag: %s",flagBuffer);
  }
  else {
    puts("Thats not the password!");
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```
2. Use ROT 119 base 256 on the byte array of the `password` use in the `strcmp`. As the function uses ROT -0x77 (decimal: 119) on our input. We can get the bytes by clicking on `password` in `Ghidra`.
@import "pass.png"
Python is here quite handy.
```Python
data = [0xFC,0xFD,0xEA,0xC0,0xBA,0xEC,0xE8,0xFD,0xFB,0xBD,0xF7,0xBE,0xEF,0xB9,0xFB,0xF6,0xBD,0xC0,0xBA,0xB9,0xF7,0xE8,0xF2,0xFD,0xE8,0xF2,0xFC]
print("".join(map(lambda x: chr((x+119)&0xFF),data)))

> sta71c_tr4n5f0rm4710n_it_is
```
3. Get the flag:
```shell
$ nc hax1.allesctf.net 9601
Give me your password:
sta71c_tr4n5f0rm4710n_it_is
Thats the right password!
Flag: CSCG{1s_th4t_wh4t_they_c4ll_on3way_transf0rmati0n?}
```
## Mitigation
- check the hash of the password and use the plaintext as a decryption key for the program or something similar

## Flag
CSCG{1s_th4t_wh4t_they_c4ll_on3way_transf0rmati0n?}