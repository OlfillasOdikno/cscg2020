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

# Intro to Crypto 2 - localo


**Category:** Crypto
**Difficulty:** Baby        
**Author:** black-simon

## Description
>This is an introductory challenge for beginners which want to dive into the world of Cryptography. The three stages of this challenge will increase in difficulty.
>
>I learned my lesson from the mistakes made in the last challenge! Now p and q are huge, I promise!
## Summery
The author provided a `message.txt` and a `pubkey.pem` 
The `message.txt` contains just a number and the `pubkey.pem` is a public key. All we have to do is to decrypt the `message.txt`.

## Solution
We need to factor `N`. `Factordb` has not factored it. From the description I expected, that they have roughly the same length and used `Fermat's factorization method` [Wikipedia](https://en.wikipedia.org/wiki/Fermat%27s_factorization_method)
@import "solve.sage" {as="python" code_block=true class="line-numbers"}

## Mitigation
- never roll your own crypto
- use large primes of different length

## Flag
CSCG{Ok,_next_time_I_choose_p_and_q_random...}