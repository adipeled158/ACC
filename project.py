__author__ = 'project'
import os.path
from os import walk
import pickle
import pro_file
import user

path = "F:\cc"




class acc_project(object):
    def __init__(self, name_pro, user_name, password):
        name_pro = "acc"+name_pro
        self.password = password
        self.path = path +"\\"+ name_pro
        self.name_pro = name_pro
        self.user_name = user_name
        self.path_info_pro = self.path+"\\"+"info_pro.txt"
        """
        info file:
        {"authorized_users":[user,user],
            "files_version":{file_name: ver, file_name2, ver} ,
            "num_current_ver" : num.num

            }
        """

    def name_files(self):
        """
        check all the 'files' name of the project.

        return lst[(file_name, ver), (file_name2, ver)]
        """
        info_file = self.read_from_pickle_file(self.path_info_pro)
        return info_file["files_version"]

    def get_all_info_of_acc_pro(self):
        """
        return all the info of the acc project
        (the file self.path_info_pro)
        """
        return self.read_from_pickle_file(self.path_info_pro)


    def name_authorized_users(self):
        """
        call module 'dict_ Authorized_users' and return the list
        [manager user(str), lst[user, user...]]
        """
        info = self.read_from_pickle_file(self.path_info_pro)
        return info["authorized_users"]



    def read_from_pickle_file(self, name_file):
        """
        return the content of file
        """
        try:
            return pickle.load(open(name_file, "r"))
        except Exception as err:
            print ("problem with write to file '%s' :" % (name_file)),err.args
            return False

    def add_new_user_to_project(self, user_name, password):
        """
        use the module ' dict_ Authorized_users'
        and add new user to the project
        """
        info = self.read_from_pickle_file(self.path_info_pro)

        authorized_users = info["authorized_users"]
        if len(authorized_users)>0:
            if self.user_name == authorized_users[0] and (not user_name in authorized_users): #the manager of the project
                if user.is_user_exists(user_name):
                    authorized_users.append(user_name)
        info["authorized_users"] = authorized_users
        self.write_to_pickle_file(self.path_info_pro, info)
        user.add_user_to_pro(user_name, password, self.name_pro)


    def num_vers(self):
        """
        check the num of version that
        the project has and return the num.
        """

        dict_info_file = self.read_from_pickle_file(self.path_info)
        num_current_ver = float(dict_info_file["num_current_ver"])
        return num_current_ver

    def get_name_files_by_ver(self, ver):
        """
        gets num of version,  open with 'read_from_pickle_file' func
        the 'files_ver.txt' that is inside the version of project.
        gets from it the name of the files and the number of version that they has.
        go to the project folder, use 'get_lst_files' func and return that value.


        'files_ver.txt':
            {name_file:num_ver....}

        """
        name_dir_ver = self.path + "\Ver_pro_" + str(ver) + "files_ver.txt"
        info_ver = self.read_from_pickle_file(name_dir_ver)

        return self.get_lst_files(info_ver)

    def get_ver_file(self, name_file, num_ver):
        """
        use the file module,
        and return the content of the file version.
        """
        file_use = pro_file.file(self.name_pro, name_file, self.user_name)
        return file_use.get_file_by_ver(num_ver)

    def get_lst_files (self, lst_name_files):
        """
        pass one by one according to the name of the file
        and the version, and call 'get_ver_file' func.
        return the list of the content of the file- inside a dict.

        """
        dict_files_content = {}

        for name_file, ver in lst_name_files:
            dict_files_content[name_file] = self.get_ver_file(name_file, ver)
        return dict_files_content


    def upload_ver(self):
        """
        create a folder of 'version' and add a text file
        that has all the version files+the version of every file.
        """
        dict_info_file = self.read_from_pickle_file(self.path_info)

        num_current_ver = float(dict_info_file["num_current_ver"])


        dict_info_file["num_current_ver"] = str(num_current_ver+ 0.1)

        path_ver = self.path+"\\" + str(num_current_ver)
        #self.write_to_file(path_ver, content_new_code)

        self.write_to_pickle_file(self.path_info, dict_info_file)

        self.create_pro_in_dir(self,("Ver_pro_" + str(num_current_ver) ))


    def create_pro_in_dir(self, pro_name):
        """
        create a new dir that represent a project
        also, create the file
        'files_ver.txt':
            {name_file:num_ver....}
            that inside the direct of the ver
        """
        new_path = self.path+ "\\" + pro_name
        if not os.path.exists(new_path):
            os.makedirs(new_path)
            dict_info_pro = self.read_from_pickle_file(self.name_pro)
            dict_info_pro["files_version"]
            content = dict_info_pro["files_version"]
            self.write_to_pickle_file((new_path+"\\"+"files_ver.txt"), content)

            return True
        return False

    def get_num_file_ver(self, file):
            """
            check how many version there is,
            and return the number
            """
            file_in_pro = pro_file.file(self.name_pro, file, self.user_name)
            return file_in_pro.get_num_ver()


    def create_new_file(self, name_file, content):
        """
        use the module file and create a new file in the project
        return the name of the new file
        """
        self.upload_ver_file(name_file, content)


    def update_file(self, tuple_new):
        """
        update in the file of the info of the acc project, the file
        """
        dict_info_file = self.read_from_pickle_file(self.path_info)
        lst_files = dict_info_file["files_version"]
        lst_files.append(tuple_new)

        dict_info_file["files_version"] = lst_files


        self.write_to_pickle_file(self.path_info, dict_info_file)




    def w_and_r_file(self, file_name):
        """
        use the module file and
        if it can get the file,
        return the content of the file,
        if it cannot, return None.
        """

        file_use =  pro_file.file(self.name_pro, file_name, self.user_name)
        return file_use.get_file_for_r_and_w()

    def r_file(self, file_name):
        """
        use the module file and
        return the content of the file
        only for reading and not for writing
        """
        file_use =  pro_file.file(self.name_pro, file_name, self.user_name)
        return file_use.get_file_for_r()

    def upload_ver_file(self, file_name, content):
        """
        use the module file and try to upload a new version of file,
        return True if it worked.
        """
        file_use =  pro_file.file(self.name_pro, file_name, self.user_name)
        file_use.upload_ver(content)
        self.update_file((file_use.name_file, file_use.get_num_ver()))



    def write_to_pickle_file(self, name, content):
        """
        write to 'name_file' the 'content'
        """
        try:
            pickle.dump(content, open(name, "w"))
        except Exception as err:
            print ("problem with write to file '%s' :" % (name)),err.args
            return False




    def get_all_dirs(self, path_of_pro):
        """
        return all the names of fprojects - that represent by dirs.
        """
        f = []

        for (dirpath, dirnames, filenames) in walk(path_of_pro):
            #name of dirs are removed to a list
            f.extend(dirnames)
            break
        return f


    def get_files_and_info_to_client(self, lst_headers_return):
        """
        irders the files by that:
        {file-name: [creater, date create..]}
        'lst_headers_return' contains a list with all the headers that the function will return
        for example, if the list contains - ["date_created", "num_current_ver"]
        the function will return a dictionary:
        { 'name_file1' : [ "11.2.2017",  "0.7"] , ....}
        """
        dct_final ={}
        for file_name, ver in self.name_files():
            cls_file = pro_file.file(self.name_pro, file_name, self.user_name)
            dict_info_file = cls_file.get_all_info_of_acc_pro()
            lst_info = []
            for header in lst_headers_return:
                if dict_info_file.has_key(header):
                    lst_info.append(dict_info_file[header])
            dct_final[file_name] = lst_info
        return dct_final

