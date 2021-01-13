<h1>Quo <img src="https://media.giphy.com/media/12oufCB0MyZ1Go/giphy.gif" width="50"></h2>



---

Quo is a Python based toolkit for creating Command-Line Interface (CLI) applications. Quo improves programmer's productivity because it's easy to use and supports auto completion which means less time will be spent debugging.

---

<a href="https://viewerdiscretion.github.io/quo"><img src="https://miro.medium.com/max/1400/1*SGa8qRilRIMzAM0PO2U-0Q.png" alt="Quo"></a>
</p> 
<a href="https://pypi.org/project/quo/"><img src="https://img.shields.io/static/v1?label=&labelColor=505050&message=website&color=%230076D6&style=flat&logo=google-chrome&logoColor=%230076D6" alt="Documentation"/></a>
<a href="https://github.com/viewerdiscretion/quo/stargazers"><img src="https://img.shields.io/github/stars/viewerdiscretion/quo" alt="Stars Badge"/></a>
<a href="https://github.com/viewerdiscretion/quo/network/members"><img src="https://img.shields.io/github/forks/viewerdiscretion/quo" alt="Forks Badge"/></a>
<a href="https://github.com/viewerdiscretion/quo/pulls"><img src="https://img.shields.io/github/issues-pr/viewerdiscretion/quo" alt="Pull Requests Badge"/></a>
<a href="https://github.com/viewerdiscretion/quo/issues"><img src="https://img.shields.io/github/issues/viewerdiscretion/quo" alt="Issues Badge"/></a>
<a href="https://github.com/viewerdiscretion/quo/graphs/contributors"><img alt="GitHub contributors" src="https://img.shields.io/github/contributors/viewerdiscretion/quo?color=2b9348"></a>
<a href="https://github.com/viewerdiscretion/quo/blob/master/LICENSE"><img src="https://img.shields.io/github/license/viewerdiscretion/quo?color=2b9348" alt="License Badge"/></a>

![Twitter Follow](https://img.shields.io/twitter/follow/gerrishon_s?label=Follow)
[![Linkedin: anmol](https://img.shields.io/badge/-Gerrishon-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/gerrishonsirere/)](https://www.linkedin.com/in/gerrishonsirere/)
![](https://visitor-badge.glitch.me/badge?page_id=viewerdiscretion.quo)

---

**Quo📄** : <a href="https://quodocs.netlify.com" class="external-link" target="_blank">Documentation</a>

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

* Create a  file `test.py` 

```Python
import quo
quo.secho(f'Hello Gerry', fg='black', bg='cyan')

```

* Run the application
```console
$ python test.py

// Usage: quo.secho() bg=Background color, fg=Foreground color
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

## Donate
In order to for me to maintain this project, `please consider donating today` 

* <a href="https://www.buymeacoffee.com/gerrishon" target="_blank"><img src="https://res.cloudinary.com/edev/image/upload/v1583011476/button_y8hgt8.png" alt="Donate" style="width: 250px !important; height: 60px !important;" width="250" height="60"></a>
* <a href="https://PayPal.me/gerrishon" target="_blank"><img src="https://raw.githubusercontent.com/aha999/DonateButtons/master/Paypal.png" alt="Donate" style="width: 250px !important; height: 60px !important;" width="250" height="60"></a>

