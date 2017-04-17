__author__ = 'Tomer Zabo'

class Massage_codes():
    def __init__(self):
        self.Error_massge_list=["Bad Port","Bad IP","Bad Port or IP","Socket Error","General Error ,Something bad happend ", #6
                                "One or More or the fields is empty","Passwords does not match","Email must be Gmail type",#9
                                "Email alraedy in use","User Name already exists","Email not exists","Failed ... Please check your email",#13
                                "Sorry your answer is not correct","User Name Not Exists","Wrong Password ......"]#16

        self.Success_massge_list=["Good IP and Port", "Connection succeeded press OK to continue","Sent Public key and got Public key from server", #3
                                  "Created Account Successfully","Recovered Password successfully","Login succeeded press OK to continue"] #6
        self.Actions_massge_list=["nothing"]

    def Return_massage(self,code):
        if code>0 and code<100:
            return self.Error_massge_list[code-1],"Error"

        elif code>100 and code<200:
            return  self.Success_massge_list[code-101],"Success"

        else:
            return  self.Actions_massge_list[code-201],"Action"

