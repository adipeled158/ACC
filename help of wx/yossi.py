
__author__ = 'Yossi'
import wx
import random
import socket
import time
APP_SIZE_Y =1300
APP_SIZE_X = 700

class MyButtons(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(APP_SIZE_Y, APP_SIZE_X))
        self.app = wx.App(redirect=True)
        p = wx.Panel(self, -1)

        self.fgs = wx.FlexGridSizer(cols=2, hgap=10, vgap=10)
        images = [ "black-dark-clouds-Sky-HD-Wallpaper.jpg", "Leer-Jet-Blue-Sky-Desktop-Wallpaper.jpg", "nature-sand-pink-wet-pools-evening-sky-2400x1350-wallpaper.jpg", "s61bxS.jpg", "unnamed.jpg"]


        self.imageFile=images[random.randint(0, len(images)-1)]
        print self.imageFile
        img1 = wx.Image(self.imageFile, wx.BITMAP_TYPE_ANY)

        self.sb1 = wx.StaticBitmap(p, -1, wx.BitmapFromImage(img1),size=(APP_SIZE_Y,APP_SIZE_X))

        self.fgs.Add(self.sb1)
        p.SetSizerAndFit(self.fgs)




        #(y, x)
        wx.Button(self.sb1, 1, 'Sign In', ((APP_SIZE_Y/13), ((APP_SIZE_X*11)/20)), (250, 100))
        wx.Button(self.sb1, 2, 'Sign Up', ((APP_SIZE_Y/13), ((APP_SIZE_X*11)/20)+150), (250, 100))

     #   self.editname = wx.TextCtrl(self, value="Enter name", pos=(120, 60), size=(140,-1))
  #      self.data_to_server = wx.TextCtrl(self, value="Hello Server", pos=(120, 20), size=(140,-1))

        self.Bind(wx.EVT_BUTTON, self.sign_in, id=1)
        self.Bind(wx.EVT_BUTTON, self.sign_out, id=2)


        self.Centre() #make the screen be in the middle of the screen

        self.ShowModal()

        #self.Destroy()
  #  def sign_in_b(self, event):


    def sign_in(self, event):
        #self.button.SetDefault()
        self.sb1.Destroy()
        #self.app.MainLoop()
        img = "1069398__beautiful-sunset-hd1080p_p.jpg"
        p = wx.Panel(self, 1)
        fgs = wx.FlexGridSizer(cols=2, hgap=10, vgap=10)
      #  self.Close(True)
        print "signing in"
        img1 = wx.Image(img, wx.BITMAP_TYPE_ANY)

        self.sb2 = wx.StaticBitmap(p, -1, wx.BitmapFromImage(img1),size=(APP_SIZE_Y,APP_SIZE_X))
        #fgs._ReplaceItem(self.sb1, )
        fgs.Add(self.sb2)
        p.SetSizerAndFit(fgs)

        print "before buttom"


        #(y, x)
        wx.Button(self.sb2, 1, 'Eva', ((APP_SIZE_Y/13), ((APP_SIZE_X*11)/20)), (250, 100))
   #     wx.Button(self.sb1, 2, 'Sign Up', ((APP_SIZE_Y/13), ((APP_SIZE_X*11)/20)+150), (250, 100))

     #   self.editname = wx.TextCtrl(self, value="Enter name", pos=(120, 60), size=(140,-1))
  #      self.data_to_server = wx.TextCtrl(self, value="Hello Server", pos=(120, 20), size=(140,-1))

        self.Bind(wx.EVT_BUTTON, self.sign_out, id=1)
      #  self.Bind(wx.EVT_BUTTON, self.sign_out, id=2)


        self.Centre() #make the screen be in the middle of the screen
        print "before show"
        self.ShowModal()
        print("showed")


    def relly_sign_in(self, event):
        panel=wx.Panel(self)
        box=wx.TextEntryDialog(None,('User-name:','Password'),'CODE CONTROL',"default-text")#first parameter is parent wx.OK
       # box=wx.TextEntryDialog(None,'Password:','CODE CONTROL',"default-text")#first parameter is parent wx.OK
        if box.ShowModal()==wx.ID_OK:#its ok or cancel
            answer=box.GetValue()

    def sign_out(self, event):
        global client_sock

        client_sock.connect(("127.0.0.1", 5555))

    def OnTcpSend(self, event):
        global client_sock
        client_sock.send(self.data_to_server.Value)


app = wx.App(0)
MyButtons(None, -1, 'buttons.py')
app.MainLoop()