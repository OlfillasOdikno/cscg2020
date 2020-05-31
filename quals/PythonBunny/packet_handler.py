from packets import *
from utils import *
from reload import Reloader

handlers={'srv':{},'cli':{}}
def register(cmd,packet,dir='booth'):
    def r(fn):
        r = Reloader(fn)
        fn = r.exec
        if dir == 'booth':
            handlers['srv'][cmd]={'fn':fn,'type': packet}
            handlers['cli'][cmd]={'fn':fn,'type': packet}
        else:
            handlers[dir][cmd]={'fn':fn,'type': packet}
    return r

@register(80,ClientPositionPacket,'cli')
def player_update(sniffer,pkt):
    if sniffer.drop_pos:
        return True
    sniffer.secret = pkt.secret
    sniffer.state['pos']={
        'x':pkt.x,
        'y':pkt.y,
        'z':pkt.z
    }
    sniffer.state['rot']={
        'x':pkt.rx,
        'y':pkt.ry,
        'z':pkt.rz
    }
    gp = coords_to_map([pkt.x,pkt.z])
    sniffer.state['grid_pos']= {
        'x':gp[0],
        'y':gp[1]
    }
    if pkt.time > sniffer.fake_time:
        sniffer.fake_time = pkt.time
    pkt.time = sniffer.fake_time
    sniffer.fake_time+=1000*90000

@register(69,ClientEmojiPacket,'cli')
def emoji(sniffer,pkt):
    print("Emoji: %d" % (pkt.emoji))


@register(84,ServerTeleportPacket)
def tp(sniffer,pkt):
    print("tp: %f %f %f"%(pkt.x,pkt.y,pkt.z))



@register(80,ServerPositionPacket,'srv')
def other_player_update(sniffer,pkt):
    data = pkt.data
    data.insert(0,80)
    for p in pkt.players:
        uid = p.uid
        if not uid in sniffer.state['npcs']:
            sniffer.state['npcs'][uid]={}
        sniffer.state['npcs'][uid]={
            'pos':{
               'x':p.x,
               'y':p.y,
               'z':p.z,
            }
        }
