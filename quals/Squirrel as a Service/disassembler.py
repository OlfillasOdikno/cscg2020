import struct

from sqdef import *
from common import *

class SQFile:

    def __init__(self, data):
        self.data = data
        self.pos = 0
        self.main = None

    def parse(self):
        magic = self.read(2)
        assert(magic == b'\xFA\xFA')
        head = self.read(4)
        assert(head == b'RIQS')
        [sz_sqchar] = struct.unpack("I", self.read(4))
        assert(sz_sqchar == 1)
        [sz_sqint] = struct.unpack("I", self.read(4))
        assert(sz_sqint == 8)
        [sz_sqfloat] = struct.unpack("I", self.read(4))
        assert(sz_sqfloat == 4)
        self.main = self.parse_function()
        tail = self.read(4)
        assert(tail == b'LIAT')

    def parse_object(self):
        [t] = struct.unpack("I", self.read(4))
        if t == tmap['OT_STRING']:
            [v] = struct.unpack("Q", self.read(8))
            return (t,self.read(v).decode())
        elif t == tmap['OT_INTEGER']:
            [v] = struct.unpack("Q", self.read(8))
            return (t,v)
        elif t == tmap['OT_BOOL']:
            [v] = struct.unpack("Q", self.read(8))
            return (t,v != 0)
        elif t == tmap['OT_FLOAT']:
            [v] = struct.unpack("f", self.read(4))
            return (t,v)
        elif t == tmap['OT_NULL']:
            return (t,None)

    def parse_function(self):
        part = self.read(4)
        assert(part == b'TRAP')
        sourcename = self.parse_object()[1]
        function_name = self.parse_object()[1]
        part = self.read(4)
        assert(part == b'TRAP')

        [n_literals] = struct.unpack("Q", self.read(8))
        [n_parameters] = struct.unpack("Q", self.read(8))
        [n_outervalues] = struct.unpack("Q", self.read(8))
        [n_localvarinfos] = struct.unpack("Q", self.read(8))
        [n_lineinfos] = struct.unpack("Q", self.read(8))
        [n_defaultparams] = struct.unpack("Q", self.read(8))
        [n_instructions] = struct.unpack("Q", self.read(8))
        [n_functions] = struct.unpack("Q", self.read(8))

        part = self.read(4)
        assert(part == b'TRAP')

        literals = []
        for _ in range(n_literals):
            literals.append(self.parse_object())

        part = self.read(4)
        assert(part == b'TRAP')

        parameters = []
        for _ in range(n_parameters):
            parameters.append(self.parse_object())

        part = self.read(4)
        assert(part == b'TRAP')

        outervalues = []
        for _ in range(n_outervalues):
            [t] = struct.unpack("Q", self.read(8))
            o = self.parse_object()
            name = self.parse_object()
            outervalues.append((name, o, t))

        part = self.read(4)
        assert(part == b'TRAP')

        localvarinfos = []
        for _ in range(n_localvarinfos):
            name = self.parse_object()
            [pos, start, end] = struct.unpack("QQQ", self.read(8*3))
            localvarinfos.append((name, pos, start, end))

        part = self.read(4)
        assert(part == b'TRAP')

        lineinfos = self.read(n_lineinfos*16)

        part = self.read(4)
        assert(part == b'TRAP')

        defaultparams = self.read(n_defaultparams*8)

        part = self.read(4)
        assert(part == b'TRAP')

        instructions = []
        for i in range(n_instructions):
            [arg1, op, arg0, arg2, arg3] = struct.unpack("iBBBB", self.read(8))
            ins = SQInstruction(op, arg0, arg1, arg2, arg3)
            instructions.append(ins)


        part = self.read(4)
        assert(part == b'TRAP')

        functions = []
        for _ in range(n_functions):
            functions.append(self.parse_function())

        [stack_size] = struct.unpack("Q", self.read(8))
        [is_generator] = struct.unpack("B", self.read(1))
        [var_params] = struct.unpack("Q", self.read(8))

        return SQFunction(sourcename,function_name,literals,parameters,outervalues,localvarinfos,lineinfos,defaultparams,instructions,functions,stack_size,is_generator,var_params)

    def read(self, n):
        b = self.pos+n
        data = self.data[self.pos:b]
        self.pos = b
        return data

    def __repr__(self):
        return "%r" % (self.main)

    


if __name__ == "__main__":
    with open("test.cnut", "rb") as f:
        data = f.read()

    f = SQFile(data)
    f.parse()
    print("%r" % (f))
