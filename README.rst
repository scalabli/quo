

.. image:: https://raw.githubusercontent.com/secretum-inc/quo/main/pics/quo.png

===========================
 Quo
===========================

|build-status| |coverage| |license| |wheel| |pyversion| |pyimp|

:Version: 2.1.0
:Web: http://quo.readthedocs.io/
:Download: http://pypi.org/project/quo
:Source: http://github.com/secretum-inc/quo


.. sourcecode:: python

    # Quo
    # Forever scalable

**Quo** is a Python based toolkit for writing Command-Line Interface(CLI) applications.
Quo improves programmer's productivity because it's easy to use and supports auto completion which means less time will be spent debugging. Simple to code, easy to learn, and does not come with needless baggage

Quo requires Python 3.6 or later. 

Installation
============
You can install quo via the Python Package Index (PyPI)

.. sourcecode:: console

    $ pip install -U quo

**Example 1**

.. sourcecode:: python

    import quo
    quo.echo('Hello, World!')
    

**Example 2**

.. sourcecode:: python

  import quo
  quo.flair(f'Hello, World!', fg="red", bold=True)


**Example 3**

.. sourcecode:: python

  import quo
  @quo.command()
  @quo.option("--name", prompt="What is your name?:")
  def hello(name):
  quo.echo(f'Hello {name}!')
  if __name__ == '__main__':
      hello() 


**Example 4**

.. sourcecode:: python

    import quo 
    @quo.command()
    @quo.option("--count", default=1, help="The number of times the feedback is printed.")
    @quo.option("--name", prompt="What is your name", help="This prompts the user to input their name.")
    @quo.option("--profession", prompt="What is your profession", help="This prompts user to input their proffession")
    def survey(count, name, proffession):
       
        for _ in range(count):
            quo.echo(f"Thank you for your time, {name}!")

    if __name__ == '__main__':
        survey



Donate
=======

In order to for us to maintain this project and grow our community of contributors, `please consider donating today`_.

.. _please consider donating today: https://www.paypal.com/donate?hosted_button_id=KP893BC2EKK54



Quo is...
===========

**Simple**
     If you know Python you can  easily use quo and it can integrate with just about anything.


.. _`introduction`: http://faust.readthedocs.io/en/latest/introduction.html

.. _`quickstart`: http://faust.readthedocs.io/en/latest/playbooks/quickstart.html

.. _`User Guide`: http://faust.readthedocs.io/en/latest/userguide/index.html



Getting Help
=============

.. _gitter-channel:

Gitter
-------

For discussions about the usage, development, and future of quo,
please join our Gitter community

* https://gitter.im/secretum-inc
* Join: https://gitter.im/secretum-inc/quo

Resources
==========

.. _bug-tracker:

Bug tracker
------------

If you have any suggestions, bug reports, or annoyances please report them
to our issue tracker at https://github.com/secretum-inc/quo/issues/

.. _license:

License
========

This software is licensed under the `MIT License`. See the ``LICENSE``
file in the top distribution directory for the full license text.

.. # vim: syntax=rst expandtab tabstop=4 shiftwidth=4 shiftround

.. _`introduction`: http://quo.readthedocs.io/en/latest/introduction.html

.. _`quickstart`: http://quo.readthedocs.io/en/latest/playbooks/quickstart.html

.. _`User Guide`: http://quo.readthedocs.io/en/latest/userguide/index.html


Code of Conduct
================

Everyone interacting in the project's code bases, issue trackers, chat rooms,
and mailing lists is expected to follow the Faust Code of Conduct.

As contributors and maintainers of these projects, and in the interest of fostering
an open and welcoming community, we pledge to respect all people who contribute
through reporting issues, posting feature requests, updating documentation,
submitting pull requests or patches, and other activities.

We are committed to making participation in these projects a harassment-free
experience for everyone, regardless of level of experience, gender,
gender identity and expression, sexual orientation, disability,
personal appearance, body size, race, ethnicity, age,
religion, or nationality.

Examples of unacceptable behavior by participants include:

* The use of sexualized language or imagery
* Personal attacks
* Trolling or insulting/derogatory comments
* Public or private harassment
* Publishing other's private information, such as physical
  or electronic addresses, without explicit permission
* Other unethical or unprofessional conduct.

Project maintainers have the right and responsibility to remove, edit, or reject
comments, commits, code, wiki edits, issues, and other contributions that are
not aligned to this Code of Conduct. By adopting this Code of Conduct,
project maintainers commit themselves to fairly and consistently applying
these principles to every aspect of managing this project. Project maintainers
who do not follow or enforce the Code of Conduct may be permanently removed from
the project team.

This code of conduct applies both within project spaces and in public spaces
when an individual is representing the project or its community.

Instances of abusive, harassing, or otherwise unacceptable behavior may be
reported by opening an issue or contacting one or more of the project maintainers.

This Code of Conduct is adapted from the Contributor Covenant,
version 1.2.0 available at http://contributor-covenant.org/version/1/2/0/.

.. _`introduction`: http://faust.readthedocs.io/en/latest/introduction.html

.. _`quickstart`: http://faust.readthedocs.io/en/latest/playbooks/quickstart.html

.. _`User Guide`: http://faust.readthedocs.io/en/latest/userguide/index.html

.. |build-status| image:: https://secure.travis-ci.org/secretum-inc/quo.png?branch=master
    :alt: Build status
    :target: https://travis-ci.org/secretum-inc/quo

.. |coverage| image:: https://codecov.io/github/secretum-inc/quo/coverage.svg?branch=master
    :target: https://codecov.io/github/secretum-inc/quo?branch=main

.. |license| image:: https://img.shields.io/pypi/l/quo.svg
    :alt: MIT License
    :target: https://opensource.org/licenses/MIT

.. |wheel| image:: https://img.shields.io/pypi/wheel/quo.svg
    :alt: quo can be installed via wheel
    :target: http://pypi.org/project/quo/

.. |pyversion| image:: https://img.shields.io/pypi/pyversions/quo.svg
    :alt: Supported Python versions.
    :target: http://pypi.org/project/quo/

.. |pyimp| image:: https://img.shields.io/pypi/implementation/quo.svg
    :alt: Support Python implementations.
    :target: http://pypi.org/project/quo/

.. _`introduction`: http://faust.readthedocs.io/en/latest/introduction.html

.. _`quickstart`: http://faust.readthedocs.io/en/latest/playbooks/quickstart.html

.. _`User Guide`: http://faust.readthedocs.io/en/latest/userguide/index.html

