from sqdef import *

class SQInstruction:

    def __init__(self, op, arg0, arg1, arg2, arg3=0):
        self.op = op
        self.arg0 = arg0
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3

    def __repr__(self):
        if self.op in op2name:
            op_name = "%s" % op2name[self.op]
        else:
            op_name = "UNKNOWN_%d" % self.op
        return "%-20s a0: 0x%02x a1: %s0x%08x a2: 0x%02x a3: 0x%02x" % (op_name, self.arg0, "-" if self.arg1 <0 else " ",abs(self.arg1), self.arg2, self.arg3)


class SQFunction:

    def __init__(self, sourcename="h4x", function_name="h4x", literals=[], parameters=[], outervalues=[], localvarinfos=[], lineinfos=b'', defaultparams=b'', instructions=[], functions=[],stack_size=0x8,is_generator=False,var_params=1):
        self.sourcename = sourcename
        self.function_name = function_name
        self.literals = literals
        self.parameters = parameters
        self.outervalues = outervalues
        self.localvarinfos = localvarinfos
        self.lineinfos = lineinfos
        self.defaultparams = defaultparams
        self.instructions = instructions
        self.functions = functions
        self.stack_size = stack_size
        self.is_generator= is_generator
        self.var_params = var_params
        super().__init__()

    def __repr__(self):
        ret = "*********************************************************************\n"
        ret+=" - Function: %s\n" % (self.function_name)
        ret+="\n - Literals: \n"
        for idx,x in enumerate(self.literals):
            ret+= "[%03d] %r\n"%(idx,x[1])
        ret+="\n - Instructions: \n"
        for idx, x in enumerate(self.instructions):
            ret += "[%03d] %r\n"  %(idx+1,x)
        ret += "*********************************************************************\n"
        return ret
