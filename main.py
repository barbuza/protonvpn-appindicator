#!/usr/bin/env python3

import os
import signal
import subprocess

import gi

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import GLib
from gi.repository import Gtk
from gi.repository import AppIndicator3

INDICATOR_ID = 'proton-applet'

connect_item = None

def main():
    indicator = AppIndicator3.Indicator.new(INDICATOR_ID, '', AppIndicator3.IndicatorCategory.SYSTEM_SERVICES)

    indicator.set_icon(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'inactive.png'))
    indicator.set_attention_icon(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'active.png'))

    indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())

    def check_status():
        global connect_item
        try:
            subprocess.check_call(['pgrep', 'openvpn'], stdout=subprocess.PIPE)
            indicator.set_status(AppIndicator3.IndicatorStatus.ATTENTION)
            connect_item.set_label('Disconnect')
        except:
            indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
            connect_item.set_label('Connect')

        GLib.timeout_add(1000, check_status)

    GLib.timeout_add(1000, check_status)
    Gtk.main()

def build_menu():
    global connect_item
    menu = Gtk.Menu()

    connect_item = Gtk.MenuItem('Connect')
    connect_item.connect('activate', connect)
    menu.append(connect_item)

    item_quit = Gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)

    menu.show_all()
    
    return menu

def connect(source):
    try:
        subprocess.check_call(['pgrep', 'openvpn'], stdout=subprocess.PIPE)
        active = True
    except:
        active = False
    subprocess.check_call(['sudo', 'protonvpn-cli', '-d' if active else '-f'])

def quit(source):
    Gtk.main_quit()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
