import wx


class InputPanel(wx.Panel):
    def __init__(self, parent, ID, vbox):
        wx.Panel.__init__(self, parent, ID)
        font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
        # font.SetPointSize(11)

        # Input file name
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(parent, wx.ID_ANY, label="File name: ")
        st1.SetFont(font)
        hbox1.Add(st1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        self.fname_txtctrl1 = wx.TextCtrl(
            parent, wx.ID_ANY, value="1704146U2_0001.Raw8.txt")
        hbox1.Add(self.fname_txtctrl1, proportion=1)
        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT |
                 wx.RIGHT | wx.TOP, border=10)

        # Input directory
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        st2 = wx.StaticText(parent, label="Directory: ")
        st2.SetFont(font)
        hbox2.Add(st2, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        # self.dname_txtctrl1 = wx.TextCtrl(parent, value="/home/outrera/Devel/Python/plasmonitor/limpieza")
        self.dname_txtctrl1 = wx.TextCtrl(
            parent, value='DatosEspectroscopicos/Avantes/i8u/UV')
        hbox2.Add(self.dname_txtctrl1, proportion=1)
        btn_browse = wx.Button(parent, wx.ID_ANY, "Browse")
        btn_browse.Bind(wx.EVT_BUTTON, self.on_browse)
        hbox2.Add(btn_browse, flag=wx.EXPAND)
        vbox.Add(hbox2, flag=wx.EXPAND | wx.LEFT |
                 wx.RIGHT | wx.TOP, border=10)

        # Set start and reset buttons
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_start = wx.Button(parent, -1, "Start")
        self.btn_start.Bind(wx.EVT_BUTTON, self.on_start)
        hbox3.Add(self.btn_start, flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(hbox3, flag=wx.EXPAND, border=10)

        ### Select materials#########################

    def on_browse(self, event):
        default_dir = self.dname_txtctrl1.GetValue()
        dir_dlg = wx.DirDialog(
            None, "Select directory to open", default_dir, 0, (10, 10))

        # This function returns the button pressed to close the dialog
        if dir_dlg.ShowModal() == wx.ID_OK:
            self.dname_txtctrl1.SetValue(dir_dlg.GetPath())

        dir_dlg.Destroy()

    def on_start(self, event):
        self.start = not self.start
        if self.start:
            label = "Stop"
        else:
            label = "Start"
        self.btn_start.SetLabel(label)
