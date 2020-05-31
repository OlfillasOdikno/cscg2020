from scapy.all import *
import struct
import proxy
import server
import logging
import intercept
import random
import json
from utils import *
from map import Map
import time
import packet_handler
import command_handler

ports = range(1337, 1357)

def random_byte():
    return 0

def decode(data):
    dec=bytearray((len(data)-2))
    key = data[0]
    for i in range(2,len(data)):
        dec[i-2]=data[i]^key
        key = (key+data[1])%0xFF
    return dec

def encode(data):
    enc=bytearray((len(data)+2))
    enc[0] = key = random_byte()
    enc[1] = random_byte()
    for i in range(len(data)):
        enc[i+2]=data[i]^key
        key = (key+enc[1])%0xFF
    return enc

class MsgInterceptor(intercept.Interceptor):

    def __init__(self,sniffer):
        super().__init__()
        self.sniffer = sniffer

    def intercept(self,data,from_server):
        msg = decode(data)
        msg_type = msg[0]
        msg_payload = msg[1:]
        handlers = packet_handler.handlers['srv' if from_server else 'cli']
        if(msg_type in handlers):
            h = handlers[msg_type]
            fn = h['fn']
            packet = h['type']()
            packet.decode(msg_payload)
            r = fn(self.sniffer,packet)
            if r:
                print("DROP")
                return
            msg = packet.encode()
            msg.insert(0,msg_type)
        return encode(msg)

class Sniffer:

    def __init__(self):
        self.dp = None
        self.map = Map()
        self.state={
            'npcs':{},
            'pos':{
                'x':0,
                'y':0,
                'z':0,
            },
            'rot':{
                'x':0,
                'y':0,
                'z':0,
            }
        }
        self.secret = []
        
        self.fake_time = 0
        self.drop_pos = False
        self.spoof_time = False
    
    def send_to_server(self,type,pkt):
        data = pkt.encode()
        data.insert(0,type)
        enc = encode(data)
        self.dp.to_server.send(enc,self.dp.to_server.last_addr)

    def send_to_client(self,type,pkt):
        data = pkt.encode()
        data.insert(0,type)
        enc = encode(data)
        self.dp.to_client.send(enc,self.dp.to_client.last_addr)


    def send_to_server_multi(self,sends):
        print("multi")
        f = bytearray()
        for send in sends: 
            data = send[1].encode()
            data.insert(0,send[0])
            enc = encode(data)
            enc.ljust(65536, b'\0')
            f+=enc
        print("send")
        self.dp.to_server.send(f,self.dp.to_server.last_addr)

    def start_proxy(self,ip="147.75.85.99",port=random.choice(range(1337, 1357))):
        logging.basicConfig(level=logging.DEBUG)
        self.dp = proxy.DoubleProxy(('0.0.0.0',1336),(ip,port),MsgInterceptor(self))
        self.dp.start()
        self.map.load("static/map.bmp")
        server.run(self.handle_cmd)
        self.dp.stop()

    def handle_cmd(self,h,cmd):
        args = cmd.split(" ")
        cmd = args[0]
        args = args[1:]
        resp = ''
        if cmd in command_handler.handlers:
            resp = command_handler.handlers[cmd](self,args)
        else:
            resp = "no handler for command: %s %r" % (cmd,args)
        h._set_response(True)
        h.wfile.write(json.dumps({
            'resp':resp,
        }).encode('utf-8'))



if __name__ == "__main__":
    sn = Sniffer()
    sn.start_proxy()