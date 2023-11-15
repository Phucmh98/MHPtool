__title__="Add Name\nRoom"
__doc__ = 'Cut Category form Void Cut'
__author__ = 'Phuc'
# -*- coding: utf-8 -*-

import Autodesk
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Outline, BoundingBoxIntersectsFilter, LogicalAndFilter, ElementCategoryFilter, Transaction, InstanceVoidCutUtils
from pyrevit import revit, DB, script, forms
from rpw.ui.forms import FlexForm, Label, TextBox, Button, ComboBox, CheckBox, Separator,Alert
import rpw
from rpw import DB,ui
from rpw.ui.forms import SelectFromList
from pyrevit.forms import ProgressBar
import GetTextNoteIntersectWithElement

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# theme Dictionary



allRoomToRun = FilteredElementCollector(doc, doc.ActiveView.Id).OfCategory(BuiltInCategory.OST_Rooms).WhereElementIsNotElementType().ToElements()
print(allRoomToRun)
#max_value = len(allGenToRun)


    
#t = Transaction(doc, "Py: New Add Parameter")
#t.Start()
for room in allRoomToRun:
    textNote = room.GetTextNoteIntersectWithElement(room,doc.ActiveView.Id, 50)
    print(textNote)
    
  
#t.Commit()

