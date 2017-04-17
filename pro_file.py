__author__ = 'user'
import os.path
from os import walk
import pickle
import time


path = "F:\cc"




class file (object):
    def __init__(self, name_pro, name_file, user_name):
        """
        open a exists version file,
        if the file doesn't exists,
        it add it to the project's
        files and to the latest version.
        """

        name_file = "acc" + name_file

        help = name_file[::-1]
        lst_name = help.split(".")
        name_file = name_file[1:]
        self.type_file = lst_name[0][::-1]
        name_file = ("".join(str(x) for x in lst_name[1::]))[::-1]
        self.path = path +"\\" + name_pro +"\\"+ name_file
        self.name_pro = name_pro
        self.name_file = name_file
        self.user_name = user_name
        self.path_info = self.path+"\\"+"info_of_file.txt"
        if not os.path.isdir(self.path):
            self.create_new_file()






    def get_file_for_r_and_w(self):
        """
        call the func 'who_locked'.
        if the user that returned match the user(in the input),
        return the content of the last version file.
        if it isn't the user that locked, return None.
        if no-one locked the file,
        call to 'lock_file' func and lock the file,
        and send to the user the content of file.
        """
        dict_info_file = self.read_from_pickle_file(self.path_info)



        who_locked = dict_info_file["locked_by"]
        if str(who_locked) !="None":
            if str(who_locked) != self.user_name:
                return None
        else:
            dict_info_file["locked_by"] = self.user_name

        self.write_to_pickle_file(self.path_info, dict_info_file)
        num_current_ver = dict_info_file["num_current_ver"]
        return self.get_file_by_ver(self, num_current_ver)

    def get_file_for_r(self):
        """
        return the content of the latest version's file
        """
        dict_info_file = self.read_from_pickle_file(self.path_info)
        num_current_ver = dict_info_file["num_current_ver"]
        return self.get_file_by_ver(self, num_current_ver)



    def create_new_file(self):
        """
        create a new file in the project and upload it to the 'current version' file
        """

        if os.path.isdir((path+"\\"+self.name_pro)):
            lst_all_name_files = self.get_all_dirs()
            self.change_name_of_file_or_dir(lst_all_name_files)
            os.makedirs(self.path)
            time_n = time.localtime()
            date = str(time_n[1])+"."+str(time_n[2])+"."+str(time_n[0])
            dict_file_info = {"locked_by": "None",
                              "num_current_ver": 0.0,
                              "date_created":date,
                             "created by":self.user_name,
                             "type":self.type_file}



            self.write_to_pickle_file(self.path_info, dict_file_info)

    def read_from_pickle_file(self, name_file):
        """
        return the content of file
        """
        try:
            return pickle.load(open(name_file,"r"))
        except Exception as err:
            print ("problem with write to file '%s' :" % (name_file)),err.args
            return False


    def upload_ver(self, content_new_code):
        """
        upload the new version

        """
        dict_info_file = self.read_from_pickle_file(self.path_info)



        who_locked = dict_info_file["locked_by"]
        if str(who_locked) !="None":
            if str(who_locked) != self.user_name:
                return False


        num_current_ver = float(dict_info_file["num_current_ver"])


        dict_info_file["locked_by"] = "None"
        dict_info_file["num_current_ver"] = str(num_current_ver+0.1)

        path_ver = self.path+"\\" + str(num_current_ver)
        self.write_to_file(path_ver, content_new_code)

        self.write_to_pickle_file(self.path_info, dict_info_file)

        return True


    def get_num_ver(self):
        """
        check how many version there is,
        and return the number
        """
        dict_info_file = self.read_from_pickle_file(self.path_info)
        num_current_ver = dict_info_file["num_current_ver"]
        return num_current_ver



    def get_file_by_ver(self, num_ver):
        """
        the return value is the content of the version's content
        """
        path_ver = self.path+"\\"+str(num_ver)
        if os.path.isfile(path_ver):
            return self.read_from_file(path_ver)


        return False


    def read_from_file(self, name):
        """
        write to 'name_file' the 'content'
        """
        try:
            with open(name, "r") as c_file:
                c_file.read()
        except Exception as err:
            print ("problem with read file '%s' :" % (name)),err.args
            return False



    def write_to_file(self, name, content):
        """
        write to 'name_file' the 'content'
        """
        try:
            with open(name, "wb") as c_file:
                c_file.write(content)
        except Exception as err:
            print ("problem with write to file '%s' :" % (name)),err.args
            return False

    def write_to_pickle_file(self, name, content):
        """
        write to 'name_file' the 'content'
        """
        try:
            pickle.dump(content, open(name, "w"))
        except Exception as err:
            print ("problem with write to file '%s' :" % (name)),err.args
            return False


    def get_all_dirs(self):
        """
        return all the names of files - that represent by dirs.
        """
        f = []

        for (dirpath, dirnames, filenames) in walk((path+"\\"+self.name_pro)):
            #name of dirs are removed to a list
            f.extend(dirnames)
            break
        return f

    def change_name_of_file_or_dir(self, lst_names):
        """
        the function add to the name of file or dir 3 digits
        """
        lst_all_current_names = [new_name for new_name in lst_names if(new_name.find(self.name))]
        cnt_same_names = 0
        for same_nam in lst_all_current_names:
            if same_nam[:len(same_nam)-4] == same_nam:
                cnt_same_names+=1

        str_num_name = str(cnt_same_names)
        if len(str_num_name) == 1:
            str_num_name = "00" + str_num_name
        elif len(str_num_name) == 2:
            str_num_name = "0"+ str_num_name
        elif len(str_num_name) > 3:
            return False


        self.name_file = self.name_file + str_num_name
        self.path = path +"\\" + self.name_pro +"\\"+ self.name_file
        self.path_info = self.path+"\\"+"info_of_file.txt"
    def get_all_info_of_acc_file(self):
        """
        return all the info about the file
        """
        return self.read_from_pickle_file(self.path_info)