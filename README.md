<h1>Quo <img src="https://media.giphy.com/media/12oufCB0MyZ1Go/giphy.gif" width="50"></h2>



---

Quo is a Python  based module for writing Command-Line Interface(CLI) applications.

---

[![quo](pics/quo.png)](https://github.com/secretuminc/quo)

---
</p> 
<a href="https://pypi.org/project/quo/"><img src="https://img.shields.io/static/v1?label=&labelColor=505050&message=website&color=%230076D6&style=flat&logo=google-chrome&logoColor=%230076D6" alt="Documentation"/></a>
<a href="https://github.com/viewerdiscretion/quo/stargazers"><img src="https://img.shields.io/github/stars/viewerdiscretion/quo" alt="Stars Badge"/></a>
<a href="https://github.com/viewerdiscretion/quo/network/members"><img src="https://img.shields.io/github/forks/viewerdiscretion/quo" alt="Forks Badge"/></a>
<a href="https://github.com/viewerdiscretion/quo/pulls"><img src="https://img.shields.io/github/issues-pr/viewerdiscretion/quo" alt="Pull Requests Badge"/></a>
<a href="https://github.com/viewerdiscretion/quo/issues"><img src="https://img.shields.io/github/issues/viewerdiscretion/quo" alt="Issues Badge"/></a>
<a href="https://github.com/viewerdiscretion/quo/graphs/contributors"><img alt="GitHub contributors" src="https://img.shields.io/github/contributors/viewerdiscretion/quo?color=2b9348"></a>
<a href="https://github.com/viewerdiscretion/quo/blob/master/LICENSE"><img src="https://img.shields.io/github/license/viewerdiscretion/quo?color=2b9348" alt="License Badge"/></a>

[![PyPI version](https://img.shields.io/pypi/v/quo.svg?logo=pypi&logoColor=FFE873)](https://pypi.org/project/quo/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/quo.svg?logo=python&logoColor=FFE873)](https://pypi.org/project/quo/)
[![PyPI downloads](https://img.shields.io/pypi/dm/quo.svg)](https://quo.rtfd.io)
[![Travis CI status](https://img.shields.io/travis/secretum/quo/master?label=Travis%20CI&logo=travis)](https://travis-ci.org/secretum/quo)
[![Azure Pipelines status](https://dev.azure.com/hugovk/hugovk/_apis/build/status/hugovk.pypistats?branchName=master)](https://dev.azure.com/hugovk/hugovk/_build?definitionId=1)
[![codecov](https://codecov.io/gh/secretum/quo/branch/master/graph/badge.svg)](https://codecov.io/gh/secretuminc/quo)
[![GitHub](https://img.shields.io/github/license/secretuminc/quo.svg)](LICENSE.txt)
[![DOI](https://zenodo.org/badge/149862343.svg)](https://zenodo.org/badge/latestdoi/149862343)
[![Code style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![Twitter Follow](https://img.shields.io/twitter/follow/gerrishon_s?label=Follow)
[![Linkedin: anmol](https://img.shields.io/badge/-Gerrishon-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/gerrishonsirere/)](https://www.linkedin.com/in/gerrishonsirere/)
![](https://visitor-badge.glitch.me/badge?page_id=viewerdiscretion.quo)

---

Quo improves programmer's productivity because it's easy to use and supports auto completion which means less time will be spent debugging. Simple to code, easy to learn, and does not come with needless baggage.

---

---

**Quo📄** : <a href="https://quo.rtfd.io" class="external-link" target="_blank">Documentation</a>

---

## Requirements

Python 2.7+

## Installation

<div class="termy">

```console
Install
$ pip install quo

or install and update
$ pip install -U quo
🔸🔸🔸🔸🔸💯 
Quo has been installed successfully🎉 
```

</div>

## Example

### Example 1

* Create a  file `test.py` 

```Python
import quo
quo.echo(f'Hello Gerry')

```

* Run the application
```console
$ python test.py

```

### Example2
* `test.py`

```Python
import quo 
    @quo.command()
    @quo.option("--count", default=1, help="The number of times the feedback is printed.")
    @quo.option("--name", prompt="What is your name", help="This prompts the user to input their name.")
    @quo.option("--profession", prompt="What is your profession", help="This prompts user to input their proffession")
    def survey(count, name, proffession):
       
        for _ in range(count):
            quo.echo(f"Thank you for your time, {name}!")

    if __name__ == '__main__':
        survey() 
// A simple survey application
```

## Shell

Quo can detect the current Python executable is running in.

```Python

    import quo
    quo.shelldetector()
```

``shelldetector`` pokes around the process's running environment to determine
what shell it is run in. ``ShellDetectionFailure`` is raised if ``shelldetector`` fails to detect the
surrounding shell.

## Contributing

If you run into an issue or want to contribute, we would be very happy if you would file a bug on the [issue tracker](https://github.com/viewerdiscretion/quo/issues).

## Donate
In order to for me to maintain this project, `please consider donating today` 

* <a href="https://www.buymeacoffee.com/gerrishon" target="_blank"><img src="https://res.cloudinary.com/edev/image/upload/v1583011476/button_y8hgt8.png" alt="Donate" style="width: 250px !important; height: 60px !important;" width="250" height="60"></a>
* <a href="https://PayPal.me/gerrishon" target="_blank"><img src="https://raw.githubusercontent.com/aha999/DonateButtons/master/Paypal.png" alt="Donate" style="width: 250px !important; height: 60px !important;" width="250" height="60"></a>

