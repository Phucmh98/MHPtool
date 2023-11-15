__title__="Casework Column"
__doc__ = 'Change Heigth Casework form Wall'
__author__ = 'Phuc'


import Autodesk
from Autodesk.Revit.DB import Outline,ElementFilter,BuiltInParameter, FilteredElementCollector, BuiltInCategory, Outline, BoundingBoxIntersectsFilter, LogicalAndFilter, ElementCategoryFilter, Transaction, InstanceVoidCutUtils
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


#print(doc_revitlink)


#filter column to run222222222
allFlToRun = FilteredElementCollector(doc_revitlink).OfCategory(BuiltInCategory.OST_Floors).WhereElementIsNotElementType().ToElements()
#print(allClToRun)

t = Transaction(doc, "Py: New Change Void Cut")
t.Start()
for fl in allFlToRun:
    #filter category wall
    
    
    #intersect wall and column
    fl_id = fl.Id
    #print(fl_id)
    get_fl_Id = doc_revitlink.GetElement(fl_id)
    box = get_fl_Id.get_BoundingBox(doc.ActiveView)
    #print(box)
    
    param_floor_thickness = get_fl_Id.LookupParameter("Thickness")
    if param_floor_thickness == None:
        continue
    print(param_floor_thickness)
    param_floor_thickness_value = param_floor_thickness.AsDouble()   
       
    if(box==None):
        continue
    
    outline = Outline(box.Min, box.Max)
    bbFilter = BoundingBoxIntersectsFilter(outline)
    #logicalAndFilter
    categoryFilter_column = ElementCategoryFilter(BuiltInCategory.OST_StructuralColumns)
    print(categoryFilter_column)
    logicalAndFilter_floor = LogicalAndFilter(bbFilter, categoryFilter_column)
    print(logicalAndFilter_floor)
    
    allCl =FilteredElementCollector(doc,doc.ActiveView.Id).WherePasses(logicalAndFilter_floor).ToElements()
    
    if len(allCl) ==0:
        continue
    print(allCl)

    for cl in allCl:
        eleid_Column = cl.Id
        ele_Column = doc.GetElement(eleid_Column)
        param_Column_top = ele_Column.get_Parameter(BuiltInParameter.SCHEDULE_TOP_LEVEL_OFFSET_PARAM)
        param_Column_top.Set((float(value)/304.8)-param_floor_thickness_value)




t.Commit()

#Alert('{} Void Cut Success'.format(len(allClToRun)), title="Element Changed", header="Complete")