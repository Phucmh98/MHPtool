__title__="Delete\nSheet"
__doc__ = 'Delete Sheets by seleted sheet'
__author__ = 'Phuc'

import Autodesk
from Autodesk.Revit.DB import  *
from Autodesk.Revit.UI.Selection import *
import rpw
from rpw import DB,ui
from pyrevit import forms


doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

dest_sheets = forms.select_sheets(include_placeholder=False)

t = Transaction(doc, "Delete Sheets")
t.Start()
for i in dest_sheets:
    delete = doc.Delete(i.Id)
t.Commit()