#!/usr/bin/python3
import sys
import os
import inspect
import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

__author__ = "1966bc"
__copyright__ = "Copyleft"
__credits__ = ["hal9000", "Luana Lionetto"]
__license__ = "GNU GPL Version 3, 29 June 2007"
__version__ = "1.0"
__maintainer__ = "1966bc"
__email__ = "giuseppecostanzi@gmail.com"
__date__ = "Aestas MMXXI"
__status__ = "production"

#<a href="https://www.flaticon.com/free-icons/white-blood-cells"
#title="white blood cells icons">White blood cells icons created by Icongeek26
#- Flaticon</a>


class Main(ttk.Frame):
    def __init__(self, parent, ):
        super().__init__(name="main")

        self.parent = parent

        
        self.wbc = tk.IntVar()
        self.lower_wbc_limit = tk.IntVar()
        self.higher_wbc_limit = tk.IntVar()
        self.max_allowable_cells = tk.IntVar()
        self.min_allowable_cells = tk.IntVar()
        self.factor = tk.IntVar()
        self.status_bar_text = tk.StringVar()
        self.counters = tk.StringVar()

        self.vcmd = self.master.get_validate_integer(self)
        
        self.init_menu()
        self.init_status_bar()
        self.init_ui()

    def init_menu(self):

        m_main = tk.Menu(self, bd=1)

        m_file = tk.Menu(m_main, tearoff=0, bd=1)
        m_edit = tk.Menu(m_main, tearoff=0, bd=1)

        m_about = tk.Menu(m_main, tearoff=0, bd=1)

        items = (("File", m_file), ("?", m_about),)

        for i in items:
            m_main.add_cascade(label=i[0], underline=0, menu=i[1])

        m_file.add_command(label="Exit", underline=0, command=self.parent.on_exit)

        items = (("About", self.on_about),
                 ("Python", self.on_python_version),
                 ("Tkinter", self.on_tkinter_version),)

        for i in items:
            m_about.add_command(label=i[0], underline=0, command=i[1])

        self.master.config(menu=m_main)

    def init_status_bar(self):

        self.status = ttk.Label(self,
                                style='StatusBar.TLabel',
                                textvariable=self.status_bar_text,
                                anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)


    def init_ui(self):

        f0 = ttk.Frame(self, style='W.TFrame')
        f1 = ttk.Frame(self, style='W.TFrame')

        ttk.Label(f1, text="Input WBC counts", anchor=tk.W, style='W.TLabel').pack(fill=tk.X, expand=0)
        self.txWBC = ttk.Entry(f1,
                               textvariable=self.wbc,
                               validate="key",
                               validatecommand=self.vcmd)
        self.txWBC.bind("<Return>", self.get_values)
        self.txWBC.bind("<KP_Enter>", self.get_values)

        self.txWBC.pack(fill=tk.X,)

        ttk.Label(f1, textvariable=self.counters).pack(fill=tk.X)
        self.lstCounters = tk.Listbox(f1,)
        self.lstCounters.pack(side=tk.LEFT, fill=tk.BOTH, expand=1, padx=5, pady=5)
        self.lstCounters.bind("<<ListboxSelect>>", self.on_item_select)
        self.lstCounters.bind("<Double-Button-1>", self.on_item_activated)


        f2 = ttk.Frame(self, style='W.TFrame', padding=5)

        bts = [("Compute", 0, self.get_values, "<Alt-c>"),
               ("Reset", 0, self.on_reset, "<Alt-r>"),
               ("Quit", 0, self.on_close, "<Alt-q>")]

        for btn in bts:
            ttk.Button(f2,
                       text=btn[0],
                       underline=btn[1],
                       command=btn[2],
                       style='W.TButton',).pack(fill=tk.X, padx=5, pady=5)
            self.parent.bind(btn[3], btn[2])

        f1.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        f2.pack(side=tk.RIGHT, fill=tk.Y, expand=0)
        f0.pack(fill=tk.BOTH, expand=1)

    def on_open(self):
        self.on_reset()

    def on_reset(self, evt=None):

        self.wbc.set('')
        self.lstCounters.delete(0, tk.END)

        self.lower_wbc_limit.set(self.master.read_file("lower_wbc_limit"))
        self.higher_wbc_limit.set(self.master.read_file("higher_wbc_limit"))

        self.max_allowable_cells.set(self.master.read_file("max_allowable_cells"))
        self.min_allowable_cells.set(self.master.read_file("min_allowable_cells"))

        self.factor.set(self.master.read_file("factor"))

        s = "WBC max {0} min {1} Cells max {2} min {3}".format(self.higher_wbc_limit.get(),
                                                               self.lower_wbc_limit.get(),
                                                               self.max_allowable_cells.get(),
                                                               self.min_allowable_cells.get())
        self.status_bar_text.set(s)

        self.counters.set("Calculation")

        self.txWBC.focus()

    def get_values(self, evt=None):

        self.lstCounters.delete(0, tk.END)

        if self.on_fields_control() == False: return
        if self.check_limits() == False: return

        s = "Calculation for {0} wbc cells.".format(self.wbc.get())

        self.counters.set(s)

        pbs = 64

        cells = self.wbc.get() * self.factor.get()

        array = []

        try:

            if self.wbc.get() == 2000:
                array.append("PBS {0:2d}{1} Sample {2}{3}".format(32, '\u03BC', 32, '\u03BC'))


            elif self.wbc.get() > 2000:
                for i in range(24, 33):
                    x = cells * i
                    y = pbs - i

                    #print(x,y)

                    if x in range(self.min_allowable_cells.get(), self.max_allowable_cells.get()):
                        array.append("PBS {0:2d}{1}l Sample {2:2d}{3}l cells {4:7d}".format(y, '\u03BC', i, '\u03BC', x))

            elif self.wbc.get() < 2000:
                for i in range(32, 65):
                    x = cells * i
                    y = pbs - i

                    if x in range(self.min_allowable_cells.get(), self.max_allowable_cells.get()):
                        array.append("PBS {0:2d}{1}l Sample {2:2d}{3}l cells {4:7d}".format(y, '\u03BC', i, '\u03BC', x))

            self.set_values(array)

            self.wbc.set('')
            self.txWBC.focus()

        except:
            s = "{0}".format(sys.exc_info()[1],)
            messagebox.showwarning(self.master.title(), s, parent=self)


    def set_values(self, array):

        self.lstCounters.delete(0, tk.END)

        if array:
            for i in array:
                s = "{0}".format(i,)
                self.lstCounters.insert(tk.END, s)


    def on_item_select(self, evt=None):

        if self.lstCounters.curselection():
            index = self.lstCounters.curselection()

    def on_item_activated(self, evt=None):

        if self.lstCounters.curselection():
            index = self.lstCounters.curselection()
            s = self.lstCounters.get(index[0])
            messagebox.showinfo(self.master.title(), s, parent=self)

    def on_fields_control(self):

        dict_fields = {self.txWBC:"WBC",}

        for k, v in dict_fields.items():
            if not k.get():
                msg = "The {0} field is mandatory".format(dict_fields[k])
                messagebox.showwarning(self.master.title(), msg, parent=self)
                self.counters.set("Calculation")
                self.focus()
                k.focus_set()
                return 0

    def check_limits(self,):

        msg = None

        if self.wbc.get() < self.lower_wbc_limit.get():
            msg = "Attention\nthe input value {0} is lower than the minimum allowed value {1}.".format(self.wbc.get(),
                                                                                                       self.lower_wbc_limit.get())

        elif self.wbc.get() > self.higher_wbc_limit.get():
            msg = "Attention\nthe input value {0} is larger than the maximum allowed value {1}.".format(self.wbc.get(),
                                                                                                        self.higher_wbc_limit.get())

        if msg:

            messagebox.showwarning(self.master.title(), msg, parent=self)

            self.counters.set("Calculation")

            return 0

        else:

            return 1

    def on_about(self,):
        messagebox.showinfo(self.master.title(),
                            self.master.info,
                            parent=self)

    def on_python_version(self):
        s = self.master.get_python_version()
        messagebox.showinfo(self.master.title(), s, parent=self)

    def on_tkinter_version(self):
        s = "Tkinter patchlevel\n{0}".format(self.master.tk.call("info", "patchlevel"))
        messagebox.showinfo(self.master.title(), s, parent=self)

    def on_close(self, evt=None):
        self.parent.on_exit()


class App(tk.Tk):
    """Main Application start here"""
    def __init__(self, ):
        super().__init__()

        self.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.set_style()
        self.title("5-FluorouraCells Counter")
        self.set_icon()
        self.set_info()

        w = Main(self)
        w.on_open()
        w.pack(fill=tk.BOTH, expand=1)

    def set_style(self):

        self.style = ttk.Style()

        self.style.theme_use("clam")

        self.style.configure(".", background=self.get_rgb(240, 240, 237))

        self.style.configure('W.TFrame', background=self.get_rgb(240, 240, 237))

        self.style.configure('W.TButton',
                             background=self.get_rgb(240, 240, 237),
                             padding=5,
                             border=1,
                             relief=tk.RAISED,
                             font="TkFixedFont")

        self.style.configure('W.TLabel',
                             background=self.get_rgb(240, 240, 237),
                             padding=2,
                             font="TkFixedFont")

        self.style.configure('W.TLabelframe',
                             background=self.get_rgb(240, 240, 237),
                             relief=tk.GROOVE,
                             padding=2,
                             font="TkFixedFont")

        self.style.configure('StatusBar.TLabel',
                             background=self.get_rgb(240, 240, 237),
                             padding=2,
                             border=1,
                             relief=tk.SUNKEN,
                             font="TkFixedFont")


        self.style.configure("Mandatory.TLabel",
                             foreground=self.get_rgb(0, 0, 255),
                             background=self.get_rgb(255, 255, 255))

    def set_icon(self):
        icon = tk.PhotoImage(data=self.read_file("app"))
        self.call("wm", "iconphoto", self._w, "-default", icon)

    def set_info(self,):
        msg = "{0}\nauthor: {1}\ncopyright: {2}\ncredits: {3}\nlicense: {4}\nversion: {5}\
               \nmaintainer: {6}\nemail: {7}\ndate: {8}\nstatus: {9}"
        info = msg.format(self.title(), __author__, __copyright__, __credits__, __license__, __version__, __maintainer__, __email__, __date__, __status__)
        self.info = info

    def get_python_version(self,):
        return "Python version:\n{0}".format(".".join(map(str, sys.version_info[:3])))

    def get_full_path(self, file):
        """# return full path of the directory where program resides."""

        return os.path.join(os.path.dirname(__file__), file)

    def read_file(self, file):

        try:
            path = self.get_full_path(file)
            f = open(path, "r")
            v = f.readline()
            f.close()
            return v

        except FileNotFoundError:
            self.on_log(self,
                        inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])

    def on_log(self, container, function, exc_value, exc_type, module):

        now = datetime.datetime.now()
        log_text = "{0}\n{1}\n{2}\n{3}\n{4}\n\n".format(now, function, exc_value, exc_type, module)
        log_file = open("log.txt", "a")
        log_file.write(log_text)
        log_file.close()


    def get_icon(self, which):

        try:
            path = self.get_full_path(which)
            f = open(path, "r")
            v = f.readline()
            f.close()
            return v

        except FileNotFoundError:
            self.on_log(self,
                        inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])

    def get_validate_integer(self, caller):
        return (caller.register(self.validate_integer), '%d', '%P', '%S')

    def get_validate_float(self, caller):
        return (caller.register(self.validate_float), '%d', '%P', '%S')

    def validate_integer(self, action, value_if_allowed, text,):
        # action=1 -> insert
        if action == '1':
            if text in '0123456789':
                try:
                    int(value_if_allowed)
                    return True
                except ValueError:
                    return False
            else:
                return False
        else:
            return True

    def get_rgb(self, r, g, b):
        """translates an rgb tuple of into a tkinter friendly color code"""
        return "#%02x%02x%02x" % (r, g, b)

    def on_exit(self):
        """Close all"""
        msg = "Do you want to quit?"
        if messagebox.askokcancel(self.title(), msg, parent=self):
            self.destroy()

def main():

    app = App()

    app.mainloop()

if __name__ == '__main__':
    main()

