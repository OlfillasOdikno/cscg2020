SQUIRREL_VERSION_NUMBER =  310

SQ_BYTECODE_STREAM_TAG = 0xFAFA
SQOBJECT_REF_COUNTED   = 0x08000000
SQOBJECT_NUMERIC       = 0x04000000
SQOBJECT_DELEGABLE     = 0x02000000
SQOBJECT_CANBEFALSE    = 0x01000000
SQ_MATCHTYPEMASKSTRING = (-99999)
_RT_MASK = 0x00FFFFFF
_RT_NULL           = 0x00000001
_RT_INTEGER        = 0x00000002
_RT_FLOAT          = 0x00000004
_RT_BOOL           = 0x00000008
_RT_STRING         = 0x00000010
_RT_TABLE          = 0x00000020
_RT_ARRAY          = 0x00000040
_RT_USERDATA       = 0x00000080
_RT_CLOSURE        = 0x00000100
_RT_NATIVECLOSURE  = 0x00000200
_RT_GENERATOR      = 0x00000400
_RT_USERPOINTER    = 0x00000800
_RT_THREAD         = 0x00001000
_RT_FUNCPROTO      = 0x00002000
_RT_CLASS          = 0x00004000
_RT_INSTANCE       = 0x00008000
_RT_WEAKREF        = 0x00010000
_RT_OUTER          = 0x00020000

tmap={
    'OT_NULL' :          _RT_NULL|SQOBJECT_CANBEFALSE,
    'OT_INTEGER' :       _RT_INTEGER|SQOBJECT_NUMERIC|SQOBJECT_CANBEFALSE,
    'OT_FLOAT' :         _RT_FLOAT|SQOBJECT_NUMERIC|SQOBJECT_CANBEFALSE,
    'OT_BOOL' :          _RT_BOOL|SQOBJECT_CANBEFALSE,
    'OT_STRING' :        _RT_STRING|SQOBJECT_REF_COUNTED,
    'OT_TABLE' :         _RT_TABLE|SQOBJECT_REF_COUNTED|SQOBJECT_DELEGABLE,
    'OT_ARRAY' :         _RT_ARRAY|SQOBJECT_REF_COUNTED,
    'OT_USERDATA' :      _RT_USERDATA|SQOBJECT_REF_COUNTED|SQOBJECT_DELEGABLE,
    'OT_CLOSURE' :       _RT_CLOSURE|SQOBJECT_REF_COUNTED,
    'OT_NATIVECLOSURE' : _RT_NATIVECLOSURE|SQOBJECT_REF_COUNTED,
    'OT_GENERATOR' :     _RT_GENERATOR|SQOBJECT_REF_COUNTED,
    'OT_USERPOINTER' :   _RT_USERPOINTER,
    'OT_THREAD' :        _RT_THREAD|SQOBJECT_REF_COUNTED,
    'OT_FUNCPROTO' :     _RT_FUNCPROTO|SQOBJECT_REF_COUNTED,
    'OT_CLASS' :         _RT_CLASS|SQOBJECT_REF_COUNTED,
    'OT_INSTANCE' :      _RT_INSTANCE|SQOBJECT_REF_COUNTED|SQOBJECT_DELEGABLE,
    'OT_WEAKREF' :       _RT_WEAKREF|SQOBJECT_REF_COUNTED,
    'OT_OUTER' :         _RT_OUTER|SQOBJECT_REF_COUNTED,
}

name2op={
'LINE':               0x00,
'LOAD':               0x01,
'LOADINT':            0x02,
'LOADFLOAT':          0x03,
'DLOAD':              0x04,
'TAILCALL':           0x05,
'CALL':               0x06,
'PREPCALL':           0x07,
'PREPCALLK':          0x08,
'GETK':               0x09,
'MOVE':               0x0A,
'NEWSLOT':            0x0B,
'DELETE':             0x0C,
'SET':                0x0D,
'GET':                0x0E,
'EQ':                 0x0F,
'NE':                 0x10,
'ADD':                0x11,
'SUB':                0x12,
'MUL':                0x13,
'DIV':                0x14,
'MOD':                0x15,
'BITW':               0x16,
'RETURN':             0x17,
'LOADNULLS':          0x18,
'LOADROOT':           0x19,
'LOADBOOL':           0x1A,
'DMOVE':              0x1B,
'JMP':                0x1C,
'JCMP':               0x1D,
'JZ':                 0x1E,
'SETOUTER':           0x1F,
'GETOUTER':           0x20,
'NEWOBJ':             0x21,
'APPENDARRAY':        0x22,
'COMPARITH':          0x23,
'INC':                0x24,
'INCL':               0x25,
'PINC':               0x26,
'PINCL':              0x27,
'CMP':                0x28,
'EXISTS':             0x29,
'INSTANCEOF':         0x2A,
'AND':                0x2B,
'OR':                 0x2C,
'NEG':                0x2D,
'NOT':                0x2E,
'BWNOT':              0x2F,
'CLOSURE':            0x30,
'YIELD':              0x31,
'RESUME':             0x32,
'FOREACH':            0x33,
'POSTFOREACH':        0x34,
'CLONE':              0x35,
'TYPEOF':             0x36,
'PUSHTRAP':           0x37,
'POPTRAP':            0x38,
'THROW':              0x39,
'NEWSLOTA':           0x3A,
'GETBASE':            0x3B,
'CLOSE':              0x3,
}
op2name = {v: k for k, v in name2op.items()}
