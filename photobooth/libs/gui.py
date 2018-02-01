import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from picamera import PiCamera
import time


class Gui(Gtk.Window):

    def __init__(self, title, width, height, labels_dictionary):
        """
        Init Gui with title, width and height.
        :param title: Gui title.
        :param width: Gui width in pixel.
        :param height: Gui height in pixel.
        :param labels_dictionary: Labels text in specific language.
        :type title: String.
        :type width: Integer.
        :type height: Integer.
        :type labels_dictionary: Dictionary.
        """
        # Define labels text dictionary.
        self.labels_dictionary = labels_dictionary

        # Create GTK Window
        Gtk.Window.__init__(self, title=title)
        self.set_size_request(width, height)
        self.connect('delete-event', Gtk.main_quit)
        self.set_border_width(10)
        self.set_icon_from_file("./img/photobooth.png")

        # Add widgets
        self.__set_pane()

    def _set_camera(self):
        """
        Init Camera module
        :return:
        """
        camera = PiCamera()
        camera.resolution = (800, 480)
        camera.hflip = True
        camera.start_preview(alpha=128)

    def __set_pane(self):
        """
        Set all elements for photobooth Gui.
        """
        # Create main pane.
        box_main_pane = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box_main_pane.set_homogeneous(False)

        # Create take picture button
        button_take_picture = Gtk.Button(label=self.labels_dictionary['buttons']['take_pictures'])
        button_take_picture.connect("clicked", self.take_picture)
        box_main_pane.pack_end(button_take_picture, False, False, 10)

        # Attach layout to window
        self.add(box_main_pane)

    def take_picture(self, widget, waiting_time=5):
        for i in range(waiting_time):
            print("wait {} secondes.".format(1))
            time.sleep(1)

        print("Take picture !!")

    def run(self):
        """
        Start GTK gui.
        """
        # Enable widget
        self.show_all()

        # Run GTK loop
        Gtk.main()