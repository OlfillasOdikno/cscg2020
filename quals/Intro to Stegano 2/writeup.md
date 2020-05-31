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

# Intro to Stegano 2 - localo


**Category:** Stegano
**Difficulty:** Baby        
**Author:** explo1t

## Description
>This is an introductory challenge for the almighty steganography challenges. The three stages contain very different variants of hidden information. Find them!
## Summery
The author provided a `chall.jpg`.

## Solution
1. Use reverse image search to find original image
2. Use online image diffing tool to get difference [link](https://www.diffchecker.com/image-diff)
@import "diff.png"
3. Decode the lights on/off in `chall.jpg` to binary
```
01000011
01010011
01000011
01000111
01111011
01100001
01011111
01000110
01101100
00110100
01100111
01111101
```
4. Decode it to ASCII
`CSCG{a_Fl4g}`
## Mitigation
- use own pictures

## Flag
CSCG{a_Fl4g}