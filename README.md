[![Downloads](https://pepy.tech/badge/quo)](https://pepy.tech/project/quo)
[![PyPI version](https://badge.fury.io/py/quo.svg)](https://badge.fury.io/py/quo)
[![Wheel](https://img.shields.io/pypi/wheel/quo.svg)](https://pypi.com/project/quo)
[![Windows Build Status](https://img.shields.io/appveyor/build/gerrishons/quo/master?logo=appveyor&cacheSeconds=600)](https://ci.appveyor.com/project/gerrishons/quo)
[![pyimp](https://img.shields.io/pypi/implementation/quo.svg)](https://pypi.com/project/quo)
[![RTD](https://readthedocs.org/projects/quo/badge/)](https://quo.readthedocs.io)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5848515.svg)](https://doi.org/10.5281/zenodo.5848515)
[![licence](https://img.shields.io/pypi/l/quo.svg)](https://opensource.org/licenses/MIT)
[![Twitter Follow](https://img.shields.io/twitter/follow/gerrishon_s.svg?style=social)](https://twitter.com/gerrishon_s)


[![Logo](https://raw.githubusercontent.com/secretum-inc/quo/master/pics/quo.png)](https://github.com/secretum-inc/quo)


`Forever Scalable`

**Quo** is a Python based toolkit for writing Command-Line Interface(CLI) applications.
Quo is making headway towards composing speedy and orderly CLI applications while forestalling any disappointments brought about by the failure to execute a CLI API.
Simple to code, easy to learn, and does not come with needless baggage. 

## Compatibility
Quo works flawlessly  with Linux, OSX, and Windows.
Quo requires Python `3.8` or later. 


## Features
- [x] Support for Ansi, RGB and HTML color models
- [x] Support for tabular presentation of data
- [x] Interactive progressbars
- [x] Code completions
- [x] Nesting of commands
- [x] Automatic help page generation
- [x] Syntax highlighting
- [x] Autosuggestions
- [x] Key Binders

## Getting Started
### Installation
You can install quo via the Python Package Index (PyPI)

```
pip install -U quo

```
Run the following to test Quo output on your terminal:
                                                           ```
python -m quo

```
To output formatted text to your terminal you can import the [echo](https://quo.readthedocs.io/en/latest/introduction.html) method.
Try this:

**Example 1**
```python
   from quo import echo

   echo(f"Hello, World!", fg="red", italic=True, bold=True))
```
![Hello World](https://github.com/secretum-inc/quo/raw/master/pics/print.png)

**Example 2**
```python
   from quo import echo

   echo(f"Quo is ", nl=False)
   echo(f"scalable", bg="red", fg="black") 
```
![Scalable](https://github.com/secretum-inc/quo/raw/master/pics/scalable.png)


### Quo prompt
```python
   from quo import prompt

   prompt("What is your name?")
```
![quo.prompt](https://github.com/secretum-inc/quo/raw/master/pics/prompt.png)

### quo.Prompt toolbar
```python
   from quo.prompt import Prompt
   
   session = Prompt(bottom_toolbar="Python 🐍 is great")
   session.prompt("Type something:") 
```
![quo.Prompt.prompt](https://github.com/secretum-inc/quo/raw/master/docs/images/prompt2.png)

### Quo autocompletion
```python
   # Press [Tab] to autocomplete
   from quo.prompt import Prompt
   from quo.completion import WordCompleter

   example = WordCompleter(['USA', 'UK', 'Canada', 'Kenya'])
   session = Prompt(completer=example)
   session.prompt('Which country are you from?: ')
```
![Autocompletion](https://github.com/secretum-inc/quo/raw/master/docs/images/autocompletion.png)

### Using the Console
For more control over quo terminal content, import and construct a [Console](https://quo.readthedocs.io/en/latest/console.html) object.

```python

  from quo import Console

  console = Console()
```
The Console object has a `print` method which has an intentionally similar interface to the builtin `print` function. Here's an example of use:

### Quo frame
```python
  
   from quo import container
   from quo.widgets import Frame, TextArea

   # Example of a simple layout
   content = TextArea(text="Hello world🌍")
   container(
        Frame(
            content,
            title="Quo: python🐍"))

```
![Frame](https://github.com/secretum-inc/quo/raw/master/docs/images/print_frame.png)

<details>
<summary>Progress</summary>
Creating a new progress bar can be done by calling the class [ProgressBar](https://quo.readthedocs.io/en/latest/progress.html)
The progress can be displayed for any iterable. This w
orks by wrapping the iterable (like ``range``) with the class `ProgressBar`.

```python

   import time
   from quo.progress import ProgressBar
  
   with ProgressBar() as pb:
                 for i in pb(range(800)):
                               time.sleep(.01)
```
![Progress]( https://raw.githubusercontent.com/secretum-inc/quo/master/docs/pics/simplepb.png)
</details>

<details>
<summary>Key Binding</summary>
A key binding is an association between a physical key on a keyboard and a parameter.

```python
  
   from quo import echo
   from quo.prompt import Prompt
   from quo.keys import KeyBinder
  
   kb = KeyBinder()
   # Print "Hello world" when ctrl-h is pressed
   @kb.add("ctrl-h")
   def _(event):
       echo("Hello, World!")
   session.prompt(">>", bind=kb)
```
</details>

<details>
<summary>Dialog</summary>
High level API for displaying [dialog](https://quo.readthedocs.io/en/latest/dialogs.html) boxes to the user for informational purposes, or get input fromthe user.

1) Example of a message box dialog.
```python

   from quo.dialog import MessageBox

   MessageBox(
           title="Message pop up window",
           text="Do you want to continue?\nPress ENTER to quit.").run()                                       
```
The above produces the following output
![Message Box](https://github.com/secretum-inc/quo/raw/master/docs/images/messagebox.png)

2) Example of a prompt box dialog
```python
   from quo.dialog import PromptBox

   PromptBox(
             title="PromptBox shenanigans",
             text="What Country are you from?:").run()

```
![Prompt Box](https://github.com/secretum-inc/quo/raw/master/docs/images/promptbox.png)

</details>

<details>
<summary>Table</summary>

Function [Table](https://quo.readthedocs.io/en/latest/table.html) offers a number of configuration options to set the look and feel of the table, including how borders are rendered and the style and alignment of the columns.

Example
```python
   from quo import echo
   from quo.table import Table

   data = [
     ["Name", "Gender", "Age"],
     ["Alice", "F", 24],
     ["Bob", "M", 19],
     ["Dave", "M", 24]
   ]
   echo(Table(data))
```
![tabulate](https://github.com/secretum-inc/quo/raw/master/pics/tabulate.png)
</details>

<details>
<summary>Widgets</summary>
A collection of reusable components for building full screen applications.

## ``Label``
Widget that displays the given text. It is not editable or focusable.
```python

   from quo import Console
   from quo.widget import Label
   from quo.keys import KeyBinder
   from quo.layout import Layout
   from quo.style import Style

   # Styling for the label
   example_style = Style(                                 [
        ("hello-world", "bg:red fg:black")
        ] 
          )
   root = Label("Hello, World", style="class:hello-world")
  
   layout = Layout(container=root)
  
   # Ctrl-c to exit
   kb = KeyBinder()
  
   @kb.add("ctrl-c")
   def _(event):
      event.app.exit()

   Console(
       layout=layout,
       bind=kb,
       style=example_style
       full_screen=True).run()

```
Read more on [Widgets](https://quo.readthedocs.io/en/latest/widgets.html)

</details>

For more intricate  examples, have a look in the [examples](https://github.com/secretum-inc/quo/tree/master/examples) directory and the documentation.

## Donate🎁

In order to for us to maintain this project and grow our community of contributors.
[Donate](https://www.paypal.com/donate?hosted_button_id=KP893BC2EKK54)



## Quo is...

**Simple**
     If you know Python you can  easily use quo and it can integrate with just about anything.




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


## Code of Conduct
Code of Conduct is adapted from the Contributor Covenant,
version 1.2.0 available at
[Code of Conduct](http://contributor-covenant.org/version/1/2/0/)
