__title__="Void Cut\nCategory"
__doc__ = 'Cut Category form Void Cut'
__author__ = 'Phuc'


import Autodesk
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Outline, BoundingBoxIntersectsFilter, LogicalAndFilter, ElementCategoryFilter, Transaction, InstanceVoidCutUtils
from pyrevit import revit, DB, script, forms
from rpw.ui.forms import FlexForm, Label, TextBox, Button, ComboBox, CheckBox, Separator,Alert
import rpw
from rpw import DB,ui
from rpw.ui.forms import SelectFromList
from pyrevit.forms import ProgressBar
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# theme Dictionary


forms.alert('Hien is Gay!!!!', exitscript=False)

cat_sel = SelectFromList('Select Category to Cut', ['Structure Framings', 
                                        'Floors'])


allGenToRun = FilteredElementCollector(doc, doc.ActiveView.Id).OfCategory(BuiltInCategory.OST_GenericModel).WhereElementIsNotElementType().ToElements()
#print(allGenToRun)
max_value = len(allGenToRun)

for gen in allGenToRun:
    #filter category
    categoryFilter_beam = ElementCategoryFilter(BuiltInCategory.OST_StructuralFraming)
    categoryFilter_floor = ElementCategoryFilter(BuiltInCategory.OST_Floors)
    #intersect
    box = gen.get_BoundingBox(doc.ActiveView)
    outline = Outline(box.Min, box.Max)
    bbFilter = BoundingBoxIntersectsFilter(outline)
    #logicalAndFilter
    logicalAndFilter_beam = LogicalAndFilter(bbFilter, categoryFilter_beam)
    logicalAndFilter_floor = LogicalAndFilter(bbFilter, categoryFilter_floor)
    
    
    #FILTER element intersect generic
    allBeams= FilteredElementCollector(doc, doc.ActiveView.Id).WherePasses(logicalAndFilter_beam).ToElements()
    allFloor =FilteredElementCollector(doc, doc.ActiveView.Id).WherePasses(logicalAndFilter_floor).ToElements()
    #===============>>>>>>>Main code
    t = Transaction(doc, "Py: New Change Casework")
    t.Start()
    
    if cat_sel == 'Structure Framings':    
        for beam in allBeams:                    
            try:
                InstanceVoidCutUtils.RemoveInstanceVoidCut(doc, beam, gen)
                InstanceVoidCutUtils.AddInstanceVoidCut(doc, beam, gen)
            except:
                break
    elif cat_sel == 'Floors':
        for floor in allFloor:                    
            try:
                InstanceVoidCutUtils.RemoveInstanceVoidCut(doc, floor, gen)
                InstanceVoidCutUtils.AddInstanceVoidCut(doc, floor, gen)
            except:
                break
    t.Commit()

Alert('{} Void Cut Success'.format(len(allGenToRun)), title="Element Changed", header="Complete")