__author__ = 'Irit'
import socket
import threading
import random
from sys import argv
import time
import datetime
import struct
import user
import pickle
from acc_msg_editor import Acc_msg_edit as editor_data
import project



LOG_ALL = True


EWOULDBLOCK = 10035
EINPROGRESS = 10036
EALREADY = 10037
ECONNRESET = 10054
ENOTCONN = 10057
ESHUTDOWN = 10058
WSAECONNABORTED = 10053



change_total_clients =  threading.Lock()
write_to_log =  threading.Lock()
change_circles_clients  = threading.Lock()
change_small_balls = threading.Lock()
change_died_circles = threading.Lock()
change_account = threading.Lock()





class State_enum:
        start = 1
        logged_in = 2
        rejected = 3
        end = 4



class ClientThread(threading.Thread):

    stid = str(0)

    def __init__(self,ip,port,conn,tid):
        threading.Thread.__init__(self)
        #print "New thread started for "+ip+":"+str(port)
        self.ip = ip
        self.port = port
        self.conn = conn
        self.stid = str(tid) #threading.current_thread().ident
        self.state = State_enum.start
        self.client_name = ""
        self.division_line = "\n\n\n\n\n"
        self.name_current_acc_pro = ""
        self.name_current_acc_file = ""

    def recv_msg(self):
        """
        recv data
        """
        return self.conn.recv(1000000)

    def send_msg(self, send_to):
        """
        send the msg to the client
        """
        self.conn.send(send_to)

    def sign_up(self, user_name, password):
        #enroll the new accont
        if not user.is_user_exists(user_name):
            user.add_new_user_to_stockpile(user_name, password)
            self.user_name = user_name
            self.password = password
            return True
        return False

    def sign_in(self, user_name, password):
        #check the sign in
        if user.check_user_by_password(user_name, password):
            self.user_name = user_name
            self.password = password
            return True
        return False

    def send_client_info_pro(self,data_before, headers):
        """
        the function send to the client all of his projects in a list:

        """
        try:
            to_send = user.get_projects_and_info_to_client(self.client_name, self.password, headers)
            if len(to_send) !=0:
                data_obj = editor_data(to_send, False)
                to_send = data_obj.data
            else:
                to_send = "0"
            self.send_msg((data_before+to_send))
        except Exception as err:
            print "problem is here:", err.args


    def check_what_client_want(self, data):
        """
        check what client ask for from server
        and act properley
        """
        edited_data = editor_data(data, True)
        dct_help = edited_data.dct_data
        if dct_help.has_key("NEW PROJECT") and dct_help.has_key("HEADERS"):

            name_new_pro =dct_help["NEW PROJECT"]
            is_succseed = user.add_new_project_to_user(self.user_name, name_new_pro)
            """if not is_succseed:
                 self.send("not correct name")
            else:"""
            headers = dct_help["HEADERS"]
            self.send_client_info_pro("", headers)
        if dct_help.has_key("OPEN PROJECT") and dct_help.has_key("HEADERS"):

            name_pro = dct_help["OPEN PROJECT"]
            self.name_current_acc_pro = name_pro
            pro_help = project.acc_project(name_pro, self.user_name, self.password)
            to_send = pro_help.get_files_and_info_to_client(dct_help["HEADERS"])

            data_obj = editor_data(to_send, False)
            to_send = data_obj.data

            self.send_msg((to_send))

        if dct_help.has_key("NEW FILE") and dct_help.has_key("HEADERS") and dct_help.has_key("CONTENT"):


            name_new_file =dct_help["NEW FILE"]
            pro = project.acc_project(self.name_current_acc_pro, self.user_name, self.password)
            content = dct_help["CONTENT"]
            pro.create_new_file(name_new_file,content)

            """if not is_succseed:
                 self.send("not correct name")
            else:"""
            headers = dct_help["HEADERS"]
            self.send_client_info_pro("", headers)

    def run(self):
        global total_clients
        global father_going_to_close
        global circles_clients
        global changes_with_clients
        global died_circles
        change_total_clients.acquire()
        total_clients += 1
        change_total_clients.release()

        dict_all_clients_info = {}

        print "New Thread, New connection from : "+self.ip+":"+str(self.port)

        headers = self.first_recv_to_log_in()

        if self.state!=State_enum.end:
            self.send_client_info_pro("", headers)

        while self.state!=State_enum.end:
            try:

                if self.state == State_enum.end:
                    break

                recv = self.recv_msg()

                self.check_what_client_want(recv)
                """
                data_during_running = ""

                dict_all_clients_info = self.send_to_client_during_game(dict_all_clients_info)

                data_during_running = self.recv_msg()
                print "got entered"
                if data_during_running == "byby":
                    self.state = State_enum.end
                    break

                if data_during_running !="don't change anything":
                    dict_all_clients_info = self.recv_from_client_during_game(dict_all_clients_info, data_during_running)
                """


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
                    pass
                else:
                    print "Unhandled Socket error at recv. Server will exit %s " % e
                    break
            except Exception as general_err:
                print "General Error - ", general_err.args
                break






        print "Client disconnected..."
        print "Before close son socket - total clients = %d (%d)" % (how_many_clients("Child"),total_clients)
        change_total_clients.acquire()
        total_clients -= 1
        change_total_clients.release()





        self.send_msg("closing now byby")

        self.conn.close()




    def first_recv_to_log_in(self):
        #check if the msg we got is the log is' and if it does, so log in
        to_send =""
        headers = []
        while self.state != State_enum.logged_in:
            try:

                #  first msg: 'LOGIN:Adi\n\n\n\n\nPassword\n\n\n\n\n '
                data = self.recv_msg()

                if data=="":
                    print "Got empty data from Recv Will close this client socket"
                    self.conn.close()
                    return False


                if data == "byby":
                    self.state = State_enum.end
                    break
                to_send = self.check_login(data)

                if (self.state == State_enum.start) and (to_send == "not correct log in"):
                    self.send_msg(to_send)


                return to_send




            except socket.error as e:
                if e.errno == ECONNRESET: #'Connection reset by peer'
                    print "Error %s - Seems Client Disconnect. try Accept new Client " % e.errno
                    break
                elif e.errno == EWOULDBLOCK or str(e) == "timed out":  # if we use conn.settimeout(x)
                    if father_going_to_close:
                        print "Father Going To Die"
                        self.conn.close()
                        return []
                    print ",",
                    continue
                else:
                    print "Unhandled Socket error at recv. Server will exit %s " % e
                    self.conn.close()
                    return []
            except Exception as general_err:
                print "General Error - ", general_err.args
                self.conn.close()
                return []



        return []


    def check_login(self, data):
        """
        check the syntax of the msg of log in.
        """
        edited_data = editor_data(data, True)
        dct_info = edited_data.dct_data
        str_return  = "not correct log in"
        if dct_info.has_key("LOGIN") and dct_info.has_key("PASSWORD"):
            user_name = dct_info["LOGIN"]
            password = dct_info["PASSWORD"]

            print 'got login ' + user_name + " and " + password

            if self.sign_in(user_name, password):
                self.client_name = user_name
                self.password = password
                self.state = State_enum.logged_in
                str_return =  []
                if dct_info.has_key("HEADERS"):
                    str_return = dct_info["HEADERS"]



        elif dct_info.has_key("NEW ACCOUNT") and dct_info.has_key("PASSWORD"):
            user_name = dct_info["NEW ACCOUNT"]
            password = dct_info["PASSWORD"]
            print 'got user ' + user_name + " and " + password
            if self.sign_up(user_name, password):
                self.client_name = user_name
                self.password = password
                self.state = State_enum.logged_in
                str_return =  []
                if dct_info.has_key("HEADERS"):
                    str_return = dct_info["HEADERS"]
        return str_return


def how_many_clients(caller):
        if caller == "main":
            return threading.activeCount() -1
        else:
            return threading.activeCount()-1


def main(port):
    global total_clients
    global father_going_to_close



    print 'SMC version 1.1'

    father_going_to_close = False

    total_clients = 0

    s = socket.socket()
    ip = socket.gethostname() #"127.0.0.1"

    #  SO_REUSEADDR means : reopen  socket even if its in wait state from last execution without waiting
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", port))
    print "After bind to " + ip + " port: " + str(port)

    s.listen(10)
    print "After listen"

    threads = []
    tid =0

    s.settimeout(None)
    cnt =0

    IsAttackOfConnect = False
    countHowManyConnect =0
    while True:
        try:
            print "start"

            if not IsAttackOfConnect:
                print "just entered"
                conn, (ip, port) = s.accept()
                print ip, port
                print "\n new client\n"
                tid += 1

                new_thread = ClientThread(ip, port, conn, tid)
                new_thread.start()
                print "Clients = %d (%d) "% (how_many_clients("main"),total_clients)
                threads.append(new_thread)
                countHowManyConnect+=1

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


    s.close()
    print "Server Says: Bye Bye ...."
    for t in threads:
         t.join()
    return

# End main

global father_going_to_close
global users
if __name__ == '__main__':


    try:
        main(3001)
    except KeyboardInterrupt:
        print "\nGot ^C Main\n"
        father_going_to_close = True


