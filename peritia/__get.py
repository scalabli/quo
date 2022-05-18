def _get_text():
    global entr
    string= entry.get()
    label.configure(text=string)
    print(entry.get())
