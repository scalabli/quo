def TextField(text=None, prompt=None, hide=False, highlighter=None, scrollbar=False):
    from quo.shortcuts.utils import container
    from quo.widget import TextArea

    content = TextArea(prompt=prompt, hide=hide, highlighter=highlighter, scrollbar=scrollbar)
    return container(content, bind=True)
