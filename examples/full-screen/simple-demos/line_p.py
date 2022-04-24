#!/usr/bin/env python
"""
An example of a BufferControl in a full screen layout that offers auto
completion.

Important is to make sure that there is a `CompletionsMenu` in the layout,
otherwise the completions won't be visible.
"""
from quo import container
from quo.console import Console
from quo.buffer import Buffer
from quo.completion import WordCompleter
from quo.filters import Condition
from quo.text import Text
from quo.keys import KeyBinder
from quo.layout.containers import Float, FloatContainer, HSplit, Window
from quo.layout.controls import BufferControl, FormattedTextControl
from quo.layout.layout import Layout
from quo.layout.menus import CompletionsMenu

#wrap_lines = True

def dd(message):
    message = ""
    def get_line_prefix(lineno, wrap_count):
        if wrap_count == 0:
            return Text('[%s] <style bg="orange" fg="black">--&gt;</style> ') % lineno

        text = str(lineno) + "-" + "*" * (lineno // 2) + ": "
        return Text('[%s.%s] <style bg="green" fg="black">%s</style>') % (
                lineno,
                wrap_count,
                text,)

    kb = KeyBinder()
    wl= True
    buff = Buffer(complete_while_typing=True)
    buff.text = message #

    wrap_lines = True
    body = FloatContainer(
            content=HSplit(
                [
                    Window(
                        FormattedTextControl(
                            'Press "q" to quit. Press "w" to enable/disable wrapping.'
                    ),
                        height=1,
                        style="reverse",
                        ),
                    Window(
                        BufferControl(buffer=buff),
                        get_line_prefix=get_line_prefix,
                        wrap_lines=Condition(lambda: wl),
                        ),
                    ]
                ),
    floats=[
        Float(
            xcursor=True,
            ycursor=True,
            content=CompletionsMenu(max_height=16, scroll_offset=1),
            )
        ],
    )


    @kb.add("q")
    @kb.add("ctrl-c")

    def _(event):
        "Quit application."
        event.app.exit()

    @kb.add("w")
    def _(event):
        "Disable/enable wrapping."
        global wrap_lines
        wrap_lines = not wrap_lines

        # The `Application`
    Console(
            layout=Layout(body),
            bind=kb,
            full_screen=True,
            mouse_support=True).run()




LIPSUM = """
Quo is a Python based toolkit for writing Command-Line Interface(CLI) applications. Quo is making headway towards composing speedy and orderly CLI applications while forestalling any disappointments brought about by the failure to execute a CLI API. Simple to code, easy to learn, and does not come with needless baggage.\n"""

def get_line_prefix(lineno, wrap_count):
    if wrap_count == 0:
        return Text('[%s] <style bg="orange" fg="black">--&gt;</style> ') % lineno

    text = str(lineno) + "-" + "*" * (lineno // 2) + ": "
    return Text('[%s.%s] <style bg="green" fg="black">%s</style>') % (
        lineno,
        wrap_count,
        text,
    )


# Global wrap lines flag.
#wrap_lines = True


# The layout
#buff = Buffer(complete_while_typing=True)
#buff.text = message # LIPSUM


#body = FloatContainer(
   # content=HSplit(
#        [
    #        Window(
    #            FormattedTextControl(
   #                 'Press "q" to quit. Press "w" to enable/disable wrapping.'
#                ),
 #   2            height=1,
  #              style="reverse",
  #          ),
   #         Window(
    #            BufferControl(buffer=buff),
     #           get_line_prefix=get_line_prefix,
 #               wrap_lines=Condition(lambda: wrap_lines),
   #         ),
   #     ]
#    ),
#    floats=[
#        Float(
#            xcursor=True,
 #           ycursor=True,
 #           content=CompletionsMenu(max_height=16, scroll_offset=1),
 #       )
#    ],
#)


# Key bindings
#kb = KeyBinder()


#@kb.add("q")
#@kb.add("ctrl-c")
#def _(event):
 #   "Quit application."
 #   event.app.exit()


#@kb.add("w")
#def _(event):
 #   "Disable/enable wrapping."
#    global wrap_lines
 #   wrap_lines = not wrap_lines
#

# The `Application`
#nsole(
#        layout=Layout(body),
#        bind=kb,
  #      full_screen=True, 
   #     mouse_support=True).run()
