from reload import Reloader
import time
from packets import *
from utils import *
handlers={}
def register(cmd):
    def r(fn):
        r = Reloader(fn)
        fn = r.exec
        handlers[cmd]=fn
    return r

@register("ping")
def ping(sniffer,args):
    return "pong"


@register("tp")
def tp(sniffer,args):
    if len(args) != 3:
        return "x y z"
    pkt = ServerTeleportPacket()
    pkt.data = bytearray(4*3+1)
    pkt.x = float(args[0])
    pkt.y = float(args[1])
    pkt.z = float(args[2])
    pkt.instant = 255
    sniffer.send_to_client(84,pkt)
    return "ok"

@register("emoji")
def emoji(sniffer,args):
    if len(args) != 1:
        return "id"
    pkt = ClientEmojiPacket()
    pkt.data = bytearray(9)
    pkt.secret = sniffer.secret
    pkt.emoji = int(args[0])
    sniffer.send_to_server(69,pkt)
    return "ok"

@register("tpr")
def tpr(sniffer,args):
    if len(args) != 3:
        return "x y z"
    pkt = ServerTeleportPacket()
    pkt.data = bytearray(4*3+1)
    pkt.x = sniffer.state['pos']['x']+float(args[0])
    pkt.y = sniffer.state['pos']['y']+float(args[1])
    pkt.z = sniffer.state['pos']['z']+float(args[2])
    pkt.instant = 255
    sniffer.send_to_client(84,pkt)
    return "ok"


@register("state")
def state(sniffer,args):
    return sniffer.state

@register("path")
def path(sniffer,args):
    if len(args)==4:
        src = [int(s) for s in args[0:2]]
        dst = [int(s) for s in args[2:4]]
    elif len(args) == 2:
        src = [sniffer.state['grid_pos']['x'],sniffer.state['grid_pos']['y']]
        dst = [int(s) for s in args[0:2]]
    else:
        return "invalid args"
    return sniffer.map.find_path(src,dst)

@register("move_test")
def move(sniffer,args):
    if len(args) == 3:
        src = [sniffer.state['grid_pos']['x'],sniffer.state['grid_pos']['y']]
        dst = [int(s) for s in args[0:2]]
        dt =float(args[2])
    else:
        return "invalid args"
    path = sniffer.map.find_path(src,dst)
    sniffer.drop_pos = True
    sends = []
    for p in path:
        pkt = ClientPositionPacket()
        pkt.data = bytearray(45)
        pkt.secret = sniffer.secret
        pkt.time = sniffer.fake_time
        c = map_to_coords(p)
        pkt.x = c[0]
        pkt.y = 10
        pkt.z = c[1]
        pkt.rx = sniffer.state['rot']['x']
        pkt.ry = sniffer.state['rot']['y']
        pkt.rz = sniffer.state['rot']['z']

        sends.append([80,pkt])

        sniffer.fake_time+=10**10
    sniffer.send_to_server_multi(sends)
    sniffer.drop_pos = False

@register("move")
def move(sniffer,args):
    if len(args) == 3:
        src = [sniffer.state['grid_pos']['x'],sniffer.state['grid_pos']['y']]
        dst = [int(s) for s in args[0:2]]
        dt =float(args[2])
    else:
        return "invalid args"
    path = sniffer.map.find_path(src,dst)
    sniffer.drop_pos = True
    for p in path:
        pkt = ClientPositionPacket()
        pkt.data = bytearray(45)
        pkt.secret = sniffer.secret
        pkt.time = sniffer.fake_time
        c = map_to_coords(p)
        pkt.x = c[0]
        pkt.y = 10
        pkt.z = c[1]
        pkt.rx = sniffer.state['rot']['x']
        pkt.ry = sniffer.state['rot']['y']
        pkt.rz = sniffer.state['rot']['z']

        sniffer.send_to_server(80,pkt)

        sniffer.fake_time+=10**10
        time.sleep(dt)
    sniffer.drop_pos = False
