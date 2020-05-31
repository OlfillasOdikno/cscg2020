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

# Squirrel as a Service - localo


**Category:** Pwn
**Difficulty:** Hard        
**Author:** 0x4d5a

## Description
> 🐿️ as a Service! Squirrel lang (ˈaɪ̯çˌhœʁnçən) is a super simple programming language. And our server will execute your squirrel scripts, either in text or binary based format. Go exploit it. To test this service, take this cool script:
>
>class CSCG
>{	
>  constructor()
>  {
>    isCool = true;
>  }
>  isCool = false;
>}
>
>function CSCG::IsCool()
>{
>  if (isCool)
>  {
>    print("CSCG is so cool!\n");
>  }
>}
>local cscg = CSCG()
>cscg.IsCool()
>
>Server: nc hax1.allesctf.net 9888
## Summery
Squirrel is a scripting language similar to lua, it aims to be used in video games and as such can be integrated and interfaced with easily. The language implements most techniques that are expected in a modern language. And is in my opinion easier to read than lua. Even though it is not that well known, it is used in quite some Projects like `Code::Blocks` and the `Source` engine by Valve, and therefore vulnerabilities in it would affect millions. 
The author provided an archive containing instruction to get the server side setup. 

## Solution

### Fuzz all the Things
I started to write a docker based fuzzing setup and let that run over the night, the next day I had roughly 9k crashes. I used crashwalk to reduce it, but it were too many for me to analyze.

@import "crashwalk.txt"

### Target analysis
I decided to do some `source code review`, since I now knew that the target is full of bugs. Since the server binary has `all common exploit mitigations enabled`, the bugs that are most interesting are `Out-Of-Bounds read/write`, `Use-After-Free`, `Type Confusion` and `Logic` bugs. For the input either use `source code` that squirrel compiles or `pre compiled code` that is directly interpreted can be used. I took a quick look at the `lexer` (since that would allow source code based exploitation), but found nothing of interest and continued to search for bugs in the `VM` itself. The VM implements `61` opcodes and is written in **hard to read** `C++` code. The instructions like other structures are directly copied from the binary into memory, before being parsed. Each instruction is structured like this:
```CPP
typedef struct{
    int_32 _arg1;
    unsigned char op;
    unsigned char _arg0;
    unsigned char _arg2;
    unsigned char _arg3;
} SQInstruction;
```
The VM uses a `stack` and `lives in the heap`. Each stack object is a `SQObjectPtr`, basically a structure on that contains a type id and a pointer to an object.
```CPP
typedef struct tagSQObject
{
    SQObjectType _type;     //4 bytes, padded to 8
    SQObjectValue _unVal;   //8 bytes
}SQObject;
```
There are `18` (+1 `WIERD_TYPE`) basic types, most of the just hold pointer, but 4 hold their value directly: `OT_NULL, OT_INTEGER, OT_FLOAT, OT_BOOL`. The types are implemented using an `enum` and hold additional information such as if their reference has to be counted. 

```CPP
typedef enum tagSQObjectType {
	OT_NULL = (_RT_NULL | SQOBJECT_CANBEFALSE),
	OT_INTEGER = (_RT_INTEGER | SQOBJECT_NUMERIC | SQOBJECT_CANBEFALSE),
	OT_FLOAT = (_RT_FLOAT | SQOBJECT_NUMERIC | SQOBJECT_CANBEFALSE),
	OT_BOOL = (_RT_BOOL | SQOBJECT_CANBEFALSE),
	OT_STRING = (_RT_STRING | SQOBJECT_REF_COUNTED),
	OT_TABLE = (_RT_TABLE | SQOBJECT_REF_COUNTED | SQOBJECT_DELEGABLE),
	OT_ARRAY = (_RT_ARRAY | SQOBJECT_REF_COUNTED),
	OT_USERDATA = (_RT_USERDATA | SQOBJECT_REF_COUNTED | SQOBJECT_DELEGABLE),
	OT_CLOSURE = (_RT_CLOSURE | SQOBJECT_REF_COUNTED),
	OT_NATIVECLOSURE = (_RT_NATIVECLOSURE | SQOBJECT_REF_COUNTED),
	OT_GENERATOR = (_RT_GENERATOR | SQOBJECT_REF_COUNTED),
	OT_USERPOINTER = _RT_USERPOINTER,
	OT_THREAD = (_RT_THREAD | SQOBJECT_REF_COUNTED),
	OT_FUNCPROTO = (_RT_FUNCPROTO | SQOBJECT_REF_COUNTED), //internal usage only
	OT_CLASS = (_RT_CLASS | SQOBJECT_REF_COUNTED),
	OT_INSTANCE = (_RT_INSTANCE | SQOBJECT_REF_COUNTED | SQOBJECT_DELEGABLE),
	OT_WEAKREF = (_RT_WEAKREF | SQOBJECT_REF_COUNTED),
	OT_OUTER = (_RT_OUTER | SQOBJECT_REF_COUNTED), //internal usage only
	WIERD_TYPE = 0x00
}SQObjectType;
```
Everything else is implemented as a class.

### Bug hunting

I found many bugs in the VM code, some that are exploitable, and some that aren't, well at least not that easy (*try to exploit the type confusion in `_OP_APPENDARRAY`, I tried to do it using a string, but you need some leaks and there are many easier bugs to exploit*).

For my exploit I used mainly `OOB bugs` since there are `no argument bounds check` for any opcode. Opcodes that are useful are `_OP_LOAD`, it loads a object pointer from the literals section onto the stack and `_OP_MOVE` that copies a pointer from one location on the stack to another one. The literals section is quite interesting, because it is used in a big chunk of memory that contains multiple sections an therefore a OOB onto the other sections would not be affected by the heap layout.
@import "proto.c"

Using this `"fake" object` pointers can be loaded onto the stack, if they are created in one of the sections in the same chunk. I decided to append `16 bytes` to the `instructions` and then use a `_OP_LOAD` oob read to load for example a `fake native closure`, a object pointing to a native function, onto the stack. I wrote a **basic** `disassembler` and an `assembler` for squirrel and did some testing, it worked, but what ever I tried there was `no way around a leak`. But even if I would get a leak, `I can't change my instructions in runtime`. This problem was quite hard for me to overcome. I searched for other bugs and developed some strategies that would utilise `heap sprays` or `static offsets on the heap`, I should have gone with heap spraying, but for some reason I can't remember I didn't. 

I did some Windows pwning and got used to the tooling, therefore I decided to exploit it on Windows first and then back-port it to Linux. This was a bad idea, since I later realized, that the `heap offsets on Linux were static`, but the `Windows heap offsets were random` and therefore I decided to go back to my first idea.

### Something something self-modifying code -> shell

`I can't change my instructions in runtime.` or can I?! If I would know the offset from the stack to the instruction section I could use a `JMP` instruction to jump to the stack and execute my squirrel code there. And since every Instruction is just `8 bytes` I could just use the `_OT_INTEGER` objects, since I can do simple integer arithmetic with their value, which is exactly `8 bytes`. And `_OT_INTEGER` type interpreted as a instruction is:
```lua
0x0500000200000000: _OP_LINE arg0: 0x00 arg1: 0x05000002 arg2: 0x00 arg3: 0x00
```
By taking a look at the `_OP_LINE` implementation, it can be seen that it is like a `NOP` instruction if no `_debughook` is set, which is the case.
```CPP
case _OP_LINE: 
	if (_debughook) CallDebugHook(_SC('l'),arg1); continue;
```
The instruction pointer will just continue to the value of the `_OT_INTEGER`. If I now get a leak I can change for example `arg1` for `_OP_MOVE` to read at any address I want. For the leak I use the `tostring` closure, it reads a `SQObjectPtr` from the stack and depending on the type return different strings.
```CPP
bool SQVM::ToString(const SQObjectPtr &o,SQObjectPtr &res)
{
    switch(sq_type(o)) {
    case OT_STRING:
        res = o;
        return true;
    case OT_FLOAT:
        scsprintf(_sp(sq_rsl(NUMBER_MAX_CHAR+1)),sq_rsl(NUMBER_MAX_CHAR),_SC("%g"),_float(o));
        break;
    case OT_INTEGER:
        scsprintf(_sp(sq_rsl(NUMBER_MAX_CHAR+1)),sq_rsl(NUMBER_MAX_CHAR),_PRINT_INT_FMT,_integer(o));
        break;
    case OT_BOOL:
        scsprintf(_sp(sq_rsl(6)),sq_rsl(6),_integer(o)?_SC("true"):_SC("false"));
        break;
    case OT_NULL:
        scsprintf(_sp(sq_rsl(5)),sq_rsl(5),_SC("null"));
        break;
    case OT_TABLE:
    case OT_USERDATA:
    case OT_INSTANCE:
        if(_delegable(o)->_delegate) {
            SQObjectPtr closure;
            if(_delegable(o)->GetMetaMethod(this, MT_TOSTRING, closure)) {
                Push(o);
                if(CallMetaMethod(closure,MT_TOSTRING,1,res)) {
                    if(sq_type(res) == OT_STRING)
                        return true;
                }
                else {
                    return false;
                }
            }
        }
    default:
        int a = sizeof(SQString);
        SQObjectPtr*  b = _array(o)->_values._vals;
        scsprintf(_sp(sq_rsl((sizeof(void*)*2)+NUMBER_MAX_CHAR)),sq_rsl((sizeof(void*)*2)+NUMBER_MAX_CHAR),_SC("(%s : 0x%p)"),GetTypeName(o),(void*)_rawval(o));
    }
    res = SQString::Create(_ss(this),_spval);
    return true;
}
```
The default case is quite interesting, since it will `print just the raw pointer value`. There is the leak. One problem remains, how do I get the instruction pointer onto the squirrel stack?! A `heap scanner` could be used to scan for a value on the stack to get the offset. My first idea was using `_OP_MOVE` with a negative `arg1` to scan the heap. A basic heap scanner would look like this:
```lua
local cmp = 0x411337421337
local cmp2 = 0
for(local i = 10; i< scan_width; i+=1){
	asm{
		_OP_MOVE: arg0: stack_addr(cmp2) arg1: -i arg2:0 arg3: 0
	}
	if(cmp == cmp2){
		asm{
			_OP_JMP: arg0: 0 arg1: i-ip_offset-stack_base-literal_offset arg2: 0 arg3: 0
		}
	}
}

```
The code above would, in theory, scan the heap `from the stack` `to the literals section` of the function, since integers with more than 4 bytes are stored as a literal. After that it would jump that offset, but the offset needs to be adjusted depending on the `stack_base, literal location and instruction pointer location`. The loop has to be enrolled, since it is still not possible to modify the instruction in runtime. I wrote some assembly code based on that, optimized for size. After many hours of fine tuning I came up with those instructions:
```
stack:
	base + 0x00: 0x411337421337

NE          a0: 1 a1:-10 a2:0x00 a3:0x00
JZ          a0: 1 a1:-10 a2:0x00 a3:0x00
NE          a0: 1 a1:-11 a2:0x00 a3:0x00
JZ          a0: 1 a1:-11 a2:0x00 a3:0x00
NE          a0: 1 a1:-12 a2:0x00 a3:0x00
JZ          a0: 1 a1:-12 a2:0x00 a3:0x00
NE          a0: 1 a1:-13 a2:0x00 a3:0x00
JZ          a0: 1 a1:-13 a2:0x00 a3:0x00
[...]
```
The idea is to use `_OP_NE` instead of `_OP_MOVE` and `_OP_CMP` since it is less code and more important: `_OP_MOVE` copies the `SQObjectPtr` on the stack first, by doing so, squirrel will increase the reference count if the `SQOBJECT_REF_COUNTED` bit is set, this will result in many invalid dereferences and crash the program. `_OP_NE` uses `SQVM::IsEqual` and checks if th types match and if their raw value matches, if not it will do some special checks for integers and floats, but `it will never dereference anything` and is therefore perfect. 
```CPP
case _OP_NE:{
    bool res;
    if(!IsEqual(STK(arg2),COND_LITERAL,res)) { SQ_THROW(); }
    TARGET = (!res)?true:false;
    } continue;
```
`_OP_JZ` just checks if the target (`STK(arg0)`) is false and increments the instruction pointer by `arg1` if thats the case.
```CPP
case _OP_JZ:
	if(IsFalse(STK(arg0))) ci->_ip+=(sarg1); continue;
```
And by combining those two instructions, the instruction count is reduced to `2 instructions per loop cycle`.

And it can be done even better:
By not trying to find the exact offset by using a search step size of 64 and creating that amount of literals, it is possible to scan `n = 0x1000` in `128` instructions instead of `8192‬`, but it would produce more literals resulting in $ \frac{2n}{x} \cdot 8 + x \cdot 16= 2048 ‬$ bytes compared to $ 2n \cdot 8 + 1 \cdot 16 = 65552 $ bytes
Here the calculation for the step size:
$$
f(x) = \frac{n}{x} + x \\
f'(x) = 1-\frac{n}{x^2} \\
f'(x) \overset{!}{=} 0 \\
\llap{$\rightarrow$\hspace{50pt}} x = \pm\sqrt{n}
$$

I use a step size of 40 in my code, because `I fucked up somewhere in the offset calculation` and 40 seems to work for the Docker image.


By loading the code somewhere later into the stack and before that a `big nop slide`, code on the stack can be executed. So basically the classic `jmp esp`, but in squirrel. But how to get back? I ended up using `traps`, since they save the stack base and the instruction pointer location. On the stack all that is needed is to `throw an exception to get back` into a "normal" state. 

### How to shell
On linux the system function is compiled into the binary even though it is not registered.I can't just use `system("sh")` in squirrel, but if I create a native closure with the `_function` pointer pointing to `_system_system` I can call that native closure to get a shell. I would need to leak a pointer pointing somewhere inside the `sqstdlib` library and could then calculate the address of `_system_system` based on the docker setup. But I decided to try to exploit it without the `_system_system` since that would require "remote information" which I avoided to this point.
I decided that a `libc leak` would be okay, since `libc-db` can be used to get the version and use it to calculate the offset. I could also have used a pattern scan and then no offset would be needed, but `I left implementing that as an exercise for the reader`.

I ended up using a `vtable` of a fake `blob` instead of `_function` since I can control the arguments in `self->Write` used in `_stream_writen`
```CPP
SQInteger _stream_writen(HSQUIRRELVM v)
{
    SETUP_STREAM(v);
    SQInteger format, ti;
    SQFloat tf;
    sq_getinteger(v, 3, &format);
    switch(format) {
    case 'l': {
        SQInteger i;
        sq_getinteger(v, 2, &ti);
        i = ti;
        self->Write(&i, sizeof(SQInteger));
              }
        break;
        [...]
```
That is perfect for a `one_gadget` just a libc pointer leak is needed. By allocating `a big chunk` on the heap, a libc pointer is `placed directly after the chunk` and therefore can be leaked.
To create the `fake blob` I used a blob, because it is easy to write data to it and the object address can be leaked using `tostring`. Using that address and the offset to the blob data, I can write a fake `instance` pointing to the fake `blob` and move it on the squirrel stack, to execute `writen` and spawn a shell.
## Code
**assembler:**
@import "assembler.py"

**disassembler:**
@import "disassembler.py"

**patcher:**
@import "patcher.py"

**common:**
@import "common.py"

**sqdef:**
@import "sqdef.py"

**template:**
@import "test.nut" {as=lua}

## Mitigation
- don't use squirrel
- sandbox your programs

## Flag
CSCG{t3chnic4lly_an_0d4y_but_...}