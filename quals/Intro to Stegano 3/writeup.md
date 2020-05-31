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

# Intro to Stegano 3 - localo


**Category:** Stegano
**Difficulty:** Baby        
**Author:** explo1t

## Description
>This is an introductory challenge for the almighty steganography challenges. The three stages contain very different variants of hidden information. Find them!
## Summery
The author provided a `chall.png`.

## Solution
1. Use foremost to extract embedded `zip` archive 
2. Use stego tool to browse bitplanes and extract password: `s33_m3_1f_y0u_c4n`
3. use password to extract `flag.txt` from `zip` archive
4. cat `flag.txt`
## Mitigation
- write a poem as the password, nobody will try to use that as password

## Flag
CSCG{H1dden_1n_pla1n_s1ght}