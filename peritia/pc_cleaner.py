#!/usr/bin/python3

"""
    Author: Israel Dryer
    Modified: 2021-12-12
    Adapted from: https://images.idgesg.net/images/article/2018/08/cw_win10_utilities_ss_02-100769136-orig.jpg
"""
from pathlib import Path
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox, Querybox
from tkinter.filedialog import askopenfilename

PATH = Path(__file__).parent / 'assets'


class Cleaner(ttk.Frame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.pack(fill=BOTH, expand=YES)

        # application images
        self.images = [
            ttk.PhotoImage(
                name='logo',
                file=PATH / 'icons8_broom_64px_1.png'),
            ttk.PhotoImage(
                name='cleaner',
                file=PATH / 'icons8_broom_64px.png'),
            ttk.PhotoImage(
                name='__$cancel',
                file=PATH / 'icons8_cancel_24px_1.png'),
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
                file=PATH / 'icons8_protect_40px.png'),
            ttk.PhotoImage(
                name='exit',
                file=PATH / 'icons8-exit-sign-48.png'),
            ttk.PhotoImage(
                name='about',
                file=PATH / 'icons8-about-50.png'),
            ttk.PhotoImage(
                name='haha',
                file=PATH / 'icons8-arrow-64.png'),

            # ASL LETTERS & NUMBERS
            ttk.PhotoImage(
                name='a',
                file=PATH / 'a.png'),
            ttk.PhotoImage(
                name='b',
                file=PATH / 'b.png'),
            ttk.PhotoImage(
                name='c',
                file=PATH / 'c.png'),

            ttk.PhotoImage(
                name='d',
                file=PATH / 'd.png'),
            ttk.PhotoImage(
                name='e',
                file=PATH / 'e.png'),
            ttk.PhotoImage(
                name='f',
                file=PATH / 'f.png'),
            ttk.PhotoImage(
                name='g',
                file=PATH / 'g.png'),
            ttk.PhotoImage(
                name='h',
                file=PATH / 'h.png'),
            ttk.PhotoImage(
                name='i',
                file=PATH / 'i.png'),
            ttk.PhotoImage(
                name='j',
                file=PATH / 'j.png'),
            ttk.PhotoImage(
                name='k',
                file=PATH / 'k.png'),
            ttk.PhotoImage(
                name='l',
                file=PATH / 'l.png'),
            ttk.PhotoImage(
                name='m',
                file=PATH / 'm.png'),
            ttk.PhotoImage(
                name='n',
                file=PATH / 'n.png'),
            ttk.PhotoImage(
                name='o',
                file=PATH / 'o.png'),
            ttk.PhotoImage(
                name='p',
                file=PATH / 'p.png'),
            ttk.PhotoImage(
                name='q',
                file=PATH / 'q.png'),

            ttk.PhotoImage(
                name='r',
                file=PATH / 'r.png'),
            ttk.PhotoImage(
                name='s',
                file=PATH / 's.png'),
            ttk.PhotoImage(
                name='t',
                file=PATH / 't.png'),
            ttk.PhotoImage(
                name='u',
                file=PATH / 'u.png'),
            ttk.PhotoImage(
                name='v',
                file=PATH / 'v.png'),
            ttk.PhotoImage(
                name='w',
                file=PATH / 'w.png'),
            ttk.PhotoImage(
                name='x',
                file=PATH / 'x.png'),
            ttk.PhotoImage(
                name='y',
                file=PATH / 'y.png'),
            ttk.PhotoImage(
                name='z',
                file=PATH / 'z.png'),

            #ASL NUMBERS 0-9
            ttk.PhotoImage(                                                name='0',                                                  file=PATH / '0.png'),
            ttk.PhotoImage(                                                name='1',                                                  file=PATH / '1.png'),
            ttk.PhotoImage(                                                name='2',                                                  file=PATH / '2.png'),
            ttk.PhotoImage(                                                name='3',                                                  file=PATH / '3.png'),
            ttk.PhotoImage(                                                name='4',                                                  file=PATH / '4.png'),
            ttk.PhotoImage(                                                name='5',                                                  file=PATH / '5.png'),
            ttk.PhotoImage(                                                name='6',                                                  file=PATH / '6.png'),
            ttk.PhotoImage(                                                name='7',                                                  file=PATH / '7.png'),
            ttk.PhotoImage(                                                name='8',                                                  file=PATH / '8.png'),
            ttk.PhotoImage(                                                name='9',                                                  file=PATH / '9.png')
        ]

        # header
        hdr_frame = ttk.Frame(self, padding=20, bootstyle=SECONDARY)
        hdr_frame.grid(row=0, column=0, columnspan=3, sticky=EW)

        hdr_label = ttk.Label(
            master=hdr_frame,
            image='haha', #logoi',
            bootstyle=(INVERSE, SECONDARY)
        )
        hdr_label.pack(side=LEFT)

        logo_text = ttk.Label(
            master=hdr_frame,
            text='Peritia',
            font=('TkDefaultFixed', 30),
            bootstyle=(INVERSE, SECONDARY)
        )
        logo_text.pack(side=LEFT, padx=10)

        ##
        style = ttk.Style()
        theme_names = style.theme_names()
        theme_selection = ttk.Frame(hdr_frame, padding=(10, 10, 10, 0))
        theme_selection.pack(padx=10)#fill=X, expand=YES)

        lbl = ttk.Label(theme_selection, text="Select a theme:")

        theme_cbo = ttk.Combobox(
                master=theme_selection,
                text=style.theme.name,
                values=theme_names
                )

        theme_cbo.pack(padx=10, side=RIGHT)
        theme_cbo.current(theme_names.index(style.theme.name))
        lbl.pack(side=RIGHT)

        ttk.Separator(hdr_frame).pack(fill=X, pady=10, padx=10)

        def change_theme(e):
            t = cbo.get()
            style.theme_use(t)
          # not using the .configure func since ....
            theme_cbo.selection_clear()
           # default.focus_set()

        theme_cbo.bind('<<ComboboxSelected>>', change_theme)

        cbo = ttk.Combobox(
        master=hdr_frame,
        text=style.theme.name,
        values=theme_names,
        exportselection=False
        )
        cbo.pack(fill=X, pady=5)
        cbo.current(theme_names.index(style.theme.name))

        # action buttons
        action_frame = ttk.Frame(self)
        action_frame.grid(row=1, column=0, sticky=NSEW)

        cleaner_btn = ttk.Button(
            master=action_frame,
            image='cleaner',
            text='summary',
            compound=TOP,
            bootstyle=INFO
        )
        cleaner_btn.pack(side=TOP, fill=BOTH, ipadx=10, ipady=10)

        _tools = lambda: Messagebox.ok(message="1) Data Analysis & Forecasting tool\nForecasting is to predict or estimate (a future event or trend). This is actualized by determining what is going to happen in the future by analyzing what happened in the past and what is going on now.This tool can be used to analyse students' performance.\n\n2) Finger spelling\nTranslation of text to sign language is also be given as a task during sign language study session. This tool can easily produce the correct answers and because the visual stays on screen, students can follow the hand movements at their own pace.", icon="/root/peritia/assets/icons8_registry_editor_32px.png")

        tools_btn = ttk.Button(
            master=action_frame,
            image='tools',
            text='Tools',
            compound=TOP,
            command=_tools,
            bootstyle=INFO
        ).pack(side=TOP, fill=BOTH, ipadx=10, ipady=10)

        features_btn = ttk.Button(
            master=action_frame,
            image='registry',
            text='features',
            compound=TOP,
            bootstyle=INFO
        ).pack(side=TOP, fill=BOTH, ipadx=10, ipady=10)
        games_btn = ttk.Button(
                master=action_frame,
                image='registry',
                text='Games',
                compound=TOP,
                bootstyle=INFO).pack(side=TOP, fill=BOTH, ipadx=10, ipady=10)

        _func = lambda: Messagebox.ok(message='About Peritia\n\nPeritia is Latin word which means experience or practical knowledge.\nIn this context peritia is an assistive technology aiming to people with quick solutions...\n\n© Gerrishon Sirere\nTHE SOFTWARE IS PROVIDED AS IS WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE', icon='/root/peritia/assets/icons8-about-64.png')

        options_btn = ttk.Button(
            master=action_frame,
            image='about', #options',
            text='About',
            compound=TOP,
            command=_func,
            bootstyle=INFO
        ).pack(side=TOP, fill=BOTH, ipadx=10, ipady=10)

        def _exit():
            exit()

        exit_btn = ttk.Button(
                master=action_frame,
                image='exit',
                text='Exit',
                compound=TOP,
                command=_exit,
                bootstyle=INFO
                ).pack(side=TOP, fill=BOTH, ipadx=10, ipady=10)

        # option notebook
        notebook = ttk.Notebook(self)
        notebook.grid(row=1, column=1, sticky=NSEW, pady=(25, 0))

        # windows tab
        windows_tab = ttk.Frame(notebook, padding=10)
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
            'Performance', 'Trend', 'Forecasting', 'Puzzle games', 'Finger spelling', 'Letters', 'Numbers']
          #  'Download History', 'Last Download Location',
          #  'Session', 'Set Aside Tabs', 'Recently Typed URLs',
           # 'Saved Form Information', 'Saved Password'
       # ]

        edge = ttk.Labelframe(
            master=scroll_frame,
            text='Data analysis',
            padding=(20, 5)
        )
        edge.pack(fill=BOTH, expand=YES, padx=20, pady=10)

        explorer = ttk.Labelframe(
            master=scroll_frame,
            text='Finger Spelling',
            padding=(20, 5)
        )
        explorer.pack(fill=BOTH, padx=20, pady=10, expand=YES)

        # add radio buttons to each label frame section
        for section in [edge, explorer]:
            for opt in radio_options:
                cb = ttk.Checkbutton(section, text=opt, state=NORMAL)
                cb.invoke()
                cb.pack(side=TOP, pady=2, fill=X)
        notebook.add(windows_tab, text='Features')

        # empty tab for looks
        notebook.add(ttk.Frame(notebook), text='Applications/usage')

        # results frame
        results_frame = ttk.Frame(self)
        results_frame.grid(row=1, column=2, sticky=NSEW)

        # progressbar with text indicator
        pb_frame = ttk.Frame(results_frame, padding=(0, 10, 10, 10))
        pb_frame.pack(side=TOP, fill=X, expand=YES)

        pb = ttk.Progressbar(
            master=pb_frame,
            bootstyle=(SUCCESS, STRIPED),
            variable='progress'
        )
        pb.pack(side=LEFT, fill=X, expand=YES, padx=(15, 10))

        ttk.Label(pb_frame, text='%').pack(side=RIGHT)
        ttk.Label(pb_frame, textvariable='progress').pack(side=RIGHT)
        self.setvar('progress', 78)

        # result cards
        cards_frame = ttk.Frame(
            master=results_frame,
            name='cards-frame',
            bootstyle=SECONDARY
        )
        cards_frame.pack(fill=BOTH, expand=YES)

        # privacy card
        priv_card = ttk.Frame(
            master=cards_frame, 
            padding=1, 
        )
        priv_card.pack(side=LEFT, fill=BOTH, padx=(10, 5), pady=10)

        priv_container = ttk.Frame(
            master=priv_card, 
            padding=40,
        )
        priv_container.pack(fill=BOTH, expand=YES)

        priv_lbl = ttk.Label(
            master=priv_container,
            image='privacy',
            text='DATA ANALYTICS',
            compound=TOP,
            anchor=CENTER
        )
        priv_lbl.pack(fill=BOTH, padx=20, pady=(40, 0))

        ttk.Label(
            master=priv_container,
            textvariable='priv_lbl',
            bootstyle=PRIMARY
        ).pack(pady=(0, 20))
        self.setvar('priv_lbl', 'Data Analysis & forecasting')

        def open_file():
         #   from autots import AutoTS
        #    import numpy as np
        #    import pandas as pd
         #   import matplotlib.pyplot as plt
         #   import seaborn as sns
         #   from seaborn import regression

         #   sns.set()
         #   plt.style.use('seaborn-whitegrid')

            #Now that we have imported the modules, we will be loading the dataset
            path_file = askopenfilename()
            if path_file.endswith(".csv"):
                import pandas as pd
              #  data = pd.read_csv(path_file)
               # print("Shape of Dataset is: ",data.shape,"\n")
              #  print(data.head())
                #data.dropna()
                import matplotlib.pyplot as plt
                import seaborn as sns
                from seaborn import regression

                sns.set()
                plt.style.use('seaborn-whitegrid')
                data = pd.read_csv(path_file)
                print("Shape of Dataset is: ",data.shape,"\n")
                print(data.head())
                data.dropna()
                plt.figure(figsize=(10, 4))
                _title = Querybox.get_string(title="Title", prompt="What will be the title of your graph? ")
                if _title:
                    _x = Querybox.get_string(title="x axis", prompt="X-axis label")
                if _x:
                    _y = Querybox.get_string(title="y axis", prompt="Y-axis label")
                plt.title(_title)#ogeCoin Price INR")
                plt.xlabel(_x)#Date")
                plt.ylabel(_y) #Close")
                plt.plot(data["Close"])
                plt.show()

                from autots import AutoTS

                model = AutoTS(
                        forecast_length=10,
                        frequency='infer',
                        ensemble='simple',
                        drop_data_older_than_periods=200
                        )

                model = model.fit(
                        data,
                        date_col=_x, #Date',
                        value_col=_y, #'Close',
                        id_col=None
                        )

                prediction = model.predict()
                forecast = prediction.forecast
                print("DogeCoin Price Prediction")
                print(forecast)

        ttk.Button(priv_container, text= "Browse", command=open_file, width= 20).pack(padx=20, pady=(40, 0))

        #Initialize a Label to display the User Input
      #  label=ttk.Label(priv_container, text="", font=("Courier 22 bold"))
     #   label.pack()
        #Create an Entry widget to accept User Input

     #   entry= ttk.Entry(priv_container, width= 40)
      #  entry.focus_set()
      #  entry.pack()

      #  def get_text(self):
        #    global entry
        #    string= self.entry.get()
          #  self.label.configure(text=string)
       #     print(self.entry.get())
        
        #Create a Button to validate Entry Widget
     #   ttk.Button(priv_container, text= "Okay",width= 20, command=get_text()).pack(pady=20) #command=display_text

        # junk card

        junk_card = ttk.Frame(
                master=cards_frame,
                padding=1)
        junk_card.pack(side=LEFT, fill=BOTH, padx=(10, 20), pady=10) #(5, 10), pady=20)#10)

        junk_container = ttk.Frame(junk_card, padding=40)
        junk_container.pack(fill=BOTH, expand=YES)

        junk_lbl = ttk.Label(
                master=junk_container,
                image='haha', #junk',
                text='Finger spelling',  #PRIVACY', 
                compound=TOP, 
                anchor=CENTER
                )
        junk_lbl.pack(fill=BOTH, padx=20, pady=(40, 0))
        
        ttk.Label(
            master=junk_container, 
            textvariable='junk_lbl',
            bootstyle=PRIMARY, 
            justify=CENTER).pack(pady=(0, 20))
        self.setvar('junk_lbl', 'Finger spelling, games, data analysis and so much more!')
        #,150 MB of unneccesary file(s) \nremoved')

###########################################################

        def get_texts():
            from tkinter import TclError
            string = entry.get()
            try:
                sign_lbl.configure(text="", image=string.lower())
            except TclError:
                sign_lbl.configure(text="Image not found", image='__$cancel')
            print(entry.get())

        sign_lbl = ttk.Label(
                master=junk_container,
                image= "1",
                text='FINGER SPELLING',
                compound=TOP,
                anchor=CENTER
                )
        sign_lbl.pack(padx=20) #fill=BOTH, padx=20, pady=(40, 0)

        entry= ttk.Entry(junk_container, width= 30)
        entry.focus_set()
        entry.pack()

        ttk.Button(junk_container, text= "Check",width= 20, command=get_texts).pack(pady=20) 

       # sign_lbl = ttk.Label(
           #     master=junk_container,
             #   image= entry.get(),#'junk',
              #  text='PRIVACY',                                 #  compound=TOP,                                     anchor=CENTER
              #  )
       # junk_lbl.pack(fill=BOTH, padx=20, pady=(40, 0))



      #  label=ttk.Label(junk_container, text="", font=("Courier 22 bold"))
     #   label.pack()

     #   entry= ttk.Entry(junk_container, width= 30)
     #   entry.focus_set()
      #  entry.pack()


        #Create a Button to validate Entry Widget
      #  ttk.Button(junk_container, text= "Okay",width= 20, command=get_text).pack(pady=20)

        #win.withdraw()
        # the input dialog
     #   def qb():
       #     USER_INP = Querybox.get_string(title="Test", prompt="What's your Name?:")
       #     print(USER_INP)
          #  label=ttk.Label(junk_container, text=USER_INP, font=("Courier 22 bold"))
         #   label.pack(pady20)

     #   ttk.Button(junk_container, text= "Start",width= 20, command=qb).pack(pady=20)
        # user notification
        note_frame = ttk.Frame(
            master=results_frame, 
            bootstyle=SECONDARY, 
            padding=40
        )
        note_frame.pack(fill=BOTH)
        
        note_msg = ttk.Label(
            master=note_frame, 
            text='All in one finger spelling software and a data analytics tool to gauge students performance and packed with puzzle games too!!', 
            anchor=CENTER,
            font=('Helvetica', 12, 'italic'),
            bootstyle=(INVERSE, SECONDARY)
        )
        note_msg.pack(fill=BOTH)

        def know_more_clicked(event):
            import webbrowser
            instructions = (
                    "https://github.com/scalabli/peritia/blob/main/docs/instructions.md")

            webbrowser.open_new_tab(instructions)

        know_more = ttk.Label(
                master=note_msg,
                text="Click here for instructions"
              #  cursor="hand2"
                )
               # ibg="#3A7FF6", fg="white", cursor="hand2")
        know_more.pack(padx=20, pady=(40,0))#place(x=27, y=400)
        know_more.bind('<Button-1>', know_more_clicked)


if __name__ == '__main__':

    app = ttk.Window("Peritia:  All in one assistive software", "vapor")
    Cleaner(app)
    app.mainloop()
