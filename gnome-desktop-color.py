import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gio, Gtk, Gdk  # NOQA


class Handler:
    SETTINGS_BASE = "org.gnome.desktop.background"
    BLACK = "rgb(0, 0, 0)"

    def __init__(self):
        self.settings = Gio.Settings.new(self.SETTINGS_BASE)
        self.shading = 0  # 0 = solid

        self.combo_shading = builder.get_object("combo_color_shading_type")
        self.button_primary = builder.get_object("button_color_primary")
        self.button_secondary = builder.get_object("button_color_secondary")

        color_value_primary = self.settings.get_string("primary-color")
        color_value_secondary = self.settings.get_string("secondary-color")

        # Setup initial colors
        self.color_primary = Gdk.RGBA()
        if color_value_primary:
            valid = self.color_primary.parse(color_value_primary)
            if not valid:
                self.color_primary.parse(self.BLACK)
        else:
            self.color_secondary.parse(self.BLACK)

        self.color_secondary = Gdk.RGBA()
        if color_value_secondary:
            valid = self.color_secondary.parse(color_value_secondary)
            if not valid:
                self.color_secondary.parse(self.BLACK)
        else:
            self.color_secondary.parse(self.BLACK)

        # Setup shading
        if self.settings.get_enum("color-shading-type"):
            self.shading = self.settings.get_enum("color-shading-type")

        # Setup widget values
        self.combo_shading.set_active(self.shading)
        self.button_primary.set_rgba(self.color_primary)
        self.button_secondary.set_rgba(self.color_secondary)

        if self.shading > 0:
            self.button_secondary.set_property("sensitive", True)

    def on_combo_color_shading_type_changed(self, combo):
        self.shading = combo.get_active()

        if self.shading > 0:
            self.button_secondary.set_property("sensitive", True)
        else:
            self.button_secondary.set_property("sensitive", False)

        print(f"Changed shading type: {combo.get_active()}")

    def on_button_color_primary_color_set(self, button):
        self.color_primary = button.get_rgba()
        print(f"Changed primary color: {self.color_primary}")

    def on_button_color_secondary_color_set(self, button):
        self.color_secondary = button.get_rgba()
        print(f"Changed secondary color: {self.color_secondary}")

    def on_window_main_destroy(self, *args):
        Gtk.main_quit()

    def on_button_apply_clicked(self, *args):
        if self.settings.get_string("picture-uri"):
            self.settings.set_string("picture-uri", "")

        self.settings.set_string("primary-color", self.color_primary.to_string())
        self.settings.set_string("secondary-color", self.color_secondary.to_string())
        self.settings.set_enum("color-shading-type", self.shading)


builder = Gtk.Builder()
builder.add_from_file("gnome-desktop-color.glade")
builder.connect_signals(Handler())

window = builder.get_object("window_main")
window.set_title("Gnome desktop color picker")
window.show_all()

Gtk.main()
