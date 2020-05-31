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

# Maze - Emoji - localo


**Category:** Gamehax
**Difficulty:** Easy        
**Author:** LiveOverflow

## Description
>Only real hackers can use secret emojis.
>
>See also: maze.liveoverflow.com
## Summery
The author provided a game called `maze` we have to solve some challenges to get the flags.
Inside the game the players can communicate by emoji. To get the flag we have to send the hidden flag emoji. 

## Solution
I used `Il2CppDumper` [link](https://github.com/Perfare/Il2CppDumper) to dump the game code. The code can then be examined by using IDA or Ghidra. I reverse engineered the netcode and wrote a simple proxy. After decrypting the packets using the following function:
```python
def decode(data):
    dec=bytearray((len(data)-2))
    key = data[0]
    for i in range(2,len(data)):
        dec[i-2]=data[i]^key
        key = (key+data[1])%0xFF
    return dec
```
We get packets in the form `id[secret]data`. The emoji packet has the id `69` and is structured like this:
```
id  secret          emoji_id
69|AABBCCDDEEFF0011|04
```
We can inject our own packet and set emoji_id to 13 to get the flag.
I implemented the command `emoji` to do that.
@import "emoji.png"

## Mitigation
- always verify client data

## Flag
CSCG{Your_hack_got_reported_to_authorities!}