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

# Maze - Tower - localo


**Category:** Gamehax
**Difficulty:** Easy        
**Author:** LiveOverflow

## Description
>Find a path to reach the tower and climb to the top.
>
>See also: maze.liveoverflow.com
## Summery
The author provided a game called `maze` we have to solve some challenges to get the flags.
There is a little tower in the top left of the map, we have to get on top of it to get the flag. 
## Solution
I implemented a command into my cheat to teleport the player relative to their position, we can use the same techniques as in `The Floor Is Lava` to get under the tower and then use the command `tpr 0 100 0` to teleport on top of it.
## Mitigation
- pls fix cheat detection

## Flag
CSCG{SOLVED_THE_MAZE_LONG_WAY_BACK}