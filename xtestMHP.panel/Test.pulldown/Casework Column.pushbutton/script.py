__title__="Casework Column"
__doc__ = 'Change Heigth Casework form Wall'
__author__ = 'Phuc'


import Autodesk
from Autodesk.Revit.DB import BuiltInParameter, FilteredElementCollector, BuiltInCategory, Outline, BoundingBoxIntersectsFilter, LogicalAndFilter, ElementCategoryFilter, Transaction, InstanceVoidCutUtils
from Autodesk.Revit.DB.RevitLinkInstance import GetLinkDocument 
from pyrevit import revit, DB, script, forms
from rpw.ui.forms import FlexForm, Label, TextBox, Button, ComboBox, CheckBox, Separator,Alert
import rpw
from rpw import DB,ui
from rpw.ui.forms import SelectFromList,TextInput
from pyrevit.forms import ProgressBar
import deletewarning
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

value = TextInput('Change Height Casework By Revit Link', default="-50",description="Distance between 2 Levels (mm)", sort=True, exit_on_close=True)

revit_link_select = revit.get_selection().first



doc_revitlink=revit_link_select.GetLinkDocument()


print(doc_revitlink)


#filter column to run222222222
allClToRun = FilteredElementCollector(doc, doc.ActiveView.Id).OfCategory(BuiltInCategory.OST_StructuralColumns).WhereElementIsNotElementType().ToElements()
#print(allClToRun)

t = Transaction(doc, "Py: New Change Void Cut")
t.Start()
for cl in allClToRun:
    #filter category wall
    
    categoryFilter_floor = ElementCategoryFilter(BuiltInCategory.OST_Floors)
    #intersect wall and column
    box = cl.get_BoundingBox(doc.ActiveView)
    outline = Outline(box.Min, box.Max)
    bbFilter = BoundingBoxIntersectsFilter(outline)
    #logicalAndFilter
    
    logicalAndFilter_floor = LogicalAndFilter(bbFilter, categoryFilter_floor)
    print(logicalAndFilter_floor)
    
    
    #FILTER wall intersect column
    
    allFloor =FilteredElementCollector(doc_revitlink).WherePasses(logicalAndFilter_floor).ToElements()
    print(allFloor)
    

    eleid_Floor = allFloor[0].Id
    print(eleid_Floor)
    ele_Floor = doc_revitlink.GetElement(eleid_Floor)
    print(ele_Floor)
    ###Parameter wall
    param_floor_thickness = ele_Floor.get_Parameter(BuiltInParameter.FLOOR_ATTR_THICKNESS_PARAM).AsDouble()
    print(param_floor_thickness)
    
    
    # param_wall_top = ele_wall.LookupParameter("Top Offset").AsDouble()
    # print(param_wall_top)
    # param_wall_top_constraint=ele_wall.LookupParameter("Top Constraint").AsValueString()
    # print(param_wall_top_constraint)
    # new_str = param_wall_top_constraint.strip('Up to level: ')
    # print(new_str)

    ###Parameter column
    eleid_Column = cl.Id
    ele_Column = doc.GetElement(eleid_Column)

    # param_Column_base = ele_Column.LookupParameter("Base Offset")
    # param_Column_base.Set(param_wall_base)
    param_Column_top = ele_Column.get_Parameter(BuiltInParameter.SCHEDULE_TOP_LEVEL_OFFSET_PARAM)
    param_Column_top.Set((float(value)/304.8)-param_floor_thickness)
    # param_Column_top_constraint = ele_Column.LookupParameter("Top Level")
    # param_Column_top_constraint.Set(new_str)

t.Commit()

Alert('{} Void Cut Success'.format(len(allClToRun)), title="Element Changed", header="Complete")