#!/usr/bin/env python
# -*- coding: utf-8 -*-
from imutils.video import VideoStream
from io import BytesIO
from PIL import ImageTk
import PIL.Image
import threading
import cv2

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

        # Define stop event for video loop threading
        self.stop_thread_event = threading.Event()

        # Create main window
        self.window = Tk()

        # Start camera handler.
        self._start_cam_handler()

        # Append Widget on window
        self.panel_video_stream = None
        self._set_widgets(labels_text)

        # Define window title
        self.window.wm_title(labels_text['title'])

        # Set screen position.
        self.window.wm_geometry('%dx%d+%d+%d' % self._define_window_position(width, height))

        # Close window event.
        self.window.wm_protocol("WM_DELETE_WINDOW", self._on_close())

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

    def _video_loop(self):
        """
          Run video in loop
        """
        self.log4py.debug("Run video loop..")

        # Create VideoStream Flux
        _video_stream = VideoStream(usePiCamera=args["picamera"] > 0).start()

        # Define cam resolution
        #_cam_width = (self.window.winfo_width() - 20)
        #_cam_height = (self.window.winfo_height() - self.panel_video_stream.winfo_height() - 40)
        #_cam.resolution = (_cam_width, _cam_height)

        # Run until stop thread event is set.
        while self.stop_thread_event.is_set():
            # Get Video Frame and resize it
            _video_fram = _video_stream.read()
            _video_fram = imutils.resize(_video_fram, width=(self.window.winfo_width() - 20))

            # Get Image
            image = cv2.cvtColor(_video_fram, cv2.COLOR_BGR2RGB)
            image = PIL.Image.fromarray(image)
            image = ImageTk.PhotoImage(image)

            #stream = BytesIO()
            #_cam.capture(stream, format='jpeg')
            #stream.seek(0)
            #tmpImage = PIL.Image.open(stream)
            #tmpImg = ImageTk.PhotoImage(tmpImage)
            self.panel_video_stream.configure(image=image)
            self.panel_video_stream.image = image

    def _start_cam_handler(self):
        """
          Create Thread to video loop.
        """
        self.log4py.debug("Start thread camera handler.")

        cam_thread = threading.Thread(target=self._video_loop)
        cam_thread.start()

    def run(self):
        """
            Start Gui apps.
        """
        self.log4py.debug("Start main loop.")
        self.window.mainloop()

    def _on_close(self):
        """
          Close photobooth apps
        """
        self.log4py.info("Stop photoobooth apps.")

        # Close Video loop Thread
        self.log4py.debug("Stop Video loop thread.")
        self.stop_thread_event.set()

        # Close Window
        self.log4py.debug("Close window.")
        self.window.quit()
