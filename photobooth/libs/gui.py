#!/usr/bin/env python
# -*- coding: utf-8 -*-
from picamera import PiCamera
from picamera.array import PiRGBArray
from PIL import ImageTk
import PIL.Image
import cv2
import numpy
import threading

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

        # Create Video Stream panel
        self.panel_video_stream = None
        self._set_widgets(labels_text)

        # Init cam and video Flux.
        self.cam = PiCamera()
        self.raw_capture = PiRGBArray(self.cam)

        # Start camera handler.
        self._start_cam_handler()

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
            :param labels_set: language data set.
            :type labels_set: Configuration
        """
        self.log4py.info("Create photobooth window.")

        # Add Label for Video stream in main window
        self.panel_video_stream = Label(self.window)
        self.panel_video_stream.pack(side="top", fill="both", padx=10, pady=10)

        # Add Snapshot button
        btn_take_picture = Button(self.window, text=labels_set["buttons"]["take_pictures"], command=self._take_picture)
        btn_take_picture.pack(side="bottom", fill="both", padx=10, pady=10)

    def _video_loop(self):
        """
          Run video in loop
        """
        self.log4py.info("Start video loop..")

        # Define Camera settings
        self.cam.sharpness = 0
        self.cam.contrast = 0
        self.cam.brightness = 50
        self.cam.saturation = 0
        self.cam.ISO = 0
        self.cam.video_stabilization = False
        self.cam.exposure_compensation = 0
        self.cam.meter_mode = 'average'
        self.cam.awb_mode = 'auto'
        self.cam.image_effect = 'none'
        self.cam.color_effects = None
        self.cam.exposure_mode = 'auto'
        self.cam.rotation = 270
        self.cam.hflip = False
        self.cam.vflip = False
        self.cam.crop = (0.0, 0.0, 1.0, 1.0)

        # Define cam resolution
        _cam_width = (self.window.winfo_width() - 20)
        _cam_height = (self.window.winfo_height() - self.panel_video_stream.winfo_height() - 40)
        self.cam.resolution = (_cam_width, _cam_height)

        # Run capture loop.
        self.log4py.debug("run capture loop.")

        while self.stop_thread_event.is_set():
            for frame in self.cam.capture_continuous(self.raw_capture, format='jpeg', use_video_port=True):
                # Get image array and display
                img = frame.array
                img = PIL.Image.fromarray(img)
                img = ImageTk.PhotoImage(img)
                self.panel_video_stream.configure(image=img)

        self.log4py.info("Stop video loop.")

    def _start_cam_handler(self):
        """
          Create Thread to video loop.
        """
        self.log4py.debug("Start thread camera handler.")

        cam_thread = threading.Thread(target=self._video_loop)
        cam_thread.start()

    def _take_picture(self):
        """
            Take picture from video flux.
        """
        self.log4py.debug("Take picture.")
        self.cam.capture(self.raw_capture, format="bgr", resize=(1920, 1080))

        # Construct a numpy array from the stream
        data = numpy.fromstring(self.raw_capture.getvalue(), dtype=numpy.uint8)
        # "Decode" the image from the array, preserving colour
        image = cv2.imdecode(data, 1)
        cv2.imshow("Faces", image)

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

        self.log4py.debug("Close camera.")
        self.cam.stop_preview()

        # Close Video loop Thread
        self.log4py.debug("Stop Video loop thread.")
        self.stop_thread_event.set()

        # Close Window
        self.log4py.debug("Close window.")
        self.window.quit()
