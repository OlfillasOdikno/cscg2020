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

# Maze - Map Radar - localo


**Category:** Gamehax
**Difficulty:** Medium        
**Author:** LiveOverflow

## Description
>There are rumours of a player who found a secret place and walks in a weird pattern. A radar map could be useful.
>
>See also: maze.liveoverflow.com
## Summery
The author provided a game called `maze` we have to solve some challenges to get the flags.
As the title says, we have to implement a radar.

## Solution
I wrote a parser for the npc position packets and dumped the map using Ninja Ripper [link](http://cgig.ru/ninjaripper/), filtered the maze tiles, imported it into blender and rendered it to a png using a top view. I cleaned it up using Gimp and exported it to a `64x64` bmp.

<style>
.map{
  width: 400px;
  image-rendering: pixelated;
}
</style>
@import "map.bmp" {class="map"}

The ingame maze is roughly `480x480`, we have to add some offsets to the position, I calculated those by flying to the edges.
The implementation of the map was not that gard for me, since I wrote something similar for CS:GO [Youtube](https://www.youtube.com/watch?v=nn_hD1-Xe5Q&t=108s).
I noticed a player, who was under the map, walking a weird pattern, the uid is `-0x1337`, I wrote a tracer and got the flag.
@import "trace.png"

## Mitigation
- don't exchange valuable information over a game?!

## Flag
CSCG{RADAR_HACK_XYZ}