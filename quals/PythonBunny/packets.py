import struct

class GamePacket:
    def __init__(self):
        self.data = bytearray()
    
    def decode(self, data):
        self.data = data

    def encode(self):
        return self.data


class ServerCheckpoint(GamePacket):

    def decode(self,data):
        super().decode(data)
        self.cp_id = data[0]

class ServerNPCInfoResponse(GamePacket):

    def decode(self, data):
        super().decode(data)
        [self.uid] = struct.unpack('I',data[0:4])
        self.name = data[7:].decode()

class ServerTeleportPacket(GamePacket):

    def decode(self, data):
        super().decode(data)
        self.instant = data[0]
        [self.__x,self.__y,self.__z] = struct.unpack('iii',data[1:13])


    @property
    def x(self):
        return self.__x/10000

    @x.setter
    def x(self,x):
        self.__x=int(x*10000)

    @property
    def y(self):
        return self.__y/10000

    @y.setter
    def y(self,y):
        self.__y=int(y*10000)

    @property
    def z(self):
        return self.__z/10000

    @z.setter
    def z(self,z):
        self.__z=int(z*10000)


    def encode(self):
        self.data[0]=self.instant
        struct.pack_into("iii",self.data,1,self.__x,self.__y,self.__z)
        return super().encode()

class ServerPositionPacket(GamePacket):

    class PlayerData:

        def __init__(self,uid,x,y,z):
            self.uid = uid
            self.x=x
            self.y=y
            self.z=z        
        

    def decode(self, data):
        super().decode(data)
        self.players=[]
        i = 0
        n = len(data)//42
        for i in range(n):
            d = data[i*42:(i+1)*42]
            [uid] = struct.unpack('I',d[0:4])
            [x,y,z] = struct.unpack('iii',d[12:24])
            self.players.append(self.PlayerData(uid,x/10000,y/10000,z/10000))

class ClientEmojiPacket(GamePacket):

    def decode(self, data):
        super().decode(data)
        self.secret = data[0:8]
        [self.emoji] = struct.unpack('B',data[8:9])

    def encode(self):
        self.data[0:8]=self.secret
        struct.pack_into("B",self.data,8,self.emoji)
        return super().encode()

class ClientPositionPacket(GamePacket):

    def decode(self, data):
        super().decode(data)
        self.secret = data[0:8]
        [self.time] = struct.unpack('Q',data[8:16])
        [self.__x,self.__y,self.__z] = struct.unpack('iii',data[16:28])

        [self.__rx,self.__ry,self.__rz] = struct.unpack('iii',data[28:40])

        [self.trigger] = struct.unpack('B',data[40:41])
        [self.ground_blend] = struct.unpack('H',data[41:43])
        [self.not_ground_blend] = struct.unpack('H',data[43:45])

    @property
    def x(self):
        return self.__x/10000

    @x.setter
    def x(self,x):
        self.__x=int(x*10000)

    @property
    def y(self):
        return self.__y/10000

    @y.setter
    def y(self,y):
        self.__y=int(y*10000)

    @property
    def z(self):
        return self.__z/10000

    @z.setter
    def z(self,z):
        self.__z=int(z*10000)


    @property
    def rx(self):
        return self.__rx/10000

    @rx.setter
    def rx(self,rx):
        self.__rx=int(rx*10000)

    @property
    def ry(self):
        return self.__ry/10000

    @ry.setter
    def ry(self,ry):
        self.__ry=int(ry*10000)

    @property
    def rz(self):
        return self.__rz/10000

    @rz.setter
    def rz(self,rz):
        self.__rz=int(rz*10000)

    def encode(self):
        self.data[0:8]=self.secret
        struct.pack_into("Q",self.data,8,self.time)
        struct.pack_into("iiiiii",self.data,16,self.__x,self.__y,self.__z,self.__rx,self.__ry,self.__rz)
        return super().encode()