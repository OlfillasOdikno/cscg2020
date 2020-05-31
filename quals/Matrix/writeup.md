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

# Matrix - localo


**Category:** Stegano
**Difficulty:** Hard        
**Author:** explo1t

## Description
>Thｉs is ｙouｒ last chaｎcｅ. Afｔｅr this, there is no turning back. You take the blue pill, the story ends, you wake up in your bed and believe whatever you want to believe. You take the red pill, you stay in Wonderland, and I show you how deep the rabbit hole goes. Remember, all I'm offering is the flag. Nothing more.
## Summery
The author provided a `matrix.7z`.


## Solution
1. extract `matrix.7z` to get `matrix.wav`
2. use Spectrogram viewer to get password
@import "spec.png"
3. use `steghide --extract -p "Th3-R3D-P1ll?" -sf matrix.wav` to extract `redpill.jpg` from `matrix.wav`
4. reverse image search `redpill.jpg` and diff with the original
@import "diff.png"
5. interpret the lights as binary and decode to ascii
```
01101110
00100001
01000011
00110011
01011111
01010000
01010111
00111111
--------
n!C3_PW?
```
6. use `foremost` to extract `zip` archive from `redpill.jpg` and use the password to extract it
7. decode `secret.txt` with `base85`
`6W6?BHW,#BB/FK[?VN@u2e>m8 -> CSCG{St3g4n0_M4s7eR}`

## Mitigation
- add more layers and do back references, everybody will like this

## Flag
CSCG{St3g4n0_M4s7eR}