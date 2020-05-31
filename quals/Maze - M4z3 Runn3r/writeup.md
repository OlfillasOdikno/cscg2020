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

# Maze - M4z3 Runn3r - localo


**Category:** Gamehax
**Difficulty:** Hard        
**Author:** LiveOverflow

## Description
>Complete the scorch trials in under 5 seconds!
>
>See also: maze.liveoverflow.com
## Summery
The author provided a game called `maze` we have to solve some challenges to get the flags.
There is a little race we have to go quickly from checkpoint to checkpoint till the end in under 5 seconds.

## Solution
We have to find a bug in the anti cheat to gain more speed.
Since the anti cheat probably just checks if our current velocity is less than a certain threshold and we send a timestamp inside our position packet, we can just spoof the time difference to make the server think that our velocity is quite low.
$$ v = \frac{\Delta s}{\Delta t} $$
If $\Delta t $ is large, $v$ is small. I used `A*` to calculate my route. Inside the cheat UI the user has just to click inside the map to set the destination and hit the `TP` button to fast-travel to that point.

## Mitigation
- never trust client information

## Flag
CSCG{N3VER_TRUST_T1111ME}