"""Plasmonitor"""

import wx

from plasmonitor.main_frame import MyFrame


def main():
    """ Entry point of application"""
    app = wx.App()
    app.frame = MyFrame("SAOM-Lab: Live Plot", size=(950, 600))
    app.SetTopWindow(app.frame)
    app.frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    main()
