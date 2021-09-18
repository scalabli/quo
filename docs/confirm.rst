Confirm
========
To ask if a user wants to continue with an action, the :func:`confirm` function comes in handy.  By default, it returns the result of the prompt as a boolean value:

.. code:: python

   from quo import confirm
   
   confirm("Do you want to continue?")                                            
