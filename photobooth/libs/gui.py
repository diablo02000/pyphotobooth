import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Gui(Gtk.Window):

    def __init__(self, title, width, height):
        """
        Init Gui with title, width and height.
        :param title: Gui title.
        :param width: Gui width in pixel.
        :param height: Gui height in pixel.
        :type title: String.
        :type width: Integer.
        :type height: Integer.
        """
        Gtk.Window.__init__(self, title=title)
        self.set_size_request(width, height)
        self.connect('delete-event', Gtk.main_quit)

    def __set_pane(self):
        """
        Create Grid layout with 6 px space
        between rows and columns
        """
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(1000)

        checkbutton = Gtk.CheckButton("Click me!")
        stack.add_titled(checkbutton, "check", "Check Button")

        label = Gtk.Label()
        label.set_markup("<big>A fancy label</big>")
        stack.add_titled(label, "label", "A label")

        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)
        vbox.pack_start(stack_switcher, True, True, 0)
        vbox.pack_start(stack, True, True, 0)

        # Attach layout to window
        self.add(vbox)

    def run(self):
        """
        Start GTK gui.
        """
        # Enable widget
        self.show_all()

        # Run GTK loop
        Gtk.main()