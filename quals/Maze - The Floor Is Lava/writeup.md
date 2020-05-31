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

# Maze - The Floor Is Lava - localo


**Category:** Gamehax
**Difficulty:** Medium        
**Author:** LiveOverflow

## Description
>Reach the chest surrounded by dangerous lava.
>
>See also: maze.liveoverflow.com
## Summery
The author provided a game called `maze` we have to solve some challenges to get the flags.
There is a lava lake in the top right of the map, if we touch it, we die.

## Solution
We can use the same techniques as in `Maze Runner` to fly to the chest. The anti cheat does not check the y position. In my GUI just set the destination to the location of the chest, hit `TP` and get the flag. 

## Mitigation
- use better cheat detection, you could install a kernel mode ~~rootkit~~ driver for that 

## Flag
CSCG{FLYHAX_TOO_CLOSE_TO_THE_SUN!}