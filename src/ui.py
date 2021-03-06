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

import midi
from pygame import Color
import pygame.midi

FAVICON_PATH = '../img/favicon.ico'

class KeyboardDisplay(wx.Window):
    def __init__(self, parent, ID, input_id, output_id,
            instrument_id = 0, start_note = 60, n_notes = 24):
        wx.Window.__init__(self, parent, ID)
        self.parent = parent
        self.hwnd = self.GetHandle()
        
        self.start_note = start_note
        self.n_notes = n_notes
        keys = [wx.WXK_TAB]
        keys += [ord(i) for i in ['1', 'Q', '2', 'W', 'E', '4', 'R', '5', 'T',
            '6', 'Y', 'U', '8', 'I', '9', 'O', 'P', '-', '[', '+', ']']]
        keys += [wx.WXK_BACK, ord('\\')]
        self.key_mapping = midi.make_key_mapping(keys, start_note)
        
        pygame.midi.init()
        if input_id:
            self.input_device = pygame.midi.Input(input_id)
        else:
            self.input_device = None

        self.output_device = pygame.midi.Output(output_id)
        self.output_device.set_instrument(instrument_id)
        self.keyboard = midi.Keyboard(start_note, n_notes)
        
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_click)
        self.Bind(wx.EVT_LEFT_UP, self.off_click)
        self.Bind(wx.EVT_KEY_DOWN, self.on_key)
        self.Bind(wx.EVT_KEY_UP, self.off_key)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        
        self.fps = 60.0
        self.timespacing = 1000.0 / self.fps
        self.timer.Start(self.timespacing, False)

        self.size = self.keyboard.rect.size
        self.screen = pygame.Surface(self.size)
        self.background = pygame.Surface(self.screen.get_size(), 0, 32)
        bg_color = Color('slategray')
        self.background.fill(bg_color)

        self.regions = pygame.Surface(self.screen.get_size())
        self.keyboard.map_regions(self.regions)

        self.mouse_note = None
        self.on_notes = set()
        
        self.redraw()
    
    def update(self, event):
        update_keyboard = False
        if self.input_device and self.input_device.poll():
            midi_events = self.input_device.read(10)
            for m_e in midi_events:
                [[status, note, velocity, _data3], _timestamp] = m_e
                if event.status == 144: # pressed note
                    if note not in self.on_notes:
                        self.output_device.note_on(note, velocity)
                        self.on_notes.add(note)
                        if self.start_note <= note < self.start_note + self.n_notes:
                            keyboard.key_down(note)
                            update_keyboard = True
                elif event.status == 128: # released note
                    if note not in self.on_notes and note != self.mouse_note:
                        self.output_device.not_off(note)
                        self.on_notes.remove(note)
                        if self.start_note <= note < self.start_note + self.n_notes:
                            keyboard.key_up(note)
                            update_keyboard = True
                
        if update_keyboard:
            self.redraw()
            
        event.Skip()
        
    def on_click(self, event):
        try:
            self.mouse_note, velocity, _, _  = self.regions.get_at(event.GetPositionTuple())
            if self.mouse_note and self.mouse_note not in self.on_notes:
                self.keyboard.key_down(self.mouse_note)
                self.output_device.note_on(self.mouse_note, velocity)
                self.on_notes.add(self.mouse_note)
                self.redraw()
        except IndexError:
            pass

        event.Skip()
        
    def off_click(self, event):
        if self.mouse_note:
            self.keyboard.key_up(self.mouse_note)
            self.output_device.note_off(self.mouse_note)
            self.on_notes.remove(self.mouse_note)
            self.mouse_note = None
            self.redraw()
            
        event.Skip()
        
    def on_key(self, event):
        try:
            note, velocity = self.key_mapping[event.GetKeyCode()]
        except KeyError:
            pass
        else:
            if note not in self.on_notes:
                self.keyboard.key_down(note)
                self.output_device.note_on(note, velocity)
                self.on_notes.add(note)
                self.redraw()
                
        event.Skip()
        
    def off_key(self, event):
        try:
            note, velocity = self.key_mapping[event.GetKeyCode()]
        except KeyError:
            pass
        else:
            if note in self.on_notes and note != self.mouse_note:
                self.keyboard.key_up(note)
                self.output_device.note_off(note)
                self.on_notes.remove(note)
                self.redraw()
                
        event.Skip()
        
    def redraw(self):
        self.keyboard.draw(self.screen, self.background, [])
        s = pygame.image.tostring(self.screen, 'RGB')
        img = wx.ImageFromData(self.size[0], self.size[1], s)
        bmp = wx.BitmapFromImage(img)
        dc = wx.ClientDC(self)
        dc.DrawBitmap(bmp, 0, 0, False)
        del dc

    def on_paint(self, event):
        self.redraw()
        event.Skip()
        
    def kill(self):
        # Make sure Pygame can't be asked to redraw /before/ quitting by unbinding all methods which
        # call the Redraw() method
        # (Otherwise wx seems to call Draw between quitting Pygame and destroying the frame)
        # This may or may not be necessary now that Pygame is just drawing to surfaces
        self.Unbind(event = wx.EVT_TIMER, handler = self.update, 
            source = self.timer)
        self.Unbind(event = wx.EVT_LEFT_DOWN, handler = self.on_click)
        self.Unbind(event = wx.EVT_LEFT_UP, handler = self.off_click)
        self.Unbind(event = wx.EVT_KEY_DOWN, handler = self.on_key)
        self.Unbind(event = wx.EVT_KEY_UP, handler = self.off_key)
        self.Unbind(event = wx.EVT_PAINT, handler = self.on_paint)
        # ensure midi is properly shut down
        del self.input_device
        del self.output_device
        pygame.midi.quit()
        self.Destroy()

class Instrument(wx.Frame):
    def __init__(self, parent, input_id, output_id, *args, **kwds):
        # begin wxGlade: Instrument.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, parent, -1, *args, **kwds)
        self.display = KeyboardDisplay(self, wx.ID_ANY, input_id, output_id)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade
        
        self.Bind(wx.EVT_CLOSE, self.kill)

    def __set_properties(self):
        # begin wxGlade: Instrument.__set_properties
        self.SetTitle(_("Instrument"))
        # end wxGlade
        self.SetSize(self.display.size)
        favicon = wx.Icon(FAVICON_PATH, wx.BITMAP_TYPE_ICO, 32, 32)
        self.SetIcon(favicon)

    def __do_layout(self):
        # begin wxGlade: Instrument.__do_layout
        sizer_17 = wx.BoxSizer(wx.VERTICAL)
        sizer_17.Add(self.display, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_17)
        sizer_17.Fit(self)
        self.Layout()
        # end wxGlade
        
    def kill(self, event):
        self.display.kill()
        self.Destroy()
    
# end of class Instrument
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
        self.button_refresh = wx.Button(self.notebook_devices, wx.ID_ANY, _("Refresh"))
        self.button_disconnect = wx.Button(self.notebook_devices, wx.ID_ANY, _("Disconnect"))
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

        self.Bind(wx.EVT_LISTBOX, self.select_input_id, self.list_box_input)
        self.Bind(wx.EVT_LISTBOX, self.select_output_id, self.list_box_output)
        self.Bind(wx.EVT_BUTTON, self.connect_devices, self.button_connect)
        self.Bind(wx.EVT_BUTTON, self.refresh_devices, self.button_refresh)
        self.Bind(wx.EVT_BUTTON, self.disconnect_devices, self.button_disconnect)
        self.Bind(wx.EVT_BUTTON, self.start_instrument, self.button_play)
        # end wxGlade
        
        self.input_id = None
        self.output_id = None

    def __set_properties(self):
        # begin wxGlade: Root.__set_properties
        self.SetTitle(_("Music Tutor"))
        self.SetSize((400, 300))
        self.button_connect.Enable(False)
        self.button_disconnect.Enable(False)
        self.combo_box_1.SetSelection(-1)
        self.text_ctrl_2.SetFocus()
        self.combo_box_2.SetSelection(-1)
        # end wxGlade
        favicon = wx.Icon(FAVICON_PATH, wx.BITMAP_TYPE_ICO, 32, 32)
        self.SetIcon(favicon)
        self.update_devices()

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
        sizer_7.Add(self.button_refresh, 1, wx.EXPAND, 0)
        sizer_7.Add(self.button_disconnect, 1, wx.EXPAND, 0)
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
        self.instrument = Instrument(self, self.input_id, self.output_id)
        #self.Bind(wx.EVT_CLOSE, self.disconnect_devices, self.instrument.kill)
        self.instrument.Bind(wx.EVT_CLOSE, self.disconnect_devices)
        self.instrument.Show()
        self.Layout()
        self.button_disconnect.Enable(True)
        self.button_connect.Enable(False)
        event.Skip()
        
    def refresh_devices(self, event):  # wxGlade: Root.<event_handler>
        self.update_devices()
        event.Skip()

    def disconnect_devices(self, event):  # wxGlade: Root.<event_handler>
        self.instrument.kill(event)
        self.button_connect.Enable(True)
        self.button_disconnect.Enable(False)

    def start_instrument(self, event):  # wxGlade: Root.<event_handler>
        print "Event handler 'start_instrument' not implemented!"
        event.Skip()
        
    def update_devices(self):
        input_devices, output_devices = midi.get_devices(True)
        self.list_box_input.Clear()
        self.list_box_input.AppendItems(input_devices)
        self.list_box_output.Clear()
        self.list_box_output.AppendItems(output_devices)

    def select_input_id(self, event):  # wxGlade: Root.<event_handler>
        device = self.list_box_input.GetStringSelection()
        self.input_id = int(device.split()[0])
        event.Skip()
    
    def select_output_id(self, event):  # wxGlade: Root.<event_handler>
        device = self.list_box_output.GetStringSelection()
        self.output_id = int(device.split()[0])
        self.button_connect.Enable(True)
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