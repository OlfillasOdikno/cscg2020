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

# Follow The White Rabbit - Cave - localo


**Category:** Gamehax
**Difficulty:** Easy        
**Author:** LiveOverflow

## Description
>Follow the white rabbit... into the hole. Game Trailer

## Summery
The author provides a unity game. Two flags are hidden inside it.

## Solution
We can use a uTinyRipper [Github](https://github.com/mafaca/UtinyRipper) to extract the game assets.
The flag is in `Assets/Texture2D/flag1.png`
@import "flag1.png"
## Mitigation
- don't hide valuable information in game assets

## Flag
CSCG{data_mining_teleport_or_gravity_patch?}