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

# Follow The White Rabbit - Datamining - localo


**Category:** Gamehax
**Difficulty:** Hard        
**Author:** LiveOverflow
**Dependencies:** Follow The White Rabbit - Cave

## Description
>It looks like the prison is still under construction on the currently shipped game... But I heard somebody figured out, that early parts of the unreleased content accidentally leaked into this release! Can you find it and follow the white rabbit? Game Trailer
## Summery
The author provides a unity game. Two flags are hidden inside it.

## Solution
The second flag is in another scene, we need to overlay it on top of the standard scene.
I wrote a short `C#` library that can be injected using `SharpMonoInjector` I used `Cheat-Engine` to get all necessary information. (The `dissect mono` option is quite handy)
I implemented a `console` and a `teleport` and `load` command.
The `load` command just overlays the two scenes.
I went to the coordinates `-83 205 24` and pressed `F3` to open the console, used the `load` command and `tp -83 217 24`, walked to the display and got the flag.
## Mitigation
- don't leak game content ;)

## Flag
CSCG{03ASY_teleport_and_datamining_scenes}