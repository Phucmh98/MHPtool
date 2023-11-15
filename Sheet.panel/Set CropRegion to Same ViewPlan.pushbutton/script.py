"""Add selected view to selected sheets."""

from pyrevit import revit, DB
from pyrevit import forms
from pyrevit import script
from Autodesk.Revit.DB import (ViewCropRegionShapeManager ,
                                        CurveLoop, Line, Transaction, 
                                        BoundingBoxXYZ, FilteredElementCollector, 
                                        BuiltInCategory, ElementCategoryFilter, 
                                        LinkElementId, UV, LocationPoint, 
                                        Location, XYZ)
doc   = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

#selected view to get Curveloop
selected_views_getCurveloop = forms.select_views(
                    title='Select Views to Get Shape Crop Region',
                    filterfunc=lambda x: x.ViewType != DB.ViewType.DrawingSheet,
                    use_selection=True)
#Choosing true
if not selected_views_getCurveloop:
        forms.alert("No views selected. Please try again.", exitscript = True)
#empty list curvelop
views_curveLoop = []
for views_getcurveloop in selected_views_getCurveloop:
        #Creat Crop region manager
        get_crop = views_getcurveloop.GetCropRegionShapeManager()
        #get 1 first crop in list cropshape
        list_curveloop = get_crop.GetCropShape()[0]
        #assign crop to list list curveloop        
        views_curveLoop.append(list_curveloop)

#selected view to set Crop Region same viewplan
selected_views_setCurveloop = forms.select_views(
                    title='Select Views to Set Shape Crop Region',
                    filterfunc=lambda x: x.ViewType != DB.ViewType.DrawingSheet,
                    use_selection=True)
#Choosing true
if len(selected_views_setCurveloop) != len(selected_views_getCurveloop):
        forms.alert("The number of 1st Views selected is different from the number of 2nd Views. Please try again.", exitscript = True)
#=>>Print views change
print("="*15 +" {} Views changed  .".format(len(selected_views_setCurveloop))+ "="*15)
#Start Code

t=Transaction(doc,"Crop View")
t.Start()
for views_setCurveloop, curveloop in zip(selected_views_setCurveloop, views_curveLoop[0:]):
        
        view_getcrop = views_setCurveloop.GetCropRegionShapeManager()
        view_remove_crop = view_getcrop.RemoveCropRegionShape()
        view_setcrop = view_getcrop.SetCropShape(curveloop)
        print("Views changed: " + str(views_setCurveloop.Name))
t.Commit()

