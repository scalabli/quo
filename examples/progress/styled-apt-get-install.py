#!/usr/bin/env python
"""
Styled just like an apt-get installation.
"""
import time

from quo.progress import ProgressBar



    #custom_formatters = [
     #   formatters.Label(),
      #  formatters.Text(": [", style="class:percentage"),
       # formatters.Percentage(),
        #formatters.Text("]", style="class:percentage"),
        #ormatters.Text(" "),
        #formatters.Bar(sym_a="#", sym_b="#", sym_c="."),
        #formatters.Text("  "),


with ProgressBar() as pb:
    for i in pb(range(1600), label="Installing"):
        time.sleep(0.01)


