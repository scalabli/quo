class Rule:
    def __init__(self, height:int = 1, char: str="\u2501"):
        self.height= height
        self.char = char

       
    def draw(self, color:str="aquamarine", multicolored:bool=False):
        if multicolored:
            import os
            from termcolor import colored

            # Get the width of the terminal
            width = os.get_terminal_size().columns

            # Define a list of colors
            colorList = ['red', 'yellow', 'green', 'cyan', 'blue', 'magenta']

            # Initialize a variable to keep track of the current color index
            colorIndex = 0

            # Draw the line, with each character a different color
            for i in range(width):
                # Get the current color from the list
                selectedColor = colorList[colorIndex]
                # Print the current character in the current color
                print(colored(self.char, selectedColor), end='')
                # Increment the color index
                colorIndex = (colorIndex + 1) % len(colorList)
    
            # Print a newline to move to the next line
            print()

        else:
            from quo.layout.containers import Window
            from quo.shortcuts.utils import container
            container(Window(char=self.char, height=self.height, style="fg:" +color),bind=False)


