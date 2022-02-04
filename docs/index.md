[![Logo](https://raw.githubusercontent.com/secretum-inc/quo/master/pics/quo.png)](https://github.com/secretum-inc/quo)


`Forever Scalable`

**Quo** is a Python based toolkit for writing Command-Line Interface(CLI) applications.
Quo is making headway towards composing speedy and orderly CLI applications while forestalling any disappointments brought about by the failure to execute a CLI API.
Simple to code, easy to learn, and does not come with needless baggage. 

Quo requires Python `3.8` or later. 


- [x] `Support for Ansi, RGB and HTML color models`
- [x] `Support for tabular presentation of data`
- [x] `Interactive progressbars`
- [x] `Code completions`
- [x] `Nesting of commands`
- [x] `Automatic help page generation`
- [x] `Syntax highlighting`
- [x] `Autosuggestions`
- [x] `Key Binders`

# Quo is...

**Simple**
     If you know Python you can  easily use Quo and it can integrate with just about anything.

```{toctree}
:maxdepth: 2
:caption: Tutorials & Explanations
introduction
utils
commands.rst
apps.rst
args.rst
printing_text.rst
prompt.rst
exceptions.rst
dialogs.rs
full_screen_apps.rst
kb.rst
progress
filters.rst
styling
help_text.rst
changes.rst
reference.rst
unicode-support.rst
appendix.rst
```
   
## Donate🎁

In order to for us to maintain this project and grow our community of contributors.
[Donate](https://www.paypal.com/donate?hosted_button_id=KP893BC2EKK54)



## Getting Help

### Community

For discussions about the usage, development, and the future of quo, please join our Google community

* [Community👨‍👩‍👦‍👦](https://groups.google.com/forum/#!forum/secretum)

## Resources

### Bug tracker

If you have any suggestions, bug reports, or annoyances please report them
to our issue tracker at 
[Bug tracker](https://github.com/secretum-inc/quo/issues/) or send an email to:

 📥 secretum@googlegroups.com


## License📑

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)  
This software is licensed under the `MIT License`. See the [License](https://github.com/secretum-inc/quo/blob/master/LICENSE) file in the top distribution directory for the full license text.



## Example

### Create it

* Create a file `main.py` with:

```Python
from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
```

<details markdown="1">
<summary>Or use <code>async def</code>...</summary>

If your code uses `async` / `await`, use `async def`:

```Python hl_lines="9  14"
from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
```


..

.. image:: https://raw.githubusercontent.com/secretum-inc/quo/main/pics/quo.png

Quo's Documentation
================================
:Version: 2022.x
:Web: http://quo.readthedocs.io/
:Download: http://pypi.org/project/quo
:Source: http://github.com/secretum-inc/quo



.. toctree::
   :maxdepth: 2
   :caption: Contents:

   introduction.rst
   
   confirm.rst.
   
   r
   terminal.rst
   style.rst
   markup.rst
   text.rst
   highlighting.rst
   pretty.rst
   logging.rst
   traceback.rst

   columns.rst
   padding.rst
   panel.rst
   
   progress_bars.rst
   syntax.rst
   styling.rst
   tables.rst
   utils.rst
   tree.rst

   protocol.rst

   

Support
========
Subscribe to one of our mailing lists to stay up to date with everything in the Quo community:

  `Community👨‍👩‍👦‍👦 <https://groups.google.com/g/secretum/>`_

You can also subscribe by sending an email to secretum+subscribe@googlegroups.com

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
