__title__="Add Name\nRoom"
__doc__ = 'Cut Category form Void Cut'
__author__ = 'Phuc'
# -*- coding: utf-8 -*-

import Autodesk
from Autodesk.Revit.DB import XYZ ,FilteredElementCollector, BuiltInCategory, Outline, BoundingBoxIntersectsFilter, LogicalAndFilter, ElementCategoryFilter, Transaction, InstanceVoidCutUtils
from pyrevit import revit, DB, script, forms
from rpw.ui.forms import FlexForm, Label, TextBox, Button, ComboBox, CheckBox, Separator,Alert
import rpw
from rpw import DB,ui
from rpw.ui.forms import SelectFromList
from pyrevit.forms import ProgressBar

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

def MmToFeet(mm):
    ConvertFeetToMillimeters = 12 * 25.4
    return mm / ConvertFeetToMillimeters

def GetTextNoteIntersectWithElement(element, doc,saiSo):
    allTextNote = FilteredElementCollector(doc, doc.ActiveView.Id).OfCategory(BuiltInCategory.OST_TextNotes).WhereElementIsNotElementType().ToElements()
    box = element.get_BoundingBox(doc.ActiveView)
    minPoint = XYZ(box.Min.X - MmToFeet(saiSo), box.Min.Y - MmToFeet(saiSo), 0)
    maxPoint = XYZ(box.Max.X + MmToFeet(saiSo), box.Max.Y + MmToFeet(saiSo), 0)
    outlineElement = Outline(minPoint, maxPoint)

    listTextNote = []
    for text in allTextNote:
        box2 = text.get_BoundingBox(doc.ActiveView)
        minPoint = XYZ(box2.Min.X, box2.Min.Y, 0)
        maxPoint = XYZ(box2.Max.X, box2.Max.Y, 0)
        outlineText = Outline(minPoint, maxPoint)

        b = outlineElement.intersection(outlineText, 0.001)
        if b==True:
            listTextNote.append(text)
    return listTextNote



