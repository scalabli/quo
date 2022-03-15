#!/usr/bin/env python
"""
A simple example of a calculator program.
This could be used as inspiration for a REPL.
"""
from quo import Console
from quo.document import Document
from quo.keys import Bind
from quo.widget import SearchToolbar, TextArea
from quo.layout import Layout, Window, HSplit
from quo.text import Text

help_text = """
Type any expression (e.g. "4 + 4") followed by enter to execute.
Press Control-C to exit.
"""


def main():
    # The layout.
    search_field = SearchToolbar()  # For reverse search.

    output_field = TextArea(f'{help_text}', style="bg:blue fg:yellow bold")
         #   tyle="class:output-field", text=help_text)
    input_field = TextArea(
        height=2,
        prompt=">>",
        style="bg:green", #class:input-field",
        multiline=False,
        wrap_lines=False,
        search_field=search_field,
    )

    container = HSplit(
        [
            output_field,
            Window(height=1, char="-", style="fg:magenta"),
            input_field,
            search_field,
        ]
    )

    # Attach accept handler to the input field. We do this by assigning the
    # handler to the `TextArea` that we created earlier. it is also possible to
    # pass it to the constructor of `TextArea`.
    # NOTE: It's better to assign an `accept_handler`, rather then adding a
    #       custom ENTER key binding. This will automatically reset the input
    #       field and add the strings to the history.
    def accept(buff):
        # Evaluate "calculator" expression.
        try:
            output = "\n\nIn:  {}\nOut: {}".format(
                input_field.text, eval(input_field.text)
            )  # Don't do 'eval' in real code!
        except BaseException as e:
            output = "\n\n{}".format(e)
        new_text = output_field.text + output

        # Add text to output buffer.
        output_field.buffer.document = Document(
            text=new_text, cursor_position=len(new_text)
        )

    input_field.accept_handler = accept

    # The key bindings.
    bind = Bind()

    @bind.add("ctrl-c")
    @bind.add("ctrl-q")
    def _(event):
        "Pressing Ctrl-Q or Ctrl-C will exit the user interface."
        event.app.exit()

    layout = Layout(container, focused_element=input_field)


    # Run application.
    Console(
            layout=layout,
            bind=bind,
            mouse_support=True,
            full_screen=True,
            ).run()

if __name__ == "__main__":
    main()
