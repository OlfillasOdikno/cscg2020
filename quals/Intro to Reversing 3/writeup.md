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

# Intro to Reversing 3 - localo


**Category:** Reverse Engineering       
**Difficulty:** Baby        
**Author:** 0x4d5a
**Dependencies:** Intro to Reversing 2

## Description
>This is a introductory challenge for beginners which are eager to learn reverse engineering on linux. The three stages of this challenge will increase in difficulty. But for a gentle introduction, we have you covered: Check out the video of LiveOverflow or follow the authors step by step guide to solve the first part of the challenge.
>
>Once you solved the challenge locally, grab your real flag at: nc hax1.allesctf.net 9602
>
>Note: Create a dummy flag file in the working directory of the rev1 challenge. The real flag will be provided on the server
## Summery
The author provided again a simple password checker. If the password is correct we get the flag. 

## Solution
1. Throw the binary in the `Ghidra-Decompiler`
```C
undefined8 main(void)

{
  int iVar1;
  ssize_t len;
  long in_FS_OFFSET;
  int i;
  byte input [40];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  initialize_flag();
  puts("Give me your password: ");
  len = read(0,input,0x1f);
  input[(int)len + -1] = 0;
  i = 0;
  while (i < (int)len + -1) {
    input[i] = input[i] ^ (char)i + 10U;
    input[i] = input[i] - 2;
    i = i + 1;
  }
  iVar1 = strcmp((char *)input,"lp`7a<qLw\x1ekHopt(f-f*,o}V\x0f\x15J");
  if (iVar1 == 0) {
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
2. This time the algorithm is a bit more complex, but still easy to just reverse. Just use the inverse operation, and go from the back.
Python is nice again:
```Python
data = b"lp`7a<qLw\x1ekHopt(f-f*,o}V\x0f\x15J"
print("".join(chr((data[i]+2)^(i+10)&0xff) for i in range(len(data))))

> dyn4m1c_k3y_gen3r4t10n_y34h
```
3. Get the flag:
```shell
$ nc hax1.allesctf.net 9602
Give me your password:
dyn4m1c_k3y_gen3r4t10n_y34h
Thats the right password!
Flag: CSCG{pass_1_g3ts_a_x0r_p4ss_2_g3ts_a_x0r_EVERYBODY_GETS_A_X0R}
```
## Mitigation
- check the hash of the password and use the plaintext as a decryption key for the program or something similar

## Flag
CSCG{pass_1_g3ts_a_x0r_p4ss_2_g3ts_a_x0r_EVERYBODY_GETS_A_X0R}