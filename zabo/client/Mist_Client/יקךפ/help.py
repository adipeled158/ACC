import wx
import sys, glob, random

#capter 13\list_report_virtual.py
class headers_name:
    lst_headers = ["Project", "Manager", "Last editor", "Date"]


class VirtualListCtrl(wx.ListCtrl):
    """
    A generic virtual listctrl that fetches data from a DataSource.
    """
    def __init__(self, parent,  lst_info_projects):
        # lst_info_projects = [(name-project, manager-name, last edited)...]
        self.lst_info_projects = lst_info_projects
        lst_headers_name = headers_name.lst_headers


        wx.ListCtrl.__init__(self, parent,
            style=wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.LC_VIRTUAL)
        self.Bind(wx.EVT_LIST_CACHE_HINT, self.DoCacheItems)
        self.SetItemCount(len(self.lst_info_projects))

        columns = lst_headers_name
        for col, text in enumerate(columns):
            self.InsertColumn(col, text)
        

    def DoCacheItems(self, evt):
        pass

    def OnGetItemText(self, item, col):
        data = self.lst_info_projects[item]
        return data[col]

    def OnGetItemAttr(self, item):  return None
    def OnGetItemImage(self, item): return -1

        
    def MakeMenu(self):
        mbar = wx.MenuBar()
        menu = wx.Menu()
        item = menu.Append(-1, "E&xit\tAlt-X")
        self.Bind(wx.EVT_MENU, self.OnExit, item)
        mbar.Append(menu, "&File")

        menu = wx.Menu()



        item = menu.Append(-1, "Sort by Project")
        self.Bind(wx.EVT_MENU, self.OnSortAscending, item)

        item = menu.Append(-1, "Sort by manager name")
        self.Bind(wx.EVT_MENU, self.OnSortDescending, item)
        item = menu.Append(-1, "Sort by date")
        self.Bind(wx.EVT_MENU, self.OnSortBySubmitter, item)

        menu.AppendSeparator()
        item = menu.Append(-1, "Show selected")
        self.Bind(wx.EVT_MENU, self.OnShowSelected, item)
        item = menu.Append(-1, "Select all")
        self.Bind(wx.EVT_MENU, self.OnSelectAll, item)
        item = menu.Append(-1, "Select none")
        self.Bind(wx.EVT_MENU, self.OnSelectNone, item)

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
        mbar.Append(menu, "&Demo")

        self.SetMenuBar(mbar)
class DemoFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1,
                          "Virtual wx.ListCtrl",
                          size=(600,400))
        lst_help = [("Pro1","Adi", "Moni"), ("Pro2", "Rani","Dani" )]
        helpm = lst_help + lst_help+lst_help+lst_help+lst_help
        for i in range(30):
            helpm = helpm+lst_help
        self.list = VirtualListCtrl(self, helpm)



app = wx.PySimpleApp()
frame = DemoFrame()
frame.Show()
app.MainLoop()
