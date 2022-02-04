
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
   commands.rst
   apps.rst
   args.rst
   confirm.rst.
   printing_text.rst
   prompt.rst
   exceptions.rst
   dialogs.rsr
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
   help_text.rst
   filters.rst
   full_screen_apps.rst
   kb.rst
   progress_bars.rst
   syntax.rst
   styling.rst
   tables.rst
   utils.rst
   tree.rst

   protocol.rst

   changes.rst
   reference.rst
   unicode-support.rst
   appendix.rst

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
