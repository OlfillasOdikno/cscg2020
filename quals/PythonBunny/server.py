import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import urllib 
import mimetypes

class Server(HTTPServer):

    def __init__(self, server_address, RequestHandlerClass):
        self.cmd_cb = None
        super().__init__(server_address, RequestHandlerClass)
        

    def set_cmd_cb(self,cb):
        self.cmd_cb = cb

class S(BaseHTTPRequestHandler):
    def _set_response(self, is_json=False):
        self.send_response(200)
        self.send_header('Content-type','application/json' if is_json else 'text/html')
        self.end_headers()
    def log_message(self, format, *args):
        return

    def handle_api(self):
        resp = ""
        if(self.path == "/api/hostname"):
            resp = "127.0.0.1"
        elif(self.path == "/api/min_port"):
            resp ="1336"
        elif(self.path == "/api/max_port"):
            resp ="1336"
        elif(self.path == "/api/health"):
            resp ="yes"
        elif(self.path == "/api/login_queue"):
            resp ="0"
        elif(self.path == "/api/ratelimit"):
            resp ="20"
        self._set_response()
        self.wfile.write(resp.encode('utf-8'))

    def on_cmd(self,cmd):
        if self.server.cmd_cb != None:
            self.server.cmd_cb(self,cmd)
        else:
            self._set_response()
            self.wfile.write("no callback".encode('utf-8'))

    def do_GET(self):
        if(self.path.startswith("/api/")):
            self.handle_api()
        elif self.path.startswith("/cmd/"):
            self.on_cmd(urllib.parse.unquote(self.path.split("/cmd/")[1]))
        elif self.path.startswith("/static"):
            d1 = os.path.realpath(os.curdir+"/static")
            d2 = os.path.realpath(os.curdir+self.path)
            
            if not os.path.commonprefix([d1,d2]) == d1:
                self.send_response(300)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write("invalid file".encode('utf-8'))
                return
            else:
                self.send_response(200)
                self.send_header('Content-type', mimetypes.guess_type(self.path))
                self.end_headers()
                with open(d2,"rb") as f: #probably raceable, but i dont care
                    self.wfile.write(f.read())
        else:
            self._set_response()
            with open("./static/index.html","rb") as f:
                self.wfile.write(f.read())


def run(cmd_handler,server_class=Server, handler_class=S, port=80):
    server_address = ('', port)
    srv = server_class(server_address, handler_class)
    srv.set_cmd_cb(cmd_handler)
    
    logging.info('starting http server...')
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    srv.server_close()
    logging.info('stopping http server...')