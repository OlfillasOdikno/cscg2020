import socket
import threading
import logging
import select
import intercept

class Proxy(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setblocking(0)
        self.running = False
        self.cb = lambda data, addr:0
        self.last_addr = None
    
    def bind(self,addr):
        self.sock.bind(addr)
    
    def run(self):
        self.running = True
        while self.running:
            ready = select.select([self.sock], [], [], 2)
            if ready[0]:
                data, addr = self.sock.recvfrom(4096)
                self.last_addr = addr
                self.cb(data,addr)
        self.sock.close()

    def send(self,msg,addr):
        if not self.running or not msg:
            return
        self.sock.sendto(msg,addr)

class DoubleProxy:
    
    def __init__(self,listen_addr,srv_addr,interceptor=intercept.Interceptor()):
        self.to_client = Proxy()
        self.to_server = Proxy()
        self.to_client.bind(listen_addr)
        self.to_client.cb = lambda data, addr: self.to_server.send(interceptor.intercept(data,False),srv_addr)
        self.to_server.cb = lambda data, addr: self.to_client.send(interceptor.intercept(data,True),self.to_client.last_addr)
    
    def start(self):
        logging.info("starting double proxy")
        self.to_client.start()
        logging.info("client proxy running..")
        self.to_server.start()
        logging.info("server proxy running..")

    def stop(self):
        logging.info("stopping double proxy")
        self.to_client.running = False
        self.to_server.running = False
        self.to_client.join()
        logging.info("client proxy stopped..")
        self.to_server.join()
        logging.info("server proxy stopped..")
