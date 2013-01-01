import gtk
import gtk.glade
import os
import sys

class ClientConf(object):

    def __init__(self):
        self.get_widgets()
        self.connections()

    def get_widgets(self):
        xml = gtk.glade.XML(os.path.join("glade", "clientconf.glade"), 'clientconf')
        self.conf_window = xml.get_widget("clientconf")
        self.nametxt = xml.get_widget("nametxt")
        self.colorcmb = xml.get_widget("colorcmb")
        self.servertxt = xml.get_widget("servertxt")
        self.servertxt.set_text("127.0.0.1")
        self.porttxt = xml.get_widget("porttxt")
        self.porttxt.set_text("5678")
        self.closebtn = xml.get_widget("closebtn")
        self.startbtn = xml.get_widget("startbtn")

    def connections(self):
        self.conf_window.connect("delete_event", self.on_close_clicked)
        self.closebtn.connect("clicked", self.on_close_clicked)
        self.startbtn.connect("clicked", self.on_start_clicked)

    def show(self):
        self.conf_window.show_all()

    def on_close_clicked(self, *args):
        gtk.main_quit()

    def on_start_clicked(self, *args):
        pass

if __name__ == '__main__':
    client_conf = ClientConf()
    client_conf.show()
    gtk.main()
