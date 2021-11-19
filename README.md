[![Downloads](https://pepy.tech/badge/quo)](https://pepy.tech/project/quo)
[![PyPI version](https://badge.fury.io/py/quo.svg)](https://badge.fury.io/py/quo)
[![Wheel](https://img.shields.io/pypi/wheel/quo.svg)](https://pypi.com/project/quo)
[![Windows Build Status](https://img.shields.io/appveyor/build/gerrishons/quo/master?logo=appveyor&cacheSeconds=600)](https://ci.appveyor.com/project/gerrishons/quo)
[![pyimp](https://img.shields.io/pypi/implementation/quo.svg)](https://pypi.com/project/quo)
[![RTD](https://readthedocs.org/projects/quo/badge/)](https://quo.readthedocs.io)
[![licence](https://img.shields.io/pypi/l/quo.svg)](https://opensource.org/licenses/MIT)
[![Twitter Follow](https://img.shields.io/twitter/follow/gerrishon_s.svg?style=social)](https://twitter.com/gerrishon_s)


[![Logo](https://raw.githubusercontent.com/secretum-inc/quo/master/pics/quo.png)](https://github.com/secretum-inc/quo)


`Forever Scalable`

**Quo** is a Python based toolkit for writing Command-Line Interface(CLI) applications.
Quo is making headway towards composing speedy and orderly CLI applications while forestalling any disappointments brought about by the failure to execute a CLI API.
Simple to code, easy to learn, and does not come with needless baggage. 

Quo requires Python `3.6.1` or later. 


## Features
- Support for ANSI and RGB color models
- Support for tabular presentation of data
- Interactive progressbars
- Code completions
- Nesting of commands
- Automatic help page generation
- Highlighting
- Lightweight

## Getting Started
### Installation
You can install quo via the Python Package Index (PyPI)

```
pip install -U quo
```


### Quo print
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

### Quo prompt
```python
   import quo

   quo.prompt("What is your name?")
```
![prompt](https://github.com/secretum-inc/quo/raw/master/pics/prompt.png)

### Quo log
```python
   import quo

   console = quo.Console()
   console.log("Quo status")

```

### Quo tabular
```python
   import quo


   table = [
     ["Name", "Gender", "Age"],
     ["Alice", "F", 24],
     ["Bob", "M", 19],
     ["Dave", "M", 24]
   ]

   quo.echo(quo.tabular(table))
```
![tabulate](https://github.com/secretum-inc/quo/raw/master/pics/tabulate.png)
   
### Quo Status
```python
   from time import sleep
    
   import quo

   console = quo.Console()

   tasks = [f"task {n}" for n in range(1, 11)]
   quo.echo(f"Working on tasks...", fg="green", bold=True)
   with console.status("[bold green] ",) as status:
       while tasks:
           task = tasks.pop(0)
           sleep(1)
           console.log(f"{task} complete")
```

![Status](https://github.com/secretum-inc/quo/raw/master/pics/status.gif)


For more intricate  examples, have a look in the [tutorials](https://github.com/secretum-inc/quo/tree/master/tutorials) directory and the documentation.

## Donate🎁

In order to for us to maintain this project and grow our community of contributors.
[Donate](https://www.paypal.com/donate?hosted_button_id=KP893BC2EKK54)



## Quo is...

**Simple**
     If you know Python you can  easily use quo and it can integrate with just about anything.




## Getting Help

### Gitter

For discussions about the usage, development, and future of quo, please join our Gitter community

* [Join](https://gitter.im/secretum-inc/quo)

## Resources

### Bug tracker

If you have any suggestions, bug reports, or annoyances please report them
to our issue tracker at 
[Bug tracker](https://github.com/secretum-inc/quo/issues/)


## License📑

This software is licensed under the `MIT License`. See the [License](https://github.com/secretum-inc/quo/blob/master/LICENSE) file in the top distribution directory for the full license text.


## Code of Conduct
Code of Conduct is adapted from the Contributor Covenant,
version 1.2.0 available at
[Code of Conduct](http://contributor-covenant.org/version/1/2/0/)

