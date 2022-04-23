from quo import container
from quo.keys import bind
from quo.layout import Float, CompletionsMenu
from quo.widget import Label
from quo.widget import MenuContainer, MenuItem


def do_it():
    return "me it is"


@bind.add("ctrl-c")
def _(event):
    event.app.exit()


content = Label("Hello, World")



content = MenuContainer(
        body=content,
        menu_items=[
            MenuItem("File",
                subset=[
                    MenuItem("Fine", handler=do_it)
                    ]
                )],
            floats=[
                Float(
                    xcursor=True,
                    ycursor=True,
                    content=CompletionsMenu(max_height=16, scroll_offset=1)
                )],
                bind=bind)

container(content, bind=True, full_screen=True)


