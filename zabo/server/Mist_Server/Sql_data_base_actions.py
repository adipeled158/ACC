__author__ = 'Tomer Zabo'


import sqlite3

import hashlib



class Sql_Data_Base_Actions():
    def __init__(self):
        self.All_user_info_Table = sqlite3.connect('All_Users_Info')
        self.cur = self.All_user_info_Table.cursor()

    def Add_new_user(self,table_name,user_name,password,first_name,last_name,email,secret_question):
        self.cur.execute("INSERT INTO "+table_name+ "(User_name,Password,First_Name,Last_Name,Email,Secret_Question) VALUES "\
                                                    "('" +str(user_name)+"' , '"+str(password)+"' , '"+str(first_name)+"' , '"+str(last_name)+"' , '"+str(email)+"' , '"+str(secret_question) +"');" )

        self.All_user_info_Table.commit()



    def Check_email(self,table_name,email):
        string="SELECT EXISTS (SELECT  'True' FROM "+table_name + " WHERE "+table_name+".Email='"+email+"' ) "

        check=self.cur.execute(string)

        return check.fetchone()[0]
        self.cur.close()

    def check_email_and_answer(self,table_name,secret_answer,email):
        string="SELECT EXISTS (SELECT  'True' FROM "+table_name + " WHERE "+table_name+".Email='"+email+"' AND "+table_name+".Secret_Question='"+secret_answer+"' ) "
        check=self.cur.execute(string)
        return check.fetchone()[0]
        self.cur.close()

    def Check_user_name(self,table_name,user_name):
        string="SELECT EXISTS (SELECT  'True' FROM "+table_name + " WHERE "+table_name+".User_name='"+user_name+"' ) "
        print user_name
        check=self.cur.execute(string)

        return check.fetchone()[0]
        self.cur.close()

    def set_password_by_email(self,table_name,email,password):
        m = hashlib.md5()
        m.update(str(password))
        passowrd_to_insert=m.hexdigest()
        string="UPDATE "+table_name+ " SET Password='"+passowrd_to_insert+"' WHERE Email='"+email+"' ;"
        check=self.cur.execute(string)

        self.All_user_info_Table.commit()
        return
        self.cur.close()


    def Check_password_correct_by_user_name(self,table_name,user_name,password):
        string="SELECT EXISTS (SELECT  'True' FROM "+table_name + " WHERE "+table_name+".User_name='"+user_name+"' AND "+table_name+".Password='"+password+"' ) "
        check=self.cur.execute(string)
        return check.fetchone()[0]
        self.cur.close()



    def get_all_info_by_user_name(self,table_name,user_name):
        string="SELECT First_Name,Last_Name,Email,Secret_Question FROM "+table_name+" WHERE "+table_name+".User_name='"+user_name+"';"
        check=self.cur.execute(string)
        return check.fetchone()
        self.cur.close()


"""
All_user_info_Table = Sql_Data_Base_Actions()
All_user_info_Table.Add_new_user("All_User_Info","toasdfmer","zasdfabo","tomasfderrr","zaboasdfooo","arktomer","secret_santa")
All_user_info_Table.Check_email("All_User_Info","arktomer")
"""