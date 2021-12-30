echo
=====
This function prints a message plus a newline to the given file or stdout. On first sight, this looks like the print function, but it has improved support for handling Unicode and binary data.

Supported color names:

* ``black (might be a gray)``
* ``red``
* ``green``
* ``yellow`` *(might be an orange)*
* ``blue``
* ``magenta``
* ``cyan``
* ``white`` *(might be light gray)*
* ``vblack``  *vibrant black*
* ``vblue``
* ``vmagenta``
* ``vwhite``
* ``vcyan``
* ``vred``
* ``vgreen``
* ``vyellow``

RGB color codes


Parameters
   * ``text`` – the string to style with ansi codes.

   * ``fg``  – if provided this will become the foreground color.

   * ``bg``  – if provided this will become the background color.

   * ``bold``  – if provided this will enable or disable bold mode.

   * ``dim``  – if provided this will enable or disable dim mode.

   * ``nl`` - if provided this will print a new line.

   * ``ul or underline`` – if provided this will enable or disable underline

   * ``italic`` - if provided this will print data in italics

   * ``blink`` – if provided this will enable or disable blinking.

   * ``strike`` -if provided this will print a strikethrough text

   * ``hidden`` - if privided this will prevent the input from getting printed

   * ``reverse`` – if provided this will enable or disable inverse rendering (foreground becomes background and the other way round).

   * ``reset``  – by default a reset-all code is added at the end of the string which means that styles do not carry over. This can be disabled to compose styles.
