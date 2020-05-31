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

# Intro to Stegano 1 - localo


**Category:** Stegano
**Difficulty:** Baby        
**Author:** explo1t

## Description
>This is an introductory challenge for the almighty steganography challenges. The three stages contain very different variants of hidden information. Find them!
## Summery
The author provided a `chall.jpg`.

## Solution
Its the typical passphrase for some stegotool in file challenge.
`strings -n8 chall.jpg | while read p; do steghide --extract -f -p "$p" -sf chall.jpg 2>/dev/null; done ; cat flag.txt` 
## Mitigation
- use more unknown stego tools
- don't put stego password into file without stegoing it

## Flag
CSCG{Sup3r_s3cr3t_d4t4}