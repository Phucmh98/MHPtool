__title__="Select Category\nin Views"
__doc__ = 'Change height of casework form height of wall'
__author__ = 'Phuc'

from pyrevit import revit, DB, script, forms
from rpw.ui.forms import FlexForm, Label, TextBox, Button, ComboBox, CheckBox, Separator
from Autodesk.Revit.DB import ElementId, FamilyInstance,FamilySymbol,Element,Transaction, FilteredElementCollector, BuiltInCategory, ElementCategoryFilter, SelectionFilterElement 
from pyrevit import revit
from Autodesk.Revit.UI.Selection import Selection 
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

from System.Collections.Generic import List


selected_option = forms.CommandSwitchWindow.show(
            ['Columns',
             'Structural Columns',
             'Dimensions',
             'Doors',
             'Door Tags',
             'Floors',
             'Structural Framing',
             'Rooms',
             'Room Tags',
             'Walls',
             'Windows',
             'Windows Tags',
             'Ceilings',

             
             ])
#Select view of category
selected_views = forms.select_views(
                    title='Select View',
                    filterfunc=lambda x: x.ViewType != DB.ViewType.DrawingSheet,
                    use_selection=True)
if not selected_views:
       forms.alert("No views selected. Please try again.", exitscript = True)
list_type = []

#main Code
#>>>>>>Get door
if selected_option == 'Doors':
        for i in selected_views:
                el_type = FilteredElementCollector(doc,i.Id).OfCategory(BuiltInCategory.OST_Doors).WhereElementIsNotElementType().ToElements()
                
                for n in el_type:
                        eleid = n.Id                                               
                        list_type.append(eleid)
               
 #>>>>>>Get door
elif selected_option == 'Door Tags':
        for i in selected_views:
                el_type = FilteredElementCollector(doc,i.Id).OfCategory(BuiltInCategory.OST_DoorTags).WhereElementIsNotElementType().ToElements()
                
                for n in el_type:
                        eleid = n.Id                                               
                        list_type.append(eleid)
                             
#>>>>>>Get Columns
elif selected_option == 'Columns':
        for i in selected_views:
                el_type = FilteredElementCollector(doc,i.Id).OfCategory(BuiltInCategory.OST_Columns).WhereElementIsNotElementType().ToElements()
                
                for n in el_type:
                        eleid = n.Id                                               
                        list_type.append(eleid)

 #>>>>>>Get Dimension
elif selected_option == 'Dimensions':
        for i in selected_views:
                el_type = FilteredElementCollector(doc,i.Id).OfCategory(BuiltInCategory.OST_Dimensions).WhereElementIsNotElementType().ToElements()
                
                for n in el_type:
                        eleid = n.Id                                               
                        list_type.append(eleid)                       
               
#>>>>>>Get Columns
elif selected_option == 'Structural Columns':
        for i in selected_views:
                el_type = FilteredElementCollector(doc,i.Id).OfCategory(BuiltInCategory.OST_StructuralColumns).WhereElementIsNotElementType().ToElements()
                
                for n in el_type:
                        eleid = n.Id                                               
                        list_type.append(eleid)

#>>>>>>Get Floors
elif selected_option == 'Floors':
        for i in selected_views:
                el_type = FilteredElementCollector(doc,i.Id).OfCategory(BuiltInCategory.OST_Floors).WhereElementIsNotElementType().ToElements()
                
                for n in el_type:
                        eleid = n.Id                                               
                        list_type.append(eleid)

#>>>>>>Get Framming
elif selected_option == 'Structural Framing':
        for i in selected_views:
                el_type = FilteredElementCollector(doc,i.Id).OfCategory(BuiltInCategory.OST_StructuralFraming).WhereElementIsNotElementType().ToElements()
                
                for n in el_type:
                        eleid = n.Id                                               
                        list_type.append(eleid)

#>>>>>>Get Rooms
elif selected_option == 'Rooms':
        for i in selected_views:
                el_type = FilteredElementCollector(doc,i.Id).OfCategory(BuiltInCategory.OST_Rooms).WhereElementIsNotElementType().ToElements()
                
                for n in el_type:
                        eleid = n.Id                                               
                        list_type.append(eleid)
                        
   #>>>>>>Get Room tag
elif selected_option == 'Room Tags':
        for i in selected_views:
                el_type = FilteredElementCollector(doc,i.Id).OfCategory(BuiltInCategory.OST_RoomTags).WhereElementIsNotElementType().ToElements()
                
                for n in el_type:
                        eleid = n.Id                                               
                        list_type.append(eleid)

   #>>>>>>Get wall
elif selected_option == 'Walls':
        for i in selected_views:
                el_type = FilteredElementCollector(doc,i.Id).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElements()
                
                for n in el_type:
                        eleid = n.Id                                               
                        list_type.append(eleid)          

   #>>>>>>Get window
elif selected_option == 'Windows':
        for i in selected_views:
                el_type = FilteredElementCollector(doc,i.Id).OfCategory(BuiltInCategory.OST_Windows).WhereElementIsNotElementType().ToElements()
                
                for n in el_type:
                        eleid = n.Id                                               
                        list_type.append(eleid)

   #>>>>>>Get window Tag
elif selected_option == 'Windows Tags':
        for i in selected_views:
                el_type = FilteredElementCollector(doc,i.Id).OfCategory(BuiltInCategory.OST_WindowTags).WhereElementIsNotElementType().ToElements()
                
                for n in el_type:
                        eleid = n.Id                                               
                        list_type.append(eleid)


   #>>>>>>Get Ceilings
elif selected_option == 'Ceilings':
        for i in selected_views:
                el_type = FilteredElementCollector(doc,i.Id).OfCategory(BuiltInCategory.OST_Ceilings).WhereElementIsNotElementType().ToElements()
                
                for n in el_type:
                        eleid = n.Id                                               
                        list_type.append(eleid)

elif selected_option == None:
        forms.alert("No views selected. Please try again.", exitscript = True)

#Main Code

uidoc.Selection.SetElementIds(List[ElementId](list_type))





