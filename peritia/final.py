from pathlib import Path

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox

from tkinter.filedialog import askopenfilename

win = ttk.Window(
        "Peritia:  All in one assistive software",
        themename= "vapor",
        resizable=(True, True)
        )

#Set the geometry of Tkinter frame
PATH = Path(__file__).parent / 'assets'
images = [
        ttk.PhotoImage(
            name='logo',
            file=PATH / 'icons8_broom_64px_1.png'),
        ttk.PhotoImage(
            name='cleaner',
            file=PATH / 'icons8_broom_64px.png'),
        ttk.PhotoImage(
            name='registry',
            file=PATH / 'icons8_registry_editor_64px.png'),
        ttk.PhotoImage(
            name='tools',
            file=PATH / 'icons8_wrench_64px.png'),
        ttk.PhotoImage(
            name='options',
            file=PATH / 'icons8_settings_64px.png'),
        ttk.PhotoImage(
            name='privacy',
            file=PATH / 'icons8_spy_80px.png'),
        ttk.PhotoImage(
            name='junk',
            file=PATH / 'icons8_trash_can_80px.png'),
        ttk.PhotoImage(
            name='protect',
            file=PATH / 'icons8_protect_40px.png')
        ]

# HEADER
hdr_frame = ttk.Frame(win, padding=20, bootstyle=SECONDARY)
hdr_frame.grid(row=0, column=0, columnspan=3, sticky=EW)

hdr_label = ttk.Label(
        master=hdr_frame,
        image='logo',
        bootstyle=(INVERSE, SECONDARY)
        ).pack(side=LEFT)

logo_text = ttk.Label(
        master=hdr_frame,
        text='Peritia',
        font=('TkDefaultFixed', 30),
        bootstyle=(INVERSE, SECONDARY)
        ).pack(side=LEFT, padx=10)


# ACTION BUTTONS

action_frame = ttk.Frame(win)
action_frame.grid(row=1, column=0, sticky=NSEW)

cleaner_btn = ttk.Button(
        master=action_frame,
        image='cleaner',
        text='summary',
        compound=TOP,
        bootstyle=INFO
        ).pack(side=TOP, fill=BOTH, ipadx=10, ipady=10)

registry_btn = ttk.Button(
        master=action_frame,
        image='tools', #egistry',
        text='tools',
        compound=TOP,
        bootstyle=INFO
        ).pack(side=TOP, fill=BOTH, ipadx=10, ipady=10)

tools_btn = ttk.Button(
    master=action_frame,
    image='registry',
    text='features',
    compound=TOP,
    bootstyle=INFO
    ).pack(side=TOP, fill=BOTH, ipadx=10, ipady=10)

_about = lambda: Messagebox.ok(message='About Peritia\n\nPeritia is Latin word which means experience or practical knowledge.\nIn this context peritia is an assistive technology aiming to people with quick solutions...', icon='/root/peritia/assets/icons8-about-64.png',)


options_btn = ttk.Button(
    master=action_frame,
    image='options',
    text='about',
    compound=TOP,
    command=_about,
    bootstyle=INFO
    ).pack(side=TOP, fill=BOTH, ipadx=10, ipady=10)



# RESULTS FRAME

results_frame = ttk.Frame(win).pack(side=TOP, fill=X, expand=YES)#results_frame.grid(row=1, column=2, sticky=NSEW)

# progressbar with text indicator
#pb_frame = ttk.Frame(win, padding=(0, 10, 10, 10)).pack(side=TOP, fill=X, expand=YES)

pb = ttk.Progressbar(
        master=results_frame,
        bootstyle=(SUCCESS, STRIPED),
        variable='progress').pack(side=LEFT, fill=X, expand=YES, padx=(15, 10))

      #  ttk.Label(pb_frame, text='%').pack(side=RIGHT)
     #   ttk.Label(pb_frame, textvariable='progress').pack(side=RIGHT)
    #    self.setvar('progress', 78)

        # result cards
    #    cards_frame = ttk.Frame(
      #      master=results_frame,
      #      name='cards-frame',
      #      bootstyle=SECONDARY
   #     )
     #   cards_frame.pack(fill=BOTH, expand=YES)
win.mainloop()
