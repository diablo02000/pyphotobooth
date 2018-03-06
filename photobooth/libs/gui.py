#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import imutils
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

        # Create thread for video loop.
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self._videoLoop, args=())
        self.thread.start()

        # Get screen size
        _screen_width = self.window.winfo_screenwidth() # width of the screen
        _screen_height = self.window.winfo_screenheight() # height of the screen

        # define coordonate
        x = (_screen_width/2) - (width/2)
        y = (_screen_height/2) - (height/2)

        self.panel_video_stream = None
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
        self.panel_video_stream = Label(image=frame_video_stream)
        self.panel_video_stream.pack(side="top", fill="both", padx=10, pady=10)

        # Add Snapshot button
        btn_take_picture = Button(self.window, text=labels_set["buttons"]["take_pictures"])
        btn_take_picture.pack(side="bottom", fill="both", padx=10, pady=10)

    def _videoLoop(self):
        """
            Get Video from picamera.
        """
        try:
            # keep looping over frames until we are instructed to stop
            while not self.stopEvent.is_set():
                # grab the frame from the video stream and resize it to
                # have a maximum width of 300 pixels
                self.frame = self.vs.read()
                self.frame = imutils.resize(self.frame, width=300)

                # OpenCV represents images in BGR order; however PIL
                # represents images in RGB order, so we need to swap
                # the channels, then convert to PIL and ImageTk format
                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)
                # if the panel is not None, we need to initialize it
                if self.panel_video_stream is None:
                    self.panel_video_stream = tki.Label(image=image)
                    self.panel_video_stream.image = image
                    self.panel_video_stream.pack(side="left", padx=10, pady=10)
                    # otherwise, simply update the panel
                else:
                    self.panel_video_stream.configure(image=image)
                    self.panel_video_stream.image = image
        except RuntimeError as e:
            print("[INFO] caught a RuntimeError")

    def run(self):
        """
            Start Gui apps.
        """
        self.window.mainloop()
