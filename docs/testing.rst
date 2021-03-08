Testing Quo Applications
==========================

.. currentmodule:: quo.testing

We provide the :mod:`quo.testing` module which will help you to test and configure your application.

It is advisable to only use these tools in a virtual environment

Basic Testing
-------------

The basic functionality for testing quo applications is the
:class:`CliRunner` which can invoke commands as command line scripts.  The
:meth:`CliRunner.invoke` method runs the command line script in isolation
and captures the output as both bytes and binary data.

The return value is a :class:`Result` object, which has the captured output
data, exit code, and optional exception attached:

.. code-block:: python
   :caption: hello.py

   import quo

   @quo.command()
   @quo.argument('name')
   def hello(name):
      quo.echo(f'Hello {name}!')

.. code-block:: python
   :caption: test_hello.py

   from quo.testing import CliRunner
   from hello import hello

   def test_hello_world():
     runner = CliRunner()
     result = runner.invoke(hello, ['Peter'])
     assert result.exit_code == 0
     assert result.output == 'Hello Peter!\n'

For subcommand testing, a subcommand name must be specified in the `args` parameter of :meth:`CliRunner.invoke` method:

.. code-block:: python
   :caption: sync.py

   import quo

   @quo.group()
   @quo.option('--debug/--no-debug', default=False)
   def cli(debug):
      quo.echo(f"Debug mode is {'on' if debug else 'off'}")

   @cli.command()
   def sync():
      quo.echo('Syncing')

.. code-block:: python
   :caption: test_sync.py

   from quo.testing import CliRunner
   from sync import cli

   def test_sync():
     runner = CliRunner()
     result = runner.invoke(cli, ['--debug', 'sync'])
     assert result.exit_code == 0
     assert 'Debug mode is on' in result.output
     assert 'Syncing' in result.output

Additional keyword arguments passed to ``.invoke()`` will be used to construct the initial Context object.
For example, if you want to run your tests against a fixed terminal width you can use the following::

    runner = CliRunner()
    result = runner.invoke(cli, ['--debug', 'sync'], terminal_width=60)

File System Isolation
---------------------

For basic command line tools with file system operations, the
:meth:`CliRunner.isolated_filesystem` method is useful for setting the
current working directory to a new, empty folder.

.. code-block:: python
   :caption: cat.py

   import quo

   @quo.command()
   @quo.argument('f', type=quo.File())
   def cat(f):
      quo.echo(f.read())

.. code-block:: python
   :caption: test_cat.py

   from quo.testing import CliRunner
   from cat import cat

   def test_cat():
      runner = CliRunner()
      with runner.isolated_filesystem():
         with open('hello.txt', 'w') as f:
             f.write('Hello World!')

         result = runner.invoke(cat, ['hello.txt'])
         assert result.exit_code == 0
         assert result.output == 'Hello World!\n'

Input Streams
-------------

The test wrapper can also be used to provide input data for the input
stream (stdin).  This is very useful for testing prompts, for instance:

.. code-block:: python
   :caption: prompt.py

   import quo

   @quo.command()
   @quo.option('--foo', prompt=True)
   def prompt(foo):
      quo.echo(f"foo={foo}")

.. code-block:: python
   :caption: test_prompt.py

   from quo.testing import CliRunner
   from prompt import prompt

   def test_prompts():
      runner = CliRunner()
      result = runner.invoke(prompt, input='wau wau\n')
      assert not result.exception
      assert result.output == 'Foo: wau wau\nfoo=wau wau\n'

Note that prompts will be emulated so that they write the input data to
the output stream as well.  If hidden input is expected then this
obviously does not happen.
