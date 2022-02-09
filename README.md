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


### quo.echo
**Example 1**
```python
   import quo

   quo.echo(f"Hello, World!", fg="red", italic=True, bold=True))
```
![Hello World](https://github.com/secretum-inc/quo/raw/master/pics/print.png)

**Example 2**
```python
   import quo

   quo.echo(f"Quo is ", nl=False)
   quo.echo(f"scalable", bg="red", fg="black") 
```
![Scalable](https://github.com/secretum-inc/quo/raw/master/pics/scalable.png)

Unlike the builtin print function, ``echo`` function has improved support for handling Unicode and binary data.
It also supports handling of ANSI color sequences.

### quo.prompt
```python
   import quo

   quo.prompt("What is your name?")
```
![quo.prompt](https://github.com/secretum-inc/quo/raw/master/pics/prompt.png)

### quo.Prompt
```python
   import quo
   
   session = quo.Prompt(bottom_toolbar="Python 🐍 is great")
   session.prompt("Type something:") 
```
![quo.Prompt.prompt](https://github.com/secretum-inc/quo/raw/master/docs/images/prompt2.png)

### Quo autocompletion
```python
   # Press [Tab] to autocomplete
   import quo

   completer = quo.completion.WordCompleter(['USA', 'UK', 'Canada', 'Kenya'])
   session = quo.Prompt(completer=completer)
   session.prompt('Which country are you from?: ')
```
![Autocompletion](https://github.com/secretum-inc/quo/raw/master/docs/images/autocompletion.png)

### Quo frame
```python
  
   import quo

   def frame():
    """ Example of a simple layout"""
   content = quo.widgets.TextArea(text="Hello world🌍")
   quo.container(
        quo.widgets.Frame(
            content,
            title="Quo: python🐍"))

   if __name__ == "__main__":
       frame()
```
![Frame](https://github.com/secretum-inc/quo/raw/master/docs/images/print_frame.png)

### Message Box
Example of a message box window.
```python
   import quo

   def main():
       quo.MessageBox(
           title="Message pop up window",
           text="Do you want to continue?\nPress ENTER to quit.").run()                                       

   if __name__ == "__main__":
      main()
```
![Message Box](https://github.com/secretum-inc/quo/raw/master/docs/images/messagebox.png)


### Prompt Box
Example of an prompt box window
```python
   import quo

   def main():
       result = quo.PromptBox(
                    title="PromptBox shenanigans",
                    text="What Country are you from?:").run()

       quo.echo(f"Result = {result}")

   if __name__ == "__main__":
       main()
```
![Prompt Box](https://github.com/secretum-inc/quo/raw/master/docs/images/promptbox.png)

### Quo tabular
```python
   import quo

   table = [
     ["Name", "Gender", "Age"],
     ["Alice", "F", 24],
     ["Bob", "M", 19],
     ["Dave", "M", 24]
   ]
   tabular = quo.tabular
   quo.echo(tabular(table))
```
![tabulate](https://github.com/secretum-inc/quo/raw/master/pics/tabulate.png)
   


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
