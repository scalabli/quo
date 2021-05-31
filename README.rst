

.. image:: https://raw.githubusercontent.com/secretum-inc/quo/main/pics/quo.png

===========================
 Quo
===========================

|build-status| |coverage| |license| |wheel| |pyversion| |pyimp|

:Version: 2.1.0
:Web: http://quo.readthedocs.io/
:Download: http://pypi.org/project/quo
:Source: http://github.com/secretum-inc/quo
:Keywords: distributed, stream, async, processing, data, queue, state management


.. sourcecode:: python

    # Quo
    # Forever scalable

**Quo** is a Python based toolkit for writing Command-Line Interface(CLI) applications.



Quo requires Python 3.6 or later for the new `async/await`_ syntax,
and variable type annotations.

Here's an example processing a stream of incoming orders:

.. sourcecode:: python

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
  @quo.decree()
  @quo.option("--name", prompt="What is your name?:")
  def hello(name):
  quo.echo(f'Hello {name}!')
  if __name__ == '__main__':
      hello() 


**Example 4**

.. sourcecode:: python

    import quo 
    @quo.decree()
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


**Highly Available**
    Faust is highly available and can survive network problems and server
    crashes.  In the case of node failure, it can automatically recover,
    and tables have standby nodes that will take over.

**Distributed**
    Start more instances of your application as needed.

**Fast**
    A single-core Faust worker instance can already process tens of thousands
    of events every second, and we are reasonably confident that throughput will
    increase once we can support a more optimized Kafka client.

**Flexible**
    Faust is just Python, and a stream is an infinite asynchronous iterator.
    If you know how to use Python, you already know how to use Faust,
    and it works with your favorite Python libraries like Django, Flask,
    SQLAlchemy, NTLK, NumPy, SciPy, TensorFlow, etc.

.. _`introduction`: http://faust.readthedocs.io/en/latest/introduction.html

.. _`quickstart`: http://faust.readthedocs.io/en/latest/playbooks/quickstart.html

.. _`User Guide`: http://faust.readthedocs.io/en/latest/userguide/index.html


Installation
============

You can install Faust either via the Python Package Index (PyPI)
or from source.

To install using `pip`:

.. sourcecode:: console

    $ pip install -U faust

.. _bundles:

Bundles
-------

Faust also defines a group of ``setuptools`` extensions that can be used
to install Faust and the dependencies for a given feature.

You can specify these in your requirements or on the ``pip``
command-line by using brackets. Separate multiple bundles using the comma:

.. sourcecode:: console

    $ pip install "faust[rocksdb]"

    $ pip install "faust[rocksdb,uvloop,fast,redis]"

The following bundles are available:

Stores
~~~~~~

:``faust[rocksdb]``:
    for using `RocksDB`_ for storing Faust table state.

    **Recommended in production.**


.. _`RocksDB`: http://rocksdb.org

Caching
~~~~~~~

:``faust[redis]``:
    for using `Redis_` as a simple caching backend (Memcached-style).

Codecs
~~~~~~

:``faust[yaml]``:
    for using YAML and the ``PyYAML`` library in streams.

Optimization
~~~~~~~~~~~~

:``faust[fast]``:
    for installing all the available C speedup extensions to Faust core.

Sensors
~~~~~~~

:``faust[datadog]``:
    for using the Datadog Faust monitor.

:``faust[statsd]``:
    for using the Statsd Faust monitor.

Event Loops
~~~~~~~~~~~

:``faust[uvloop]``:
    for using Faust with ``uvloop``.

:``faust[eventlet]``:
    for using Faust with ``eventlet``

Debugging
~~~~~~~~~

:``faust[debug]``:
    for using ``aiomonitor`` to connect and debug a running Faust worker.

:``faust[setproctitle]``:
    when the ``setproctitle`` module is installed the Faust worker will
    use it to set a nicer process name in ``ps``/``top`` listings.
    Also installed with the ``fast`` and ``debug`` bundles.

Downloading and installing from source
--------------------------------------

Download the latest version of Faust from
http://pypi.org/project/faust

You can install it by doing:

.. sourcecode:: console

    $ tar xvfz faust-0.0.0.tar.gz
    $ cd faust-0.0.0
    $ python setup.py build
    # python setup.py install

The last command must be executed as a privileged user if
you are not currently using a virtualenv.

Using the development version
-----------------------------

With pip
~~~~~~~~

You can install the latest snapshot of Faust using the following
``pip`` command:

.. sourcecode:: console

    $ pip install https://github.com/robinhood/faust/zipball/master#egg=faust

.. _`introduction`: http://faust.readthedocs.io/en/latest/introduction.html

.. _`quickstart`: http://faust.readthedocs.io/en/latest/playbooks/quickstart.html

.. _`User Guide`: http://faust.readthedocs.io/en/latest/userguide/index.html

FAQ
===

Can I use Faust with Django/Flask/etc.?
---------------------------------------

Yes! Use ``eventlet`` as a bridge to integrate with ``asyncio``.


Using ``eventlet``
~~~~~~~~~~~~~~~~~~~~~~

This approach works with any blocking Python library that can work with
``eventlet``.

Using ``eventlet`` requires you to install the ``aioeventlet`` module,
and you can install this as a bundle along with Faust:

.. sourcecode:: console

    $ pip install -U faust[eventlet]

Then to actually use eventlet as the event loop you have to either
use the ``-L <faust --loop>`` argument to the ``faust`` program:

.. sourcecode:: console

    $ faust -L eventlet -A myproj worker -l info

or add ``import mode.loop.eventlet`` at the top of your entry point script:

.. sourcecode:: python

    #!/usr/bin/env python3
    import mode.loop.eventlet  # noqa

.. warning::

    It's very important this is at the very top of the module,
    and that it executes before you import libraries.

Can I use Faust with Tornado?
-----------------------------

Yes! Use the ``tornado.platform.asyncio`` bridge:
http://www.tornadoweb.org/en/stable/asyncio.html

Can I use Faust with Twisted?
-----------------------------

Yes! Use the ``asyncio`` reactor implementation:
https://twistedmatrix.com/documents/17.1.0/api/twisted.internet.asyncioreactor.html

Will you support Python 2.7 or Python 3.5?
------------------------------------------

No. Faust requires Python 3.6 or later, since it heavily uses features that were
introduced in Python 3.6 (`async`, `await`, variable type annotations).

I get a maximum number of open files exceeded error by RocksDB when running a Faust app locally. How can I fix this?
--------------------------------------------------------------------------------------------------------------------

You may need to increase the limit for the maximum number of open files. The
following post explains how to do so on OS X:
https://blog.dekstroza.io/ulimit-shenanigans-on-osx-el-capitan/


What kafka versions faust supports?
---------------------------------------

Faust supports kafka with version >= 0.10.

.. _`introduction`: http://faust.readthedocs.io/en/latest/introduction.html

.. _`quickstart`: http://faust.readthedocs.io/en/latest/playbooks/quickstart.html

.. _`User Guide`: http://faust.readthedocs.io/en/latest/userguide/index.html

.. _getting-help:

Getting Help
============

.. _slack-channel:

Slack
-----

For discussions about the usage, development, and future of quo,
please join the `secretum-inc`_ Gitter.

* https://gitter.im/secretum-inc
* Join: https://gitter.im/secretum-inc/quo

Resources
=========

.. _bug-tracker:

Bug tracker
-----------

If you have any suggestions, bug reports, or annoyances please report them
to our issue tracker at https://github.com/secretum-inc/quo/issues/

.. _license:

License
=======

This software is licensed under the `MIT License`. See the ``LICENSE``
file in the top distribution directory for the full license text.

.. # vim: syntax=rst expandtab tabstop=4 shiftwidth=4 shiftround

.. _`introduction`: http://faust.readthedocs.io/en/latest/introduction.html

.. _`quickstart`: http://faust.readthedocs.io/en/latest/playbooks/quickstart.html

.. _`User Guide`: http://faust.readthedocs.io/en/latest/userguide/index.html


Code of Conduct
===============

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
    :target: https://codecov.io/github/robinhood/faust?branch=master

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

