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

# Intro to Crypto 3 - localo


**Category:** Crypto
**Difficulty:** Baby        
**Author:** black-simon

## Description
>This is an introductory challenge for beginners which want to dive into the world of Cryptography. The three stages of this challenge will increase in difficulty.
>
>After a new potentially deadly disease first occurring in Wuhan, China, the Chinese Corona Response Team sends messages to the remainder of the world. However, to avoid disturbing the population, they send out this message encrypted.
>
>We have intercepted all messages sent by the Chinese government and provide you with the public keys found on the governments' website.
>
>Please, find out if we are all going to die!
## Summery
The author provided a `intercepted-messages.txt` and three `.pem` files. 
The `intercepted-messages.txt` contains three numbers and the `.pem` files contains three public keys. All we have to do is to decrypt the messages.

## Solution
Since `e` is 3 in all public keys and we have three message-key pairs, we can use the `Håstad's_broadcast_attack` [Wikipedia](https://en.wikipedia.org/wiki/Coppersmith%27s_attack#H%C3%A5stad%27s_broadcast_attack)
@import "solve.sage" {as="python" code_block=true class="line-numbers"}

## Mitigation
- never roll your own crypto
- use larger exponents
- use different messages

## Flag
CSCG{ch1nes3_g0vernm3nt_h4s_n0_pr0blem_w1th_c0ron4}