from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas
import numpy as np
import os
import pylab
import wx

from plasmonitor.controls import PlotControls


class LivePlot(wx.Panel):
    """ A static box with a couple of radio buttons and a text
        box. Allows to switch between an automatic mode and a 
        manual mode with an associated value.
    """

    def __init__(self, parent, ID, vbox):
        wx.Panel.__init__(self, parent, ID)

        # Initialize plot and canvas
        dpi = wx.ScreenDC().GetPPI()[0]
        fig = Figure((3.0, 3.0), dpi=dpi)

        # Init data used just to draw the canvas and plots
        data_init = np.zeros(1)

        # Create first plot axis
        ##
        # Serie "a"
        self.axis1a = fig.add_subplot(211)
        self.axis1a.set_title("Plot 1", size=10)
        self.axis1a.set_ylabel("Slope", size=10)
        self.axis1a.axhline(0, linestyle="--")
        self.axis1a.grid(True, color='gray')
        pylab.setp(self.axis1a.get_xticklabels(), fontsize=8)
        pylab.setp(self.axis1a.get_yticklabels(), fontsize=8)
        self.plot1a = self.axis1a.plot(
            data_init, linewidth=0, color="blue", marker="o",)[0]
        # Serie "b"
        self.axis1b = fig.add_subplot(211)
        self.plot1b = self.axis1b.plot(
            data_init, linewidth=0, color="black", marker="o",)[0]
        # Serie "c"
        self.axis1c = fig.add_subplot(211)
        self.plot1c = self.axis1c.plot(
            data_init, linewidth=0, color="red", marker="o",)[0]
        # Serie "d"
        self.axis1d = fig.add_subplot(211)
        self.plot1d = self.axis1d.plot(
            data_init, linewidth=0, color="green", marker="o",)[0]

        # Create second plot axis
        ##
        # Serie "a"
        self.axis2a = fig.add_subplot(212)
        self.axis2a.set_ylabel("Integral", size=10)
        self.axis2a.set_xlabel("File number", size=10)
        self.axis2a.grid(True, color='gray')
        pylab.setp(self.axis2a.get_xticklabels(), fontsize=8)
        pylab.setp(self.axis2a.get_yticklabels(), fontsize=8)
        self.plot2a = self.axis2a.plot(
            data_init, linewidth=0, color="blue", marker="o",)[0]
        # Serie "b"
        self.axis2b = fig.add_subplot(212)
        self.plot2b = self.axis2b.plot(
            data_init, linewidth=0, color="black", marker="o",)[0]
        # Serie "c"
        self.axis2c = fig.add_subplot(212)
        self.plot2c = self.axis2c.plot(
            data_init, linewidth=0, color="red", marker="o",)[0]
        # Serie "d"
        self.axis2d = fig.add_subplot(212)
        self.plot2d = self.axis2d.plot(
            data_init, linewidth=0, color="green", marker="o",)[0]

        # Create canvas to add plot windows
        self.canvas = FigCanvas(parent, -1, fig)
        vbox.Add(self.canvas, 1, flag=wx.LEFT | wx.RIGHT |
                 wx.TOP | wx.DOWN | wx.GROW, border=10)

        # Set plot controls
        # Creates a box to manipulate zoom of the first plot and second plot
        self.xmin_control = PlotControls(parent, -1, "X min 1", 0)
        self.xmax_control = PlotControls(parent, -1, "X max 1", 200)
        self.ymin_control = PlotControls(parent, -1, "Y min 1", -0.0015)
        self.ymax_control = PlotControls(parent, -1, "Y max 1", 0.0015)

        # Creates a box to manipulate zoom of the second plot
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

        vbox.Add(hbox1, flag=wx.ALIGN_CENTER | wx.TOP)

    def draw_plot(self, xdata1, ydata1, xdata2, ydata2):
        """ Redraws the plot
        """
        # Set X-axis limits and set data for the first plot
        # NOTE: changing axes ranges only works for the first plot
        if self.xmax_control.is_auto():
            xmax1 = max(xdata1)
        else:
            xmax1 = float(self.xmax_control.manual_value())

        if self.xmin_control.is_auto():
            xmin1 = min(xdata1)
        else:
            xmin1 = float(self.xmin_control.manual_value())

        # Set Y-axis limits and set data for the first plot
        if self.ymin_control.is_auto():
            ymin1 = min(ydata2) - 0.05*min(ydata2)
        else:
            ymin1 = float(self.ymin_control.manual_value())

        if self.ymax_control.is_auto():
            ymax1 = max(ydata2) + 0.05*max(ydata2)
        else:
            ymax1 = float(self.ymax_control.manual_value())

        # If axis min aquals max add small difference in order to avoid warning message
        if xmin1 == xmax1:
            xmin1 -= 0.001
            xmax1 += 0.001
        if ymin1 == ymax1:
            ymin1 -= 0.001
            ymax1 += 0.001

        # Set axis for the first plot
        self.axis1a.set_xbound(lower=xmin1, upper=xmax1)
        self.axis1a.set_ybound(lower=ymin1, upper=ymax1)

        # Set data to plot in window 1
        self.plot1a.set_xdata(xdata1)
        self.plot1a.set_ydata(ydata1)

        # Set X-axis automatic limits and set data for the second plot
        # NOTE: changing axes ranges only works for the first plot.
        ##
        # If axis min aquals max add small difference in order to avoid warning message
        xmax2 = max(xdata2)
        xmin2 = min(xdata2)
        ymin2 = min(ydata2) - 0.05*min(ydata2)
        ymax2 = max(ydata2) + 0.05*max(ydata2)

        # If axis min aquals max add small difference in order to avoid warning message
        if xmin2 == xmax2:
            xmin2 -= 0.001
            xmax2 += 0.001
        if ymin2 == ymax2:
            ymin2 -= 0.001
            ymax2 += 0.001

        # Set axis for the second plot
        self.axis2a.set_xbound(lower=xmin2, upper=xmax2)
        self.axis2a.set_ybound(lower=ymin2, upper=ymax2)

        # Set data to plot in window 1
        self.plot2a.set_xdata(xdata2)
        self.plot2a.set_ydata(ydata2)

        self.canvas.draw()

    def draw_plot_2s(self, xdata1_a, ydata1_a, xdata2_a, ydata2_a, xdata1_b, ydata1_b, xdata2_b, ydata2_b):
        """ Redraws the plot
        """

        # Get max values from series a and b
        if max(xdata1_a) >= max(xdata1_b):
            xdata1 = xdata1_a
        else:
            xdata1 = xdata1_b

        if max(ydata1_a) >= max(ydata1_b):
            ydata1 = ydata1_a
        else:
            ydata1 = ydata1_b

        # Set X-axis limits and set data for the first plot
        # NOTE: changing axes ranges only works for the first plot
        if self.xmax_control.is_auto():
            xmax1 = max(xdata1)
        else:
            xmax1 = float(self.xmax_control.manual_value())

        if self.xmin_control.is_auto():
            xmin1 = min(xdata1)
        else:
            xmin1 = float(self.xmin_control.manual_value())

        # Set Y-axis limits and set data for the first plot
        if self.ymin_control.is_auto():
            ymin1 = min(ydata2) - 0.05*min(ydata2)
        else:
            ymin1 = float(self.ymin_control.manual_value())

        if self.ymax_control.is_auto():
            ymax1 = max(ydata2) + 0.05*max(ydata2)
        else:
            ymax1 = float(self.ymax_control.manual_value())

        # If axis min aquals max add small difference in order to avoid warning message
        if xmin1 == xmax1:
            xmin1 -= 0.001
            xmax1 += 0.001
        if ymin1 == ymax1:
            ymin1 -= 0.001
            ymax1 += 0.001

        # Set axis for the first plot
        self.axis1a.set_xbound(lower=xmin1, upper=xmax1)
        self.axis1a.set_ybound(lower=ymin1, upper=ymax1)

        # Set data to plot in window 1
        self.plot1a.set_xdata(xdata1_a)
        self.plot1a.set_ydata(ydata1_a)
        self.plot1b.set_xdata(xdata1_b)
        self.plot1b.set_ydata(ydata1_b)

        # Set X-axis automatic limits and set data for the second plot
        # NOTE: changing axes ranges only works for the first plot.
        ##
        # If axis min aquals max add small difference in order to avoid warning message
        xmax2 = max(xdata2)
        xmin2 = min(xdata2)
        ymin2 = min(ydata2) - 0.05*min(ydata2)
        ymax2 = max(ydata2) + 0.05*max(ydata2)

        # If axis min aquals max add small difference in order to avoid warning message
        if xmin2 == xmax2:
            xmin2 -= 0.001
            xmax2 += 0.001
        if ymin2 == ymax2:
            ymin2 -= 0.001
            ymax2 += 0.001

        # Set axis for the second plot
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

        # Get max values for first plot from series a, b and c
        datatmp = np.array([max(xdata1_a), max(xdata1_b), max(xdata1_c)])
        datatmpmax = np.where(datatmp == max(datatmp))[0][0]
        if datatmpmax == 0:
            xdata1 = xdata1_a
        elif datatmpmax == 1:
            xdata1 = xdata1_b
        else:
            xdata1 = xdata1_c

        datatmp = np.array([max(ydata1_a), max(ydata1_b), max(ydata1_c)])
        datatmpmax = np.where(datatmp == max(datatmp))[0][0]
        if datatmpmax == 0:
            ydata1 = ydata1_a
        elif datatmpmax == 1:
            ydata1 = ydata1_b
        else:
            ydata1 = ydata1_c

        # Set X-axis limits and set data for the first plot
        # NOTE: changing axes ranges only works for the first plot
        if self.xmax_control.is_auto():
            xmax1 = max(xdata1)
        else:
            xmax1 = float(self.xmax_control.manual_value())

        if self.xmin_control.is_auto():
            xmin1 = min(xdata1)
        else:
            xmin1 = float(self.xmin_control.manual_value())

        # Set Y-axis limits and set data for the first plot
        if self.ymin_control.is_auto():
            ymin1 = min(ydata1) - 0.05*min(ydata1)
        else:
            ymin1 = float(self.ymin_control.manual_value())

        if self.ymax_control.is_auto():
            ymax1 = max(ydata1) + 0.05*max(ydata1)
        else:
            ymax1 = float(self.ymax_control.manual_value())

        # If axis min aquals max add small difference in order to avoid warning message
        if xmin1 == xmax1:
            xmin1 -= 0.001
            xmax1 += 0.001
        if ymin1 == ymax1:
            ymin1 -= 0.001
            ymax1 += 0.001

        # Set axis for the first plot
        self.axis1a.set_xbound(lower=xmin1, upper=xmax1)
        self.axis1a.set_ybound(lower=ymin1, upper=ymax1)

        # Set data to plot in window 1
        self.plot1a.set_xdata(xdata1_a)
        self.plot1a.set_ydata(ydata1_a)
        self.plot1b.set_xdata(xdata1_b)
        self.plot1b.set_ydata(ydata1_b)
        self.plot1c.set_xdata(xdata1_c)
        self.plot1c.set_ydata(ydata1_c)

        # Set X-axis automatic limits and set data for the second plot
        # NOTE: changing axes ranges only works for the first plot.
        ##
        # Get max values for first plot from series a, b and c
        datatmp = np.array([max(xdata2_a), max(xdata2_b), max(xdata2_c)])
        datatmpmax = np.where(datatmp == max(datatmp))[0][0]
        if datatmpmax == 0:
            xdata2 = xdata2_a
        elif datatmpmax == 1:
            xdata2 = xdata2_b
        else:
            xdata2 = xdata2_c

        datatmp = np.array([max(ydata2_a), max(ydata2_b), max(ydata2_c)])
        datatmpmax = np.where(datatmp == max(datatmp))[0][0]
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

        # If axis min aquals max add small difference in order to avoid warning message
        if xmin2 == xmax2:
            xmin2 -= 0.001
            xmax2 += 0.001
        if ymin2 == ymax2:
            ymin2 -= 0.001
            ymax2 += 0.001

        # Set axis for the second plot
        self.axis2a.set_xbound(lower=xmin2, upper=xmax2)
        self.axis2a.set_ybound(lower=ymin2, upper=ymax2)

        # Set data to plot in window 2
        self.plot2a.set_xdata(xdata2_a)  # COMENTAMOS PARA QUE NO
        self.plot2a.set_ydata(ydata2_a)  # SE MUESTREN ESTAS GRAFICAS
        self.plot2b.set_xdata(xdata2_b)  # EN LA SEGUNDA GRAFICA
        self.plot2b.set_ydata(ydata2_b)
        self.plot2c.set_xdata(xdata2_c)
        self.plot2c.set_ydata(ydata2_c)

        self.canvas.draw()

    def draw_plot_4s(self, xdata1_a, ydata1_a, xdata2_a, ydata2_a, xdata1_b, ydata1_b, xdata2_b, ydata2_b,
                     xdata1_c, ydata1_c, xdata2_c, ydata2_c, xdata1_d, ydata1_d, xdata2_d, ydata2_d):
        """ Redraws the plot
        """

        # Get max values for first plot from series a, b, c, d, e, f
        datatmp = np.array([max(xdata1_a), max(xdata1_b),
                            max(xdata1_c), max(xdata1_d)])
        datatmpmax = np.where(datatmp == max(datatmp))[0][0]
        if datatmpmax == 0:
            xdata1 = xdata1_a
        elif datatmpmax == 1:
            xdata1 = xdata1_b
        elif datatmpmax == 2:
            xdata1 = xdata1_c
        else:
            xdata1 = xdata1_d

        datatmp = np.array([max(ydata1_a), max(ydata1_b),
                            max(ydata1_c), max(ydata1_d)])
        datatmpmax = np.where(datatmp == max(datatmp))[0][0]
        if datatmpmax == 0:
            ydata1 = ydata1_a
        elif datatmpmax == 1:
            ydata1 = ydata1_b
        elif datatmpmax == 2:
            ydata1 = ydata1_c
        else:
            ydata1 = ydata1_d

        # Set X-axis limits and set data for the first plot
        if self.xmax_control.is_auto():
            xmax1 = max(xdata1)
        else:
            xmax1 = float(self.xmax_control.manual_value())

        if self.xmin_control.is_auto():
            xmin1 = min(xdata1)
        else:
            xmin1 = float(self.xmin_control.manual_value())

        # Set Y-axis limits and set data for the first plot
        if self.ymin_control.is_auto():
            ymin1 = min(ydata1) - 0.05*min(ydata1)
        else:
            ymin1 = float(self.ymin_control.manual_value())

        if self.ymax_control.is_auto():
            ymax1 = max(ydata1) + 0.05*max(ydata1)
        else:
            ymax1 = float(self.ymax_control.manual_value())

        # If axis min aquals max add small difference in order to avoid warning message
        if xmin1 == xmax1:
            xmin1 -= 0.001
            xmax1 += 0.001
        if ymin1 == ymax1:
            ymin1 -= 0.001
            ymax1 += 0.001

        # Set axis for the first plot
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

        # Get max values for the second plot from series a, b, c and d
        datatmp = np.array([max(xdata2_a), max(xdata2_b),
                            max(xdata2_c), max(xdata2_d)])
        datatmpmax = np.where(datatmp == max(datatmp))[0][0]
        if datatmpmax == 0:
            xdata2 = xdata2_a
        elif datatmpmax == 1:
            xdata2 = xdata2_b
        elif datatmpmax == 2:
            xdata2 = xdata2_c
        else:
            xdata2 = xdata2_d

        # Get max values just for the two ratios (O/Ar y Ti/Ar), because we only
        # want to monitorate those intensities
        datatmp = np.array([max(ydata2_a), max(ydata2_b),
                            max(ydata2_c), max(ydata2_d)])
        datatmpmax = np.where(datatmp == max(datatmp))[0][0]
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
        # Set X and Y-axis automatic limits and set data for the second plot
        ##
        xmax2 = max(xdata2)
        xmin2 = min(xdata2)

        # Set Y-axis limits and set data for the second plot
        if self.ymin_control2.is_auto():
            ymin2 = min(ydata2) - 0.05*min(ydata2)
        else:
            ymin2 = float(self.ymin_control2.manual_value())

        if self.ymax_control2.is_auto():
            ymax2 = max(ydata2) + 0.05*max(ydata2)
        else:
            ymax2 = float(self.ymax_control2.manual_value())

        # If axis min aquals max add small difference in order to avoid warning message
        if xmin2 == xmax2:
            xmin2 -= 0.001
            xmax2 += 0.001
        if ymin2 == ymax2:
            ymin2 -= 0.001
            ymax2 += 0.001

        # Set axis for the second plot
        self.axis2a.set_xbound(lower=xmin2, upper=xmax2)
        self.axis2a.set_ybound(lower=ymin2, upper=ymax2)

        # Set data to plot in window 2
        self.plot2a.set_xdata(xdata2_a)  # COMENTAMOS PARA QUE NO
        self.plot2a.set_ydata(ydata2_a)  # SE MUESTREN ESTAS GRAFICAS
        self.plot2b.set_xdata(xdata2_b)  # EN LA SEGUNDA GRAFICA
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
