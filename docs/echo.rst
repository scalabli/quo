echo
=====
**quo.echo** *(message=None, file=None, n
l=True, err=False, color=None)*
This function prints a message plus a newline to the given file or stdout. On first sight, this looks like the print function, but it has improved support for handling Unicode and binary data.

If colorama is installed, the echo function will also support clever handling of ANSI color codes.

Supported color names:

* ``black (might be a gray)``
* ``red``                                                                                                   * ``green``                                                                                                 * ``yellow`` *(might be an orange)*                                                                         * ``blue``                                                                                                  * ``magenta``                                                                                               * ``cyan``                                                                                                  * ``white`` *(might be light gray)*                                                                         * ``vblack``  *vibrant black*                                                                               * ``vred``                                                                                                  * ``vgreen``                                                                                                * ``vyellow``                                         -- INSERT --



Parameters
   * ``message`` – the message to print

   * ``file`` – the file to write to (defaults to stdout)

   * ``err`` – if set to true the file defaults to stderr instead of stdout. This is faster and easier than calling get_text_stderr() yourself.

   * ``nl`` – if set to True (the default) a newline is printed afterwards.

   * ``color`` – controls if the terminal supports ANSI colors or not. The default is autodetection.
