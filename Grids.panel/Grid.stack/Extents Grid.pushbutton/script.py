__doc__ = 'Switch extents 2D/3D Grids in View'
__author__ = 'Phuc'

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, ElementCategoryFilter, Transaction, DatumExtentType
from Autodesk.Revit.UI.Selection.Selection import PickObjects
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.DB.DatumPlane import SetDatumExtentType
from Autodesk.Revit.DB.FilteredElementCollector import WherePasses, WhereElementIsNotElementType
from pyrevit import forms
from pyrevit import revit, DB
#Get UIDocument
uidoc = __revit__.ActiveUIDocument

#Get Document

doc = uidoc.Document

#Filltered Element Grid Collector
collector = FilteredElementCollector(doc,doc.ActiveView.Id).OfCategory(BuiltInCategory.OST_Grids).WhereElementIsNotElementType().ToElements()

selected_option = forms.CommandSwitchWindow.show(
            ['Switch 2D Grids',
             'Switch 3D Grids'],)

if selected_option:
    switch = True
    if selected_option == 'Switch 3D Grids':
        switch = False
    
    grids = []
    selection = revit.get_selection()
    if selection:
        grids = [x for x in selection if isinstance(x, DB.Grid)]
    else:
        grids = collector
    
    try:
        with revit.Transaction('Toggle Grid Bubbles'):
            for grid in grids:
                if switch:
                    grid.SetDatumExtentType(DB.DatumEnds.End0, revit.active_view, DatumExtentType.ViewSpecific)
                    grid.SetDatumExtentType(DB.DatumEnds.End1, revit.active_view, DatumExtentType.ViewSpecific)
                else: 
                    grid.SetDatumExtentType(DB.DatumEnds.End0, revit.active_view, DatumExtentType.Model)
                    grid.SetDatumExtentType(DB.DatumEnds.End1, revit.active_view, DatumExtentType.Model)


    except Exception:
        pass

    revit.uidoc.RefreshActiveView()


#Get all all in Current view
#select_grid = uidoc.Selection.PickObjects(ObjectType.Element, str(filter_grid))


#for i in select_grid:

		#sg = doc.GetElement(i)


