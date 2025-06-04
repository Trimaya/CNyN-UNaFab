# -*- coding: utf-8 -*-
##
# plasmonitor.py
##
# Plot the integral of several spectral lines and the slope described by a
# set of subsequent files
##
# Copyright (c) 2016, Oscar Hernandez Utrera. SAOM-Lab
# All rights reserved.
##
# This program is free software; you can redistribute it and/or  modify it
# under the terms of the GNU General Public License  as  published  by the
# Free Software Foundation; either version 2 of the License,  or  (at your
# option) any later version.
##
# This program is distributed in the hope  that  it  will  be  useful, but
# WITHOUT  ANY   WARRANTY;   without   even   the   implied   warranty  of
# MERCHANTABILITY or  FITNESS  FOR  A  PARTICULAR  PURPOSE.   See  the GNU
# General Public License for more details (to receive a  copy  of  the GNU
# General Public License, write to the Free Software Foundation, Inc., 675
# Mass Ave, Cambridge, MA 02139, USA).
##

# Import Libraries
from plasmonitor.analysis import Slope
from plasmonitor.plot import LivePlot
from plasmonitor.fileselect import InputPanel
from plasmonitor.spectrometers import get_reader_for, Spectrometer
from plasmonitor.spectra import Line, Spectrum

import os
import wx

# Set WXAgg as backend.
import matplotlib

print(matplotlib.get_backend())


class MyFrame(wx.Frame):
    """ Application main frame
    """

    def __init__(self, title, size):
        wx.Frame.__init__(self, None, -1, title=title, size=size)

        self.create_menu()
        self.create_main_panel()
        self.create_material()
        self.create_gas()
       # Initialize variables
        self.material = self.AlItem.Id
        self.gas = self.O2Item.Id
        self.lines = {}
        self.ratios = {}
        self.slope = {}
        self.slopes = {}
        self.intensity = {}
        self.intensities = {}
        self.init_lines()
        self.fcounter = 1
        self.reader = None
        self.xdata = []
        self.input_panel.start = False

        # Define events
        self.Bind(wx.EVT_CLOSE, self.on_exit)

        self.plot_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_plot_timer, self.plot_timer)
        self.plot_timer.Start(100)

    def create_menu(self):
        """ Application menu
        """
        self.menubar = wx.MenuBar()
        menu_file = wx.Menu()
        m_expt = menu_file.Append(-1, "&Save plot\tCtrl-S",
                                  "Save plot to file")
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
        # Creating the materials Items
        self.AlItem = menu_Material.Append(
            wx.NewId(), "Aluminium", kind=wx.ITEM_RADIO)
        self.Bind(wx.EVT_MENU, self.Target, self.AlItem)

        self.TiItem = menu_Material.Append(
            wx.NewId(), "Titanium", kind=wx.ITEM_RADIO)
        self.Bind(wx.EVT_MENU, self.Target, self.TiItem)

        self.SiItem = menu_Material.Append(
            wx.NewId(), "Silicon", kind=wx.ITEM_RADIO)
        self.Bind(wx.EVT_MENU, self.Target, self.SiItem)

        self.menubar.Append(menu_Material, "&Target")
        self.SetMenuBar(self.menubar)

    #Creating the material target to input##
    def Target(self, event):
        self.material = event.Id

    def create_gas(self):
        """ Application Material
        """
        self.MenuBar = wx.MenuBar()
        menu_Material = wx.Menu()
        # Creating the materials Items
        self.O2Item = menu_Material.Append(
            wx.NewId(), "Oxygen", kind=wx.ITEM_RADIO)
        self.Bind(wx.EVT_MENU, self.Reactive_gas, self.O2Item)

        self.N2Item = menu_Material.Append(
            wx.NewId(), "Nitrogen", kind=wx.ITEM_RADIO)
        self.Bind(wx.EVT_MENU, self.Reactive_gas, self.N2Item)

        self.menubar.Append(menu_Material, "&Gas")
        self.SetMenuBar(self.menubar)

        #####Creating the reactive gas input for plotting##
    def Reactive_gas(self, event):
        self.gas = event.Id

    def create_main_panel(self):
        """ Main application layout
        """
        self.panel = wx.Panel(self)

        # Set application layout
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.input_panel = InputPanel(self.panel, -1, self.vbox)
        self.live_plot = LivePlot(self.panel, -1, self.vbox)
        self.panel.SetSizer(self.vbox)
        self.vbox.Fit(self)

    def on_plot_timer(self, event):
        """ Load data and plot
        """
        # Defines when to start and stop ploting data
        if self.input_panel.start:
            # Initialize spectrometer reader
            if self.fcounter == 1:
                dir_input = self.input_panel.dname_txtctrl1.GetValue()
                self.reader = get_reader_for(Spectrometer.AVANTES, dir_input)
                self.init_slopes()

            # Get data to plot
            spectrum = next(self.reader.spectra, None)
            if spectrum:
                self.load_data(spectrum)

                # Set file name in plots title
                self.live_plot.axis1a.set_title(
                    self.reader.current_file, size=10)

                self.xdata.append(self.fcounter)
                self.slopes[('ArI', 25)].append(self.slope[('ArI', 25)].value)
                self.slopes[('ArI', 50)].append(self.slope[('ArI', 50)].value)
                self.intensities['ArI'].append(self.intensity['ArI'])
                self.intensities['OI'].append(self.intensity['OI'])
                self.slopes[(('OI', 'ArI'), 50)].append(
                    self.slope[(('OI', 'ArI'), 50)].value)
                self.intensities['TiI'].append(self.intensity['TiI'])
                self.slopes[(('TiI', 'ArI'), 50)].append(
                    self.slope[(('TiI', 'ArI'), 50)].value)
                self.intensities['Si'].append(self.intensity['Si'])
                self.slopes[(('Si', 'ArI'), 50)].append(
                    self.slope[(('Si', 'ArI'), 50)].value)
                self.intensities['AlI'].append(self.intensity['AlI'])
                self.slopes[(('AlI', 'ArI'), 50)].append(
                    self.slope[(('AlI', 'ArI'), 50)].value)
                self.intensities['N2'].append(self.intensity['N2'])
                self.slopes[(('N2', 'ArI'), 50)].append(
                    self.slope[(('N2', 'ArI'), 50)].value)
                self.fcounter += 1

                if self.material == self.TiItem.Id:
                    material = 'TiI'
                elif self.material == self.AlItem.Id:
                    material = 'AlI'
                elif self.material == self.SiItem.Id:
                    material = 'Si'
                material_slope = ((material, 'ArI'), 50)

                if self.gas == self.O2Item.Id:
                    gas = 'OI'
                elif self.gas == self.N2Item.Id:
                    gas = 'N2'
                gas_slope = ((gas, 'ArI'), 50)

                self.live_plot \
                    .draw_plot_4s(self.xdata, self.slopes[('ArI', 25)],
                                  self.xdata, self.intensities['ArI'],
                                  self.xdata, self.slopes[('ArI', 50)],
                                  self.xdata, self.intensities['ArI'],
                                  self.xdata, self.slopes[gas_slope],
                                  self.xdata, self.intensities[gas],
                                  self.xdata, self.slopes[material_slope],
                                  self.xdata, self.intensities[material])

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

    def init_lines(self):
        """ Lines dictionary
        """
        # TODO: Check the Avantes configuration that was never set
        # Define spectra lines
        self.lines['ArI'] = Line('ArI', 706.6, 1.76)
        self.intensities['ArI'] = []
        self.lines['AlI'] = Line('AlI', 397.26, 2.32)
        self.intensities['AlI'] = []
        self.lines['TiI'] = Line('TiI', 468.196, 1.46)
        self.intensities['TiI'] = []
        self.lines['Si'] = Line('Si', 288.1, 1.46)
        self.intensities['Si'] = []
        self.lines['OI'] = Line('OI', 777.26, 1.46)
        self.intensities['OI'] = []
        self.lines['N2'] = Line('N2', 315.8, 1.46)
        self.intensities['N2'] = []

    def init_slopes(self):
        """ Initialize slope buffers
        """
        self.slope[('ArI', 25)] = Slope(25)
        self.slopes[('ArI', 25)] = []
        self.slope[('ArI', 50)] = Slope(50)
        self.slopes[('ArI', 50)] = []
        self.slope[(('OI', 'ArI'), 50)] = Slope(50)
        self.slopes[(('OI', 'ArI'), 50)] = []
        self.slope[(('TiI', 'ArI'), 50)] = Slope(50)
        self.slopes[(('TiI', 'ArI'), 50)] = []
        self.slope[(('AlI', 'ArI'), 50)] = Slope(50)
        self.slopes[(('AlI', 'ArI'), 50)] = []
        self.slope[(('Si', 'ArI'), 50)] = Slope(50)
        self.slopes[(('Si', 'ArI'), 50)] = []
        self.slope[(('N2', 'ArI'), 50)] = Slope(50)
        self.slopes[(('N2', 'ArI'), 50)] = []

    def load_data(self, spectrum: Spectrum):

        # Get line intesity (compute integral simply by sum of intensities)
        for line in self.lines.values():
            self.intensity[line.name] = sum(
                [(intensity/64000.0) for intensity
                 in spectrum.intensities(line.interval)])

        # Compute ratios
        self.ratios[('OI', 'ArI')] = (self.intensity['OI'] /
                                      self.intensity['ArI'])
        self.ratios[('TiI', 'ArI')] = (self.intensity['TiI'] /
                                       self.intensity['ArI'])
        self.ratios[('AlI', 'ArI')] = (self.intensity['AlI'] /
                                       self.intensity['ArI'])
        self.ratios[('Si', 'ArI')] = (self.intensity['Si'] /
                                      self.intensity['ArI'])
        self.ratios[('N2', 'ArI')] = (self.intensity['N2'] /
                                      self.intensity['ArI'])

        # Compute slopes
        ##
        # Slope from Ar peak integral with 25 files
        self.slope[('ArI', 25)].append(self.fcounter, self.intensity['ArI'])
        # Slope from Ar peak integral with 50 files
        self.slope[('ArI', 50)].append(self.fcounter, self.intensity['ArI'])
        # Slope from OI_Ar ratio with 50 files
        self.slope[(('OI', 'ArI'), 50)].append(
            self.fcounter, self.ratios[('OI', 'ArI')])
        # Slope from NII_Ar ratio with 50 files
        self.slope[(('N2', 'ArI'), 50)].append(
            self.fcounter, self.ratios[('N2', 'ArI')])
        # Slope from Ti_Ar ratio with 50 files
        self.slope[(('TiI', 'ArI'), 50)].append(
            self.fcounter, self.ratios[('TiI', 'ArI')])
        # Slope from Al_Ar ratio with 50 files
        self.slope[(('AlI', 'ArI'), 50)].append(
            self.fcounter, self.ratios[('AlI', 'ArI')])
        # Slope from Si_Ar ratio with 50 files
        self.slope[(('Si', 'ArI'), 50)].append(
            self.fcounter, self.ratios[('Si', 'ArI')])

    def on_exit(self, event):
        self.Destroy()
