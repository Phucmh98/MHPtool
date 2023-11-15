__doc__ = 'Change Type of Tag form Views'
__author__ = 'Phuc'

from Autodesk.Revit.DB.Element import ChangeTypeId
from Autodesk.Revit.DB import  Transaction, FilteredElementCollector, BuiltInCategory, ElementCategoryFilter, LinkElementId, UV, LocationPoint, Location, XYZ
import rpw
from rpw import DB,ui
from pyrevit import forms
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument





#list_tag = ()
#ist_room = []
#room_tag_in_room_ID=[]
#filter_room=[]
room_tags_types = rpw.db.Collector(of_category='OST_RoomTags', is_type=True).elements
room_tag_type_options = {DB.Element.Name.GetValue(t): t for t in  room_tags_types}
room_tag_type = ui.forms.SelectFromList('Create Room Tag', room_tag_type_options, description='Choose room tag type')
room_type_id = room_tag_type.Id


t = Transaction(doc, "change")
selected_views = forms.select_views(use_selection=True)
if not selected_views:
    forms.alert("No views selected. Please try again.", exitscript = True)
t.Start()
for v in selected_views:
    
    room_tag = FilteredElementCollector(doc, v.Id).OfCategory(BuiltInCategory.OST_RoomTags).WhereElementIsNotElementType().ToElements()
    
    
    for n in room_tag:
        Change_room_tag_type=n.ChangeTypeId(room_type_id)
    print("View change: "+ (v.Name))
t.Commit()


