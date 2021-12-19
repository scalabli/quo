#!/usr/bin/env python
"""
A simple example of a calculator program.
This could be used as inspiration for a REPL.
"""
import quo
from quo.document import Document
from quo.filters import has_focus
from quo.styles import Style

help_text = """
Type any expression (e.g. "4 + 4") followed by enter to execute.
Press Control-C to exit.
"""


def main():
    # The layout.
    search_field = quo.widgets.SearchToolbar()  # For reverse search.

    output_field = quo.widgets.TextArea(style="class:output-field", text=help_text)
    input_field = quo.widgets.TextArea(
        height=2,
        prompt="▶️ ",
        style="class:input-field",
        multiline=False,
        wrap_lines=False,
        search_field=search_field,
    )

    container = quo.layout.HSplit(
        [
            output_field,
            quo.layout.Window(height=1, char="-", style="class:line"),
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
    kb = quo.keys.KeyBinder()

    @kb.add("ctrl-c")
    @kb.add("ctrl-q")
    def _(event):
        "Pressing Ctrl-Q or Ctrl-C will exit the user interface."
        event.app.exit()

    # Style.
    style = Style(
        [
            ("output-field", "bg:#000044 #ffffff"),
            ("input-field", "bg:#000000 #ffffff"),
            ("line", "#004400"),
        ]
    )

    # Run application.
    application = quo.Suite(
        layout=quo.layout.Layout(container, focused_element=input_field),
        key_bindings=kb,
        style=style,
        mouse_support=True,
        full_screen=True,
    )

    application.run()


if __name__ == "__main__":
    main()
