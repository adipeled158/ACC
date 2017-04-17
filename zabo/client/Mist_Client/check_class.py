__author__ = 'User'

import wx
from Mist_Client import Client as client
import wx.lib.buttons as buttons
import wx.lib.newevent
import threading
from threading import *
from Massage_codes import Massage_codes
import win32gui
import win32con
import socket
import time
from validate_email import validate_email
DataEvent, EVT_DATA = wx.lib.newevent.NewEvent()

APP_SIZE_X = 900
APP_SIZE_Y = 700



class Show_Profile(wx.Frame):
    def __init__(self, parent,client_act,list_user_info):
        """
        dispalys entry frame
        """

        wx.Frame.__init__(self, parent, -1, "Mist My Profile Page", size=(APP_SIZE_X+400,APP_SIZE_Y+100))

        p = wx.Panel(self, -1)
        fgs = wx.FlexGridSizer(cols=2, hgap=10, vgap=10)
        imageFile='background_pic.png'
        img1 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY)

        self.sb1 = wx.StaticBitmap(p, -1, wx.BitmapFromImage(img1),size=(APP_SIZE_X+400,APP_SIZE_Y+100))

        fgs.Add(self.sb1)
        p.SetSizerAndFit(fgs)



        #show mist word
        text1 = wx.StaticText(self.sb1, 1, "Mist - My Profile", pos = (APP_SIZE_X/2-150 ,50),size=(100,60))
        text1.SetFont(wx.Font(64, wx.SWISS, wx.NORMAL, wx.BOLD, False))
        text1.SetBackgroundColour("Black")
        text1.SetForegroundColour("SLATE BLUE")




        #Set my profile Button
        self.shape_button("Black","SLATE BLUE",(APP_SIZE_X,APP_SIZE_Y/2-100),(350,200),2,"BACK TO MENU",self.sb1,fgs)
        self.sb1.Bind(wx.EVT_BUTTON, self.Show_My_Profile, id=2)

        user_name=str(list_user_info[0])
        self.show_text(self.sb1,3,"User Name ",(200,200),(500,40),24,"Black","SLATE BLUE")
        self.show_text(self.sb1,4,str(user_name),(200,242),(500,40),24,"Black","White")

        l_name=str(list_user_info[1])
        self.show_text(self.sb1,5,"Last Name ",(200,300),(500,40),24,"Black","SLATE BLUE")
        self.show_text(self.sb1,6,str(l_name),(200,342),(500,04),24,"Black","White")

        f_name=str(list_user_info[2])
        self.show_text(self.sb1,7,"First Name ",(200,400),(500,40),24,"Black","SLATE BLUE")
        self.show_text(self.sb1,8,str(f_name),(200,442),(500,40),24,"Black","White")

        email=str(list_user_info[3])
        self.show_text(self.sb1,9,"Email Address ",(200,500),(500,40),24,"Black","SLATE BLUE")
        self.show_text(self.sb1,10,str(email),(200,542),(500,40),22,"Black","White")

        safe_answer=str(list_user_info[4])
        self.show_text(self.sb1,11,"Authentication Answer ",(200,600),(500,40),24,"Black","SLATE BLUE")
        self.show_text(self.sb1,11,str(safe_answer),(200,642),(500,40),24,"Black","White")

        self.Fit()
        self.Centre()
        self.Show(True)


    def Close_app(self):
        """
        closes current frame
        """
        pass
        #self.Close(True)
    def show_text(self,where_to,id,string,pos,size,font_size,color1,color2):
        text1 = wx.StaticText(where_to, id, string , pos = pos,size=size)
        text1.SetFont(wx.Font(font_size, wx.SWISS, wx.NORMAL, wx.BOLD, False))
        text1.SetBackgroundColour(color1)
        text1.SetForegroundColour(color2)

    def shape_button(self,color1,color2,loc,size,id,string,where_to,add_to):
        """
        shapes a button and presents it on the screen
        """
        b = buttons.GenButton(where_to, id, string,loc,size)
        b.SetFont(wx.Font(24, wx.SWISS, wx.NORMAL, wx.BOLD, False))
        b.SetBezelWidth(5)
        b.SetBackgroundColour(color1)
        b.SetForegroundColour(color2)
        add_to.Add(b)


    def call_massage_box(self,massage,type):
        """
        displays massage box on the screen
        """
        dlg = wx.MessageDialog(None,massage, type, wx.OK)
        retCode = dlg.ShowModal()

        dlg.Destroy()

        #retCode = wx.MessageBox("Is this way easier?", "Via Function",wx.YES_NO | wx.ICON_QUESTION)


    def Show_My_Profile(self,event):
        self.call_massage_box('hey','dayum')


app = wx.App(0)
frame = Show_Profile(None,None,["zabo","l name","f name","132456789123456789123465789132","1235647812345678"])

app.MainLoop()
