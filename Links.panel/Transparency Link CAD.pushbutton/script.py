__title__="Transparency\nLink CAD"
__doc__ = 'Change Transparency of Link CAD in Selected View'
__author__ = 'Phuc'

from Autodesk.Revit.DB import  View,Transaction, FilteredElementCollector, BuiltInCategory, ElementCategoryFilter, LinkElementId, OverrideGraphicSettings 
from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, TextBox,
                          Separator, Button, CheckBox)
import rpw
from rpw import DB,ui

from pyrevit import HOST_APP
from pyrevit import revit, DB
from pyrevit import forms
from pyrevit import script
from Autodesk.Revit.DB.OverrideGraphicSettings import SetSurfaceTransparency 

output = script.get_output()

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

#Theme choose values transparency link cad
components = [#Label('Pick Style:'),
               #ComboBox('combobox1', {'Opt 1': 10.0, 'Opt 2': 20.0}),
               Label('Transparency (0-100):'),
               TextBox('textbox1', Text="50"),
               #CheckBox('checkbox1', 'Check this'),
               Separator(),
               Button('Select')]
form = FlexForm('Suface Transparency', components)
form.show()
form.values



#Get value Transparency
value_trans = int(form.values.get('textbox1'))
#select view will be change Transparency
selected_views = forms.select_views(use_selection=True)
if not selected_views:
    forms.alert("No views selected. Please try again.", exitscript = True)

#Maincode>>>>>>>>>>>>>>>>>>>>>>>

for view in selected_views:
    #Fillte ImportInstance link cad
    dwgs = DB.FilteredElementCollector(doc, view.Id)\
            .OfClass(DB.ImportInstance)\
            .WhereElementIsNotElementType()\
            .ToElements()

#System graphic setting
    overrides = OverrideGraphicSettings()
    overrides.SetSurfaceTransparency(value_trans)

    t = Transaction(doc, "Override Element")
    t.Start()

    for dwg in dwgs:
        p = view.SetElementOverrides(dwg.Id,overrides)
        #Get ID el CAD
        dwg_id = dwg.Id
        #Get Name of CAD
        dwg_name = dwg.Parameter[DB.BuiltInParameter.IMPORT_SYMBOL_NAME].AsString()
        #Get Name who create Element
        dwg_instance_creator =  DB.WorksharingUtils.GetWorksharingTooltipInfo(revit.doc, dwg.Id).Creator
        #Get workset Name
        workset_table = revit.doc.GetWorksetTable()
        dwg_workset = workset_table.GetWorkset(dwg.WorksetId).Name
    print('\n\n')
    output.print_md("**DWG name:** {}\n\n"
                    "- DWG created by:{}\n\n"
                    "- DWG id: {}\n\n"
                    "- DWG workset: {}\n\n"
                    .format(dwg_name,
                            dwg_instance_creator,
                            output.linkify(dwg_id),
                            dwg_workset))
    t.Commit()
    


