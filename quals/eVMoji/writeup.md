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

# eVMoji - localo

**Category:** Reverse Engineering       
**Difficulty:** Hard        
**Author:** 0x4d5a

## Description
> EMOJI HYPE 🔥💯
## Summery
A virtual machine was given that can run code created in a custom instruction set based on emoji. If you have ever written an emulator or a similar virtual machine, you get known to the structure of the code quite easily. `code.bin` is a simple program that asks for a password as input and prints the flag as output if the password is correct.

## Solution
I had multiple ideas how the challenge could be solved, one could write a `disassembler` and work through that, or use `symbolic execution` with tools like `angr`. **But I don't know angr**! (*even though it would be a good opportunity to learn it*) Maybe another day/challenge. And I am lazy. Therefore writing a disassembler and doing the `hard work to go through the disassembly` was also not what I wanted. This is a **ctf challenge**, therefore I wanted a `quick` and maybe not so clean solution, that `just works`.

I decided to write a `tracer`. A `tracer` has the advantage that we get `runtime information` instead of just static instructions. Using the great `decompiler from ghidra` and some analysis based renaming/retyping, the whole VM could be decompiled using the `to C code` export function of `ghidra`. The output has still to be cleaned up, but after some minutes the `C code` could be compiled and the generated program was able to interpret the provided `code.bin`. After that I made some patches to the VM to *debug* the code, `printf`, I was able to create some traces.

I won't go too much into the internals of the vm, but it has some 1kB `rwm`, 1kB `stack`, 64kB `code` and some sort of register. It has 11 opcodes and implementing, `or`, `xor`, `lsb`, `write to stdout`, `read from stdin`, `dup`, `shr`,`exit`, `test and jeq`, `push from code` and 2x `push from rwm` (int and ptr?).

`code.bin` reads 27 chars from stdin, performs `xor` operations on the first 23 chars of the input `or` it together and checks if the result matches `0x00`. Using just null bytes as the input, the first part of the flag is quite obvious. As we can ignore the `xor` and use the `or` operands. 
Here is the trace of `xor` and `or` with 27x `A` as input.
```
read: 27
41 ^ f2 = b3
9c ^ b3 = 2f
2f | 0 = 2f 
41 ^ ea = ab
d9 ^ ab = 72
72 | 2f = 7f 
[...]
41 ^ f5 = b4
9b ^ b4 = 2f
2f | 7f = 7f 
41 ^ a2 = e3
fd ^ e3 = 1e
1e | 7f = 7f 
0 == 7f
```  
And the trace with just `or` and null bytes as input.
```
read: 27
6e | 0 = 6e 
33 | 6e = 7f 
77 | 7f = 7f 
5f | 7f = 7f 
61 | 7f = 7f 
67 | 7f = 7f 
33 | 7f = 7f 
5f | 7f = 7f 
76 | 7f = 7f 
31 | 7f = 7f 
72 | 7f = 7f 
74 | 7f = 7f 
75 | 7f = 7f 
34 | 7f = 7f 
6c | 7f = 7f 
69 | 7f = 7f 
7a | 7f = 7f 
34 | 7f = 7f 
74 | 7f = 7f 
31 | 7f = 7f 
6f | 7f = 7f 
6e | 7f = 7f 
5f | 7f = 7f 
0 == 7f
```
The first operand of the `or` is the char for the flag:
```
n3w_ag3_v1rtu4liz4t1on_
```
Using this as the input for the program we get:
`Gotta go cyclic ♻️`
We are missing 4 bytes of the flag.
The trace shows this:
```
ffffffff >> 1 = 7fffffff
edb88320 ^ 7fffffff = 92477cdf
0 == 0
0 >> 1 = 0
0 == 1
92477cdf >> 1 = 4923be6f
edb88320 ^ 4923be6f = a49b3d4f
0 == 0
0 >> 2 = 0
0 == 1
a49b3d4f >> 1 = 524d9ea7
edb88320 ^ 524d9ea7 = bff51d87
[...]
cc0e8f0e >> 1 = 66074787
0 >> 31 = 0
0 == 1
66074787 >> 1 = 3303a3c3
edb88320 ^ 3303a3c3 = debb20e3
0 == 0
f40e845e ^ debb20e3 = 2ab5a4bd
0 == 2ab5a4bd
```
Some bit shifts, and `xor` operations. Using the trace operations and the input and output I wrote the algorithm in python to get a better understanding.
```python
o = 0xFFFFFFFF
p = 0
while p<32:
    if (n>>p) & 1 != o & 1:
        o = 0xedb88320 ^ (o>>1)
    else:
        o = o>>1
    p+=1
if o ^ 0xf40e845e == 0:
    print("[*] success")
else:
    print("[*] fail")
```
I was not able to work out a way to reverse that function, but `4 bytes` **is** `brute-force-able` and the limited charset should make it feasible for a crude script in python. I wrote a script that runs the algorithm for the lower-case ascii and digits range and the chars `_`, `\n`,`\x00` but without a result. After some rubber ducky debugging I did what you should always do if you are stuck, google the constants, in this case `0xedb88320` and google says crc32, but the output of the algorithm does not match any output of online crc32 generators. But after taking a look at the source code of a crc32 code for `C` I realized that the output is just negated. But in the program it is not. I just have to negate `0xf40e845e` to `0x0bf17ba1` and find 4 byte input for that crc32. Now I can use highly optimized software to brute-force the input. I used hashcat.
```bash
$ hashcat -m 11500 -a 3 --force 0bf17ba1:00000000 ?b?b?b?b
[...]
0bf17ba1:00000000:l0l?
[...]
```
The flag includes a question mark.
```bash
$ python -c "print('n3w_ag3_v1rtu4liz4t1on_l0l?')" | ./eVMoji code.bin
Welcome to eVMoji 😎
🤝 me the 🏳🏳️
Thats the flag: CSCG{n3w_ag3_v1rtu4liz4t1on_l0l?}
```
### Code
eVMoji.c
@import "eVMoji.c" {as="c" class="line-numbers"}
----
eVMoji.h
@import "eVMoji.h" {as="c" class="line-numbers"}
## Mitigation
In my opinion it is quite hard to say `mitigation` for a re challenge, because it kind of always results in some kind of obfuscation, but for password checking stuff you can always use `hashing and decryption of the program` using the original input. But that would result in a bad ctf challenge, I guess.

## Flag
CSCG{n3w_ag3_v1rtu4liz4t1on_l0l?}