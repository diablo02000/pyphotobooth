#!/usr/bin/env python
# -*- coding: utf-8 -*-
from threading import Thread
from picamera import PiCamera
from io import BytesIO
from PIL import ImageTk
import PIL.Image

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

    def __init__(self, width, height, labels_text, log4py):
        """
            Create main window with main settings.
            :param width: Window width.
            :param height: Window height.
            :param labels_text: language data set.
            :param log4py: log4py handler.
            :type width: Int
            :type height: Int
            :type labels_text: Configuration
            :type log4py: log4py
        """
        # Get logger
        self.log4py = log4py

        # Create main window
        self.window = Tk()

        # Set screen position.
        self.window.wm_geometry('%dx%d+%d+%d' % self._define_window_position(width, height))

        # Close window event.
        self.window.wm_protocol("WM_DELETE_WINDOW", self.window.quit)

        # Define window title
        self.window.wm_title(labels_text['title'])

        # Append Widget on window
        self.panel_video_stream = None
        self._set_widgets(labels_text)

        # Start camera handler.
        self._start_cam_handler()

    def _define_window_position(self, width, height):
        """
          Define Window position base on window and screen size.
          :param width: Window width.
          :param height: Window height.
          :type width: Int
          :type height: Int
          :rtype: Tuple
        """
        self.log4py.debug("Define Window position on the screen.")

        # define coordonate
        x = (self.window.winfo_screenwidth()/2) - (width/2)
        y = (self.window.winfo_screenheight()/2) - (height/2)

        return width, height, x, y

    def _set_widgets(self, labels_set):
        """
            Add Widgets to main window
        """
        self.log4py.debug("Add Video panel and button on main window.")

        # Add Video Frame
        self.panel_video_stream = Label(self.window)
        self.panel_video_stream.pack(side="top", fill="both", padx=10, pady=10)

        # Add Snapshot button
        btn_take_picture = Button(self.window, text=labels_set["buttons"]["take_pictures"])
        btn_take_picture.pack(side="bottom", fill="both", padx=10, pady=10)

    def _start_cam_handler(self):
        """
          Create Thread to video loop.
        """
        self.log4py.debug("Start thread camera handler.")

        cam_thread = Thread(target=self._video_loop)
        cam_thread.start()

    def _video_loop(self):
        """
          Run video in loop
        """
        self.log4py.debug("Create camera video loop.")

        # Create Picamera Object
        _cam = PiCamera()

        # Define Camera settings
        _cam.exposure_mode = 'auto'
        _cam.rotation = 270
        _cam.hflip = False
        _cam.vflip = False
        _cam.crop = (0.0, 0.0, 1.0, 1.0)
        _cam.resolution = (400, 300)

        while True:
            stream = BytesIO()
            _cam.capture(stream, format='jpeg')
            stream.seek(0)
            tmpImage = PIL.Image.open(stream)
            tmpImg = ImageTk.PhotoImage(tmpImage)
            self.panel_video_stream.configure(image = tmpImg)

    def run(self):
        """
            Start Gui apps.
        """
        self.log4py.debug("Start main loop.")
        self.window.mainloop()
