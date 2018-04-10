#!/usr/bin/env python
# -*- coding: utf-8 -*-
from picamera import PiCamera
from picamera.array import PiRGBArray
from PIL import ImageTk
import PIL.Image
import cv2
import numpy
import threading
import time
import os
import logging


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

    def __init__(self, width, height, labels_text):
        """
            Create main window with main settings.
            :param width: Window width.
            :param height: Window height.
            :param labels_text: language data set.
            :type width: Int
            :type height: Int
            :type labels_text: Configuration
        """
        # Get logger
        self.logger = logging.getLogger(__name__)

        # Define stop event for video loop threading
        self.stop_thread_event = threading.Event()

        """
            Create Windows and set attributes
        """
        self.logger.debug("Init windows and set screen localisation and title.")
        self.window = Tk()

        # Define window title
        self.window.wm_title(labels_text['title'])

        # define coordonate
        x = (self.window.winfo_screenwidth()/2) - (width/2)
        y = (self.window.winfo_screenheight()/2) - (height/2)

        # Set screen position.
        self.window.wm_geometry('%dx%d+%d+%d' % (width, height, x, y))

        # Close window event.
        self.window.wm_protocol("WM_DELETE_WINDOW", self._on_close())

        """
            Init Picamera and warm up.
        """
        # Init Picamera.
        self.cam = PiCamera()
        self.raw_capture = None

        """
            Append widgets
        """
        self.logger.info("Add widgets to main windows.")

        # Add Snapshot button
        btn_take_picture = Button(self.window, text=labels_text["buttons"]["take_pictures"], command=self._take_picture)
        btn_take_picture.pack(side="bottom", fill="both", padx=10, pady=10)

        # Create Video Stream panel
        self.panel_video_stream = Label(self.window)

        # get windows size
        w, h = self._get_widget_size(self.window)

        # get button size
        bw, bh = self._get_widget_size(btn_take_picture)

        self.panel_video_stream.config(width=(w - 20), height=((h - bh) - 20))
        self.panel_video_stream.pack(side="top", fill="both", padx=10, pady=10)

        # Start camera handler.
        self._start_cam_handler()

    @staticmethod
    def _get_widget_size(widget):
        """
        Return width height of widget
        :param widget: Widget object
        :return: Width and Height
        """
        return widget.winfo_width(), widget.winfo_height()

    def _video_loop(self):
        """
          Run video in loop
        """

        self.logger.debug("Run video loop..")

        # Define Camera settings
        self.cam.sharpness = 0
        self.cam.contrast = 0
        self.cam.framerate = 30
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
        self.raw_capture = PiRGBArray(self.cam)

        # Warm up cam
        time.sleep(0.1)

        # Run capture loop.
        self.logger.debug("run capture loop.")

        for frame in self.cam.capture_continuous(self.raw_capture, format='bgr', use_video_port=True):
            if not self.stop_thread_event.is_set():
                break

            # Get image array and display
            img = frame.array
            img = PIL.Image.fromarray(img)
            img = ImageTk.PhotoImage(img)
            self.panel_video_stream.configure(image=img)
            self.panel_video_stream.image = img
            self.raw_capture.truncate(0)

        self.logger.info("Stop video loop.")

    def _start_cam_handler(self):
        """
          Create Thread to video loop.
        """
        self.logger.debug("Start thread camera handler.")

        cam_thread = threading.Thread(target=self._video_loop)
        cam_thread.start()

    def _take_picture(self):
        """
            Take picture from video flux.
        """
        self.logger.debug("Take picture.")
        self.cam.capture(self.raw_capture, format="rgb", resize=(1280, 720))

        filename = os.path.join("/home/pi/Pictures/", "images-test.jpeg")
        cv2.imwrite(filename, self.raw_capture)

    def run(self):
        """
            Start Gui apps.
        """
        self.logger.debug("Start main loop.")
        self.window.mainloop()

    def _on_close(self):
        """
          Close photobooth apps
        """
        self.logger.info("Stop photoobooth apps.")

        # Close Video loop Thread
        self.logger.debug("Stop Video loop thread.")
        self.stop_thread_event.set()

        # Close Window
        self.logger.debug("Close window.")
        self.window.quit()
