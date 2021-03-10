<h1>Quo <img src="https://media.giphy.com/media/12oufCB0MyZ1Go/giphy.gif" width="50"></h2>



---

Quo is a Python  based module for writing Command-Line Interface(CLI) applications.

---
<p align="center">
  <a href="https://quo.rtfd.io"><img src="https://miro.medium.com/max/1400/1*wXEkk8gS6FMrBC-mJvVekQ.png" alt="Quo"></a>
</p
---


[![PyPI version](https://img.shields.io/pypi/v/quo.svg?logo=pypi&logoColor=FFE873)](https://pypi.org/project/quo/)
[![Documentation Status](https://readthedocs.org/projects/quo/badge/?version=latest)](https://quo.readthedocs.io/en/latest/?badge=latest)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/quo.svg?logo=python&logoColor=FFE873)](https://pypi.org/project/quo/)
[![Travis CI status](https://img.shields.io/travis/secretum/quo/master?label=Travis%20CI&logo=travis)](https://travis-ci.org/secretum/quo)
[![codecov](https://codecov.io/gh/secretum/quo/branch/master/graph/badge.svg)](https://codecov.io/gh/secretuminc/quo)
[![GitHub](https://img.shields.io/github/license/secretuminc/quo.svg)](LICENSE.txt)
[![quo](https://snyk.io/advisor/python/quo/badge.svg)](https://snyk.io/advisor/python/quo)

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

## Contributing

If you run into an issue or want to contribute, we would be very happy if you would file a bug on the [issue tracker](https://github.com/viewerdiscretion/quo/issues).

## Donate
In order to for me to maintain this project, `please consider donating today` 

* <a href="https://www.paypal.com/donate?hosted_button_id=KLUFPDX7RT3SY" target="_blank"><img src="https://res.cloudinary.com/edev/image/upload/v1583011476/button_y8hgt8.png" alt="Donate" style="width: 250px !important; height: 60px !important;" width="250" height="60"></a>
* <a href="https://PayPal.me/gerrishon" target="_blank"><img src="https://raw.githubusercontent.com/aha999/DonateButtons/master/Paypal.png" alt="Donate" style="width: 250px !important; height: 60px !important;" width="250" height="60"></a>

