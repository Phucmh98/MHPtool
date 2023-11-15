#open Link Cad
import os
from Autodesk.Revit.DB import ExternalFileUtils, ModelPathUtils
from pyrevit import revit, forms

#select Link Cad
el = revit.get_selection().first
#Choose file path
if el != None and el.GetType().FullName == 'Autodesk.Revit.DB.ImportInstance':
    cadLink = revit.doc.GetElement(el.GetTypeId())
    cadRef = ExternalFileUtils.GetExternalFileReference(revit.doc, cadLink.Id)
    fpath = ModelPathUtils.ConvertModelPathToUserVisiblePath(cadRef.GetAbsolutePath())
else:
    forms.alert('One CAD Link instance must be selected',exitscript=True)

os.startfile(fpath)