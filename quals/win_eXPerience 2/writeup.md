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

# win_eXPerience 2 - localo


**Category:** Misc
**Difficulty:** Medium        
**Author:** TheVamp

## Description
>R3m3mb3r th3 g00d 0ld 1337 d4y5, wh3r3 3ncrypt10n t00l5 4r3 u53d, wh1ch 4r3 d34d t0d4y 4nd r3c0mm3nd b1tl0ck3r. H4v3 fun t0 f1nd th15 5m4ll g3m 1n th3 m3m0ry dump.
## Summery
The author provided a memory dump of a Windows XP machine.
We have to analyze it to get the flag, but this time we need to look deeper.
## Solution
We can use volatility to get a list of running processes:
```bash 
Volatility Foundation Volatility Framework 2.6
Offset(V)  Name                    PID   PPID   Thds     Hnds   Sess  Wow64 Start                          Exit
---------- -------------------- ------ ------ ------ -------- ------ ------ ------------------------------ ------------------------------
0x81bcca00 System                    4      0     53      262 ------      0
0x81a04da0 smss.exe                340      4      3       21 ------      0 2020-03-22 18:27:38 UTC+0000
0x81a46928 csrss.exe               496    340      9      387      0      0 2020-03-22 18:27:39 UTC+0000
0x81a41950 winlogon.exe            524    340     19      428      0      0 2020-03-22 18:27:39 UTC+0000
0x8197eda0 services.exe            632    524     16      262      0      0 2020-03-22 18:27:39 UTC+0000
0x81a2d810 lsass.exe               644    524     23      356      0      0 2020-03-22 18:27:39 UTC+0000
0x81a0cda0 VBoxService.exe         792    632      9      118      0      0 2020-03-22 18:27:39 UTC+0000
0x81a16500 svchost.exe             840    632     20      204      0      0 2020-03-22 18:27:39 UTC+0000
0x81abf9a8 svchost.exe             928    632      9      259      0      0 2020-03-22 18:27:39 UTC+0000
0x81abd0f0 svchost.exe            1024    632     67     1298      0      0 2020-03-22 18:27:39 UTC+0000
0x8194dc70 svchost.exe            1076    632      6       74      0      0 2020-03-22 18:27:39 UTC+0000
0x817da020 svchost.exe            1120    632     18      219      0      0 2020-03-22 18:27:39 UTC+0000
0x817b33c0 explorer.exe           1524   1484     14      353      0      0 2020-03-22 18:27:40 UTC+0000
0x817b2318 spoolsv.exe            1536    632     14      113      0      0 2020-03-22 18:27:40 UTC+0000
0x81794608 VBoxTray.exe           1644   1524     12      122      0      0 2020-03-22 18:27:40 UTC+0000
0x817cd690 ctfmon.exe             1652   1524      1       66      0      0 2020-03-22 18:27:40 UTC+0000
0x81791020 msmsgs.exe             1660   1524      4      169      0      0 2020-03-22 18:27:40 UTC+0000
0x8173ec08 CSCG_Delphi.exe        1920   1524      1       29      0      0 2020-03-22 18:27:45 UTC+0000
0x8176c378 mspaint.exe             264   1524      4      102      0      0 2020-03-22 18:27:48 UTC+0000
0x8172abc0 svchost.exe             548    632      8      129      0      0 2020-03-22 18:27:51 UTC+0000
0x81759820 alg.exe                1176    632      6      100      0      0 2020-03-22 18:27:51 UTC+0000
0x816e41f0 svchost.exe            1688    632      9       93      0      0 2020-03-22 18:28:00 UTC+0000
0x816d8438 TrueCrypt.exe           200   1524      1       44      0      0 2020-03-22 18:28:02 UTC+0000
0x81768310 wuauclt.exe            1300   1024      7      174      0      0 2020-03-22 18:28:35 UTC+0000
0x817a9b28 wscntfy.exe            1776   1024      1       36      0      0 2020-03-22 18:28:51 UTC+0000
0x816d8cd8 wpabaln.exe             988    524      1       66      0      0 2020-03-22 18:29:38 UTC+0000
```
There are many interesting processes, but for this flag  we need to examine `CSCG_Delphi.exe`. We can extract the executable using `vol procdump -p 1920`. Immediately Windows-Defender deletes it. We can load the executable into `Ghidra` to analyze it. As the name implies, the executable is a Delphi executable. There is a project called IDR [Github](https://github.com/crypto2011/IDR) that can extract symbols for us. We can use another tool `dhrake`[Github](https://github.com/huettenhain/dhrake/) to load them into ida. There is a function that checks if the input is the flag. It checks if the first characters are `CSCG{` and if the last character is `}` after that, it splits the content inside the curly brackets at `_` reverses them using `AnsiReverseString` and calculates the MD5 hash using `TIdHash128.HashValue`. The hashes are then checked against pre computed hashes, if they match we have the flag. We can throw the hashes into some online crackers.
```
1efc99b6046a0f2c7e8c7ef9dc416323:dl0
25db3350b38953836c36dfb359db4e27:kc4rc
40a00ca65772d7d102bb03c3a83b1f91:!3m
c129bd7796f23b97df994576448caa23:l00hcs
017efbc5b1d3fb2d4be8a431fa6d6258:1hp13d
```
And reversed we get the following parts:
```
0ld
cr4ck
m3!
sch00l
d31ph1
```

We can now either use the disassembly to get the order or just guess it and join the ordered parts with `_` and wrap it with the flag format.
`CSCG{0ld_sch00l_d31ph1_cr4ck_m3!}`


## Mitigation
- hash the complete string and use a modern hash algorithm
- you should also consider to up~~date~~grade Windows, but this could take ages

## Flag
CSCG{0ld_sch00l_d31ph1_cr4ck_m3!}