
from Autodesk.Revit.DB import  Transaction, FilteredElementCollector, BuiltInCategory, ElementCategoryFilter, LinkElementId, UV, LocationPoint, Location, XYZ, ElementTransformUtils, CopyPasteOptions

from pyrevit import forms,script,revit

from rpw import DB,ui
from rpw.ui.forms import SelectFromList
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# theme Dictionary
value = SelectFromList('Copy form Views to same Views', ['Door Tags', 
                                        'Room Tags',
                                        'Detail Items',
                                        'Window Tags'])
#select sourceView                                       
selected_views_sou = forms.select_views(
                    title='Select Views Copy',
                    filterfunc=lambda x: x.ViewType != DB.ViewType.DrawingSheet,
                    use_selection=True)
if not selected_views_sou:
        forms.alert("No views selected. Please try again.", exitscript = True)
#select view destinationView      
selected_views_dect = forms.select_views(
                    title='Select Views Paste',
                    filterfunc=lambda x: x.ViewType != DB.ViewType.DrawingSheet,
                    use_selection=False)      
if not selected_views_dect:
        forms.alert("No views selected. Please try again.", exitscript = True)                                
#empty list tag
list_tags = []
#main code
if value == 'Door Tags':
    
    for v in selected_views_sou:
        door_tag = FilteredElementCollector(doc, v.Id).OfCategory(BuiltInCategory.OST_DoorTags).WhereElementIsNotElementType().ToElementIds()
        list_tags.append(door_tag)
    #print(list_tags)

elif value == 'Room Tags':
    
    for v1 in selected_views_sou:
        room_tag = FilteredElementCollector(doc, v1.Id).OfCategory(BuiltInCategory.OST_RoomTags).WhereElementIsNotElementType().ToElementIds()
        list_tags.append(room_tag)
    #print(list_tags)

elif value == 'Detail Items':
    
    for v2 in selected_views_sou:
        Detail_select = FilteredElementCollector(doc, v2.Id).OfCategory(BuiltInCategory.OST_DetailComponents).WhereElementIsNotElementType().ToElementIds()
        list_tags.append(Detail_select)
    #print(list_tags)

elif value == 'Window Tags':
    
    for v3 in selected_views_sou:
        window_select = FilteredElementCollector(doc, v3.Id).OfCategory(BuiltInCategory.OST_WindowTags).WhereElementIsNotElementType().ToElementIds()
        list_tags.append(window_select)
    #print(list_tags)

print("="*30 +" {} Views changed  .".format(len(selected_views_dect))+ "="*30)
#Start trans to copy
t = Transaction(doc, "Copy form Views to same Views")

t.Start()
for sourceview, destView, element in zip(selected_views_sou,selected_views_dect,list_tags ):
    copy = ElementTransformUtils.CopyElements(sourceview, element, destView, None, CopyPasteOptions())
    
    print('Copy: [{}] form [{}] to [{}]'.format(str(value), str(sourceview.Name),str(destView.Name)))  
t.Commit()
