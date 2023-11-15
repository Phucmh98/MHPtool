__title__="Casework Column by Wall"
__doc__ = 'Change Heigth Casework form Wall'
__author__ = 'Phuc'


import Autodesk
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Outline, BoundingBoxIntersectsFilter, LogicalAndFilter, ElementCategoryFilter, Transaction, InstanceVoidCutUtils
from pyrevit import revit, DB, script, forms
from rpw.ui.forms import FlexForm, Label, TextBox, Button, ComboBox, CheckBox, Separator,Alert
import rpw
from rpw import DB,ui
from rpw.ui.forms import SelectFromList
from pyrevit.forms import ProgressBar
import deletewarning
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

#filter column to run
allClToRun = FilteredElementCollector(doc, doc.ActiveView.Id).OfCategory(BuiltInCategory.OST_StructuralColumns).WhereElementIsNotElementType().ToElements()
#print(allClToRun)

t = Transaction(doc, "Py: New Change Void Cut")
t.Start()
for cl in allClToRun:
    #filter category wall
    
    categoryFilter_wall = ElementCategoryFilter(BuiltInCategory.OST_Walls)
    #intersect wall and column
    box = cl.get_BoundingBox(doc.ActiveView)
    outline = Outline(box.Min, box.Max)
    bbFilter = BoundingBoxIntersectsFilter(outline)
    #logicalAndFilter
    
    logicalAndFilter_wall = LogicalAndFilter(bbFilter, categoryFilter_wall)
    print(logicalAndFilter_wall)
    
    
    #FILTER wall intersect column
    
    allWalls =FilteredElementCollector(doc).WherePasses(logicalAndFilter_wall).ToElements()
    print(allWalls)

    eleid_Wall = allWalls[0].Id
    print(eleid_Wall)
    ele_wall = doc.GetElement(eleid_Wall)
    ###Parameter wall
    param_wall_base = ele_wall.LookupParameter("Base Offset").AsDouble()
    
    print(param_wall_base)
    param_wall_top = ele_wall.LookupParameter("Top Offset").AsDouble()
    print(param_wall_top)
    param_wall_top_constraint=ele_wall.LookupParameter("Top Constraint").AsValueString()
    print(param_wall_top_constraint)
    new_str = param_wall_top_constraint.strip('Up to level: ')
    print(new_str)

    ###Parameter column
    eleid_Column = cl.Id
    ele_Column = doc.GetElement(eleid_Column)

    param_Column_base = ele_Column.LookupParameter("Base Offset")
    param_Column_base.Set(param_wall_base)
    param_Column_top = ele_Column.LookupParameter("Top Offset")
    param_Column_top.Set(param_wall_top)
    param_Column_top_constraint = ele_Column.LookupParameter("Top Level")
    param_Column_top_constraint.Set(new_str)

t.Commit()

Alert('{} Void Cut Success'.format(len(allClToRun)), title="Element Changed", header="Complete")