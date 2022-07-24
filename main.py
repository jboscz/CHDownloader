import configparser
import os
import re
import shutil
import sys
import threading
import time
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import END

import drive
from googleapiclient.errors import *
from pyunpack import Archive

wait = time.sleep
mainscreen = False
sett = None
path = None

try:
    config = configparser.ConfigParser(allow_no_value=True)
    config.read("./config.ini")
    version = config["DEFAULT"]["version"]
    key = config["DEFAULT"]["iconkey"]
    allowkey = config["DEFAULT"].getboolean("allow_icon_keybind")
    path = config["DEFAULT"]["path"]
except Exception as e:
    print("Could not parse configuration file, using defaults",file=sys.stderr)
    version = "1"
    key = 0
    pass

def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top

def vp_start_gui():
    global val, w, root
    root = tk.Tk()
    top = MainWindow(root)
    style = ttk.Style(root)
    try:
        root.tk.call('source', 'azuredark/azuredark.tcl')
        style.theme_use('azure')
    except tk.TclError:
        print("Unable to use theme")
    init(root, top)
    root.protocol("WM_DELETE_WINDOW",save_config)
    root.bind("e",on_button_pressed)
    root.mainloop()

def vp_start_settings():
    global w, root, sett
    sett = Settings(tk.Toplevel)
    sett.grab_set()
    w = sett

w = None

class MainWindow:
    def __init__(self, top=None):
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'

        top.geometry("636x450+608+327")
        top.minsize(120, 1)
        top.maxsize(1924, 1061)
        top.resizable(1,  1)
        top.title("CHDownloader")
        top.iconbitmap("favicon.ico")
        self.menubar = tk.Menu(top,font="TkMenuFont",bg=_bgcolor,fg=_fgcolor)
        top.configure(menu = self.menubar)
        self.sub_menu = tk.Menu(top)
        self.menubar.add_cascade(menu=self.sub_menu,
                 label=f"ver: {version}")
        # self.sub_menu.add_command(
        #          command=self.checkUpdate,
        #          label="Check for updates")
        # self.sub_menu.add_command(
        #            label="Settings", command=self.showSettings)
        self.sub_menu1 = tk.Menu(top)
        self.menubar.add_cascade(menu=self.sub_menu1,
                 label="Experimental features")
        # self.sub_menu1.add_command(
        #          command=self.showSpotifyMenu,
        #          label="Spotify Playlist Analyzer")

        self.Entry = ttk.Entry(root)
        self.Entry.place(relx=0.173, rely=0.262, height=35, relwidth=0.629)
        self.Entry.insert(0, 'Entry')

        self.Download = tk.Button(top, command=self.create_coroutine)
        self.Download.place(relx=0.362, rely=0.363, height=44, width=157)
        self.Download.configure(disabledforeground="#a3a3a3")
        self.Download.configure(font="-family {Segoe UI} -size 23")
        self.Download.configure(foreground="#000000")
        self.Download.configure(highlightbackground="#d9d9d9")
        self.Download.configure(highlightcolor="black")
        self.Download.configure(pady="0")
        self.Download.configure(text="Download")



        self.Status = tk.Message(top)
        self.Status.place(relx=0.204, rely=0.489, relheight=0.25, relwidth=0.568)
        self.Status.configure(foreground="#000000")
        self.Status.configure(highlightbackground="#d9d9d9")
        self.Status.configure(highlightcolor="black")
        self.Status.configure(width=361)
        self.Status.configure(borderwidth=20)

        self.Talker = tk.Label(top)
        self.Talker.place(relx=-0.031, rely=0.933, height=21, width=274)
        if allowkey == 1:
            self.Talker.configure(text=f'Press {key} to iconify CHDownloader')
        else:
            self.Talker.configure(text=f'')
   


        a = threading.Thread(target=self.variableUpdater, args=(self,))
        a.start()
    
    def variableUpdater(self,a):
        global var
        while True:
            if allowkey:
                self.Talker.configure(text=f'Press {key} to iconify CHDownloader')
                wait(1)
            else:
                self.Talker.configure(text=f'')
                wait(1)
        
            
    
    def showSettings(self):
        settings = Settings(self)
        settings.grab_set()

    def checkUpdate(self):
        return

    def showSpotifyMenu(self):
        return


    def check_link(self):
        link = self.Entry.get()
        self.Entry.delete(0, END)
        id = re.findall(r'[\w-]{19,}', link)
        try:
            file = client.get_file(id[0])
        except Exception as e:
            self.Status.configure(text=f"{link} could not be resolved.")
            return
        if file.is_directory:
            self.Status.configure(text=f"Downloading {file.name}...")
            wait(0.1)
            os.mkdir(f"./cache/{file.name}")
            for f in file.list():
                if f.is_directory:
                    a = client.get_file(f.id)
                    os.mkdir(f"./cache/{file.name}/{a.name}")
                    for i in a.list():
                        self.Status.configure(text=f"Downloading {file.name}/{a.name}...")
                        client.download_file(i.id,f"./cache/{file.name}/{a.name}/{i.name}")
                    # shutil.move(f"./cache/{file.name}/{a.name}",path)
                    continue
                self.Status.configure(text=f"Downloading {f.name}...")
                client.download_file(f.id, f"./cache/{file.name}/{f.name}")
            try:
                shutil.move(f"./cache/{file.name}", path)
            except:
                self.Status.configure(text=f"{file.name} already exists in {path}!")
                shutil.rmtree(f"./cache/{file.name}")
                return
            self.Status.configure(text=f"{file.name} downloaded successfully and moved to {path}")


        else:
            if ".7z" in file.name or ".zip" in file.name or ".rar" in file.name:
                self.Status.configure(text=f"Downloading {file.name}...")
                wait(0.1)
                client.download_file(file.id,f"./cache/{file.name}")
                archive = Archive(f'./cache/{file.name}').extractall(path)
                os.remove(f"./cache/{file.name}")
                self.Status.configure(text=f"{file.name} downloaded successfully and moved to {path}")
                return
            self.Status.configure(text="This program requires a valid Google Drive folder or archive link to work.")

    def create_coroutine(self):
        p = threading.Thread(target=self.check_link)
        p.start()
        return
    
    def toggle_screen(self):
        global mainscreen
        if mainscreen:
            mainscreen = False
        else:
            mainscreen = True

class Settings(tk.Toplevel):
    def __init__(self, top=None):
        global sett
        tk.Toplevel.__init__(self)
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        self.style = ttk.Style()
        # self.style.theme_use('azure')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])
        self.geometry("325x420+687+306")
        self.minsize(120, 1)
        self.maxsize(1924, 1061)
        self.resizable(1,  1)
        self.title("Settings")


        self.SettingsTxt = tk.Message(self)
        self.SettingsTxt.place(relx=-0.031, rely=0.0, relheight=0.14, relwidth=0.603)
        self.SettingsTxt.configure(font="-family {Segoe UI} -size 32")
        self.SettingsTxt.configure(text='''Settings''')
        self.SettingsTxt.configure(width=196)

        self.Set1 = tk.Message(self)
        self.Set1.place(relx=-0.031, rely=0.214, relheight=0.079, relwidth=0.677)
        self.Set1.configure(font="-family {Segoe UI} -size 13")
        self.Set1.configure(text='''Change ignored filenames''')
        self.Set1.configure(width=220)
   
        self.Set1Btn = tk.Button(self)
        self.Set1Btn.place(relx=0.646, rely=0.19, relheight=0.131, relwidth=0.28)
        self.Set1Btn.configure(font="-family {Segoe UI} -size 17")
        self.Set1Btn.configure(justify='left')
        self.Set1Btn.configure(command=self.changeVariable1)
        self.Set1Btn.configure(text='Edit')

    def changeVariable1(self):
        a = SetIgnoredWords(self)
        a.grab_set()

class SetIgnoredWords(tk.Toplevel):
   def __init__(self, top=None):
        tk.Toplevel.__init__(self)
        self.geometry("548x408+751+335")
        self.minsize(120, 1)
        self.maxsize(2948, 1061)
        self.resizable(0,0)
        self.title("Settings - Ignored Words")

        self.MsgTop = tk.Message(self)
        self.MsgTop.place(relx=-0.109, rely=-0.049, relheight=0.265
                , relwidth=0.67)
        self.MsgTop.configure(font="-family {Segoe UI} -size 23")
        self.MsgTop.configure(highlightcolor="black")
        self.MsgTop.configure(text='''Ignored Words''')
        self.MsgTop.configure(width=270)

        self.InfoMsg = tk.Message(self)
        self.InfoMsg.place(relx=0.077, rely=0.13, relheight=0.238
                    , relwidth=0.859)
        self.InfoMsg.configure(font="-family {Segoe UI} -size 11")
        self.InfoMsg.configure(highlightcolor="black")
        self.InfoMsg.configure(justify='center')
        self.InfoMsg.configure(text='''Here you can input file names that CHDownloader will ignore when downloading files. An example could be adding "video.mp4" to not download music videos. Format each entry with 1 space in between.''')
        self.InfoMsg.configure(width=462)
 
        self.TxtEnter = tk.Text(self)
        self.TxtEnter.place(relx=0.091, rely=0.39, relheight=0.424
                 , relwidth=0.828)
        self.TxtEnter.configure(font="TkTextFont")
        self.TxtEnter.configure(highlightcolor="black")
        self.TxtEnter.configure(insertbackground="black")
        self.TxtEnter.configure(selectbackground="blue")
        self.TxtEnter.configure(selectforeground="white")
        self.TxtEnter.configure(wrap="word")
   
        self.Save = tk.Button(self)
        self.Save.place(relx=0.429, rely=0.855, height=34, width=77)
        self.Save.configure(font="-family {Segoe UI} -size 14")
        self.Save.configure(pady="0")
        self.Save.configure(text='''Save''')
   


def save_config():
    with open(f"{os.path.dirname(os.path.realpath(sys.argv[0]))}\\config.ini","w") as f:
        config.write(f)
        f.close()
    root.destroy()
    sys.exit()

def on_button_pressed(key):
    global allowkey
    if allowkey:
        root.iconify()



if __name__ == '__main__':
    if hasattr(sys,"_MEIPASS"):
        os.chdir(sys._MEIPASS)
    client = drive.Client("./project.json")
    try:
        shutil.rmtree("./cache")
    except:
        pass
    if not path:
        path = input("Please input Clone Hero song path: ")
        config["DEFAULT"]["path"] = path
    os.mkdir("./cache")
    vp_start_gui()
