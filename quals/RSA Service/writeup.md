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
**Difficulty:** Hard        
**Author:** black-simon

## Description
> What did you say?
>
> nc hax1.allesctf.net 9400
## Summery
The author provided a script `server.py` we send a private key to decrypt a fixed message: `Quack! Quack!` if this message decrypts to a sentence chosen by the author we get the flag.

## Solution
My first approach was to come up with a general solution.
$$ m \equiv c^d\ (\textrm{mod}\ N)$$ Since we control $d$ and $N$ a simple solution is:
$$ m \equiv c^k\ (\textrm{mod}\ c^k - m) $$ And since for every divisor $ t $ of $ N $
$$ m \equiv c^d\ (\textrm{mod}\ t) $$ is a solution, we "just" need to factor $  c^k - m$ and if we find two prime-factors with their product is greater than $m$ we should get the flag. I factored it up to $k = 6$, but had no luck and the process was quite time consuming, therefore I knew it was not the ideal solution. I did some google searches and found this [writeup](https://blog.skullsecurity.org/2020/bsidessf-ctf-choose-your-own-keyventure-rsa-debugger-challenge) from this years `BSidesSF CTF` it is basically the same problem, I tried to understand what is going on, and I guess I kind of got it, but to be honest I had already thought about discrete logarithms, but I thought, that it would be even harder to solve it that way, I still don't get why there are those special cases and how they work and `I just copy-pasted the code` and did some automation.

@import "solve.sage" {as="python" code_block=true class="line-numbers"}

## Mitigation
- upgrade your google skills ;)
- don't trust user input

## Flag
CSCG{下一家烤鴨店在哪裡？}