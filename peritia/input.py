from pathlib import Path
from time import strftime
from tkinter.filedialog import askdirectory, askopenfilename
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox

import collapsing_frame as cf
#imgpath = Path(__file__).parent / 'assets/icon1.py'
#Create an instance of Tkinter frame

def flatly():
    win= ttk.Window(themename="flatly", resizable=(True, True))


win= ttk.Window(themename="vapor", resizable=(True, True))

#Set the geometry of Tkinter frame
#win.geometry("750x250")

image_files = {
        'properties-dark': 'icons8_settings_24px.png',
        'properties-light': 'icons8_settings_24px_2.png',
        'add-to-backup-dark': 'icons8_add_folder_24px.png',
        'add-to-backup-light': 'icon1.png',
        'stop-backup-dark': 'icons8_cancel_24px.png',
        'stop-backup-light': 'icons8_cancel_24px_1.png',
        'play': 'icons8_play_24px_1.png',
        'refresh': 'icons8_refresh_24px_1.png',
        'stop-dark': 'icons8_stop_24px.png',
        'stop-light': 'icons8_stop_24px_1.png',
        'opened-folder': 'icons8_opened_folder_24px.png',
        'logo': 'backup.png',
        'about-button':'icons8-about-64.png',
        '_icon':'icons8-small-blue-diamond-48.png',
        'r-arrow':'right-arrow.png'
        }

photoimages = []

imgpath = Path(__file__).parent / 'assets'
for key, val in image_files.items():
    _path = imgpath / val
    photoimages.append(ttk.PhotoImage(name=key, file=_path))

#######################################################

root = ttk.Frame(padding=10, style='primary.TFrame')
style = ttk.Style()
theme_names = style.theme_names()

theme_selection = ttk.Frame(root, padding=(10, 10,
 10, 0))
theme_selection.pack(fill=X, expand=YES)

theme_selected = ttk.Label(
        master=theme_selection,
        text="litera",
        font="-size 24 -weight bold"
        )

theme_selected.pack(side=LEFT)

lbl = ttk.Label(theme_selection, text="Select a theme:")

theme_cbo = ttk.Combobox(
        master=theme_selection,
        text=style.theme.name,
        values=theme_names
        )

theme_cbo.pack(padx=10, side=RIGHT)
theme_cbo.current(theme_names.index(style.theme.name))

lbl.pack(side=RIGHT)
ttk.Separator(root).pack(fill=X, pady=10, padx=10)

def change_theme(e):
    t = cbo.get()
    style.theme_use(t)
    theme_selected.configure(text=t)
    theme_cbo.selection_clear()
    default.focus_set()

theme_cbo.bind('<<ComboboxSelected>>', change_theme)


buttonbar = ttk.Frame(style='primary.TFrame')
buttonbar.pack(fill=X, pady=1, side=TOP)

btn = ttk.Button(
        master=buttonbar,
        text='New backup set',
        image="add-to-backup-light",
        compound=LEFT,
     #   command=_func
        )
btn.pack(side=LEFT, ipadx=5, ipady=5, padx=(1, 2), pady=1)

btn = ttk.Button(
        master=buttonbar,
        text='Backup',
        image='play',
        compound=RIGHT,
        #command=_func
        )
btn.pack(side=LEFT, ipadx=5, ipady=5, padx=(1,0), pady=1)

_func = lambda: Messagebox.ok(message='About Peritia\n\nPeritia is an assistive technology aiming to people with quick solutions...', icon='/root/peritia/assets/icons8-about-64.png',)
btn = ttk.Button(
        master=buttonbar,
        text='About',
        image='play',
        compound=RIGHT,
        command=_func
        )

btn.pack(side=LEFT, ipadx=5, ipady=5, padx=(1,0), pady=1)

#_func = lambda: Messagebox.ok(message='About Peritia\n\nPeritiais an assistive technology aiming to people with quick solutions...', icon='/root/peritia/assets/icons8-about-64.png',)
def _exit():
    from quo import exit
    exit(1)
btn = ttk.Button(
        master=buttonbar,
        text='Exit',
        image='play',
        compound=RIGHT,
        command=_exit
        ).pack(side=LEFT, ipadx=5, ipady=5, padx=(1,0), pady=1)

##############################################################

# left panel

left_panel = ttk.Frame(style='bg.TFrame')
left_panel.pack(side=LEFT, fill=Y)

## backup summary (collapsible)
bus_cf = cf.CollapsingFrame(left_panel)
bus_cf.pack(fill=X, pady=1)

bus_frm = ttk.Frame(bus_cf, padding=5)
bus_frm.columnconfigure(1, weight=6)
bus_cf.add(
        child=bus_frm,
        title='Summary',
        bootstyle=INFO
        )

def time():
    string = strftime('%H:%M:%S %p')
    lbl.config(text = string)
    lbl.after(1000, time)

lbl = ttk.Label(bus_frm, font = ('calibri', 10, 'bold'),
        #background = 'purple',
        foreground = 'white')

lbl.pack(fill=X, pady=1)#nchor = 'left')
time()

# available themes (collapsible)
themes_cf = cf.CollapsingFrame(left_panel)
themes_cf.pack(fill=BOTH, pady=1)

## container
themes_frm = ttk.Frame(themes_cf, padding=10)
themes_frm.columnconfigure(1, weight=1)
themes_cf.add(
        child=themes_frm,
        title='Themes',
        bootstyle=SECONDARY
        )

sep = ttk.Separator(themes_frm, bootstyle=SECONDARY)
sep.grid(row=5, column=0, columnspan=2, pady=10, sticky=EW)

## stop button                                        _func = lambda: Messagebox.ok(message='Stopping backup')
def _func():
    win= ttk.Window(themename="flatly", resizable=(True, True))


btn = ttk.Button(
        master=themes_frm,
        text='Flatly',
        image='stop-backup-dark',
        compound=LEFT,
        command=flatly,
        bootstyle=LINK
        )

btn.grid(row=6, column=0, columnspan=2, sticky=W)

def display_text():
   global entry
   string= entry.get()
   label.configure(text=string)

   print(entry.get())

#Initialize a Label to display the User Input
label=ttk.Label(win, text="", font=("Courier 22 bold"))
label.pack()

#Create an Entry widget to accept User Input
entry= ttk.Entry(win, width= 40)
entry.focus_set()
entry.pack()

#Create a Button to validate Entry Widget
ttk.Button(win, text= "Okay",width= 20, command= display_text).pack(pady=20)

v = ttk.StringVar(win, "1")
# Dictionary to create multiple buttons

values = {"RadioButton 1" : "1",
        "white grid" : "2",
        "RadioButton 3" : "3",
        "RadioButton 4" : "4",
        "RadioButton 5" : "5"}

# Loop is used to create multiple Radiobuttons
# rather than creating each button separately
for (text, value) in values.items():
    ttk.Radiobutton(win, text = text, variable = v, value = value).pack(side = TOP, ipady = 5)

# Infinite loop can be terminated by
# keyboard or mouse interrupt
# or by any predefined function (destroy())

def open_file():
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    from seaborn import regression

    sns.set()
    plt.style.use('seaborn-whitegrid')

    #Now that we have imported the modules, we will be loading the dataset
    path_file = askopenfilename()

    v = ttk.StringVar(win, "1")
    # Dictionary to create multiple buttons
    values = {"RadioButton 1" : "1",
            "white grid" : "2",
            "RadioButton 3" : "3",
            "RadioButton 4" : "4",
            "RadioButton 5" : "5"}

    # Loop is used to create multiple Radiobuttons
    # rather than creating each button separately
    for (text, value) in values.items():                                ttk.Radiobutton(win, text = text, variable = v, value = value).pack(side = TOP, ipady = 5)
    if path_file.endswith(".csv"):
        data = pd.read_csv(path_file)
        print("Shape of Dataset is: ",data.shape,"\n")
        print(data.head())

browse_btn = ttk.Button(win, text="Browse", width=20, command=open_file).pack(pady=20)
#.pack(side=RIGH, fill=X, padx=(5, 0), pady=10


# windows tab
windows_tab = ttk.Frame(win, padding=10)
wt_scrollbar = ttk.Scrollbar(windows_tab)
wt_scrollbar.pack(side=RIGHT, fill=Y)
wt_scrollbar.set(0, 1)

wt_canvas = ttk.Canvas(
        master=windows_tab,
        relief=FLAT,
        borderwidth=0,
        selectborderwidth=0,
        highlightthickness=0,
        yscrollcommand=wt_scrollbar.set
        )

wt_canvas.pack(side=LEFT, fill=BOTH)

# adjust the scrollregion when the size of the canvas changes

wt_canvas.bind(
        sequence='<Configure>',
        func=lambda e: wt_canvas.configure(
            scrollregion=wt_canvas.bbox(ALL))
        )

wt_scrollbar.configure(command=wt_canvas.yview)

scroll_frame = ttk.Frame(wt_canvas)
wt_canvas.create_window((0, 0), window=scroll_frame, anchor=NW)

radio_options = [
        'Internet Cache', 'Internet History', 'Cookies',
        'Download History', 'Last Download Location',
        'Session', 'Set Aside Tabs', 'Recently Typed URLs',
        'Saved Form Information', 'Saved Password'
        ]

edge = ttk.Labelframe(
        master=scroll_frame,
        text='Microsoft Edge',
        padding=(20, 5)
        )
edge.pack(fill=BOTH, expand=YES, padx=20, pady=10)

def open_file():
    path = askopenfilename()
#d = askdirectory()
    print(path)

    #print(k)

win.mainloop()
