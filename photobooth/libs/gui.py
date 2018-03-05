#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Try to import tkinter module
"""
try:
    # Python 2.7
	from Tkinter import *
except ImportError:
    # Python 3
	from tkinter import *

class Gui:

    def __init__(self, width, height, language_labels_set, videoStream=None):
        """
            Create main window with main settings.
            :param width: Window width.
            :param height: Window height.
            :param language_labels_set: language data set.
            :type width: Int
            :type height: Int
            :type language_labels_set: Configuration
        """
        self.videoStream = videoStream

        # Create main window
        self.window = Tk()

        # Get screen size
        _screen_width = self.window.winfo_screenwidth() # width of the screen
        _screen_height = self.window.winfo_screenheight() # height of the screen

        # define coordonate
        x = (_screen_width/2) - (width/2)
        y = (_screen_height/2) - (height/2)

        self.window.wm_geometry('%dx%d+%d+%d' % (width, height, x, y))
        self.window.wm_protocol("WM_DELETE_WINDOW", self.window.quit)
        self.window.wm_title(language_labels_set['title'])
        self._set_widget(language_labels_set)

    def _set_widget(self, labels_set):
        """
            Add widget to main window
        """
        # Add Video Frame
        frame_video_stream = self.videoStream.read()
        panel_video_stream = Label(image=frame_video_stream)
        panel_video_stream.pack(side="top", fill="both", padx=10, pady=10)

        # Add Snapshot button
        btn_take_picture = Button(self.window, text=labels_set["buttons"]["take_pictures"])
        btn_take_picture.pack(side="bottom", fill="both", padx=10, pady=10)

    def run(self):
        """
            Start Gui apps.
        """
        self.window.mainloop()
