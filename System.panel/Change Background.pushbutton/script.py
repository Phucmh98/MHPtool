# -*- coding: utf-8 -*-
__title__   = "Change\nBackground"
__author__ = "Phuc"

__doc__ = """
Click on the button to switch Black/Gray/White background colour in Revit.
"""

# IMPORTS
from Autodesk.Revit.DB import Color

# VARIABLES
app = __revit__.Application

# MAIN
if __name__ == '__main__':
    # COLOURS
    Black = Color(0, 0, 0)
    White = Color(255, 255, 255)
    Gray = Color(210, 210, 210)
    current_color = app.BackgroundColor

    if current_color.Blue == 255 and current_color.Red == 255 and current_color.Green == 255:
        app.BackgroundColor = Black
    elif current_color.Blue == 0 and current_color.Red == 0 and current_color.Green == 0:
        app.BackgroundColor = Gray
    else:
        app.BackgroundColor = White