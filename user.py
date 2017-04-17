__author__ = 'user'
import pickle
import sys
from os import walk
import os.path
import time
import project






name_file_users = "Authorized_Users.txt"
name_file_users_pro = "Projects.txt"
name_path = "F:\cc"

def get_all_dirs():
    """
    return in a list all the name of directories in the current folder
    """
    f = []

    for (dirpath, dirnames, filenames) in walk(name_path):
        #name of dirs are removed to a list
        f.extend(dirnames)
        break
    return f

def is_user_exists(user_name):
    """
    the function check
    if there is that user-name in the stoclpile -
    if there is, return true, else, return false
    """

    users = open_file(name_file_users)
    if users != None:
        return (users.has_key(user_name))
    return users

def check_user_by_password(user_name, password):
    """
    check if there is in the stock
    """
    if is_user_exists(user_name):
        users = open_file(name_file_users)
        if users[user_name] == password:
            return True
    return False



def add_new_user_to_stockpile(user_name, password):
    """
    the function call the 'is_user_exists' func,
    and if the user is not exists all-ready, ]
    it add the user to stockpile and return True,
    if it is exists, return False
    """

    users = open_file(name_file_users)
    if not users:
        users = {}
        users[user_name] = password
        users_pro = {}
        users_pro[user_name] = []
    else:
        # the dict looks like: {user_name:password...}
        users[user_name] = password
        # the dict looks like: {user_name:[name pro1......]}
        users_pro = open_file(name_file_users_pro)
        users_pro[user_name] = []
    write_to_file(name_file_users, users) #add to file users the new user
    write_to_file(name_file_users_pro, users_pro) #add to file projects' user the new user


def open_file(name_file):
    """
    open the 'name_file' file
    """
    try:
        return pickle.load(open(name_file, "r"))

    except Exception as err:
        print ("problem with open file '%s' :" % (name_file)),err.args

def write_to_file(name, content):
    """
    write to 'name_file' the 'content'
    """
    try:
        pickle.dump(content, open(name, "w"))
    except Exception as err:
        print ("problem with write to file '%s' :" % (name)),err.args
        return False

def get_name_projects_by_user(user_name, without_acc_key):
    """
    the function return all the users name

    """

    data = open_file(name_file_users_pro)
    if data == None:
        return data
    if data.has_key(user_name):
        if not without_acc_key:
            return data[user_name]
        return make_lst_acc_to_regular(data[user_name])
    return []

def get_projects_and_info_to_client(user_name, password, lst_headers_return):
    """
    irders the projects by that:
    {Project-name: [creater, date create..]}
    'lst_headers_return' contains a list with all the headers that the function will return
    for example, if the list contains - ["date_created", "num_current_ver"]
    the function will return a dictionary:
    { 'name_pro1' : [ "11.2.2017",  "0.7"] , ....}
    """
    dct_final ={}
    for pro in get_name_projects_by_user(user_name, True):
        cls_pro = project.acc_project(pro, user_name, password)
        dict_info_pro = cls_pro.get_all_info_of_acc_pro()
        lst_info = []
        for header in lst_headers_return:
            if dict_info_pro.has_key(header):
                lst_info.append(dict_info_pro[header])
        dct_final[pro] = lst_info
    return dct_final

def make_lst_acc_to_regular(lst_all):
    """
    get a list of name that start with the string 'acc'
    and return the list with out the 'acc' string
    """
    return [(name[len("acc"):]) for name in lst_all if name.find("acc") == 0]


def add_new_project_to_user(user_name, pro_name):
    """
    the function gets user name and name project, check
    if user-name exists (by calling the func 'is_user_exists'.
    If he doesn't exists, return False,
    If  he exists, add to the projects of the user,
    the current project and return True.
    If the user has already the project, return False.
    """

    lst_name_pros = get_all_dirs()


    lst_user_pro = get_name_projects_by_user(user_name, False)


    new_name_pro = change_name_of_file_or_dir(pro_name, lst_name_pros)
    not_exists = create_pro_in_dir(new_name_pro, user_name)
    if not not_exists:
        return False


    lst_user_pro.append(new_name_pro)

    dict_user_pros = open_file(name_file_users_pro)
    dict_user_pros[user_name] = lst_user_pro
    write_to_file(name_file_users_pro, dict_user_pros)
    create_info_file_in_new_project(new_name_pro, user_name)

    return True

def create_info_file_in_new_project(pro_name, user_name):
    """
    when user create a new project
    the function create the file that has all the information about the project:
    info file:
        {"authorized_users":[user,user],
            "files_version":{(file_name, ver), (file_name2, ver)} ,
            "num_current_ver" : num.num
            "date created"   : date
            " owner" : name owner
            }
    """
    time_n = time.localtime()
    date = str(time_n[1])+"."+str(time_n[2])+"."+str(time_n[0])
    content = {"authorized_users":[],
                "files_version":[],
                "num_current_ver" : "0.1",
                "date_created":date,
                "owner": str(user_name)}
    write_to_file((name_path+"\\"+pro_name+"\\"+"info_pro.txt"), content)
    #write_to_file((name_path+"\\"+pro_name+"file_pro.txt"), {})





def create_pro_in_dir(name_pro, user_name):
    """
    create a new dir that represent a project
    also, create the file 'Authorized_Users.txt' inside the new project.
    """

    new_path = name_path+ "\\" + name_pro
    if not os.path.exists(new_path):
        os.makedirs(new_path)

        return True
    return False





def add_user_to_pro(user_name, pro_name):
    """
    add exist project to the user
    """
    pro_name = "acc" + pro_name
    lst_user_pro = get_name_projects_by_user(user_name, False)
    if lst_user_pro.__contains__(pro_name):
        return False
    lst_user_pro.append(pro_name)
    dict_user_pros = open_file(name_file_users_pro)
    dict_user_pros[user_name] = lst_user_pro
    write_to_file(name_file_users_pro, dict_user_pros)
    create_info_file_in_new_project(lst_user_pro, user_name)

    return True





def change_name_of_file_or_dir(name, lst_names):
    """
    the function add to the name of file or dir 3 digits
    """
    lst_all_current_names = [new_name for new_name in lst_names if(new_name.find(name))]
    lst_all_current_names = make_lst_acc_to_regular(lst_all_current_names)
    cnt_same_names = 0
    for same_nam in lst_all_current_names:
        if same_nam[:len(same_nam)-3] == name:
            cnt_same_names+=1

    str_num_name = str(cnt_same_names)
    if len(str_num_name) == 1:
        str_num_name = "00" + str_num_name
    elif len(str_num_name) == 2:
        str_num_name = "0"+ str_num_name
    elif len(str_num_name) > 3:
        return ""


    return "acc" + name + str_num_name
