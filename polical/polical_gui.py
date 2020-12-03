import sys
import wx
import wx.lib.agw.ultimatelistctrl as ULC
import wx.lib.mixins.listctrl as listmix
import datetime
import os
import yaml
import logging
from trello import TrelloClient
from wx.lib.stattext import GenStaticText
import webbrowser

"""https://stackoverflow.com/questions/47280665/get-state-of-checkboxes-in-listctrl
"""


class Link(GenStaticText):
    def __init__(self, *args, **kw):
        super(Link, self).__init__(*args, **kw)

        self.font1 = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, True)
        self.font2 = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False)

        self.SetFont(self.font2)
        self.SetForegroundColour("#1B95E0")

        self.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouseEvent)
        self.Bind(wx.EVT_MOTION, self.OnMouseEvent)

    def SetUrl(self, url):

        self.url = url

    def OnMouseEvent(self, e):

        if e.Moving():

            self.SetCursor(wx.Cursor(wx.CURSOR_HAND))
            self.SetFont(self.font1)

        elif e.LeftUp():

            webbrowser.open(self.url)

        else:
            self.SetCursor(wx.NullCursor)
            self.SetFont(self.font2)

        e.Skip()


def get_working_directory(dir_name: str) -> str:
    """This functions gets the working directory path.

    Returns:
        dir_name (str): Directory name that needs the full path.
        workingDirectory (str): The directory where database and yaml are located.
    """
    userdir = os.path.expanduser("~")
    workingDirectory = os.path.join(userdir, dir_name)
    return workingDirectory


def get_file_location(filename: str) -> str:
    """This function is for getting full path location of a file from its filename

    Args:
        filename (str): Filename that needs the full path location

    Returns:
        full_path_file_location (str): Full path location of the file
    """
    workingDirectory = get_working_directory("PoliCal")
    full_path_file_location = os.path.join(workingDirectory, filename)
    return full_path_file_location


def load_config_file(config_file_path: str) -> dict:
    """This function is for loading yaml config file

    Args:
        config_file_path (str): File path for the config file to be loaded

    Returns:
        file_config (dict): Dictionary with config keys.

    Raises:
        IOError
    """
    try:
        with open(get_file_location(config_file_path), "r") as config_yaml:
            file_config = yaml.safe_load(config_yaml)
            return file_config
    except IOError:
        logging.error("Archivo de configuración no encontrado, generando llaves")
        return None


def get_trello_client(user_dict: dict) -> TrelloClient:
    """This function gets a Trello Client Object to connect to Trello.

    Args:
        user_dict (dict): File path for the config file to be loaded

    Returns:
        client (TrelloClient): Client object that has access to Trello.
    """
    client = TrelloClient(
        api_key=user_dict["api_key"],
        api_secret=user_dict["api_secret"],
        token=user_dict["oauth_token"],
        token_secret=user_dict["oauth_token_secret"],
    )

    return client


def get_cards(done_tasks_only=False) -> list:
    """This function gets a all uncompleted cards from a board.

    Returns:
        uncompleted_cards (List): List of strings from all uncompleted cards
    """
    user = load_config_file("trelloCredentials.yaml")
    client = get_trello_client(user)
    all_boards = client.list_boards()
    last_board = all_boards[-1]
    uncompleted_cards = []
    completed_cards = []
    last_list_from_board = last_board.list_lists()[1]
    for card in last_list_from_board.list_cards():
        due_date = ""
        if card.due_date is not None:
            due_date = card.due_date
        if due_date != "":
            due_date = str(due_date.strftime("%Y-%m-%d"))
        is_due_complete = False
        if card.is_due_complete is None:
            is_due_complete = False
        else:
            is_due_complete = card.is_due_complete
        if is_due_complete:
            completed_cards.append(
                {
                    "name": card.name,
                    "class": last_list_from_board.name,
                    "url": card.url,
                    "is_due_complete": is_due_complete,
                    "date": due_date,
                    "description": card.description,
                }
            )
        else:
            uncompleted_cards.append(
                {
                    "name": card.name,
                    "class": last_list_from_board.name,
                    "url": card.url,
                    "is_due_complete": is_due_complete,
                    "date": due_date,
                    "description": card.description,
                }
            )
    if done_tasks_only:
        return completed_cards
    return uncompleted_cards + completed_cards


"""Class MyUltimateListCtrlPanel is based on https://stackoverflow.com/questions/56687156/wxpython-how-to-sort-listctrl-column-items"""


class MyUltimateListCtrlPanel(wx.Panel, listmix.ColumnSorterMixin):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=wx.WANTS_CHARS)

        self.description_textctrl = wx.TextCtrl(
            self,
            style=wx.TE_MULTILINE | wx.TE_READONLY,
        )

        self.cards = cards = get_cards()

        agwStyle = (
            ULC.ULC_HAS_VARIABLE_ROW_HEIGHT
            | wx.LC_REPORT
            | wx.LC_VRULES
            | wx.LC_HRULES
            | wx.LC_SINGLE_SEL
        )

        self.mylist = mylist = ULC.UltimateListCtrl(self, wx.ID_ANY, agwStyle=agwStyle)

        mylist.InsertColumn(0, "", format=ULC.ULC_FORMAT_LEFT, width=50)
        mylist.InsertColumn(1, "Tarea", format=ULC.ULC_FORMAT_LEFT, width=150)
        mylist.InsertColumn(2, "Clase", format=ULC.ULC_FORMAT_LEFT, width=100)
        mylist.InsertColumn(3, "Fecha de Entrega", width=130)
        mylist.InsertColumn(4, "URL", format=ULC.ULC_FORMAT_CENTER, width=120)

        self.checkboxes = []
        self.hyperlinks = {}
        self.boxes = []
        self.itemDataMap = {}

        self.InitUltimateListCtrl(cards)

        listmix.ColumnSorterMixin.__init__(self, 5)
        self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColClick, self.mylist)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.mylist, 1, wx.EXPAND)
        subsizer = wx.BoxSizer(wx.HORIZONTAL)
        sync_button = wx.Button(self, -1, "Sync")
        sizer.Add(self.description_textctrl, 1, wx.EXPAND)
        subsizer.Add(sync_button)
        sizer.Add(subsizer)
        self.Bind(wx.EVT_CHECKBOX, self.OnChecked)
        self.Bind(wx.EVT_BUTTON, self.OnGetData, sync_button)
        self.mylist.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_plot, self.mylist)
        self.SetSizer(sizer)

    def InitUltimateListCtrl(self, cards, main_index=0):
        mylist = self.mylist
        boxes = 0
        list_of_tuples = []
        for card in cards:
            list_of_tuples.append(
                (card["is_due_complete"], card["name"], card["class"], card["date"], "")
            )
        for local_index, card in enumerate(cards):
            index = local_index + main_index
            name_of_checkbox = card["name"]
            mylist.InsertStringItem(index, "")
            self.checkBox = wx.CheckBox(
                mylist,
                wx.ID_ANY,
                "",
                wx.DefaultPosition,
                wx.DefaultSize,
                0,
                name=name_of_checkbox,
            )
            self.checkBox.SetValue(card["is_due_complete"])
            self.checkboxes.append(self.checkBox)
            mylist.SetItemWindow(index, boxes, self.checkBox, True)
            self.boxes.append(self.checkBox)
            mylist.SetStringItem(index, 1, card["name"])
            mylist.SetStringItem(index, 2, card["class"])
            mylist.SetStringItem(index, 3, card["date"])
            mylist.SetStringItem(index, 4, "")
            self.link = Link(mylist, label="Ver en Trello")
            self.link.SetUrl(card["url"])
            self.hyperlinks[self.link.GetId()] = index
            mylist.SetItemWindow(index, boxes + 4, self.link, True)
            mylist.SetItemData(index, list_of_tuples[local_index])

        self.itemDataMap.update({data: data for data in list_of_tuples})

    def GetListCtrl(self):
        return self.mylist

    def OnColClick(self, event):
        pass

    def ShowDoneTasks(self, e):
        if self.shst.IsChecked():
            self.statusbar.Show()
        else:
            index_list = []
            for counter, checkBox in enumerate(self.checkboxes):
                if checkBox.IsChecked():
                    index_list.append(counter)
                counter += 1
            for i in reversed(index_list):
                self.mylist.DeleteItem(i)
            print(counter)

    def on_plot(self, event):
        index = event.GetIndex()
        item = self.cards[index]
        self.description_textctrl.Clear()
        self.description_textctrl.AppendText(
            item["name"] + "\n\n" + item["description"]
        )

    def OnChecked(self, event):
        clicked = event.GetEventObject()
        print(clicked.GetName())
        print(event.IsChecked())

    def OnGetData(self, event):
        day_dict = {}
        day_list = []
        for i in self.checkboxes:
            if i.IsChecked():
                n = i.GetName()
                day_dict[n] = "Checked"
                day_list.append((n, "Checked"))
        print(day_dict)
        print(day_list)

    def OnQuit(self, e):
        self.Close()


class MyFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(
            self,
            parent,
            -1,
            "Checkbox grid based on UltimateListCtrl Demo",
            size=(720, 360),
        )
        """Menu initialization"""
        menubar = wx.MenuBar()

        fileMenu = wx.Menu()
        fileMenu.Append(wx.ID_NEW, "&New")
        fileMenu.Append(wx.ID_OPEN, "&Open")
        fileMenu.Append(wx.ID_SAVE, "&Save")
        fileMenu.AppendSeparator()

        imp = wx.Menu()
        imp.Append(wx.ID_ANY, "Import newsfeed list...")
        imp.Append(wx.ID_ANY, "Import bookmarks...")
        imp.Append(wx.ID_ANY, "Import mail...")

        self.shst = fileMenu.Append(
            wx.ID_ANY,
            "Mostrar tareas realizadas",
            "Mostrar tareas realizadas",
            kind=wx.ITEM_CHECK,
        )

        self.Bind(wx.EVT_MENU, self.ShowDoneTasks, self.shst)

        fileMenu.Check(self.shst.GetId(), True)

        fileMenu.AppendSubMenu(imp, "I&mport")

        qmi = wx.MenuItem(fileMenu, wx.ID_EXIT, "&Quit\tCtrl+W")
        fileMenu.Append(qmi)

        self.Bind(wx.EVT_MENU, self.OnQuit, qmi)

        menubar.Append(fileMenu, "&File")
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText("Ready")
        self.SetMenuBar(menubar)
        self.Centre()

        self.panel = MyUltimateListCtrlPanel(self)
        self.mylist = self.panel.mylist
        self.checkboxes = self.panel.checkboxes

    def ShowDoneTasks(self, e):
        if self.shst.IsChecked():
            done_cards = get_cards(True)
            self.panel.InitUltimateListCtrl(done_cards, self.mylist.GetItemCount() - 1)
        else:
            index_list = []
            for counter, checkBox in enumerate(self.checkboxes):
                if checkBox.IsChecked():
                    index_list.append(counter)
            for i in reversed(index_list):
                self.mylist.DeleteItem(i)

    def OnChecked(self, event):
        clicked = event.GetEventObject()
        print(clicked.GetName())
        print(event.IsChecked())

    def OnQuit(self, e):
        self.Close()


app = wx.App()
frame = MyFrame(None)
app.SetTopWindow(frame)
frame.Show()
app.MainLoop()