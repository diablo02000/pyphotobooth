#!/usr/bin/env python
# -*- coding: utf-8 -*-
from picamera import PiCamera
from picamera.array import PiRGBArray
from PIL import ImageTk
from datetime import datetime
import PIL.Image
import cv2
import threading
import os
import logging
import time


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

        # Init Picamera.
        self.cam = PiCamera()
        self.raw_capture = PiRGBArray(self.cam)
        self.CAMERA_RESOLUTION_MAPS = {'s': (640, 480),
                                       'm': (1296, 730),
                                       'l': (1296, 972),
                                       'xl': (1920, 1080),
                                       'xxl': (2592, 1944)}

        """
            Create Windows and set attributes
        """
        self.logger.info("Create windows apps.")
        self.window = Tk()

        # Define window title
        self.window.wm_title(labels_text['title'])

        # Get screen coordonate to center apps.
        x = (self.window.winfo_screenwidth()/2) - (width/2)
        y = (self.window.winfo_screenheight()/2) - (height/2)

        # Set screen position. (center)
        self.window.wm_geometry('%dx%d+%d+%d' % (width, height, x, y))

        # Close window event.
        self.window.wm_protocol("WM_DELETE_WINDOW", self._on_close())

        """
            Append widgets
        """
        self.logger.info("Add widgets to main windows.")

        # Add Snapshot button
        btn_take_picture = Button(self.window, text=labels_text["buttons"]["take_pictures"], command=self._take_picture)
        btn_take_picture.pack(side="bottom", fill="both", padx=10, pady=10)

        # Create Video Stream panel
        self.panel_video_stream = Label(self.window)

        # get button size
        bw, bh = self._get_widget_size(btn_take_picture)

        self.panel_video_stream.config(width=(width - 20), height=((height - bh) - 20))
        self.panel_video_stream.pack(side="top", fill="both", padx=10, pady=10)

        # Start camera handler.
        self._start_cam_handler()

    @staticmethod
    def _get_widget_size(widget, attr=None):
        """
        Return width height of widget
        :param widget: Widget object
        :param attr: Specific attribut.
        :return: Width and Height
        """
        if attr == "width":
            return widget.winfo_width()
        elif attr == "height":
            return widget.winfo_height()
        else:
            return widget.winfo_width(), widget.winfo_height()

    def _video_loop(self):
        """
          Run video in loop
        """

        self.logger.info("Start video loop.")

        # Define brightness
        # default: 50
        # self.cam.brightness = 50

        # Define contrast
        # self.cam.contrast = 0

        # Define Camera settings
        # self.cam.sharpness = 0

        # Define image effect
        # You can choose between none, negative, solarize, sketch, denoise, emboss, oilpaint, hatch, gpen,
        # pastel, watercolor, film, blur, saturation, coloswap, washedout, posterise, colorpoint, colorbalance, cartoon,
        # deinterlace1 and deinterlace2
        # default: none
        # self.cam.image_effect = 'none'

        # Define white balance
        # You can choose between off, auto, sunlight, cloudy, shade, tungsten, fluorescent, incandescent, flash, horizon
        # default: auto
        # self.cam.awb_mode = 'auto'

        # Define exposure mode
        # You can choose between off, auto, night, nightpreview, blacklight, spotlight, sports, snow, beach, verylong,
        # fixedfps, antishake, fireworks
        # default: auto
        # self.cam.exposure_compensation = 'auto'

        # Define camera framerate
        # default: 30
        # self.cam.framerate = 32

        # Define camera saturation
        # default: 0
        # self.cam.saturation = 0

        # Define sensitivity of the camera light
        # You can define value between 100 and 1600.
        # Lower iso speed imply less sensitivity
        # default: 400
        # self.cam.iso = 800

        # Define expose camera method
        # You can choose between average, spot, backlit, matrix
        # default: average
        # self.cam.meter_mode = 'average'

        # Rotate camera
        self.cam.rotation = 270

        # Set horizontal or vertical flip.
        # default: false
        # self.cam.hflip = False
        # self.cam.vflip = False

        # Set zoom in camera input
        # default: (0.0, 0.0, 1.0, 1.0)
        # self.cam.crop = (0.0, 0.0, 1.0, 1.0)

        """
        Define camera resolution.
        Max resolution is 2592*1944
        default: 1280*720
        """
        _cam_width = (self._get_widget_size(self.window, "width") - 20)
        _cam_height = (self._get_widget_size(self.window, "height") - self._get_widget_size(self.panel_video_stream, "height") - 40)
        # _cam_width, _cam_height = self.CAMERA_RESOLUTION_MAPS['s']
        self.logger.info("Init camera resolution ({},{})".format(_cam_width, _cam_height))
        self.cam.resolution = (_cam_width, _cam_height)
        self.raw_capture = PiRGBArray(self.cam, size=(_cam_width, _cam_height))

        self.logger.debug("Run capture loop.")
        for frame in self.cam.capture_continuous(self.raw_capture, format='rgb', use_video_port=True):

            # If stop event set break capture loop
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

    def _take_picture(self, timer=5):
        """
            Take picture from video flux.
            :param timer: Waiting time in second.
        """
        # Wait please.
        for x in range(timer, 0, -1):
            time.sleep(1)

        self.logger.debug("Take picture.")

        timestamp = datetime.now().strftime('%s')
        img_filename = os.path.join("/home/pi/Pictures/", "picture-{}.jpg".format(timestamp))
        self.cam.capture(img_filename, resize=self.CAMERA_RESOLUTION_MAPS['l'])
        self.logger.info("Picture saved in {}.".format(img_filename))

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

        self.logger.debug("Stop camera.")
        # self.cam.close()
        self.raw_capture.close()

        # Close Video loop Thread
        self.logger.debug("Stop Video loop thread.")
        self.stop_thread_event.set()

        # Close Window
        self.logger.debug("Close window.")
        self.window.quit()
