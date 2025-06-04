#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Main program template

import wx
import gui
import os.path
from pylab import *


class MyApp(wx.App):
    def __init__(self):
        wx.App.__init__(self)
        self.frame = gui.MyFrame(None, title="Application Template")

        ############################################################
        ## PUT YOUR MAIN CODE HERE
        
        ## Initialize variable
        self.lines()
        
        ## Define events
        self.Bind(wx.EVT_CLOSE, self.on_close)
        wx.EVT_BUTTON(self, self.frame.data_panel.btn_close.GetId(),self.on_close)
        wx.EVT_BUTTON(self, self.frame.data_panel.btn_start.GetId(),self.on_start)


        ## END: PUT YOUR MAIN CODE HERE
        ############################################################

        self.SetTopWindow(self.frame)
        self.frame.Show()
        

    def lines(self):
        #### Lines list ####
        ##
        ## Ar - central wlen position: 696.54 nm
        self.half_width = 3
        self.Ar_line = 2293
        self.Ar_line_min = self.Ar_line - self.half_width
        self.Ar_line_max = self.Ar_line + self.half_width
        ## ArII - min wlen in pixel position: 1064
        self.half_width = 8
        self.ArII_line = 1072
        self.ArII_line_min = self.ArII_line - self.half_width
        self.ArII_line_max = self.ArII_line + self.half_width
        ## NII - central wlen in pixel position: 999.5
        self.half_width = 4
        self.NII_line = 978
        self.NII_line_min = self.NII_line - self.half_width
        self.NII_line_max = self.NII_line + self.half_width
        ## OI - central wlen in pixel position: 777.26
        self.OI_line = 2637
        self.OI_line_min = self.OI_line - 2
        self.OI_line_max = self.OI_line + 7
        
        ## Set number of files to compute slope
        self.nb_files = 50
        
        
    def on_start(self, event):

        ## Get file name and directory        
        self.fname = self.frame.data_panel.base_name.GetValue()
        self.dname = self.frame.data_panel.base_directory
        if wx.Platform == "__WXMSW__":
            self.fname = self.dname + "\\" + self.fname
        else:
            self.fname = self.dname + "/" + self.fname

        self.fcounter = int(self.fname.split("_")[-1].split(".")[0])
        self.fcounter_length = str(len(self.fname.split("_")[-1].split(".")[0]))
        self.slope_windows = 25
        self.xsample = zeros(self.slope_windows)
        self.ysample = zeros(self.slope_windows)

        ## Create timer to read data
        self.redraw_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.load_data, self.redraw_timer)        
        self.redraw_timer.Start(5)


    def load_data(self, event):
        if os.path.isfile(self.fname):
            self.data = loadtxt(self.fname)
            self.intensity = self.data[:,1]

            ## Lines integration
            self.Ar_line_int = sum(self.intensity[self.Ar_line_min:self.Ar_line_max])
            self.ArII_line_int = sum(self.intensity[self.ArII_line_min:self.ArII_line_max])
            self.NII_line_int = sum(self.intensity[self.NII_line_min:self.NII_line_max])
            self.OI_line_int = sum(self.intensity[self.OI_line_min:self.Ar_line_max])

            ## Plot slope for Ar peak integral
            self.xsample = roll(self.xsample, -1)
            self.xsample[-1] = self.fcounter
            self.ysample = roll(self.ysample, -1)
            self.ysample[-1] = self.Ar_line_int
            
            if wx.Platform == "__WXMSW__":
                self.frame.plot_panel.axes1.set_title(self.fname.split("\\")[-1])
            else:
                self.frame.plot_panel.axes1.set_title(self.fname.split("/")[-1])
            self.frame.plot_panel.axes1.set_ylabel("Slope")
            if self.fcounter > self.slope_windows:
                self.slope = (polyfit(self.xsample, self.ysample, 1))[0]
                self.frame.plot_panel.axes1.plot(self.fcounter, self.slope, "bo")
                self.frame.plot_panel.axes1.axhline(0, linestyle="--")
                self.frame.plot_panel.axes1.legend(["Ar", "Zero slope"])
                self.frame.plot_panel.axes1.autoscale(True)
                #self.ax1.set_xlabel("File number")


            ## Plot lines integral
            #self.ax2.cla()
            #self.ax2.plot(self.data[:,0], self.data[:,1])
            #self.ax2.plot(self.xsample, self.ysample)
            self.frame.plot_panel.axes2.plot(self.fcounter, self.Ar_line_int, "bo")
            self.frame.plot_panel.axes2.plot(self.fcounter, self.ArII_line_int, "go")
            self.frame.plot_panel.axes2.plot(self.fcounter, self.NII_line_int, "yo")
            self.frame.plot_panel.axes2.plot(self.fcounter, self.OI_line_int, "ro")
            self.frame.plot_panel.axes2.legend(["Ar","ArII","NII","OI"])
            self.frame.plot_panel.axes2.set_xlabel("File number")
            self.frame.plot_panel.axes2.set_ylabel("Integral")

            #self.ax.grid()
            self.frame.plot_panel.canvas.draw()

            ## Update file name
            self.str_temp = "%."+self.fcounter_length+"d"
            self.old_index = self.str_temp %self.fcounter
            self.fcounter += 1
            self.str_temp = "%."+self.fcounter_length+"d"
            self.new_index = self.str_temp %self.fcounter
            self.fname = self.fname.replace(self.old_index, self.new_index)
            
            ## Clean memory
            del(self.data, self.intensity, self.Ar_line_int, self.ArII_line_int, self.NII_line_int, self.OI_line_int)


    def on_fit(self, event):
        popups.show_message("Fit Function", "Fit data code in progress...")

    def on_close(self, event):
        self.frame.Close()

## Launch program
if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()

