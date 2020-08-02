import os
import subprocess

try:
    from urllib import unquote
except ImportError:
    from urllib.parse import unquote

import gi
gi.require_version('GConf', '2.0')
from gi.repository import Nautilus, GObject, GConf

def get_tmux_sessions():
    sessions = subprocess.check_output(['tmux', 'ls']).decode().splitlines()
    sessions = list(map(lambda x: x[:x.find(':')], sessions))
    return sessions

class TmuxOpen(Nautilus.MenuProvider, GObject.GObject):
    def __init__(self):
        self.client = GConf.Client.get_default()
        self.tmux_session = "" 
        

    def _open_tmux(self, menu, file, session):
        filename = unquote(file.get_uri()[7:])

        subprocess.Popen(['tmux', 'new-window', '-t{}'.format(session)], cwd=filename )
        

    def get_file_items(self, window, files):
        if len(files) != 1:
            return
        
        file = files[0]
        if not file.is_directory() or file.get_uri_scheme() != 'file':
            return
       
        item = Nautilus.MenuItem(name='TmuxSession::open_tmux',
                                 label='Open In Tmux' ,
                                 tip='Open Terminal In %s' % file.get_name())

        submenu = Nautilus.Menu()
        item.set_submenu(submenu)

        tmux_sessions = get_tmux_sessions()
        for sessions in tmux_sessions:
            sub_menuitem = Nautilus.MenuItem(name='TmuxSession::' + sessions, 
                                             label=sessions, 
                                             tip='',
                                             icon='')
            sub_menuitem.connect('activate', self._open_tmux, file, sessions)
            submenu.append_item(sub_menuitem)

        return item,

    def get_background_items(self, window, file):
        item = Nautilus.MenuItem(name='TmuxSession::open_tmux2',
                                 label='Open In Tmux' ,
                                 tip='Open Terminal In %s' % file.get_name())

        submenu = Nautilus.Menu()
        item.set_submenu(submenu)
        tmux_sessions = get_tmux_sessions()
        for sessions in tmux_sessions:
            sub_menuitem = Nautilus.MenuItem(name='TmuxSession::' + sessions, 
                                             label=sessions, 
                                             tip='',
                                             icon='')
            sub_menuitem.connect('activate', self._open_tmux, file, sessions)
            submenu.append_item(sub_menuitem)

        return item,
