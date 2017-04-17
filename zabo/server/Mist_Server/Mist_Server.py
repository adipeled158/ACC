__author__ = 'Tomer Zaboklitski'


import socket
import threading
import random
import os
import time
import datetime
from sys import argv
from State_enum import State_enum
import rsa
from Crypto.Cipher import PKCS1_OAEP as pkcs1
from Sql_data_base_actions import Sql_Data_Base_Actions as data_base
import hashlib
import string
# May be more, but there is a limit.
# I suppose, the algorithm requires enough padding,
# and size of padding depends on key length.
MAX_MSG_LEN = 128

# Size of a block encoded with padding. For a 2048-bit key seems to be OK.
ENCODED_CHUNK_LEN = 256





#socket errors
EWOULDBLOCK = 10035
EINPROGRESS = 10036
EALREADY = 10037
ECONNRESET = 10054
ENOTCONN = 10057
ESHUTDOWN = 10058
WSAECONNABORTED = 10053

change_total_clients =  threading.Lock()





class ClientThread(threading.Thread):

    global all_socks
    global total_clients

    def __init__(self,ip,port,sock,tid):
        """
         creates new thread with alot of variables to make it uniqe
         """
        threading.Thread.__init__(self)
        #print "New thread started for "+ip+":"+str(port)
        self.ip = ip
        self.port = port
        self.conn = sock
        self.id=tid
        self.tid = str(tid) #threading.current_thread().ident
        self.client_user_name = "unkn"
        self.state=State_enum.start
        self.Client_public_key="unkn"
        self.key_sent=False
        (self.serv_pubk,self.serv_privk)= rsa.newkeys(1024)
        all_socks[self.conn]=[]



    def check_key(self, data):
        if data[:14].upper() == "-----BEGIN RSA":

            return True
        else:
            return False




    def send_email(self,user, pwd, recipient, subject, body):
        import smtplib

        gmail_user = user
        gmail_pwd = pwd
        FROM = user
        TO = recipient if type(recipient) is list else [recipient]
        SUBJECT = subject
        TEXT = body

        # Prepare actual message
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
        try:
            server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)

            server_ssl.ehlo() # optional, called by login()

            server_ssl.login(gmail_user, gmail_pwd)

            # ssl server doesn't support or need tls, so don't call server_ssl.starttls()
            server_ssl.sendmail(FROM, TO, message)
            #server_ssl.quit()
            server_ssl.close()
            return 105
        except:
            return 12


    def genreate_random_password(self,size=8, chars=string.ascii_uppercase + string.digits+ string.ascii_lowercase):
        return ''.join(random.choice(chars) for _ in range(size))



    def create_new_account(self,user_info_list):

        #creates new account
        user_name=user_info_list[0]


        password2=user_info_list[1] #this is how we encrypt the password into the database
        m = hashlib.md5()
        m.update(str(password2))
        password=m.hexdigest()


        l_name=user_info_list[2]
        f_name=user_info_list[3]
        email=user_info_list[4]
        secret_answer=user_info_list[5]

        data_base_temp=data_base()
        data_base_temp.Add_new_user("All_User_Info",user_name,password,f_name,l_name,email,secret_answer)
        code=self.send_email("Help.Mist1802","Tomerzabo1",str(email)+"@gmail.com","New Account Created  MIST","Hello user,\
        \nThank you for joining the MIST community\nThis is your account \nPassword =  "+str(password2)+"\nUser Name= "+user_name)


        return 104 #all good


    def check_account_info_exist(self,list_vars):
        #checks if email and user name exists
        user_name=list_vars[0]
        email=list_vars[4]

        data_base_temp=data_base()
        check_exists_email=data_base_temp.Check_email("All_User_Info",email)

        if check_exists_email==1:
            return 9 #email already exists

        data_base_temp=data_base()
        check_exists_user_name=data_base_temp.Check_user_name("All_User_Info",user_name)
        if check_exists_user_name==1:
            return 10 #user name already exists

        else:

            code=self.create_new_account(list_vars)

            return code





    def check_email_and_answer_correct(self,list_info):
        email=list_info[0]
        secret_answer=list_info[1]

        data_base_temp=data_base()
        check_exists_email=data_base_temp.Check_email("All_User_Info",email)

        if check_exists_email==0:
            return 11 #email not exists

        data_base_temp=data_base()
        Check_secret_answer=data_base_temp.check_email_and_answer("All_User_Info",secret_answer,email)
        if Check_secret_answer==0:
            return 13 #secret answer not correct
        else:
            password=self.genreate_random_password()
            data_base_temp=data_base()
            data_base_temp.set_password_by_email("All_User_Info",email,password)

            code=self.send_email("Help.Mist1802","Tomerzabo1",str(email)+"@gmail.com","Recovery Password from MIST","Hello user,\nthis is your new password for your account\n Password =  "+str(password))
            return code



    def check_user_name_and_password(self,list_info):

        user_name=list_info[0]
        password_temp=list_info[1]

        m = hashlib.md5()
        m.update(str(password_temp))
        password=m.hexdigest()

        data_base_temp=data_base()
        check_exists_user_name=data_base_temp.Check_user_name("All_User_Info",user_name)
        if check_exists_user_name==0:
            return 14 #user name not exists


        data_base_temp=data_base()
        check_exists_user_name=data_base_temp.Check_password_correct_by_user_name("All_User_Info",user_name,password)
        if check_exists_user_name==0:
            return 15 #wrong password

        return 106

    def DoAction(self,data1):


        if(self.state == State_enum.start):
            to_send= "Action~Rsa key please"



        else:
            to_send= "????"


        to_close_after_send = False


        data_len=len(data1)
        data=data1.split('~')
        if self.key_sent==False:

            if self.check_key(data[1]):

                self.Client_public_key=rsa.PublicKey.load_pkcs1(data[1],format='PEM')
                self.state=State_enum.after_key
                print "Got public key from "+ self.ip +" thread number "+ self.tid
                to_send="Action~"+self.serv_pubk.save_pkcs1(format='PEM')


        else:
            if data_len < 5:

                if self.state == State_enum.start:
                    to_send= "Action~Rsa key please"
                else:
                    to_send="Action~nothing"

            else:

                if data[0].startswith("Create Account"):
                     to_send=rsa.encrypt("Action~send all user info",self.Client_public_key)
                     self.conn.send(to_send)
                     account_info=[]
                     for i in range(0,6):

                         data=self.conn.recv(1024)
                         data=rsa.decrypt(data,self.serv_privk)
                         account_info.append(data)

                     code=self.check_account_info_exist(account_info)

                     to_send="Action~Code~"+str(code)

                elif data[0].startswith("Recover Password"):
                     to_send=rsa.encrypt("Action~send email and answer",self.Client_public_key)
                     self.conn.send(to_send)
                     account_info=[]
                     for i in range(0,2):

                         data=self.conn.recv(1024)
                         data=rsa.decrypt(data,self.serv_privk)
                         account_info.append(data)

                     code=self.check_email_and_answer_correct(account_info)
                     to_send="Action~Code~"+str(code)


                elif data[0].startswith("Login"):
                     to_send=rsa.encrypt("Action~send user info",self.Client_public_key)
                     self.conn.send(to_send)
                     account_info=[]
                     for i in range(0,2):

                         data=self.conn.recv(1024)
                         data=rsa.decrypt(data,self.serv_privk)
                         account_info.append(data)

                     code=self.check_user_name_and_password(account_info)
                     to_send="Action~Code~"+str(code)

                elif data[0].startswith("My Profile"):
                    print "i am here"
                    to_send=rsa.encrypt("send user name",self.Client_public_key)
                    self.conn.send(to_send)
                    print "send >>> send user name"
                    data=self.conn.recv(1024)

                    user_name=rsa.decrypt(data,self.serv_privk)
                    print "recv <<<< "+str(user_name)

                    data_base_temp=data_base()
                    all_user_info=data_base_temp.get_all_info_by_user_name("All_User_Info",user_name)
                    print all_user_info
                    for i in range(0,4):
                        print "4444 "+ str(all_user_info[i])
                        to_send=rsa.encrypt("Append~"+str(all_user_info[i]),self.Client_public_key)
                        self.conn.send(to_send)
                        time.sleep(0.05)


                    to_send="None"






        return to_close_after_send,to_send

    def run(self):
        """
        the thread gets massages from the client ,
        got to the function DoAction
        and then sends the data to the client
        """
        global total_clients
        global father_going_to_close
        father_going_to_close=False
        change_total_clients.acquire()
        total_clients += 1
        change_total_clients.release()




        print "New Thread, New connection from : "+self.ip+" on port: "+str(self.port)
        self.conn.settimeout(10)




        while True:
            try:
                data = self.conn.recv(1024)
                if self.state!=State_enum.start:
                    if data!=" ":
                        print data
                        data=rsa.decrypt(data,self.serv_privk)

            except socket.error as e:
                if e.errno == ECONNRESET: #'Connection reset by peer'
                    print "Error %s - Seems Client Disconnect. try Accept new Client " % e.errno
                    break
                elif e.errno == EWOULDBLOCK or str(e) == "timed out":  # if we use conn.settimeout(x)
                    if father_going_to_close:
                        print "Father Going To Die"
                        self.conn.close()
                        break
                    print ",",
                    continue
                else:
                    print "Unhandled Socket error at recv. Server will exit %s " % e
                    break
            except Exception as general_err:
                print "General Error - ", general_err.args
                break
            if data=="":
                print "Got empty data from Recv Will close this client socket"
                break
            if data!="Next Please":
                print self.tid +": Received<<< " + data
            else :
                print "sooooo what now?"


            (to_close_after_send,to_send)= self.DoAction(data)
            msg=""
            if self.key_sent==False:
                self.key_sent=True
            else:
                msg=to_send
                to_send=rsa.encrypt(to_send,self.Client_public_key)


            if msg!="None":
                self.conn.send(to_send)
                print self.tid  +": Sent   >>>" + msg
                print "-----------------------------------------------"


            if to_close_after_send:
                break

        print "Client disconnected..."
        print "Before close son socket - total clients = %d (%d)" % (how_many_clients("Child"),total_clients)
        change_total_clients.acquire()
        total_clients -= 1
        change_total_clients.release()

        self.conn.close()









def how_many_clients(caller):
    """
    returns how many clients are active at this moment
    """
    if caller == "main":
        return threading.activeCount() -1
    else:
        return threading.activeCount()-1



def main(port):
    """
    we bind the server
    the server is accepting clients now
    every client he accepts he starts a new thread that will communicate with him
    """



    server_sock = socket.socket()
    ip = "127.0.0.1"
    port=port
    #  SO_REUSEADDR means : reopen  socket even if its in wait state from last execution without waiting
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((ip, port))


    print "After bind to " + ip + " port: " + str(port)
    server_sock.listen(20)
    print "After listen"

    global total_clients
    total_clients = 0
    threads = []
    tid =0
    global all_socks
    all_socks={}



    cnt =0
    while True:
        try:
            if total_clients<=10:
                server_sock.settimeout(10)
                (conn, (ip, port)) = server_sock.accept()
                print "\n new client\n"
                tid += 1

                new_thread = ClientThread(ip, port, conn, tid)
                new_thread.start()

                print "Clients = %d (%d) "% (how_many_clients("main"),total_clients)
                threads.append(new_thread)
            else:
                print " i do not accept you sorry QQ"
                break

        except socket.error as e:
            if e.errno == EWOULDBLOCK or str(e) == "timed out":  # if we use conn.settimeout(x)
                cnt += 1
                print "#\n" if cnt % 10 == 0 else ',',
                continue

        except Exception as err:
                print "General Error at Main Accept loop - ",  err.args
                break

        except KeyboardInterrupt:
            print "\nGot ^C Main\n"
            father_going_to_close = True







    print "Server Says: Bye Bye ...."
    for t in threads:
         t.join()

    server_sock.close()

if __name__ == '__main__':


    try:
        os.system("cls")
        if len(argv)<2:
            print "<port> missing"
            exit()
        else:
            port=int(argv[1])
            if port <1023  or port >65535:
                print "port not in range (1023-65535"
                exit()
            print 'Tomer Zabo "Mist project" '
            main(port)


    except KeyboardInterrupt:
        print "\nGot ^C Main\n"
        father_going_to_close = True