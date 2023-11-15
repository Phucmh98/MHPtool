__doc__ = 'Change Type of Tag form Views'
__author__ = 'Phuc'

from Autodesk.Revit.DB.Element import ChangeTypeId
from Autodesk.Revit.DB import  Transaction, FilteredElementCollector, BuiltInCategory, ElementCategoryFilter, LinkElementId, UV, LocationPoint, Location, XYZ
import rpw
from rpw import DB,ui
from pyrevit import forms
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

#select category tag
window_tags_types = rpw.db.Collector(of_category='OST_WindowTags', is_type=True).elements

window_tag_type_options = {DB.Element.Name.GetValue(t): t for t in  window_tags_types}
window_tag_type = ui.forms.SelectFromList('Create window Tag', window_tag_type_options, description='Choose window tag type')
#Tag Id
window_type_id = window_tag_type.Id


t = Transaction(doc, "change")
selected_views = forms.select_views(use_selection=True)
if not selected_views:
    forms.alert("No views selected. Please try again.", exitscript = True)
t.Start()
for v in selected_views:
    
    window_tag = FilteredElementCollector(doc, v.Id).OfCategory(BuiltInCategory.OST_WindowTags).WhereElementIsNotElementType().ToElements()
        
    for n in window_tag:
        Change_window_tag_type=n.ChangeTypeId(window_type_id)
    print("View change: "+ (v.Name))
t.Commit()


