import wx
import sys, glob, random
import data

###13 - report etc
division_line = "\n\n\n\n\n"

class Listed_object:
    def __init__(self, lst_headers_name, lst_info_obj):
        self.lst_info_obj = lst_info_obj
        self.lst_headers = lst_headers_name




class Acc_projects(wx.Frame):
    def __init__(self, listed_object):
        wx.Frame.__init__(self, None, -1,"Code Control",size=(900,700))
        self.list = None
        self.editable = False
        self.listed_object = listed_object
        self.MakeListCtrl()
        self.MakeMenu()

    def MakeListCtrl(self, otherflags=0):
        # if we already have a listctrl then get rid of it
        if self.list:
            self.list.Destroy()

        if self.editable:
            otherflags |= wx.LC_EDIT_LABELS


        # create the list control
        self.list = wx.ListCtrl(self, -1, style=wx.LC_REPORT|otherflags)


        # Add some columns
        for col, text in enumerate(self.listed_object.lst_headers):
            self.list.InsertColumn(col, text)

        # add the rows
        for row, item in enumerate(self.listed_object.lst_info_obj):
            index = self.list.InsertStringItem(sys.maxint, item[0])
            for col, text in enumerate(item[1:]):

                self.list.SetStringItem(index, col+1, text)

            # set the data value for each item to be its position in
            # the data list
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
        item = menu.Append(-1, "E&xit\tAlt-X")
        self.Bind(wx.EVT_MENU, self.OnExit, item)
        menu.AppendSeparator()
        item = menu.Append(-1, "Create new project")
        self.Bind(wx.EVT_MENU, self.OnExit, item)
        mbar.Append(menu, "&More")

        menu = wx.Menu()
        item = menu.Append(-1, "Sort ascending")
        self.Bind(wx.EVT_MENU, self.OnSortAscending, item)        
        item = menu.Append(-1, "Sort descending")
        self.Bind(wx.EVT_MENU, self.OnSortDescending, item)
        item = menu.Append(-1, "Sort by date")
        self.Bind(wx.EVT_MENU, self.OnSortByDate, item)
        item = menu.Append(-1, "Sort by project name")
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
        wx.Frame.__init__(self, None, -1,"Code Control",size=(450,350))
        fgs = wx.FlexGridSizer(cols=900, hgap=10, vgap=10)
        imageFile='Tologin.jpg'
        img1 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY)
        p = wx.Panel(self, -1)
        self.sb1 = wx.StaticBitmap(p, -1, wx.BitmapFromImage(img1) ,size=(450,350))

        fgs.Add(self.sb1)
        p.SetSizerAndFit(fgs)
        self.new_pro = wx.TextCtrl(self.sb1, value="")
        wx.Button(self.sb1,label = "Confirm", pos = (350, 250), size=(50,40), id = 1)
        self.sb1.Bind(wx.EVT_BUTTON, self.new_pro, id=1)

    def new_pro(self,event):


        if self.new_pro.Value=="":
            code=(self.Massage_codes.Return_massage(6))
            self.call_massage_box(code[0],code[1])

        else:
            new_pro = str(self.new_pro.Value)
            info_to_send = "New Project:"+new_pro+ division_line
            self.client_actions.send(info_to_send)
            recv_data = self.client_actions.recv()

            if recv_data==( "Confirm-User!"+ division_line):
                self.Close()
                self.Close()

        Acc_projects(self.listed_object, self.client_actions)
        self.Close()

    def OnExit(self, evt):
        self.Close()


    def OnItemSelected(self, evt):
        item = evt.GetItem()
        print str(evt),"Item selected:", item.GetText()
        
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
            val1 = self.listed_object.lst_info_obj[row1][2]
            val2 = self.listed_object.lst_info_obj[row2][2]

            if val1 < val2: return 1
            if val1 > val2: return -1
            return 0

        self.list.SortItems(compare_func)
        

    def OnSortByProName(self, evt):
        def compare_func2(row1, row2):
            # compare the values in the 4th col of the data
            val1 = self.listed_object.lst_info_obj[row1][1]
            val2 = self.listed_object.lst_info_obj[row2][1]
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
            
    
class DemoApp(wx.App):
    def OnInit(self):
        lst_obj = Listed_object(["Project", "Manager", "Last edit"], [("A_PRO", "Adi", "2004-06-09 11:41"), ("MmMA", "Noam", "2003-10-07 13:34")])
        frame = Acc_projects(lst_obj)
        #self.SetTopWindow(frame)
        #print "Program output appears here..."
        frame.Show()
        return True

app = DemoApp(redirect=True)
app.MainLoop()
