__title__="Override Crop\nViews"
__doc__ = 'Override Line Pattern Crop Region in selected Views'
__author__ = 'Phuc'

from pyrevit import revit, DB, script, forms
from rpw.ui.forms import FlexForm, Label, TextBox, Button, ComboBox, CheckBox, Separator,Alert
from Autodesk.Revit.DB import  (FamilyInstance,FamilySymbol,Element,Transaction, OverrideGraphicSettings,
                            ElementId ,FilteredElementCollector, BuiltInCategory, ElementCategoryFilter, LinePatternElement)
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.UI.Selection.Selection import  PickObject
from pyrevit.forms import ProgressBar
from Autodesk.Revit.UI import UIDocument

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

linePattern = FilteredElementCollector(doc).OfClass(LinePatternElement).ToElements()
#-----Theme select linepartern
unique_title_blocks = {}
for tb in linePattern:       
    unique_title_blocks["{}".format(tb.Name)] = tb.Id   
     
components = [Label('Select Line Pattern for Crop Region:'),
             ComboBox( 'titleblocks', unique_title_blocks),                                      
             Separator(),
             Button('Create')]
form = FlexForm('Override Line Pattern Crop View', components)
#Show CommandSWitch RPW
form.show()
form.values
#----Theme select views
selected_views = forms.select_views(
                    title='Select Views Override Line Pattern',
                    filterfunc=lambda x: x.ViewType != DB.ViewType.DrawingSheet,
                    use_selection=True)

#----Selected linepattern
selected_linePattern = form.values.get('titleblocks')
#---Settiong linepattern
ogs = OverrideGraphicSettings()
ogs_set = ogs.SetProjectionLinePatternId(selected_linePattern)

#---Main code run

t = Transaction(doc, "Create new override")
t.Start()
for view in selected_views:
    id_view = view.Id
    id_crop_str= str(id_view)
    id_crop_1 = int(id_crop_str)+1
    id_crop_2 = int(id_crop_str)+2        
   
    p1 = view.SetElementOverrides(ElementId(id_crop_1),ogs)
    p2 = view.SetElementOverrides(ElementId(id_crop_2),ogs)    

t.Commit()



