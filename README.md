<h1>Quo <img src="https://media.giphy.com/media/12oufCB0MyZ1Go/giphy.gif" width="50"></h2>



---

Quo is a Python  based toolkit for writing Command-Line Interface(CLI) applications.

---
<p align="center">
  <a href="https://quo.rtfd.io"><img src="https://miro.medium.com/max/1400/1*wXEkk8gS6FMrBC-mJvVekQ.png" alt="Quo"></a>
</p
---

[![Supported Python versions](https://img.shields.io/pypi/pyversions/quo.svg?logo=python&logoColor=FFE873)](https://pypi.org/project/quo/)
[![Travis CI status](https://img.shields.io/travis/secretum/quo/master?label=Travis%20CI&logo=travis)](https://travis-ci.org/secretum-inc/quo)
[![codecov](https://codecov.io/gh/secretum-inc/quo/branch/master/graph/badge.svg)](https://codecov.io/gh/secretum-inc/quo)
[![GitHub](https://img.shields.io/github/license/secretum-inc/quo.svg)](LICENSE.txt)
[![quo](https://snyk.io/advisor/python/quo/badge.svg)](https://snyk.io/advisor/python/quo)



<table>
    <tr>
        <th>docs</th>
        <td>
            <a href="https://quo.readthedocs.io/?badge=latest"><img
                alt="Documentation Status"
                src="https://readthedocs.org/projects/quo/badge/?version=latest"></a>
        </td>
    </tr>
    <tr>
        <th>tests</th>
        <td>
            <a href="https://github.com/secretum-inc/quo/actions?query=workflow%3A%22Test+Windows%22"><img
                alt="GitHub Actions build status (Test Windows)"
                src="https://github.com/secretum-inc/quo/workflows/Test%20Windows/badge.svg"></a>
            <a href="https://github.com/python-pillow/Pillow/actions?query=workflow%3A%22Test+Docker%22"><img
                alt="GitHub Actions build status (Test Docker)"
                src="https://github.com/python-pillow/Pillow/workflows/Test%20Docker/badge.svg"></a>
            <a href="https://ci.appveyor.com/project/python-pillow/Pillow"><img
                alt="AppVeyor CI build status (Windows)"
                src="https://img.shields.io/appveyor/build/python-pillow/Pillow/master.svg?label=Windows%20build"></a>
            <a href="https://github.com/python-pillow/pillow-wheels/actions"><img
                alt="GitHub Actions wheels build status (Wheels)"
                src="https://github.com/python-pillow/pillow-wheels/workflows/Wheels/badge.svg"></a>
            <a href="https://travis-ci.com/github/python-pillow/pillow-wheels"><img
                alt="Travis CI wheels build status (aarch64)"
                src="https://img.shields.io/travis/com/python-pillow/pillow-wheels/master.svg?label=aarch64%20wheels"></a>
            <a href="https://codecov.io/gh/python-pillow/Pillow"><img
                alt="Code coverage"
                src="https://codecov.io/gh/secretum-inc/quo/branch/master/graph/badge.svg"></a>
        </td>
    </tr>
    <tr>
        <th>package</th>
        <td>
            <a href="https://zenodo.org/badge/latestdoi/17549/secretum-inc/quo"><img
                alt="Zenodo"
                src="https://zenodo.org/badge/17549/python-pillow/Pillow.svg"></a>
            <a href="https://pypi.org/project/quo/"><img
                alt="Newest PyPI version"
                src="https://img.shields.io/pypi/v/quo.svg"></a>
            <a href="https://pypi.org/project/quo/"><img
                alt="Number of PyPI downloads"
                src="https://img.shields.io/pypi/dm/quo.svg"></a>
        </td>
    </tr>
    <tr>
        <th>social</th>
        <td>
            <a href="https://gitter.im/secretum-inc/quo?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge"><img
                alt="Join the chat at https://gitter.im/secretum-inc/quo"
                src="https://badges.gitter.im/secretum-inc/quo.svg"></a>
            <a href="https://twitter.com/gerrishon_s"><img
                alt="Follow on https://twitter.com/gerrishon_s"
                src="https://img.shields.io/badge/tweet-on%20Twitter-00aced.svg"></a>
        </td>
    </tr>
</table>

---

Quo improves programmer's productivity because it's easy to use and supports auto completion which means less time will be spent debugging. Simple to code, easy to learn, and does not come with needless baggage.

---

---

**Quo📄** : <a href="https://quo.rtfd.io" class="external-link" target="_blank">Documentation</a>

---

## Requirements

Python 3.6+

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

* Create a  file `test1.py` 

```Python
import quo
quo.echo(f'Hi there')

```

### Example 2
`test2.py`

```Python
import quo
quo.flair(f'This is colorful', bg="red", fg="white")

```

### Example 3

`test3.py`

```Python
import quo
@quo.decree()
@quo.option("--name", prompt="What is your name?:") 
def hello(name):
   quo.echo(f'Hello {name}!')

if __name__ == '__main__':
    hello() 

```

### Example2
* `test.py`

```Python
import quo 
    @quo.decree()
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

* <a href="https://www.paypal.com/donate?hosted_button_id=KP893BC2EKK54" target="_blank"><img src="https://res.cloudinary.com/edev/image/upload/v1583011476/button_y8hgt8.png" alt="Donate" style="width: 250px !important; height: 60px !important;" width="250" height="60"></a>

