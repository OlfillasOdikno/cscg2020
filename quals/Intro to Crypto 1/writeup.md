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

# Intro to Crypto 1 - localo


**Category:** Crypto
**Difficulty:** Baby        
**Author:** black-simon

## Description
>This is an introductory challenge for beginners which want to dive into the world of Cryptography. The three stages of this challenge will increase in difficulty. For an introduction to the first challenge visit the authors step by step guide.
>
>For my new RSA key I used my own SecurePrimeService which definitely generates a HUGE prime!
## Summery
The author provided a `message.txt` and a `pubkey.pem` 
The `message.txt` contains just a number and the `pubkey.pem` is a public key. All we have to do is to decrypt the `message.txt`.

## Solution
We need to factor `N`. `Factordb` has already fully factored it, one prime was quite small `622751`. I wrote a small `sage` script to decrypt the message and got the flag. 
@import "solve.sage" {as="python" code_block=true class="line-numbers"}

## Mitigation
- never roll your own crypto
- use large primes

## Flag
CSCG{factorizing_the_key=pr0f1t}