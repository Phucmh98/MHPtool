from rpw.ui.forms import select_folder
from pyrevit import HOST_APP
from pyrevit import revit, DB
from pyrevit import forms
from pyrevit import script
from Autodesk.Revit.DB import WorksetConfiguration

folderpath = select_folder()

link_type = DB.RevitLinkType

links = DB.FilteredElementCollector(revit.doc) \
                .OfClass(link_type)\
                .ToElements()

xrefs = [revit.db.ExternalRef(x, None) for x in links]

linkcount = len(xrefs)
if linkcount > 1:
    selected_xrefs = \
        forms.SelectFromList.show(
            xrefs,
            title='Select Links to Reload',
            width=500,
            button_name='Reload',
            multiselect=True
            )

ws = WorksetConfiguration.WorksetConfigurationOption(OpenAllWorksets)

for i in selected_xrefs:
    i.LoadFrom(select_folder,ws)

print(selected_xrefs)