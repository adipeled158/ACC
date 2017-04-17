__author__ = 'Tomer Zaboklitski'


import socket,struct
from sys import argv
import msvcrt
import os
from State_enum import State_enum
import rsa
import time
import wx
import Queue
import threading



lock =  threading.Lock()


global QUE
QUEUE_SIZ = 20
QUE = Queue.Queue(QUEUE_SIZ)

EWOULDBLOCK = 10035
state=State_enum.start
server_key=""
# May be more, but there is a limit.
# I suppose, the algorithm requires enough padding,
# and size of padding depends on key length.
MAX_MSG_LEN = 128

# Size of a block encoded with padding. For a 2048-bit key seems to be OK.
ENCODED_CHUNK_LEN = 256

class Client():
    def __init__(self,ip,port):
        self.ip=ip
        self.port=port
        self.sock=socket.socket()
        self.state=None

    """
    def decode_msg(msg, private_key):
        msg = msg.decode('hex')
        res = []
        k = pkcs1.new(private_key)
        for i in xrange(0, len(msg), ENCODED_CHUNK_LEN):
            res.append(k.decrypt(msg[i : i+ENCODED_CHUNK_LEN]))
        return ''.join(res)


    def encode_msg(msg,pub_key):
        res = []
        k = pkcs1.new(pub_key)
        for i in xrange(0, len(msg), MAX_MSG_LEN):
            v = k.encrypt(msg[i : i+MAX_MSG_LEN])
            # There are nicer ways to make a readable line from data than using hex. However, using
            # hex representation requires no extra code, so let it be hex.
            res.append(v.encode('hex'))
            assert len(v) == ENCODED_CHUNK_LEN
        return ''.join(res)

    """
    def get_sock(self):
        return self.sock
    def check_ip_port(self):
        try:
            int_port=int(self.port)
            if int_port <1023  or int_port >65535:
                  return 1  #error code for bad port
            string_ip=self.ip
            if string_ip.find(".")==-1:
                    return 2 #bad ip
            else:
                ip_blocks=string_ip.split(".")
                print ip_blocks
                if len(ip_blocks)!=4:
                    return 2#code
                else:
                    for i in range (0,4):
                        check_if_in_range_clock=int(ip_blocks[i])
                        if check_if_in_range_clock<0 or check_if_in_range_clock>255 :
                             return 2 #code

                self.port=int(self.port)
                return 101#code

        except :
            return 3 #bad coding given string and not int something like that

    def connect_to_server(self):
        try:
            self.sock.connect((self.ip,self.port))
        except socket.error as e:
           return 4#code

        except Exception as err:
            return 5#code
        return 102#code

    def get_public_key_and_send_server(self):
        (self.pubk,self.privk)= rsa.newkeys(1024)
        self.sock.settimeout(5)

        try:
            self.sock.send("Public Key~"+self.pubk.save_pkcs1(format='PEM'))
            print "sent >>>>>" +"Public Key~"+self.pubk.save_pkcs1(format='PEM')
            self.state=State_enum.start

            code=self.recv_server_key()



        except socket.error as e:
            if e.errno == EWOULDBLOCK or str(e) == "timed out":
               pass#code

        except Exception as general_err:
            print "General Error - ", general_err.args
            return 5

        return code#code

    def recv_server_key(self):
        self.sock.settimeout(10)
        try:
            request_from_server=self.sock.recv(4096)
            if state== State_enum.start:
                print "recv<<<<<  "+ request_from_server
                data=request_from_server.split("~")

                self.server_key=rsa.PublicKey.load_pkcs1(data[1],format="PEM")

                self.state=State_enum.after_key
        except socket.error as e:
            if e.errno == EWOULDBLOCK or str(e) == "timed out":
                pass
            else:

                return 4

        except Exception as general_err:
            print "General Error - ", general_err.args
            return 5
        return 103


    def send_data_to_server(self,data):
        self.sock.settimeout(5)

        try:
            self.sock.send(rsa.encrypt(data,self.server_key))
            print "sent >>>>>" +data
            self.state=State_enum.after_key





        except socket.error as e:
            if e.errno == EWOULDBLOCK or str(e) == "timed out":
               pass#code

        except Exception as general_err:
            print "General Error - ", general_err.args
            return 5

        return #code

    def recv_and_dec_massage(self):
        request_from_server=self.sock.recv(4096)
        request_from_server=rsa.decrypt(request_from_server,self.privk)
        return request_from_server


def main():
    global QUE



    try:
        s = socket.socket()
        if len(argv)<3:
            print "<ip><port> missing"
            exit()



        ip = str(argv[1])
        port = int(argv[2])

        s.connect((ip,port))

        print "after connect"




    except socket.error as e:
           print "socket error"

    except KeyboardInterrupt:
        print "\nGot ^C Main\n"
        father_going_to_close = True
    except Exception as err:
            print "General Error at Main Accept loop - ",  err.args
            exit()


    #we are after connect
    (pubk,privk)= rsa.newkeys(1024)
    s.send("Public Key~"+pubk.save_pkcs1(format='PEM'))
    print "sent >>>>>" +"Public Key~"+pubk.save_pkcs1(format='PEM')
    state=State_enum.start
    server_key=""





    while True:
        s.settimeout(10)
        try:
            request_from_server=s.recv(4096)
            if state== State_enum.start:
                print "recv<<<<<  "+ request_from_server
                data=request_from_server.split("~")
                server_key=rsa.PublicKey.load_pkcs1(data[1],format="PEM")

                state=State_enum.after_key

                s.send(rsa.encrypt("Next Please",server_key))


            else:


                request_from_server=rsa.decrypt(request_from_server,privk)
                print "recv<<<<<  "+ request_from_server


                if state==State_enum.after_key:

                    app = wx.App(0)
                    from Entry_page import Page_Frame as entry_page
                    frame=entry_page(None)
                    app.MainLoop()
                    with lock:
                        print "BEFOR GETTING QUE"
                        print QUE
                        count=1
                        # while  QUE.empty():
                        #     print "something"
                        while  not QUE.empty():
                            value=QUE.get()
                            break


                    print "the value is: "+  value
                    #s.send(rsa.encrypt("massage to decode if",server_key))

                    server_command=request_from_server.split("~")[1]
                    print server_command
                    state=State_enum.entry_page


        except socket.error as e:
            if e.errno == EWOULDBLOCK or str(e) == "timed out":
                continue
            else:
                print "Unhandled Socket error at recv. Server will exit %s " % e
                break

        except Exception as general_err:
            print "General Error - ", general_err.args
            break

    s.close()
    print "bb"
    print " sorry you dced or somone else dced good bye have a lovley day"



if __name__ == '__main__':


    try:
        os.system("cls")
        print "This is Mist\n project written by Tomer Zaboklitski \nYud Beth Herzog Kfar Sava"
        main()

    except Exception as err:
            print "General Error at Main Accept loop - ",  err.args
            exit()

