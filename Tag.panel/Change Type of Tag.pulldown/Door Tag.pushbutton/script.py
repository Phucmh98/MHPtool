__doc__ = 'Change Type of Tag form Views'
__author__ = 'Phuc'

from Autodesk.Revit.DB.Element import ChangeTypeId
from Autodesk.Revit.DB import  Transaction, FilteredElementCollector, BuiltInCategory, ElementCategoryFilter, LinkElementId, UV, LocationPoint, Location, XYZ
import rpw
from rpw import DB,ui
from pyrevit import forms,script
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument



door_tags_types = rpw.db.Collector(of_category='OST_DoorTags', is_type=True).elements
door_tag_type_options = {DB.Element.Name.GetValue(t): t for t in  door_tags_types}
door_tag_type = ui.forms.SelectFromList('Create Door Tag', door_tag_type_options, description='Choose door tag type')
door_type_id = door_tag_type.Id


t = Transaction(doc, "change")
selected_views = forms.select_views(use_selection=True)


if not selected_views:
    forms.alert("No views selected. Please try again.", exitscript = True)
t.Start()
for v in selected_views:
    
    door_tag = FilteredElementCollector(doc, v.Id).OfCategory(BuiltInCategory.OST_DoorTags).WhereElementIsNotElementType().ToElements()
        
    for n in door_tag:
        Change_door_tag_type=n.ChangeTypeId(door_type_id)
    print("View change: "+ (v.Name))
t.Commit()


