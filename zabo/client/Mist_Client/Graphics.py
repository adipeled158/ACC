__author__ = 'Adi is here'

import sys
import pickle
import wx
import  glob, random
from wx.lib.filebrowsebutton import FileBrowseButton

from acc_client import Acc_client as client
import wx.lib.buttons as buttons
import wx.lib.newevent
import threading
from Massage_codes import Massage_codes
#import win32gui
import win32con
import socket
import time
from acc_msg_editor import Acc_msg_edit as editor_data

print "adi peled was was here"



#from validate_email import validate_email
DataEvent, EVT_DATA = wx.lib.newevent.NewEvent()

APP_SIZE_X = 900
APP_SIZE_Y = 700
division_line = "\n\n\n\n\n"
headers_pros = ["num_current_ver", "date_created", "owner"]
headers_files = ["num_current_ver", "date_created", "created by"]


def is_connented_server(ip, port):
    """
    connecting to server
    abd exchanging public keys
    """
    HELP_Massage_codes=Massage_codes()
    client_actions=client(ip,port)

    is_connected = client_actions.is_good_socket()

    if not is_connected:
        return False

    return client_actions


class Listed_object:
    def __init__(self, lst_headers_name, lst_info_obj):
        self.lst_info_obj = lst_info_obj
        self.lst_headers = lst_headers_name









class Menu(wx.Frame):
    def __init__(self, client_atc):
        """
        dispalys entry frame
        """
        self.client_actions = client_atc
        wx.Frame.__init__(self, None, -1, "Code Control", size=(APP_SIZE_X,APP_SIZE_Y))



        p = wx.Panel(self, -1)

        fgs = wx.FlexGridSizer(cols=900, hgap=10, vgap=10)
        imageFile='a.png'
        img1 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY)

        self.sb1 = wx.StaticBitmap(p, -1, wx.BitmapFromImage(img1),size=(APP_SIZE_X,APP_SIZE_Y))





        fgs.Add(self.sb1)
        p.SetSizerAndFit(fgs)



        self.shape_button("Black","SLATE BLUE",(320,300),(230,70),1,"Sign In",self.sb1,fgs)
        self.shape_button("Black","SLATE BLUE",(320,410),(230,70),2,"Sign Up",self.sb1,fgs)



        self.sb1.Bind(wx.EVT_BUTTON, self.sign_in, id=1)
        self.sb1.Bind(wx.EVT_BUTTON, self.sign_up, id=2)




        self.signal=True


        self.Fit()
        self.Centre()
        self.Show(True)





    def Close_app(self):
        """
        closes current frame
        """
        self.Close(True)

    def shape_button(self,color1,color2,loc,size,id,string,where_to,add_to):
        """
        shapes a button and presents it on the screen
        """
        b = buttons.GenButton(where_to, id, string,loc,size)
        b.SetFont(wx.Font(20, wx.SWISS, wx.NORMAL, wx.BOLD, False))
        b.SetBezelWidth(5)
        b.SetBackgroundColour(color1)
        b.SetForegroundColour(color2)
        add_to.Add(b)


    def sign_in(self,event):
        #call o sign in class
        sign_in_frame = Sign_in(None,self.client_actions)
        sign_in_frame.Show()
        self.Close()

    def sign_up(self,event):
        """
        goes to create new account frame
        """
        sign_in_frame = Sign_up(None,self.client_actions)
        sign_in_frame.Show()
        self.Close()




class Sign_in(wx.Frame):
    def __init__(self, parent,client_act):
        """
        dispalys entry frame
        """

        wx.Frame.__init__(self, parent, -1, "Code Control", size=(APP_SIZE_X,APP_SIZE_Y))
        self.Massage_codes=Massage_codes()
        self.client_actions=client_act

        p = wx.Panel(self, -1)

        fgs = wx.FlexGridSizer(cols=900, hgap=10, vgap=10)
        imageFile='Tologin.jpg'
        img1 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY)

        self.sb1 = wx.StaticBitmap(p, -1, wx.BitmapFromImage(img1) ,size=(APP_SIZE_X,APP_SIZE_Y))

        fgs.Add(self.sb1)
        p.SetSizerAndFit(fgs)


        wx.Button(self.sb1,label = "Login", pos = (320,490), size=(180,80), id = 1)


        wx.Button(self.sb1,label = "Go Back", pos = (600,590), size=(270,80), id = 2)



        self.sb1.Bind(wx.EVT_BUTTON, self.Login, id=1)
        self.sb1.Bind(wx.EVT_BUTTON, self.back_to_menu, id=2)


        self.user_name_input = wx.TextCtrl(self.sb1, value="", pos=(330, 245), size=(250,30))


        self.user_name_input.SetMaxLength(12)



        self.Password = wx.TextCtrl(self.sb1, value="", pos=(330, 410), size=(250,30),style=wx.TE_PASSWORD)
        self.Password.SetMaxLength(20)

        self.Bind(EVT_DATA, self.Login)

        self.signal=True


        self.Fit()
        self.Centre()




    def Close_app(self):
        """
        closes current frame
        """

        self.Close(True)



    def call_massage_box(self,massage,type):
        """
        displays massage box on the screen
        """
        dlg = wx.MessageDialog(None,massage, type, wx.OK)
        retCode = dlg.ShowModal()

        dlg.Destroy()

        #retCode = wx.MessageBox("Is this way easier?", "Via Function",wx.YES_NO | wx.ICON_QUESTION)

    def Login(self,event):

        if self.user_name_input.Value==""  or self.Password.Value=="":
            code=(self.Massage_codes.Return_massage(6))
            self.call_massage_box(code[0],code[1])

        else:
            user_name = str(self.user_name_input.Value)
            password = str(self.Password.Value)
            dct_to_dend = {"LOGIN": user_name, "PASSWORD":password}
            editor = editor_data(dct_to_dend, False)

            editor.union_data({"HEADERS":headers_pros})

            self.client_actions.send(editor.data)
            self.check_user_name_and_open_projects()

    def order_recv_from_server(self):
        """
        make the revieving data from server be organize

        it should look like:
        "Projects:num pro = 2
        """



    def check_user_name_and_open_projects(self):
        """
        wait for server to answer the info that just has been sent.
        and if it is correct username and password
        open the acc projects
        """
        data = self.client_actions.recv()
        if str(data) != "not correct log in":

            table = Acc_projects_or_files(self.client_actions, data, True)

            self.Close()

        else:
            Sign_up(self.client_actions)
            self.Close()


    def back_to_menu(self,event):
        """
        goes to create new account frame
        """
        menu= Menu(self.client_actions)
        menu.Show()
        self.Close()




    def listen(self,window,client_obj):
        while self.signal:

            try:
                client_obj.get_sock().settimeout(1)
                data=client_obj.recv_and_dec_massage()

                if data != "":
                    print "recv <<<<<< "+data
                    wx.PostEvent(window,DataEvent(data=data))



            except socket.error as e:
                if e.errno == 10035 or str(e) == "timed out":
                    continue


            except Exception as general_err:
                print "General Error - ", general_err.args






class Sign_up(wx.Frame):
    def __init__(self, parent,client_act):
        """
        dispalys entry frame
        """

        wx.Frame.__init__(self, parent, -1, "Code Control", size=(APP_SIZE_X,APP_SIZE_Y))
        self.Massage_codes=Massage_codes()
        self.client_actions=client_act

        p = wx.Panel(self, -1)

        fgs = wx.FlexGridSizer(cols=900, hgap=10, vgap=10)
        imageFile='Tologin.jpg'
        img1 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY)

        self.sb1 = wx.StaticBitmap(p, -1, wx.BitmapFromImage(img1) ,size=(APP_SIZE_X,APP_SIZE_Y))

        fgs.Add(self.sb1)
        p.SetSizerAndFit(fgs)


        wx.Button(self.sb1,label = "Create Account", pos = (320,490), size=(180,80), id = 1)


        wx.Button(self.sb1,label = "Go Back", pos = (600,590), size=(270,80), id = 2)



        self.sb1.Bind(wx.EVT_BUTTON, self.create_account, id=1)
        self.sb1.Bind(wx.EVT_BUTTON, self.back_to_menu, id=2)


        self.user_name_input = wx.TextCtrl(self.sb1, value="", pos=(330, 245), size=(250,30))
        self.user_name_input.SetMaxLength(12)



        self.Password = wx.TextCtrl(self.sb1, value="", pos=(330, 410), size=(250,30),style=wx.TE_PASSWORD)
        self.Password.SetMaxLength(20)

        self.Bind(EVT_DATA, self.create_account)

        self.signal=True


        self.Fit()
        self.Centre()
        self.Show(True)




    def Close_app(self):
        """
        closes current frame
        """

        self.Close(True)



    def call_massage_box(self,massage,type):
        """
        displays massage box on the screen
        """
        dlg = wx.MessageDialog(None,massage, type, wx.OK)
        retCode = dlg.ShowModal()

        dlg.Destroy()

        #retCode = wx.MessageBox("Is this way easier?", "Via Function",wx.YES_NO | wx.ICON_QUESTION)

    def create_account(self,event):


        if self.user_name_input.Value==""  or self.Password.Value=="":
            code=(self.Massage_codes.Return_massage(6))
            self.call_massage_box(code[0],code[1])

        else:
            user_name = str(self.user_name_input.Value)
            password = str(self.Password.Value)
            dct_to_dend = {"NEW ACCOUNT": user_name, "PASSWORD":password}
            editor = editor_data(dct_to_dend, False)

            editor.union_data({"HEADERS": headers_pros})

            self.client_actions.send(editor.data)

            self.check_user_name_and_open_projects()

    def check_user_name_and_open_projects(self):
        """
        wait for server to answer the info that just has been sent.
        and if it is correct username and password
        open the acc projects
        """
        data = self.client_actions.recv()
        if str(data) != "not correct log in":


            Acc_projects_or_files(self.client_actions, data, True)
            self.Close()
        else:
            Sign_up(self.client_actions)
            self.Close()


    def back_to_menu(self,event):
        """
        goes to create new account frame
        """
        menu= Menu(self.client_actions)
        menu.Show()
        self.Close()



    def listen(self,window,client_obj):
        while self.signal:

            try:
                client_obj.get_sock().settimeout(1)
                data=client_obj.recv_and_dec_massage()

                if data != "":
                    print "recv <<<<<< "+data
                    wx.PostEvent(window,DataEvent(data=data))



            except socket.error as e:
                if e.errno == 10035 or str(e) == "timed out":
                    continue


            except Exception as general_err:
                print "General Error - ", general_err.args




class Acc_projects_or_files(wx.Frame):
    def __init__(self,client_actions, data, is_pro):
        self.is_pro = is_pro

        self.make_list_project(data)

        wx.Frame.__init__(self, None, -1,"Code Control",size=(900,700))


        self.list = None
        self.editable = False

        self.client_actions = client_actions
        self.MakeListCtrl()
        self.MakeMenu()
        self.Show(True)

    def make_list_project(self, data):
        """
        the func gets a string that represent the table
        orginized it to to a list
        """

        editor = editor_data(data, True)
        dct_pros = editor.dct_data
        #'dct_pros' is a dictionary that the keys are the projects names nad the value is a list with the information about the project

        lst_projects = []

        for pro in dct_pros:
            tuple_info = tuple([pro]) + tuple(dct_pros[pro])
            lst_projects.append(tuple_info)
        if self.is_pro:
            headers = ["PROJECT"] + headers_pros
        else:
            headers = ["FILE"] + headers_files
        self.listed_obj  = Listed_object(headers, lst_projects)





    def MakeListCtrl(self, otherflags=0):


        # if we already have a listctrl then get rid of it
        if self.list:
            self.list.Destroy()

        if self.editable:
            otherflags |= wx.LC_EDIT_LABELS


        # create the list control
        self.list = wx.ListCtrl(self, -1, style=wx.LC_REPORT|otherflags)


        # Add some columns

        for col, text in enumerate(self.listed_obj.lst_headers):
            self.list.InsertColumn(col, text)

        # add the rows
        for row, item in enumerate(self.listed_obj.lst_info_obj):
            index = self.list.InsertStringItem(sys.maxint, item[0])
            for col, text in enumerate(item[1:]):
                self.list.SetStringItem(index, col+1, text)

             #set the data value for each item to be its position in
             #the data list
            self.list.SetItemData(index, row)



        # set the width of the columns in various ways
        self.list.SetColumnWidth(0, 120)
        self.list.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        self.list.SetColumnWidth(2, wx.LIST_AUTOSIZE)
        self.list.SetColumnWidth(3, wx.LIST_AUTOSIZE_USEHEADER)

        # bind some interesting events
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.list)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected, self.list)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated, self.list)

        # in case we are recreating the list tickle the frame a bit so
        # it will redo the layout
        self.SendSizeEvent()
        self.Centre()


    def MakeMenu(self):
        mbar = wx.MenuBar()
        menu = wx.Menu()

        if self.is_pro:
            pro_or_file = "project"
        else:
            pro_or_file = "file"
        item = menu.Append(-1, ("Create new "+pro_or_file))
        self.Bind(wx.EVT_MENU, self.Create_new_acc_pro, item)
        mbar.Append(menu, "&More")
        menu.AppendSeparator()
        item = menu.Append(-1, "E&xit\tAlt-X")
        self.Bind(wx.EVT_MENU, self.OnExit, item)

        menu = wx.Menu()
        item = menu.Append(-1, "Sort ascending")
        self.Bind(wx.EVT_MENU, self.OnSortAscending, item)
        item = menu.Append(-1, "Sort descending")
        self.Bind(wx.EVT_MENU, self.OnSortDescending, item)
        item = menu.Append(-1, "Sort by date")
        self.Bind(wx.EVT_MENU, self.OnSortByDate, item)
        item = menu.Append(-1, ("Sort by"+ pro_or_file+ " name"))
        self.Bind(wx.EVT_MENU, self.OnSortByProName, item)
        menu.AppendSeparator()
        item = menu.Append(-1, "Select all")
        self.Bind(wx.EVT_MENU, self.OnSelectAll, item)
        """
        menu.AppendSeparator()
        item = menu.Append(-1, "Set item text colour")
        self.Bind(wx.EVT_MENU, self.OnSetTextColour, item)
        item = menu.Append(-1, "Set item background colour")
        self.Bind(wx.EVT_MENU, self.OnSetBGColour, item)

        menu.AppendSeparator()
        item = menu.Append(-1, "Enable item editing", kind=wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.OnEnableEditing, item)
        item = menu.Append(-1, "Edit current item")
        self.Bind(wx.EVT_MENU, self.OnEditItem, item)
        """

        mbar.Append(menu, "&Sort by")

        self.SetMenuBar(mbar)
        self.Centre()

    def Create_new_acc_pro(self, evt):
        """
        create a new acc project

        """
        create = Create_new_acc_pro_or_file((not self.is_pro), self.client_actions)
        create.Show()
        self.Close()


    def OnExit(self, evt):
        self.Close()


    def OnItemSelected(self, evt):
        item = evt.GetItem()
        print "Item selected:", item.GetText()
        dct_to_dend = {"OPEN PROJECT": str(item.GetText())}
        editor = editor_data(dct_to_dend, False)

        editor.union_data({"HEADERS":headers_files})

        self.client_actions.send(editor.data)
        self.check_user_name_and_open_projects()


    def check_user_name_and_open_projects(self):
        """
        wait for server to answer the info that just has been sent.
        and if it is correct username and password
        open the acc projects
        """
        data = self.client_actions.recv()
        if str(data) != "not correct project":

            table = Acc_projects_or_files(self.client_actions, data, False)

            self.Close()




    def OnItemDeselected(self, evt):
        item = evt.GetItem()
        print "Item deselected:", item.GetText()

    def OnItemActivated(self, evt):
        item = evt.GetItem()
        print "Item activated:", item.GetText()

    def OnSortAscending(self, evt):
        # recreate the listctrl with a sort style
        self.MakeListCtrl(wx.LC_SORT_ASCENDING)

    def OnSortDescending(self, evt):
        # recreate the listctrl with a sort style
        self.MakeListCtrl(wx.LC_SORT_DESCENDING)

    def OnSortByDate(self, evt):
        def compare_func(row1, row2):
            # compare the values in the 4th col of the data
            val1 = self.listed_obj.lst_info_obj[row1][2]
            val2 = self.listed_obj.lst_info_obj[row2][2]

            if val1 < val2: return 1
            if val1 > val2: return -1
            return 0

        self.list.SortItems(compare_func)


    def OnSortByProName(self, evt):
        def compare_func2(row1, row2):
            # compare the values in the 4th col of the data
            val1 = self.listed_obj.lst_info_obj[row1][1]
            val2 = self.listed_obj.lst_info_obj[row2][1]
            val1 = val1.lower()
            val2 = val2.lower()
            if val1 < val2: return -1
            if val1 > val2: return 1
            return 0

        self.list.SortItems(compare_func2)



    def OnShowSelected(self, evt):
        print "These items are selected:"
        index = self.list.GetFirstSelected()
        if index == -1:
            print "\tNone"
            return
        while index != -1:
            item = self.list.GetItem(index)
            print "\t%s" % item.GetText()
            index = self.list.GetNextSelected(index)

    def OnSelectAll(self, evt):
        for index in range(self.list.GetItemCount()):
            self.list.Select(index, True)

    def OnSelectNone(self, evt):
        index = self.list.GetFirstSelected()
        while index != -1:
            self.list.Select(index, False)
            index = self.list.GetNextSelected(index)


    def OnSetTextColour(self, evt):
        dlg = wx.ColourDialog(self)
        if dlg.ShowModal() == wx.ID_OK:
            colour = dlg.GetColourData().GetColour()
            index = self.list.GetFirstSelected()
            while index != -1:
                self.list.SetItemTextColour(index, colour)
                index = self.list.GetNextSelected(index)
        dlg.Destroy()

    def OnSetBGColour(self, evt):
        dlg = wx.ColourDialog(self)
        if dlg.ShowModal() == wx.ID_OK:
            colour = dlg.GetColourData().GetColour()
            index = self.list.GetFirstSelected()
            while index != -1:
                self.list.SetItemBackgroundColour(index, colour)
                index = self.list.GetNextSelected(index)
        dlg.Destroy()


    def OnEnableEditing(self, evt):
        self.editable = evt.IsChecked()
        self.MakeListCtrl()

    def OnEditItem(self, evt):
        index = self.list.GetFirstSelected()
        if index != -1:
            self.list.EditLabel(index)







class Create_new_acc_pro_or_file(wx.Frame):
        def __init__(self, is_create_file, client_actions):
            """
            create a new acc project

            """

            self.client_actions = client_actions
            self.is_create_file = is_create_file
            self.name_file = ""
            if is_create_file:
                name = "Name new File"
            else:
                name = "Name new Pro"
            wx.Frame.__init__(self, None, -1,name,size=(400,400))

            self.p = wx.Panel(self, -1)

            wx.Button(self.p,label = "ADD", pos = (75, 80), size=(50,20), id = 1)
            self.p.Bind(wx.EVT_BUTTON, self.new_name_pro_file, id=1)



            is_pressed_on_file = True
            if is_create_file:
                is_pressed_on_file = False
                self.p = FileBrowseButton(self.p, id = 2, toolTip="Type fulename or click browse to choose file", dialogTitle="Choose a file", labelText="Select file:")#fileMask="*.file")


            #self.name_pro_or_file = wx.TextCtrl(self.p, value="", pos=(50, 25), size=(100,25))
            #self.name_pro_or_file.SetMaxLength(20)

         #   self.p.Bind(wx.BROWSER_NEW_WINDOW, )

            self.Centre()


        def new_name_pro_file(self, event):
            if self.is_create_file:

                content = self.new_file_helper()
                dct_to_dend = {"NEW FILE": self.name_file, "CONTENT":content, "HEADERS": headers_files}

            else:
                dct_to_dend = {"NEW PROJECT": str(self.name_pro_or_file.Value), "HEADERS": headers_pros}
            editor = editor_data(dct_to_dend, False)

            self.client_actions.send(editor.data)

            recv = self.client_actions.recv()

            #the server will return :
            #"Confirm-User!\n\n\n..Edited-Name:\n\n\n...info of the pro\file:





            Acc_projects_or_files(self.client_actions, recv, self.is_create_file)
            self.Close()

        def new_file_helper(self):
            """
            orginize propertly the info and the content of the new file

            """
            path =  str(self.p.GetValue())
            content = ""
            with open(path, "rb") as file_text:
                content = file_text.read()


            path = path[::-1]

            lst_help = path.split("\\")
            self.name_file = lst_help[0][::-1]
            print "name file:", self.name_file

            return content


        def order_new_pro_or_file(self, recv):
            #the server will return :
            #"Confirm-User!\n\n\n..Edited-Name:\n\n\n...info of the pro\file:

            tpl =  tuple(recv.split(division_line))
            tpl = tpl[:len(tpl)-1]
            return tpl










app = wx.App(0)
client_action =  is_connented_server("127.0.0.1", 3001)
if not client_action:
    print "can't connect to server"
    sys.exit()
frame = Menu(client_action)

app.MainLoop()


