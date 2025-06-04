#!/usr/bin/env python
# -*- coding: utf-8 -*-
##
## plasmonitor.py
##
## Plot the integral of several spectral lines and the slope described by a
## set of subsequent files 
##
## $Id: plasmonitor.py,v 0.1 2016/01/29 outrera $
##
## Copyright (c) 2016, Oscar Hernandez Utrera. SAOM-Lab
## All rights reserved.
##
## This program is free software; you can redistribute it and/or  modify it
## under the terms of the GNU General Public License  as  published  by the
## Free Software Foundation; either version 2 of the License,  or  (at your
## option) any later version.
##
## This program is distributed in the hope  that  it  will  be  useful, but
## WITHOUT  ANY   WARRANTY;   without   even   the   implied   warranty  of
## MERCHANTABILITY or  FITNESS  FOR  A  PARTICULAR  PURPOSE.   See  the GNU
## General Public License for more details (to receive a  copy  of  the GNU
## General Public License, write to the Free Software Foundation, Inc., 675
## Mass Ave, Cambridge, MA 02139, USA).
##
##
## $Log: plasmonitor.py,v 0.1 $
##
##

## Import Libraries
import os
import pprint
import random
import sys
import wx
import wx.lib.filebrowsebutton as filebrowse

## Set WXAgg as backend. 
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
import numpy as np
import pandas
import pylab 

class InputPanel(wx.Panel):
    def __init__(self, parent, ID, vbox):
        wx.Panel.__init__(self, parent, ID)
        font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
        # font.SetPointSize(11)
        
        ## Input file name
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(parent, wx.ID_ANY, label="File name: ")
        st1.SetFont(font)
        hbox1.Add(st1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        self.fname_txtctrl1 = wx.TextCtrl(parent, wx.ID_ANY, value="1704146U2_0001.Raw8.txt")
        hbox1.Add(self.fname_txtctrl1, proportion=1)
        vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        
        ## Input directory
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        st2 = wx.StaticText(parent, label="Directory: ")
        st2.SetFont(font)
        hbox2.Add(st2, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        # self.dname_txtctrl1 = wx.TextCtrl(parent, value="/home/outrera/Devel/Python/plasmonitor/limpieza")
        self.dname_txtctrl1 = wx.TextCtrl(parent, value="D:\DatosEspectroscopicos\Avantes\i8u\UV")
        hbox2.Add(self.dname_txtctrl1, proportion=1)
        btn_browse = wx.Button(parent, wx.ID_ANY, "Browse")
        btn_browse.Bind(wx.EVT_BUTTON, self.on_browse)
        hbox2.Add(btn_browse, flag=wx.EXPAND)
        vbox.Add(hbox2, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        ## Set start and reset buttons
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_start = wx.Button(parent, -1, "Start")
        self.btn_start.Bind(wx.EVT_BUTTON, self.on_start)
        hbox3.Add(self.btn_start, flag=wx.LEFT|wx.TOP, border=10)
        vbox.Add(hbox3, flag=wx.EXPAND, border=10)
        
        ### Select materials#########################
        
        
    def on_browse(self, event):
        default_dir = self.dname_txtctrl1.GetValue()
        dir_dlg = wx.DirDialog(None, "Select directory to open", default_dir, 0, (10, 10))

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

        
class PlotControls(wx.Panel):
    """ A static box with a couple of radio buttons and a text
        box. Allows to switch between an automatic mode and a 
        manual mode with an associated value.
    """
    def __init__(self, parent, ID, label, initval):
        wx.Panel.__init__(self, parent, ID)
        
        self.value = initval
        
        box = wx.StaticBox(self, -1, label)
        sizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        
        self.radio_auto = wx.RadioButton(self, -1, 
            label="Auto", style=wx.RB_GROUP)
        self.radio_manual = wx.RadioButton(self, -1,
            label="Manual")
        self.manual_text = wx.TextCtrl(self, -1, 
            size=(35,-1),
            value=str(initval),
            style=wx.TE_PROCESS_ENTER)
        
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_manual_text, self.manual_text)
        self.Bind(wx.EVT_TEXT_ENTER, self.on_text_enter, self.manual_text)
        
        manual_box = wx.BoxSizer(wx.HORIZONTAL)
        manual_box.Add(self.radio_manual, flag=wx.ALIGN_CENTER_VERTICAL)
        manual_box.Add(self.manual_text, flag=wx.ALIGN_CENTER_VERTICAL)
        
        sizer.Add(self.radio_auto, 0, wx.ALL, 10)
        sizer.Add(manual_box, 0, wx.ALL, 10)
        
        self.SetSizer(sizer)
        sizer.Fit(self)
    
    def on_update_manual_text(self, event):
        self.manual_text.Enable(self.radio_manual.GetValue())
    
    def on_text_enter(self, event):
        self.value = self.manual_text.GetValue()
    
    def is_auto(self):
        return self.radio_auto.GetValue()
        
    def manual_value(self):
        return self.value


class LivePlot(wx.Panel):
    """ A static box with a couple of radio buttons and a text
        box. Allows to switch between an automatic mode and a 
        manual mode with an associated value.
    """
    def __init__(self, parent, ID, vbox):
        wx.Panel.__init__(self, parent, ID)

        ## Initialize plot and canvas
        dpi = wx.ScreenDC().GetPPI()[0]
        fig = Figure((3.0, 3.0), dpi=dpi)

        ## Init data used just to draw the canvas and plots
        data_init = np.zeros(1)

        ## Create first plot axis
        ##
        ## Serie "a"
        self.axis1a = fig.add_subplot(211)
        self.axis1a.set_title("Plot 1", size=10)
        self.axis1a.set_ylabel("Slope", size=10)
        self.axis1a.axhline(0, linestyle="--")
        self.axis1a.grid(True, color='gray')
        pylab.setp(self.axis1a.get_xticklabels(), fontsize=8)
        pylab.setp(self.axis1a.get_yticklabels(), fontsize=8)
        self.plot1a = self.axis1a.plot(data_init, linewidth=0, color="blue", marker="o",)[0]
        ## Serie "b"
        self.axis1b = fig.add_subplot(211)
        self.plot1b = self.axis1b.plot(data_init, linewidth=0, color="black", marker="o",)[0]
        ## Serie "c"
        self.axis1c = fig.add_subplot(211)
        self.plot1c = self.axis1c.plot(data_init, linewidth=0, color="red", marker="o",)[0]
        ## Serie "d"
        self.axis1d = fig.add_subplot(211)
        self.plot1d = self.axis1d.plot(data_init, linewidth=0, color="green", marker="o",)[0]

        ## Create second plot axis
        ##
        ## Serie "a"
        self.axis2a = fig.add_subplot(212)
        self.axis2a.set_ylabel("Integral", size=10)
        self.axis2a.set_xlabel("File number", size=10)
        self.axis2a.grid(True, color='gray')
        pylab.setp(self.axis2a.get_xticklabels(), fontsize=8)
        pylab.setp(self.axis2a.get_yticklabels(), fontsize=8)
        self.plot2a = self.axis2a.plot(data_init, linewidth=0, color="blue", marker="o",)[0]
        ## Serie "b"
        self.axis2b = fig.add_subplot(212)
        self.plot2b = self.axis2b.plot(data_init, linewidth=0, color="black", marker="o",)[0]
        ## Serie "c"
        self.axis2c = fig.add_subplot(212)
        self.plot2c = self.axis2c.plot(data_init, linewidth=0, color="red", marker="o",)[0]
        ## Serie "d"
        self.axis2d = fig.add_subplot(212)
        self.plot2d = self.axis2d.plot(data_init, linewidth=0, color="green", marker="o",)[0]

        ## Create canvas to add plot windows
        self.canvas = FigCanvas(parent, -1, fig)
        vbox.Add(self.canvas, 1, flag=wx.LEFT | wx.RIGHT | wx.TOP | wx.DOWN | wx.GROW, border=10)        

        ## Set plot controls
        ### Creates a box to manipulate zoom of the first plot and second plot
        self.xmin_control = PlotControls(parent, -1, "X min 1", 0)
        self.xmax_control = PlotControls(parent, -1, "X max 1", 200)
        self.ymin_control = PlotControls(parent, -1, "Y min 1", -0.0015)
        self.ymax_control = PlotControls(parent, -1, "Y max 1", 0.0015)
        
        ### Creates a box to manipulate zoom of the second plot
        self.ymin_control2 = PlotControls(parent, -1, "Y min 2", 0.000)
        self.ymax_control2 = PlotControls(parent, -1, "Y max 2", 0.80)
        
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(self.xmin_control, border=5, flag=wx.ALL)
        hbox1.Add(self.xmax_control, border=5, flag=wx.ALL)
        hbox1.AddSpacer(24)
        hbox1.Add(self.ymin_control, border=5, flag=wx.ALL)
        hbox1.Add(self.ymax_control, border=5, flag=wx.ALL)
        hbox1.AddSpacer(24)
        hbox1.Add(self.ymin_control2, border=5, flag=wx.ALL)
        hbox1.Add(self.ymax_control2, border=5, flag=wx.ALL)
        
#        vbox.Add(hbox1, flag=wx.ALIGN_LEFT | wx.TOP)
        vbox.Add(hbox1, flag=wx.ALIGN_CENTER | wx.TOP)
                

    def draw_plot(self, xdata1, ydata1, xdata2, ydata2):
        """ Redraws the plot
        """
        ## Set X-axis limits and set data for the first plot
        ## NOTE: changing axes ranges only works for the first plot
        if self.xmax_control.is_auto():
            xmax1 = max(xdata1)
        else:
            xmax1 = float(self.xmax_control.manual_value())
        
        if self.xmin_control.is_auto():
            xmin1 = min(xdata1)
        else:
            xmin1 = float(self.xmin_control.manual_value())

        ## Set Y-axis limits and set data for the first plot
        if self.ymin_control.is_auto():
            ymin1 = min(ydata2) - 0.05*min(ydata2)
        else:
            ymin1 = float(self.ymin_control.manual_value())
        
        if self.ymax_control.is_auto():
            ymax1 = max(ydata2) + 0.05*max(ydata2)
        else:
            ymax1 = float(self.ymax_control.manual_value())

        ## If axis min aquals max add small difference in order to avoid warning message
        if xmin1 == xmax1:
            xmin1 -= 0.001
            xmax1 += 0.001
        if ymin1 == ymax1:
            ymin1 -= 0.001
            ymax1 += 0.001
        
        ## Set axis for the first plot        
        self.axis1a.set_xbound(lower=xmin1, upper=xmax1)
        self.axis1a.set_ybound(lower=ymin1, upper=ymax1)

        # Set data to plot in window 1
        self.plot1a.set_xdata(xdata1)
        self.plot1a.set_ydata(ydata1)

        ## Set X-axis automatic limits and set data for the second plot
        ## NOTE: changing axes ranges only works for the first plot.
        ##
        ## If axis min aquals max add small difference in order to avoid warning message
        xmax2 = max(xdata2)
        xmin2 = min(xdata2)
        ymin2 = min(ydata2) - 0.05*min(ydata2)
        ymax2 = max(ydata2) + 0.05*max(ydata2)

        ## If axis min aquals max add small difference in order to avoid warning message
        if xmin2 == xmax2:
            xmin2 -= 0.001
            xmax2 += 0.001
        if ymin2 == ymax2:
            ymin2 -= 0.001
            ymax2 += 0.001

        ## Set axis for the second plot        
        self.axis2a.set_xbound(lower=xmin2, upper=xmax2)
        self.axis2a.set_ybound(lower=ymin2, upper=ymax2)

        # Set data to plot in window 1
        self.plot2a.set_xdata(xdata2)
        self.plot2a.set_ydata(ydata2)

        self.canvas.draw()

    def draw_plot_2s(self, xdata1_a, ydata1_a, xdata2_a, ydata2_a, xdata1_b, ydata1_b, xdata2_b, ydata2_b):
        """ Redraws the plot
        """
        
        ## Get max values from series a and b
        if max(xdata1_a) >= max(xdata1_b):
            xdata1 = xdata1_a
        else:
            xdata1 = xdata1_b
            
        if max(ydata1_a) >= max(ydata1_b):
            ydata1 = ydata1_a
        else:
            ydata1 = ydata1_b

        ## Set X-axis limits and set data for the first plot
        ## NOTE: changing axes ranges only works for the first plot
        if self.xmax_control.is_auto():
            xmax1 = max(xdata1)
        else:
            xmax1 = float(self.xmax_control.manual_value())
        
        if self.xmin_control.is_auto():
            xmin1 = min(xdata1)
        else:
            xmin1 = float(self.xmin_control.manual_value())

        ## Set Y-axis limits and set data for the first plot
        if self.ymin_control.is_auto():
            ymin1 = min(ydata2) - 0.05*min(ydata2)
        else:
            ymin1 = float(self.ymin_control.manual_value())
        
        if self.ymax_control.is_auto():
            ymax1 = max(ydata2) + 0.05*max(ydata2)
        else:
            ymax1 = float(self.ymax_control.manual_value())

        ## If axis min aquals max add small difference in order to avoid warning message
        if xmin1 == xmax1:
            xmin1 -= 0.001
            xmax1 += 0.001
        if ymin1 == ymax1:
            ymin1 -= 0.001
            ymax1 += 0.001
        
        ## Set axis for the first plot        
        self.axis1a.set_xbound(lower=xmin1, upper=xmax1)
        self.axis1a.set_ybound(lower=ymin1, upper=ymax1)

        # Set data to plot in window 1
        self.plot1a.set_xdata(xdata1_a)
        self.plot1a.set_ydata(ydata1_a)
        self.plot1b.set_xdata(xdata1_b)
        self.plot1b.set_ydata(ydata1_b)

        ## Set X-axis automatic limits and set data for the second plot
        ## NOTE: changing axes ranges only works for the first plot.
        ##
        ## If axis min aquals max add small difference in order to avoid warning message
        xmax2 = max(xdata2)
        xmin2 = min(xdata2)
        ymin2 = min(ydata2) - 0.05*min(ydata2)
        ymax2 = max(ydata2) + 0.05*max(ydata2)

        ## If axis min aquals max add small difference in order to avoid warning message
        if xmin2 == xmax2:
            xmin2 -= 0.001
            xmax2 += 0.001
        if ymin2 == ymax2:
            ymin2 -= 0.001
            ymax2 += 0.001

        ## Set axis for the second plot        
        self.axis2a.set_xbound(lower=xmin2, upper=xmax2)
        self.axis2a.set_ybound(lower=ymin2, upper=ymax2)

        # Set data to plot in window 2
        self.plot2a.set_xdata(xdata2_a)
        self.plot2a.set_ydata(ydata2_a)
        self.plot2b.set_xdata(xdata2_b)
        self.plot2b.set_ydata(ydata2_b)

        self.canvas.draw()

    def on_pause_button(self, event):
        self.paused = not self.paused
    
    def on_update_pause_button(self, event):
        label = "Resume" if self.paused else "Pause"
        self.pause_button.SetLabel(label)
    
    def on_save_plot(self, event):
        file_choices = "PNG (*.png)|*.png"
        
        dlg = wx.FileDialog(
            self, 
            message="Save plot as...",
            defaultDir=os.getcwd(),
            defaultFile="plot.png",
            wildcard=file_choices,
            style=wx.SAVE)
        
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.canvas.print_figure(path, dpi=self.dpi)
            self.flash_status_message("Saved to %s" % path)


    def draw_plot_3s(self, xdata1_a, ydata1_a, xdata2_a, ydata2_a, xdata1_b, ydata1_b, xdata2_b, ydata2_b, xdata1_c, ydata1_c, xdata2_c, ydata2_c):
        """ Redraws the plot
        """
        
        ## Get max values for first plot from series a, b and c
        datatmp = np.array([max(xdata1_a), max(xdata1_b), max(xdata1_c)])
        datatmpmax = np.where(datatmp==max(datatmp))[0][0]
        if datatmpmax == 0:
            xdata1 = xdata1_a
        elif datatmpmax == 1:
            xdata1 = xdata1_b
        else:
            xdata1 = xdata1_c

        datatmp = np.array([max(ydata1_a), max(ydata1_b), max(ydata1_c)])
        datatmpmax = np.where(datatmp==max(datatmp))[0][0]
        if datatmpmax == 0:
            ydata1 = ydata1_a
        elif datatmpmax == 1:
            ydata1 = ydata1_b
        else:
            ydata1 = ydata1_c
            
        ## Set X-axis limits and set data for the first plot
        ## NOTE: changing axes ranges only works for the first plot
        if self.xmax_control.is_auto():
            xmax1 = max(xdata1)
        else:
            xmax1 = float(self.xmax_control.manual_value())
        
        if self.xmin_control.is_auto():
            xmin1 = min(xdata1)
        else:
            xmin1 = float(self.xmin_control.manual_value())

        ## Set Y-axis limits and set data for the first plot
        if self.ymin_control.is_auto():
            ymin1 = min(ydata1) - 0.05*min(ydata1)
        else:
            ymin1 = float(self.ymin_control.manual_value())
        
        if self.ymax_control.is_auto():
            ymax1 = max(ydata1) + 0.05*max(ydata1)
        else:
            ymax1 = float(self.ymax_control.manual_value())

        ## If axis min aquals max add small difference in order to avoid warning message
        if xmin1 == xmax1:
            xmin1 -= 0.001
            xmax1 += 0.001
        if ymin1 == ymax1:
            ymin1 -= 0.001
            ymax1 += 0.001
        
        ## Set axis for the first plot        
        self.axis1a.set_xbound(lower=xmin1, upper=xmax1)
        self.axis1a.set_ybound(lower=ymin1, upper=ymax1)

        # Set data to plot in window 1
        self.plot1a.set_xdata(xdata1_a)
        self.plot1a.set_ydata(ydata1_a)
        self.plot1b.set_xdata(xdata1_b)
        self.plot1b.set_ydata(ydata1_b)
        self.plot1c.set_xdata(xdata1_c)
        self.plot1c.set_ydata(ydata1_c)

        ## Set X-axis automatic limits and set data for the second plot
        ## NOTE: changing axes ranges only works for the first plot.
        ##
        ## Get max values for first plot from series a, b and c
        datatmp = np.array([max(xdata2_a), max(xdata2_b), max(xdata2_c)])
        datatmpmax = np.where(datatmp==max(datatmp))[0][0]
        if datatmpmax == 0:
            xdata2 = xdata2_a
        elif datatmpmax == 1:
            xdata2 = xdata2_b
        else:
            xdata2 = xdata2_c

        datatmp = np.array([max(ydata2_a), max(ydata2_b), max(ydata2_c)])
        datatmpmax = np.where(datatmp==max(datatmp))[0][0]
        if datatmpmax == 0:
            ydata2 = ydata2_a
        elif datatmpmax == 1:
            ydata2 = ydata2_b
        else:
            ydata2 = ydata2_c
 
        xmax2 = max(xdata2)
        xmin2 = min(xdata2)
        ymin2 = min(ydata2) - 0.05*min(ydata2)
        ymax2 = max(ydata2) + 0.05*max(ydata2)

        ## If axis min aquals max add small difference in order to avoid warning message
        if xmin2 == xmax2:
            xmin2 -= 0.001
            xmax2 += 0.001
        if ymin2 == ymax2:
            ymin2 -= 0.001
            ymax2 += 0.001

        ## Set axis for the second plot        
        self.axis2a.set_xbound(lower=xmin2, upper=xmax2)
        self.axis2a.set_ybound(lower=ymin2, upper=ymax2)

        # Set data to plot in window 2
        self.plot2a.set_xdata(xdata2_a)   ##COMENTAMOS PARA QUE NO
        self.plot2a.set_ydata(ydata2_a)   ## SE MUESTREN ESTAS GRAFICAS       
        self.plot2b.set_xdata(xdata2_b)   ## EN LA SEGUNDA GRAFICA
        self.plot2b.set_ydata(ydata2_b)
        self.plot2c.set_xdata(xdata2_c)
        self.plot2c.set_ydata(ydata2_c)

        self.canvas.draw()
        
    def draw_plot_4s(self, xdata1_a, ydata1_a, xdata2_a, ydata2_a, xdata1_b, ydata1_b, xdata2_b, ydata2_b, 
                     xdata1_c, ydata1_c, xdata2_c, ydata2_c,xdata1_d, ydata1_d, xdata2_d, ydata2_d):
        
#        xdata1_e, ydata1_e, xdata2_e, ydata2_e, xdata1_f, ydata1_f, xdata2_f, ydata2_f, xdata1_g, ydata1_g, xdata2_g, ydata2_g
        """ Redraws the plot
        """
        
        ## Get max values for first plot from series a, b, c, d, e, f
        datatmp = np.array([max(xdata1_a), max(xdata1_b), max(xdata1_c), max(xdata1_d)])
        datatmpmax = np.where(datatmp == max(datatmp))[0][0]
        if datatmpmax == 0:
            xdata1 = xdata1_a
        elif datatmpmax == 1:
            xdata1 = xdata1_b
        elif datatmpmax == 2:
            xdata1 = xdata1_c
        else:
            xdata1 = xdata1_d

        datatmp = np.array([max(ydata1_a), max(ydata1_b), max(ydata1_c), max(ydata1_d)])
        datatmpmax = np.where(datatmp==max(datatmp))[0][0]
        if datatmpmax == 0:
            ydata1 = ydata1_a
        elif datatmpmax == 1:
            ydata1 = ydata1_b
        elif datatmpmax == 2:
            ydata1 = ydata1_c
        else:
            ydata1 = ydata1_d
            
        ## Set X-axis limits and set data for the first plot
        if self.xmax_control.is_auto():
            xmax1 = max(xdata1)
        else:
            xmax1 = float(self.xmax_control.manual_value())
        
        if self.xmin_control.is_auto():
            xmin1 = min(xdata1)
        else:
            xmin1 = float(self.xmin_control.manual_value())

        ## Set Y-axis limits and set data for the first plot
        if self.ymin_control.is_auto():
            ymin1 = min(ydata1) - 0.05*min(ydata1)
        else:
            ymin1 = float(self.ymin_control.manual_value())
        
        if self.ymax_control.is_auto():
            ymax1 = max(ydata1) + 0.05*max(ydata1)
        else:
            ymax1 = float(self.ymax_control.manual_value())

        ## If axis min aquals max add small difference in order to avoid warning message
        if xmin1 == xmax1:
            xmin1 -= 0.001
            xmax1 += 0.001
        if ymin1 == ymax1:
            ymin1 -= 0.001
            ymax1 += 0.001
        
        ## Set axis for the first plot        
        self.axis1a.set_xbound(lower=xmin1, upper=xmax1)
        self.axis1a.set_ybound(lower=ymin1, upper=ymax1)

        # Set data to plot in window 1
        self.plot1a.set_xdata(xdata1_a)
        self.plot1a.set_ydata(ydata1_a)
        self.plot1b.set_xdata(xdata1_b)
        self.plot1b.set_ydata(ydata1_b)
        self.plot1c.set_xdata(xdata1_c)
        self.plot1c.set_ydata(ydata1_c)
        self.plot1d.set_xdata(xdata1_d)
        self.plot1d.set_ydata(ydata1_d)


        ## Get max values for the second plot from series a, b, c and d
        datatmp = np.array([max(xdata2_a), max(xdata2_b), max(xdata2_c),max(xdata2_d)])
        datatmpmax = np.where(datatmp==max(datatmp))[0][0]
        if datatmpmax == 0:
            xdata2 = xdata2_a
        elif datatmpmax == 1:
            xdata2 = xdata2_b
        elif datatmpmax == 2:
            xdata2 = xdata2_c
        else:
            xdata2 = xdata2_d

        ####  Get max values just for the two ratios (O/Ar y Ti/Ar), because we only 
        ####  want to monitorate those intensities 
        datatmp = np.array([max(ydata2_a), max(ydata2_b), max(ydata2_c), max(ydata2_d)])
        datatmpmax = np.where(datatmp==max(datatmp))[0][0]
        if datatmpmax == 0:
            ydata2 = ydata2_a
        elif datatmpmax == 1:
            ydata2 = ydata2_b
        elif datatmpmax == 2:
            ydata2 = ydata2_c
        else:
            ydata2 = ydata2_d
        
#        datatmp = np.array([max(ydata2_c),max(ydata2_d)])
#        datatmpmax = np.where(datatmp==max(datatmp))[0][0]
#        if datatmpmax == 0:
#            ydata2 = ydata2_c
#        else:
#            ydata2 = ydata2_d
        ## Set X and Y-axis automatic limits and set data for the second plot
        ##
        xmax2 = max(xdata2)
        xmin2 = min(xdata2)
        
        ## Set Y-axis limits and set data for the second plot
        if self.ymin_control2.is_auto():
            ymin2 = min(ydata2) - 0.05*min(ydata2)
        else:
            ymin2 = float(self.ymin_control2.manual_value())
        
        if self.ymax_control2.is_auto():
            ymax2 = max(ydata2) + 0.05*max(ydata2)
        else:
            ymax2 = float(self.ymax_control2.manual_value())
        

        ## If axis min aquals max add small difference in order to avoid warning message
        if xmin2 == xmax2:
            xmin2 -= 0.001
            xmax2 += 0.001
        if ymin2 == ymax2:
            ymin2 -= 0.001
            ymax2 += 0.001

        ## Set axis for the second plot        
        self.axis2a.set_xbound(lower=xmin2, upper=xmax2)
        self.axis2a.set_ybound(lower=ymin2, upper=ymax2)

        # Set data to plot in window 2
        self.plot2a.set_xdata(xdata2_a)   ##COMENTAMOS PARA QUE NO
        self.plot2a.set_ydata(ydata2_a)   ## SE MUESTREN ESTAS GRAFICAS       
        self.plot2b.set_xdata(xdata2_b)   ## EN LA SEGUNDA GRAFICA
        self.plot2b.set_ydata(ydata2_b)
        self.plot2c.set_xdata(xdata2_c)
        self.plot2c.set_ydata(ydata2_c)
        self.plot2d.set_xdata(xdata2_d)
        self.plot2d.set_ydata(ydata2_d)

        self.canvas.draw()

    def on_pause_button(self, event):
        self.paused = not self.paused
    
    def on_update_pause_button(self, event):
        label = "Resume" if self.paused else "Pause"
        self.pause_button.SetLabel(label)
    
    def on_save_plot(self, event):
        file_choices = "PNG (*.png)|*.png"
        
        dlg = wx.FileDialog(
            self, 
            message="Save plot as...",
            defaultDir=os.getcwd(),
            defaultFile="plot.png",
            wildcard=file_choices,
            style=wx.SAVE)
        
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.canvas.print_figure(path, dpi=self.dpi)
            self.flash_status_message("Saved to %s" % path)
    
            
class MyFrame(wx.Frame):
    """ Application main frame
    """
    def __init__(self, title, size):
        wx.Frame.__init__(self, None, -1, title=title, size=size)
        
        self.create_menu()
        self.create_main_panel()
        self.create_material()
        self.create_gas()
       ## Initialize variables
        
        self.spect="0"
        self.material = self.AlItem.Id
        self.gas = self.O2Item.Id
        self.lines()
        self.ArInt = []
        self.nbdata = 1
        self.fcount = []
        self.xdata = np.arange(1)
        self.ydata_slope25 = np.arange(1)
        self.ydata_slope50 = np.arange (1)
        self.ydata_slope75 = np.arange(1)
        self.ydata_integral = np.arange(1)
        self.ydata_OI_int = np.arange(1)
        self.slope_OI_Ar = np.arange(1)
        self.ydata_OI_Ar_ratio = np.arange(1)
        self.ydata_Al_int = np.arange(1)
        self.slope_Al_Ar = np.arange(1)
        self.ydata_Al_Ar_ratio = np.arange(1)
        self.ydata_Ti_int = np.arange(1)
        self.slope_Ti_Ar = np.arange(1)
        self.ydata_Ti_Ar_ratio = np.arange(1)
        self.ydata_NII_int = np.arange(1)
        self.slope_NII_Ar = np.arange(1)
        self.ydata_NII_Ar_ratio = np.arange(1)
        self.ydata_Si_int = np.arange(1)
        self.slope_Si_Ar = np.arange(1)
        self.ydata_Si_Ar_ratio = np.arange(1)
        self.input_panel.start = False
        
        ## Define events
        self.Bind(wx.EVT_CLOSE, self.on_exit)

        self.plot_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_plot_timer, self.plot_timer)        
        self.plot_timer.Start(100)
        
    def create_menu(self):
        """ Application menu
        """
        self.menubar = wx.MenuBar()
        menu_file = wx.Menu()
        m_expt = menu_file.Append(-1, "&Save plot\tCtrl-S", "Save plot to file")
        self.Bind(wx.EVT_MENU, self.on_save_plot, m_expt)
        menu_file.AppendSeparator()
        m_exit = menu_file.Append(-1, "E&xit\tCtrl-X", "Exit")
        self.Bind(wx.EVT_MENU, self.on_exit, m_exit)
        self.menubar.Append(menu_file, "&File")
        self.SetMenuBar(self.menubar)
    #####Define the Target buttons#####    
        
    def create_material(self):
        """ Application Material
        """
        self.MenuBar = wx.MenuBar()
        menu_Material = wx.Menu()
        #Creating the materials Items
        self.AlItem = menu_Material.Append(wx.NewId(), "Aluminium", kind = wx.ITEM_RADIO)
        self.Bind(wx.EVT_MENU, self.Target, self.AlItem)
        
        self.TiItem = menu_Material.Append(wx.NewId(),"Titanium", kind = wx.ITEM_RADIO)                  
        self.Bind(wx.EVT_MENU, self.Target, self.TiItem)
       
        self.SiItem = menu_Material.Append(wx.NewId(), "Silicon", kind = wx.ITEM_RADIO)
        self.Bind(wx.EVT_MENU, self.Target, self.SiItem)           

        self.menubar.Append(menu_Material, "&Target")
        self.SetMenuBar(self.menubar)
        
    #Creating the material target to input##    
    def Target(self, event):
       
        
        self.material = event.Id
#        TargetId=event.Id
#        
#        if TargetId == self.AlItem.Id:
#            print('culiao')
#            self.material==self.AlItem.Id
#        
#        
#        elif TargetId == self.TiItem.Id:
#            print('maraca')
#            self.TiItem.Id    
#   
#        elif TargetId == self.SiItem.Id:
#            print('wea')
#            self.SiItem.Id
            
   
      
        
    def create_gas(self):
        """ Application Material
        """
        self.MenuBar = wx.MenuBar()
        menu_Material = wx.Menu()
        #Creating the materials Items
        self.O2Item = menu_Material.Append(wx.NewId(), "Oxigen", kind = wx.ITEM_RADIO)
        self.Bind(wx.EVT_MENU, self.Reactive_gas, self.O2Item)
        
        self.N2Item = menu_Material.Append(wx.NewId(),"Nitrogen", kind = wx.ITEM_RADIO)                  
        self.Bind(wx.EVT_MENU, self.Reactive_gas, self.N2Item)         

        self.menubar.Append(menu_Material, "&Gas")
        self.SetMenuBar(self.menubar)    
        
        #####Creating the reactive gas input for plotting##
    def Reactive_gas (self, event):
        
        self.gas = event.Id
#        GasId=event.Id
#        
#        if GasId == self.O2Item.Id:
#            print('chapo')
#            self.O2Item.Id
#        
#        elif GasId == self.N2Item.Id:
#            print ('ole')
#            self.N2Item.Id    

        
        
    def create_main_panel(self):
        """ Main application layout
        """
        self.panel = wx.Panel(self)

        ## Set application layout
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.input_panel = InputPanel(self.panel, -1, self.vbox)
        self.live_plot = LivePlot(self.panel, -1, self.vbox)
        self.panel.SetSizer(self.vbox)
        self.vbox.Fit(self)

    def load_data(self, fname):
        ## Verify if data comme from AvaSpecs, Thorlabs or OceanOptics spectrograph
        ## Load Avantes data
        if 'Raw8' in fname:
            self.spect='AVANTES'
            UVfname = fname
            VIS = list(fname)
            VIS[fname.find('1704146') + 6] = '7'
            VIS[fname.find('1704146')-3:fname.find('1704146')-1] = 'VIS'
            VISfname = ''.join(VIS)
            dataUV = np.loadtxt(UVfname, delimiter=';', skiprows=8, usecols=(0,1))
            dataVIS = np.loadtxt(VISfname, delimiter=';', skiprows=8, usecols=(0,1))
            data_n = np.concatenate((dataUV,dataVIS),axis=0)
            data = data_n/64000
        elif np.fromfile(fname, count=2, sep=";").size == 1:
            ## Load Thorlabs data
            self.spect='THORLABS'
            data = pandas.read_csv(fname, sep=";").values
        else:
            ## Load OceanOptics data
            self.spect='OCEANOPTICS'
            data = pandas.read_csv(fname, sep=" ").values
            
        return data

    def on_plot_timer(self, event):
        """ Load data and plot
        """
        self.material
        self.gas
        ## Defines when to start and stop ploting data 
        if self.input_panel.start:
            ## Get data to plot
            if self.nbdata == 1:
                self.fname_base()
                self.slopes()

            if os.path.isfile(self.fname):
                self.get_data(self.fname)
                
                self.xdata = np.append(self.xdata, self.nbdata)
                self.ydata_slope25 = np.append(self.ydata_slope25, self.slope25)
                self.ydata_slope50 = np.append(self.ydata_slope50, self.slope50)
                self.ydata_slope75 = np.append(self.ydata_slope75, self.slope75)
                self.ydata_integral = np.append(self.ydata_integral, self.Ar_line_int)
                self.ydata_OI_int = np.append(self.ydata_OI_int, self.OI_line_int)
                self.slope_OI_Ar = np.append(self.slope_OI_Ar, self.slope_OI_Ar_50)
                self.ydata_OI_Ar_ratio = np.append(self.ydata_OI_Ar_ratio, self.OI_Ar_ratio)
                self.ydata_Ti_int = np.append(self.ydata_Ti_int, self.Ti_line_int)
                self.slope_Ti_Ar = np.append(self.slope_Ti_Ar, self.slope_Ti_Ar_50)
                self.ydata_Ti_Ar_ratio = np.append(self.ydata_Ti_Ar_ratio, self.Ti_Ar_ratio)
                self.ydata_Si_int = np.append(self.ydata_Si_int, self.Si_line_int)
                self.slope_Si_Ar = np.append(self.slope_Si_Ar, self.slope_Si_Ar_50)
                self.ydata_Si_Ar_ratio = np.append(self.ydata_Si_Ar_ratio, self.Si_Ar_ratio)
                self.ydata_Al_int = np.append(self.ydata_Al_int, self.Al_line_int)
                self.slope_Al_Ar = np.append(self.slope_Al_Ar, self.slope_Al_Ar_50)
                self.ydata_Al_Ar_ratio = np.append(self.ydata_Al_Ar_ratio, self.Al_Ar_ratio)
                self.ydata_NII_int = np.append(self.ydata_NII_int, self.NII_line_int)
                self.slope_NII_Ar = np.append(self.slope_NII_Ar, self.slope_NII_Ar_50)
                self.ydata_NII_Ar_ratio = np.append(self.ydata_NII_Ar_ratio, self.NII_Ar_ratio)
                self.fname_new()
             
        if self.material == self.TiItem.Id and self.gas == self.O2Item.Id:
        
            self.live_plot.draw_plot_4s(self.xdata, self.ydata_slope25, self.xdata, self.ydata_integral,
                                    self.xdata, self.ydata_slope50, self.xdata, self.ydata_integral,
                                    self.xdata, self.slope_OI_Ar, self.xdata, self.self.ydata_OI_int,
                                    self.xdata, self.slope_Ti_Ar, self.xdata, self.ydata_Ti_int)
            
        elif self.material == self.TiItem.Id and self.gas == self.N2Item.Id:
            self.live_plot.draw_plot_4s(self.xdata, self.ydata_slope25, self.xdata, self.ydata_integral,
                                    self.xdata, self.ydata_slope50, self.xdata, self.ydata_integral,
                                    self.xdata, self.slope_NII_Ar, self.xdata, self.ydata_NII_int,
                                    self.xdata, self.slope_Ti_Ar, self.xdata, self.ydata_Ti_int)
                                    
        elif self.material == self.AlItem.Id and self.gas == self.O2Item.Id:
            self.live_plot.draw_plot_4s(self.xdata, self.ydata_slope25, self.xdata, self.ydata_integral,
                                    self.xdata, self.ydata_slope50, self.xdata, self.ydata_integral,
                                    self.xdata, self.slope_OI_Ar, self.xdata, self.ydata_OI_int,
                                    self.xdata, self.slope_Al_Ar, self.xdata, self.ydata_Al_int)
            
        elif self.material == self.AlItem.Id and self.gas == self.N2Item.Id:
            self.live_plot.draw_plot_4s(self.xdata, self.ydata_slope25, self.xdata, self.ydata_integral,
                                    self.xdata, self.ydata_slope50, self.xdata, self.ydata_integral,
                                    self.xdata, self.slope_NII_Ar, self.xdata, self.ydata_NII_int,
                                    self.xdata, self.slope_Al_Ar, self.xdata, self.ydata_Al_int)
            
            
        elif self.material == self.SiItem.Id and self.gas == self.O2Item.Id:
            self.live_plot.draw_plot_4s(self.xdata, self.ydata_slope25, self.xdata, self.ydata_integral,
                                    self.xdata, self.ydata_slope50, self.xdata, self.ydata_integral,
                                    self.xdata, self.slope_OI_Ar, self.xdata, self.ydata_OI_int,
                                    self.xdata, self.slope_Si_Ar, self.xdata, self.ydata_Si_int)
            
        elif self.material == self.SiItem.Id and self.gas == self.N2Item.Id:        
            self.live_plot.draw_plot_4s(self.xdata, self.ydata_slope25, self.xdata, self.ydata_integral,
                                    self.xdata, self.ydata_slope50, self.xdata, self.ydata_integral,
                                    self.xdata, self.slope_NII_Ar, self.xdata, self.ydata_NII_int,
                                    self.xdata, self.slope_Si_Ar, self.xdata, self.ydata_Si_int)
        
            

#           elif material== 'Ti' and gas='N2'
#            self.live_plot.draw_plot_4s(self.xdata, self.ydata_slope25, self.xdata, self.ydata_integral,
#                                    self.xdata, self.ydata_slope75, self.xdata, self.ydata_integral,
#                                    self.xdata, self.slope_OI_Ar, self.xdata, self.ydata_OI_Ar_ratio,
#                                    self.xdata, self.slope_Ti_Ar, self.xdata, self.ydata_Ti_Ar_ratio,
#                                    self.xdata, self.slope_Al_Ar, self.xdata, self.ydata_Al_Ar_ratio,
#                                    self.xdata, self.slope_NII_Ar, self.xdata, self.ydata_NII_Ar_ratio,
#                                    self.xdata, self.slope_Si_Ar, self.xdata, self.ydata_Si_Ar_ratio,)  
   
    #def choose_AlItem (self, event):
        #print ("hola mundo")
       # for i in range(len(self.xdata)):
            #print self.xdata[i][0]
        
      #  pass
        
    #def choose_SiItem (self, event):
       # pass    
    
    #def choose_TiItem (self, event):
        #pass
    

    def on_save_plot(self, event):
        file_choices = "PNG (*.png)|*.png"
        
        dlg = wx.FileDialog(
            self, 
            message="Save plot as...",
            defaultDir=os.getcwd(),
            defaultFile="plot.png",
            wildcard=file_choices,
            style=wx.SAVE)
        
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.canvas.print_figure(path, dpi=self.dpi)
            self.flash_status_message("Saved to %s" % path)
       #####Define the material target#####
    def lines(self):
        """ Lines list
        """
        
        ### Define spectra lines of Avantes
        ###
        if self.spect == 'AVANTES':
            ## ArI - central wlen position: 706nm (VIS +2048)
            self.Ar_half_width = 3
            self.Ar_line = 1139 + 2048
            self.Ar_line_min = self.Ar_line - self.Ar_half_width
            self.Ar_line_max = self.Ar_line + self.Ar_half_width
            ## ArII - min wlen in pixel position: 696.51 nm
            self.ArII_half_width = 8
            self.ArII_line = 1072
            self.ArII_line_min = self.ArII_line - self.ArII_half_width
            self.ArII_line_max = self.ArII_line + self.ArII_half_width
             ## AlI- central when in pixel position: 257.57 nm
            self.Al_half_width = 3
            self.Al_line = 447
            self.Al_line_min = self.Al_line - self.Al_half_width
            self.Al_line_max = self.Al_line + self.Al_half_width
                       ## TiI - central wlen in pixel position: 468.196 nm
            self.Ti_half_width = 3
            self.Ti_line = 1295
            self.Ti_line_min = self.Ti_line - self.Ti_half_width
            self.Ti_line_max = self.Ti_line + self.Ti_half_width
                       ## Si - central wlen in pixel position: 288.1 nm (UV)
            self.Si_half_width = 3
            self.Si_line = 666
            self.Si_line_min = self.Si_line - self.Si_half_width
            self.Si_line_max = self.Si_line + self.Si_half_width
            self.nb_files = 50   
            
            ####Define the reactive gas####
    
            ## OI - central wlen in pixel position: 777.26 nm (VIS +2048)
            #self.OI_line = 2637
            self.OI_half_width = 4
            self.OI_line = 1409 + 2048
            self.OI_line_min = self.OI_line - self.half_width
            self.OI_line_max = self.OI_line + self.half_width
           
            ## N2 molecular - central wlen in pixel position: 315.86 nm (UV)
            self.NII_half_width = 2
            self.NII_line = 867
            self.NII_line_min = self.NII_line - self.NII_half_width
            self.NII_line_max = self.NII_line + self.NII_half_width
    
            ## Set number of files to compute slope
            self.nb_files = 50
            
        ### Define spectra lines of ThorLabs
        ###    
        else: 
                   
            ## ArI - central wlen position: 706.6 nm (VIS +2048)
            self.half_width = 4
            self.Ar_line = 1139+2048
            self.Ar_line_min = self.Ar_line - self.half_width
            self.Ar_line_max = self.Ar_line + self.half_width
            ## ArII - min wlen in pixel position: 476.5 nm (VIS +2048)
            self.ArII_half_width = 3
            self.ArII_line = 305 +2048
            self.ArII_line_min = self.ArII_line - self.ArII_half_width
            self.ArII_line_max = self.ArII_line + self.ArII_half_width
             ## AlI- central when in pixel position: 398.42-396.1 realnm
            self.Al_half_width = 3
            self.Al_line = 447
            self.Al_line_min = self.Al_line - self.Al_half_width
            self.Al_line_max = self.Al_line + self.Al_half_width
                       ## TiI - central wlen in pixel position: 468.196 nm
            self.Ti_half_width = 3
            self.Ti_line = 1295
            self.Ti_line_min = self.Ti_line - self.Ti_half_width
            self.Ti_line_max = self.Ti_line + self.Ti_half_width
                       ## Si - central wlen in pixel position: 288.1nm (UV)
            self.Si_half_width = 3
            self.Si_line = 666
            self.Si_line_min = self.Si_line - self.Si_half_width
            self.Si_line_max = self.Si_line + self.Si_half_width
            self.nb_files = 50   
            
            ####Define the reactive gas####
    
            ## OI - central wlen in pixel position: 777.26 nm
            self.OI_half_width = 3
            self.OI_line = 1409+2048
            self.OI_line_min = self.OI_line - self.half_width
            self.OI_line_max = self.OI_line + self.half_width
           
            ## N2 molecular - central wlen in pixel position: 315.8nm
            self.NII_half_width = 3
            self.NII_line = 867
            self.NII_line_min = self.NII_line - self.NII_half_width
            self.NII_line_max = self.NII_line + self.NII_half_width
    
            ## Set number of files to compute slope
            self.nb_files = 50

    def fname_base(self):

        ## Get file name and directory
        self.fname = self.input_panel.fname_txtctrl1.GetValue()
        self.dname = self.input_panel.dname_txtctrl1.GetValue()
        if wx.Platform == "__WXMSW__":
            self.fname = self.dname + "\\" + self.fname
        else:
            self.fname = self.dname + "/" + self.fname
            
        self.fnumber = self.fname.split("_")[-1].split(".")[0]
        self.fcounter = int(self.fnumber)
        self.fcounter_length = str(len(self.fnumber))

    def fname_new(self):
        """ Update file name
        """
        self.nbdata += 1
        self.str_temp = "%."+self.fcounter_length+"d"
        self.old_index = self.str_temp %self.fcounter
        self.fcounter += 1
        self.str_temp = "%."+self.fcounter_length+"d"
        self.new_index = self.str_temp %self.fcounter
        fname2 = list(self.fname)
        fname2[self.fname.find('Raw8')-5:self.fname.find('Raw8')-1] = self.new_index
        self.fname = ''.join(fname2)
        #self.fname = self.fname.replace(self.old_index, self.new_index)
              

    def slopes(self):
        """ Initialize slope buffers
        """
        self.slope_window25 = 25
        self.xsample25 = np.zeros(self.slope_window25)
        self.ysample25 = np.zeros(self.slope_window25)

        self.slope_window50 = 50
        self.xsample50 = np.zeros(self.slope_window50)
        self.ysample50 = np.zeros(self.slope_window50)
     
        self.slope_window75 = 75
        self.xsample75 = np.zeros(self.slope_window75)
        self.ysample75 = np.zeros(self.slope_window75)
    
        self.x_OI_Ar_50 = np.zeros(self.slope_window50)
        self.y_OI_Ar_50 = np.zeros(self.slope_window50)
        
        self.x_Ti_Ar_50 = np.zeros(self.slope_window50)
        self.y_Ti_Ar_50 = np.zeros(self.slope_window50)
        
        self.x_Al_Ar_50 = np.zeros(self.slope_window50)
        self.y_Al_Ar_50 = np.zeros(self.slope_window50)
        
        self.x_Si_Ar_50 = np.zeros(self.slope_window50)
        self.y_Si_Ar_50 = np.zeros(self.slope_window50)
        
        self.x_NII_Ar_50 = np.zeros(self.slope_window50)
        self.y_NII_Ar_50 = np.zeros(self.slope_window50)

    def get_data(self, fname):

        if os.path.isfile(fname):
            data = self.load_data(self.fname)
            self.intensity = data[:,1]

            ## Set file name in plots title    
            if wx.Platform == "__WXMSW__":
                self.live_plot.axis1a.set_title(self.fname.split("\\")[-1], size=10)
            else:
                self.live_plot.axis1a.set_title(self.fname.split("/")[-1], size=10)
                
#            self.live_plot.axis1a.set_ylabel("Pendientes")
#            self.live_plot.axis2a.set_ylabel("Intensidades")

            ## Get line intesity (compute integral simply by sum of pixel values)
            self.Ar_line_int = sum(self.intensity[self.Ar_line_min:self.Ar_line_max])
            self.ArII_line_int = sum(self.intensity[self.ArII_line_min:self.ArII_line_max])
            self.NII_line_int = sum(self.intensity[self.NII_line_min:self.NII_line_max])
            self.OI_line_int = sum(self.intensity[self.OI_line_min:self.OI_line_max])
            self.Ti_line_int = sum(self.intensity[self.Ti_line_min:self.Ti_line_max])
            self.Al_line_int = sum(self.intensity[self.Al_line_min:self.Al_line_max])
            self.Si_line_int = sum(self.intensity[self.Si_line_min:self.Si_line_max])

            ## Compute ratios
            self.OI_Ar_ratio = self.OI_line_int/self.Ar_line_int
            self.Ti_Ar_ratio = self.Ti_line_int/self.Ar_line_int
            self.Al_Ar_ratio = self.Al_line_int/self.Ar_line_int
            self.Si_Ar_ratio = self.Si_line_int/self.Ar_line_int
            self.NII_Ar_ratio = self.NII_line_int/self.Ar_line_int
            
            ## Compute slopes
            ##
            ## Slope from Ar peak integral with 25 files
            self.xsample25 = pylab.roll(self.xsample25, -1)
            self.xsample25[-1] = self.fcounter
            self.ysample25 = pylab.roll(self.ysample25, -1)
            self.ysample25[-1] = self.Ar_line_int
            if self.fcounter > self.slope_window25:
                self.slope25 = (pylab.polyfit(self.xsample25, self.ysample25, 1))[0]
            else:
                self.slope25 = 0
         
            ## Slope from Ar peak integral with 50 files
            self.xsample50 = pylab.roll(self.xsample50, -1)
            self.xsample50[-1] = self.fcounter
            self.ysample50 = pylab.roll(self.ysample50, -1)
            self.ysample50[-1] = self.Ar_line_int
            if self.fcounter > self.slope_window50:
                self.slope50 = (pylab.polyfit(self.xsample50, self.ysample50, 1))[0]
            else:
                self.slope50 = 0
            
            ## Slope from Ar peak integral with 75 files
            self.xsample75 = pylab.roll(self.xsample75, -1)
            self.xsample75[-1] = self.fcounter
            self.ysample75 = pylab.roll(self.ysample75, -1)
            self.ysample75[-1] = self.Ar_line_int
            if self.fcounter > self.slope_window75:
                self.slope75 = (pylab.polyfit(self.xsample75, self.ysample75, 1))[0]
            else:
                self.slope75 = 0


            ## Slope from OI_Ar ratio with 50 files
            self.x_OI_Ar_50 = pylab.roll(self.x_OI_Ar_50, -1)
            self.x_OI_Ar_50[-1] = self.fcounter
            self.y_OI_Ar_50 = pylab.roll(self.y_OI_Ar_50, -1)
            self.y_OI_Ar_50[-1] = self.OI_Ar_ratio
            if self.fcounter > self.slope_window50:
                self.slope_OI_Ar_50 = (pylab.polyfit(self.x_OI_Ar_50, self.y_OI_Ar_50, 1))[0]
            else:
                self.slope_OI_Ar_50 = 0
                
            ## Slope from NII_Ar ratio with 75 files
            self.x_NII_Ar_50 = pylab.roll(self.x_NII_Ar_50, -1)
            self.x_NII_Ar_50[-1] = self.fcounter
            self.y_NII_Ar_50 = pylab.roll(self.y_NII_Ar_50, -1)
            self.y_NII_Ar_50[-1] = self.NII_Ar_ratio
            if self.fcounter > self.slope_window75:
                self.slope_NII_Ar_50 = (pylab.polyfit(self.x_NII_Ar_50, self.y_NII_Ar_50, 1))[0]
            else:
                self.slope_NII_Ar_50 = 0  
                
            ## Slope from Ti_Ar ratio with 75 files
            self.x_Ti_Ar_50 = pylab.roll(self.x_Ti_Ar_50, -1)
            self.x_Ti_Ar_50[-1] = self.fcounter
            self.y_Ti_Ar_50 = pylab.roll(self.y_Ti_Ar_50, -1)
            self.y_Ti_Ar_50[-1] = self.Ti_Ar_ratio
            if self.fcounter > self.slope_window75:
                self.slope_Ti_Ar_50 = (pylab.polyfit(self.x_Ti_Ar_50, self.y_Ti_Ar_50, 1))[0]
            else:
                self.slope_Ti_Ar_50 = 0    
                
             ## Slope from Al_Ar ratio with 50 files
            self.x_Al_Ar_50 = pylab.roll(self.x_Al_Ar_50, -1)
            self.x_Al_Ar_50[-1] = self.fcounter
            self.y_Al_Ar_50 = pylab.roll(self.y_Al_Ar_50, -1)
            self.y_Al_Ar_50[-1] = self.Al_Ar_ratio
            if self.fcounter > self.slope_window50:
                self.slope_Al_Ar_50 = (pylab.polyfit(self.x_Al_Ar_50, self.y_Al_Ar_50, 1))[0]
            else:
                self.slope_Al_Ar_50 = 0    
                
              ## Slope from Si_Ar ratio with 50 files
            self.x_Si_Ar_50 = pylab.roll(self.x_Si_Ar_50, -1)
            self.x_Si_Ar_50[-1] = self.fcounter
            self.y_Si_Ar_50 = pylab.roll(self.y_Si_Ar_50, -1)
            self.y_Si_Ar_50[-1] = self.Si_Ar_ratio
            if self.fcounter > self.slope_window75:
                self.slope_Si_Ar_50 = (pylab.polyfit(self.x_Si_Ar_50, self.y_Si_Ar_50, 1))[0]
            else:
                self.slope_Si_Ar_50 = 0    
            
          
            
                
    
    def on_exit(self, event):
        # dialog = wx.MessageDialog(self, "Are you sure you want to quit?", "Caption", wx.YES_NO)
        # response = dialog.ShowModal()
        # if response == wx.ID_YES:
        self.Destroy()
    


if __name__ == '__main__':
    app = wx.App()
    app.frame = MyFrame("SAOM-Lab: Live Plot", size=(950, 600))
    app.SetTopWindow(app.frame)
    app.frame.Show()
    app.MainLoop()
