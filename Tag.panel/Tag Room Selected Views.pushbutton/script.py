__doc__="Tag all room in selected Views"
__title__="Tag All\nRoom" #Title of the extension
__author__ = "Phuc"

from Autodesk.Revit.DB import  Transaction, FilteredElementCollector, BuiltInCategory, ElementCategoryFilter, LinkElementId, UV, LocationPoint, Location, XYZ
import rpw
from pyrevit import forms
from rpw import DB,ui
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

#Change type room tag
room_tags_types = rpw.db.Collector(of_category='OST_RoomTags', is_type=True).elements
room_tag_type_options = {DB.Element.Name.GetValue(t): t for t in  room_tags_types}
room_tag_type = ui.forms.SelectFromList('Create Room Tag', room_tag_type_options, description='Choose room tag type')
room_type_id = room_tag_type.Id


t = Transaction(doc, 'Tag All Rooms')
t.Start()
selected_views = forms.select_views(
                    title='Select Views Plan',
                    filterfunc=lambda x: x.ViewType != DB.ViewType.DrawingSheet,
                    use_selection=True)
if not selected_views:
    forms.alert("No views selected. Please try again.", exitscript = True)

for n in selected_views: 
    room_tag = FilteredElementCollector(doc,n.Id).OfCategory(BuiltInCategory.OST_RoomTags).WhereElementIsNotElementType().ToElements()   
    rooms = FilteredElementCollector(doc,n.Id).OfCategory(BuiltInCategory.OST_Rooms).WhereElementIsNotElementType().ToElements()
    
    #Choose room using tag    
    room_tag_in_room_ID=[]
    
    for i in room_tag:
        room_tag_in_room_ID.append(i.Room.Id)
    #filter room using tag
    filter_room=[]
    for i in rooms:
        if i.Id not in room_tag_in_room_ID:
            filter_room.append(i)
    #main code
    for room in filter_room:
        Tags_room = doc.Create.NewRoomTag(LinkElementId(room.Id),UV(room.Location.Point.X,room.Location.Point.Y),n.Id)
        Change_room_tag_type=Tags_room.ChangeTypeId(room_type_id)
    print("View change: "+ (n.Name))
t.Commit()