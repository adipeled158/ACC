__author__ = 'Irit'
import pickle

class Acc_msg_edit():
    def __init__(self, data, is_recv_msg):
        self.data = ""
        self.dct_data = {}
        if is_recv_msg:
            self.factorize_data(data)
        else:
            self.union_data(data)



    def factorize_data(self, data):
        """
        the function get a long string and factorize him into pies in a dictionary:
        the recieved data looks like:
        "15$User name:asrvy11$Password:peled"
           ||
           \/
        a structure of a nassage build like:
        !) length msg
        2) $ - (key that sign the end of the length)
        3) key word (the msg's intention)
        4) : - simbles the beginning if the content of the msg
        5) the content of the msg

        the factorize data will be in a dictionary and it will be looking like:

        { User name : asrvy
          Password :  peled
          }

        if the value of the dictionari is pickle, so the first wird in the section, will be 'pickle'
        for example:
        "pickle15$User name:asrvy11$Password:j[kopeled"


        """
        self.data = data
        dct_data_splited = {}

        while len(data)>0:
            is_pickle = False
            if len(data)> len("pickle"):
                if data[:len("pickle")] == "pickle":
                    is_pickle = True
                    data = data[len("pickle"):]
            indx_dollar = data.find("$")
            if indx_dollar!=-1:
                len_data = int(data[:indx_dollar])
                specific_data = data[indx_dollar+1:indx_dollar+1+len_data]
                data  = data[indx_dollar+1+len_data:]

                lst_data = specific_data.split(":")
                if is_pickle:
                    lst_data[1] = pickle.loads(lst_data[1])
                dct_data_splited[lst_data[0]] =  lst_data[1]
            else:
                break

        self.dct_data = dct_data_splited


    def union_data(self, dct_got):
        """
        the function makes the oposite action then the 'factorize_data' function
        """
        self.add_to_dct_data(dct_got)

        str_data = ""
        if len(dct_got) == 0:
            self.data += "0"

        for keys in dct_got:
            val_data = dct_got[keys]
            if type(val_data) != str:
                str_data+="pickle"
                val_data = pickle.dumps(val_data)
            str_data +=str(len((keys+":"+val_data))) + "$"+str(keys)+":"+val_data

        self.data +=str_data

    def add_to_dct_data(self, dct_ata):
        """
        the function add to the dict a new data
        """
        for keys in dct_ata:
            self.dct_data[keys] = dct_ata[keys]





































































