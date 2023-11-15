__title__="Cut Void"
__doc__ = 'Disallow Join by selected Wall in View'
__author__ = 'Phuc'

import Autodesk
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Outline, BoundingBoxIntersectsFilter, LogicalAndFilter, ElementCategoryFilter, Transaction, InstanceVoidCutUtils
from Autodesk.Revit.UI.Selection import *
import rpw
from rpw import DB,ui
from rpw.ui.forms import SelectFromList
from pyrevit.forms import ProgressBar
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# theme Dictionary


cat_sel = SelectFromList('Select Category to Cut', ['Structure Framings', 
                                        'Floors',
                                        ])


#collection generic void cut
generics_sel = FilteredElementCollector(doc, doc.ActiveView.Id).OfCategory(BuiltInCategory.OST_GenericModel).WhereElementIsNotElementType().ToElements()   
max_value = len(generics_sel)
value = 0
for gen in generics_sel:
    #select structureframing cut
    frammings_sel = ElementCategoryFilter(BuiltInCategory.OST_StructuralFraming)
    #floor_sel = ElementCategoryFilter(BuiltInCategory.OST_Floors)
    #get bounding box
    box = gen.get_BoundingBox(doc.ActiveView)
    outline = Outline(box.Min, box.Max)
    #filter outline
    bbFilter = BoundingBoxIntersectsFilter(outline)
    #filter 2 element
    logicalAndFilter_beam = LogicalAndFilter(bbFilter, frammings_sel)
    #logicalAndFilter_floor = LogicalAndFilter(bbFilter, floor_sel)
    #FILTER element intersect generic
    allBeam = FilteredElementCollector(doc, doc.ActiveView.Id).WherePasses(logicalAndFilter_beam).ToElements()
    #allFloor =FilteredElementCollector(doc, doc.ActiveView.Id).WherePasses(logicalAndFilter_floor).ToElements()

#=>>>>>>>>>>>>>main code
    t = Transaction(doc, "Cut Void")
    t.Start()
    for beam in allBeam:
        InstanceVoidCutUtils.AddInstanceVoidCut(doc,beam,gen)
 
       
    t.Commit()
