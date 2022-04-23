from quo.text.core import AnyFormattedText as RichText

def Frame(title: RichText = None, text: RichText = None, height=None, width=None):
    from quo.widget.core import Frame, TextArea
    from quo.shortcuts.utils import container
    return container(Frame(TextArea(text=text, height=height, width=width),title=title))
