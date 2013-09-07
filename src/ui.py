#!/usr/bin/env python
# -*- coding: CP1252 -*-
#
# generated by wxGlade 0.6.8 (standalone edition) on Sat Sep 07 18:32:03 2013
#

import wx

# begin wxGlade: dependencies
import gettext
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class Root(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: Root.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.notebook = wx.Notebook(self, wx.ID_ANY, style=0)
        self.notebook_devices = wx.Panel(self.notebook, wx.ID_ANY)
        self.list_box_input = wx.ListBox(self.notebook_devices, wx.ID_ANY, choices=[])
        self.sizer_5_staticbox = wx.StaticBox(self.notebook_devices, wx.ID_ANY, _("Input"))
        self.list_box_output = wx.ListBox(self.notebook_devices, wx.ID_ANY, choices=[], style=wx.LB_SINGLE)
        self.sizer_6_staticbox = wx.StaticBox(self.notebook_devices, wx.ID_ANY, _("Output"))
        self.button_connect = wx.Button(self.notebook_devices, wx.ID_ANY, _("Connect"))
        self.button_2 = wx.Button(self.notebook_devices, wx.ID_ANY, _("Refresh"))
        self.button_1 = wx.Button(self.notebook_devices, wx.ID_ANY, _("Disconnect"))
        self.notebook_rules = wx.Panel(self.notebook, wx.ID_ANY)
        self.label_2 = wx.StaticText(self.notebook_rules, wx.ID_ANY, _("Type:"))
        self.combo_box_1 = wx.ComboBox(self.notebook_rules, wx.ID_ANY, choices=[_("Scale"), _("Chord"), _("Chord Progression")], style=wx.CB_DROPDOWN)
        self.label_1 = wx.StaticText(self.notebook_rules, wx.ID_ANY, _("Name:"))
        self.text_ctrl_3 = wx.TextCtrl(self.notebook_rules, wx.ID_ANY, "")
        self.label_3 = wx.StaticText(self.notebook_rules, wx.ID_ANY, _("New Rule:"))
        self.text_ctrl_2 = wx.TextCtrl(self.notebook_rules, wx.ID_ANY, "", style=wx.TE_MULTILINE)
        self.label_4 = wx.StaticText(self.notebook_rules, wx.ID_ANY, _("Rules:"))
        self.list_box_1 = wx.ListBox(self.notebook_rules, wx.ID_ANY, choices=[])
        self.notebook_play = wx.Panel(self.notebook, wx.ID_ANY)
        self.label_program = wx.StaticText(self.notebook_play, wx.ID_ANY, _("Program:"))
        self.combo_box_2 = wx.ComboBox(self.notebook_play, wx.ID_ANY, choices=[_("Scales"), _("Chords"), _("Chord Progressions"), _("Improvise")], style=wx.CB_DROPDOWN)
        self.label_rules = wx.StaticText(self.notebook_play, wx.ID_ANY, _("Rules:"))
        self.list_box_2 = wx.ListBox(self.notebook_play, wx.ID_ANY, choices=[])
        self.label_info = wx.StaticText(self.notebook_play, wx.ID_ANY, _("Info:"))
        self.label_5 = wx.StaticText(self.notebook_play, wx.ID_ANY, "")
        self.button_play = wx.Button(self.notebook_play, wx.ID_ANY, _("Start..."))

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.connect_devices, self.button_connect)
        self.Bind(wx.EVT_BUTTON, self.refresh_devices, self.button_2)
        self.Bind(wx.EVT_BUTTON, self.disconnect_devices, self.button_1)
        self.Bind(wx.EVT_BUTTON, self.start_instrument, self.button_play)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: Root.__set_properties
        self.SetTitle(_("frame_1"))
        self.SetSize((400, 300))
        self.combo_box_1.SetSelection(-1)
        self.text_ctrl_2.SetFocus()
        self.combo_box_2.SetSelection(-1)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: Root.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_8 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_16 = wx.BoxSizer(wx.VERTICAL)
        sizer_9 = wx.BoxSizer(wx.VERTICAL)
        sizer_15 = wx.BoxSizer(wx.VERTICAL)
        sizer_12 = wx.BoxSizer(wx.VERTICAL)
        sizer_10 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_11 = wx.BoxSizer(wx.VERTICAL)
        sizer_13 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_14 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.VERTICAL)
        sizer_7 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_6_staticbox.Lower()
        sizer_6 = wx.StaticBoxSizer(self.sizer_6_staticbox, wx.HORIZONTAL)
        self.sizer_5_staticbox.Lower()
        sizer_5 = wx.StaticBoxSizer(self.sizer_5_staticbox, wx.HORIZONTAL)
        sizer_5.Add(self.list_box_input, 1, wx.EXPAND, 0)
        sizer_4.Add(sizer_5, 2, wx.EXPAND, 0)
        sizer_6.Add(self.list_box_output, 1, wx.EXPAND, 0)
        sizer_4.Add(sizer_6, 2, wx.EXPAND, 0)
        sizer_7.Add(self.button_connect, 1, wx.EXPAND, 0)
        sizer_7.Add(self.button_2, 1, wx.EXPAND, 0)
        sizer_7.Add(self.button_1, 1, wx.EXPAND, 0)
        sizer_4.Add(sizer_7, 1, wx.EXPAND, 0)
        self.notebook_devices.SetSizer(sizer_4)
        sizer_14.Add(self.label_2, 0, 0, 0)
        sizer_14.Add(self.combo_box_1, 1, wx.EXPAND, 0)
        sizer_11.Add(sizer_14, 1, wx.EXPAND, 0)
        sizer_13.Add(self.label_1, 0, wx.EXPAND, 0)
        sizer_13.Add(self.text_ctrl_3, 1, wx.EXPAND, 0)
        sizer_11.Add(sizer_13, 1, wx.EXPAND, 0)
        sizer_11.Add(self.label_3, 0, 0, 0)
        sizer_11.Add(self.text_ctrl_2, 6, wx.EXPAND, 0)
        sizer_2.Add(sizer_11, 2, wx.EXPAND, 0)
        sizer_3.Add(self.label_4, 0, 0, 0)
        sizer_3.Add(self.list_box_1, 1, wx.EXPAND, 0)
        sizer_2.Add(sizer_3, 1, wx.EXPAND, 0)
        self.notebook_rules.SetSizer(sizer_2)
        sizer_10.Add(self.label_program, 0, 0, 0)
        sizer_10.Add(self.combo_box_2, 1, wx.EXPAND, 0)
        sizer_9.Add(sizer_10, 1, wx.EXPAND, 0)
        sizer_12.Add(self.label_rules, 0, 0, 0)
        sizer_12.Add(self.list_box_2, 1, wx.EXPAND, 0)
        sizer_9.Add(sizer_12, 5, wx.EXPAND, 0)
        sizer_15.Add(self.label_info, 0, 0, 0)
        sizer_15.Add(self.label_5, 1, wx.ALL | wx.EXPAND, 0)
        sizer_9.Add(sizer_15, 1, wx.EXPAND, 0)
        sizer_8.Add(sizer_9, 2, wx.EXPAND, 0)
        sizer_16.Add(self.button_play, 1, wx.EXPAND, 0)
        sizer_8.Add(sizer_16, 1, wx.EXPAND, 0)
        self.notebook_play.SetSizer(sizer_8)
        self.notebook.AddPage(self.notebook_devices, _("Devices"))
        self.notebook.AddPage(self.notebook_rules, _("Rules"))
        self.notebook.AddPage(self.notebook_play, _("Play"))
        sizer_1.Add(self.notebook, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade

    def connect_devices(self, event):  # wxGlade: Root.<event_handler>
        print "Event handler 'connect_devices' not implemented!"
        event.Skip()

    def refresh_devices(self, event):  # wxGlade: Root.<event_handler>
        print "Event handler 'refresh_devices' not implemented!"
        event.Skip()

    def disconnect_devices(self, event):  # wxGlade: Root.<event_handler>
        print "Event handler 'disconnect_devices' not implemented!"
        event.Skip()

    def start_instrument(self, event):  # wxGlade: Root.<event_handler>
        print "Event handler 'start_instrument' not implemented!"
        event.Skip()

# end of class Root
if __name__ == "__main__":
    gettext.install("app") # replace with the appropriate catalog name

    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = Root(None, wx.ID_ANY, "")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()