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

# win_eXPerience 1 - localo


**Category:** Misc
**Difficulty:** Easy        
**Author:** TheVamp

## Description
>R3m3mb3r th3 g00d 0ld 1337 d4y5, wh3r3 3ncrypt10n t00l5 4r3 u53d, wh1ch 4r3 d34d t0d4y 4nd r3c0mm3nd b1tl0ck3r. H4v3 fun t0 f1nd th15 5m4ll g3m 1n th3 m3m0ry dump.
## Summery
The author provided a memory dump of a Windows XP machine.
We have to analyze it to get the flag.

## Solution
We can extract a `zip` archive from the memory dump, containing a file called `flag.txt`,  using `foremost`. But the archive is encrypted.
We need to get the password. I created a dictionary from the memorydump using strings and grep `strings memory.dmp > dict`. After that the archive can be cracked using `john the ripper`. 
```bash
$zip2john flag.zip > crackme && john crackme --wordlist=dict`
Using default input encoding: UTF-8
Loaded 1 password hash (ZIP, WinZip [PBKDF2-SHA1 256/256 AVX2 8x])
Will run 8 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
BorlandDelphiIsReallyCool (00225083.zip/flag.txt)
1g 0:00:00:00 DONE (2020-05-25 23:19) 1.204g/s 78959p/s 78959c/s 78959C/s ...OOOOOOOqqqqqq..X_^]
Use the "--show" option to display all of the cracked passwords reliably
Session completed
```
After extracting the file using the password `BorlandDelphiIsReallyCool`, we get the flag.

## Mitigation
- never let someone dump your memory, make sure to always hut down you system when you don't use it

## Flag
CSCG{c4ch3d_p455w0rd_fr0m_0p3n_tru3_cryp1_c0nt41n3r5}