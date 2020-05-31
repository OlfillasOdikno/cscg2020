import struct

from sqdef import *
from common import *

def parse_assembly(assembly):
    instructions = []
    for x in assembly.split("\n"):
        data = x.strip()
        if data and  data[0]!="#":
            data = data.split("a0:")
            op = data[0].strip()
            if op in name2op:
                op = name2op[op]
            else:
                print("UNKNOWN instruction: %s" %(op))
                return
            data = data[1].split("a1:")
            a0 = int(data[0].strip(),16)
            data = data[1].split("a2:")
            a1 = int(data[0].strip(),16)
            data = data[1].split("a3:")
            a2 = int(data[0].strip(),16)
            a3 = int(data[1].strip(),16)
            instructions.append(SQInstruction(op,a0,a1,a2,a3))
    return instructions

class SQFile:

    def __init__(self):
        self.data = bytearray()
        self.pos = 0

    def assemble(self,main,rawdata=bytearray(0)):
        self.write(b'\xFA\xFA')
        self.write(b'RIQS')
        self.write(struct.pack("I",1))
        self.write(struct.pack("I",8))
        self.write(struct.pack("I",4))
        self.write_function(main,data=rawdata)
        self.write(b'LIAT')


    def write_object(self,t,o):
        self.write(struct.pack("I",t))
        if t == tmap['OT_STRING']:
            self.write(struct.pack("Q",len(o)))
            if type(o) == str:
                self.write(o.encode())
            else:
                self.write(o)
        elif t == tmap['OT_INTEGER']:
            self.write(struct.pack("Q",o))
        elif t == tmap['OT_BOOL']:
            self.write(struct.pack("Q",1 if o else 0))
        elif t == tmap['OT_FLOAT']:
            self.write(struct.pack("f",self.read(4)))

    def write_function(self,fun,data=bytearray(0)):
        self.write(b'TRAP')
        self.write_object(tmap['OT_STRING'],fun.sourcename)
        self.write_object(tmap['OT_STRING'],fun.function_name)
        self.write(b'TRAP')

        self.write(struct.pack("Q",len(fun.literals)))
        self.write(struct.pack("Q",len(fun.parameters)))
        self.write(struct.pack("Q",len(fun.outervalues)))
        self.write(struct.pack("Q",len(fun.localvarinfos)))
        self.write(struct.pack("Q",len(fun.lineinfos) //16 ))
        self.write(struct.pack("Q",len(fun.defaultparams)//8))
        self.write(struct.pack("Q",len(fun.instructions)+((len(data) // 8) + (1 if len(data) % 8 != 0 else 0))))
        self.write(struct.pack("Q",len(fun.functions)))
        self.write(b'TRAP')


        for x in fun.literals:
            self.write_object(x[0],x[1])

        self.write(b'TRAP')

        
        for x in fun.parameters:
            self.write_object(x[0],x[1])

        self.write(b'TRAP')


        for x in fun.outervalues:
            self.write(struct.pack("Q",x[0]))
            self.write_object(x[1],x[2])
            self.write_object(tmap['OT_STRING'],x[3])
        
        self.write(b'TRAP')

        for x in fun.localvarinfos:
            self.write_object(x[0][0],x[0][1])
            self.write(struct.pack("QQQ",x[1],x[2],x[3]))
        
        self.write(b'TRAP')

        self.write(fun.lineinfos)

        self.write(b'TRAP')

        self.write(fun.defaultparams)

        self.write(b'TRAP')

        for ins in fun.instructions:
            self.write(struct.pack("iBBBB",ins.arg1,ins.op,ins.arg0,ins.arg2,ins.arg3))
        
        for x in range(len(data)+(len(data)%8)):
            if x < len(data):
                self.write(struct.pack('B',data[x]))
            else:
                self.write(b'\x00')

        self.write(b'TRAP')

        for x in fun.functions:
            self.write_function(x)
        
        self.write(struct.pack("q",fun.stack_size))
        self.write(struct.pack("B",1 if fun.is_generator else 0))
        self.write(struct.pack("Q",fun.var_params))

    def write1(self,val):
        self.pos+=1
        self.data+=val


    def write(self,data):
        self.pos+=len(data)
        self.data+= data 
    
if __name__ == "__main__":
    assembly="""
    LOADNULLS a0: 0x00 a1: 0x01 a2: 0x00 a3: 0x00
    LOADINT   a0: 0x01 a1: 0x41 a2: 0x00 a3: 0x00
    SETOUTER  a0: 0x01 a1: %x   a2: 0x01 a3: 0x00
    """%(-1)
    s = SQFile()
    t = tmap['OT_NATIVECLOSURE']
    main = SQFunction("h4x","name",var_params=1,stack_size=4,instructions=parse_assembly(assembly),literals=[])

    s.assemble(main)
    with open("test.cnut","wb") as f:
        f.write(s.data)