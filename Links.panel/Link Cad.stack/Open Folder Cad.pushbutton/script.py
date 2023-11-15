#open Link Cad
import os
from Autodesk.Revit.DB import ExternalFileUtils, ModelPathUtils, Transaction
from pyrevit import revit, forms
from os import startfile
from os.path import dirname


doc     = __revit__.ActiveUIDocument.Document
uidoc   = __revit__.ActiveUIDocument


#select Link Cad
el = revit.get_selection().first
#Choose file path
if el != None and el.GetType().FullName == 'Autodesk.Revit.DB.ImportInstance':
    cadLink = revit.doc.GetElement(el.GetTypeId())
    cadRef = ExternalFileUtils.GetExternalFileReference(revit.doc, cadLink.Id)
    fpath = ModelPathUtils.ConvertModelPathToUserVisiblePath(cadRef.GetAbsolutePath())
    f_path = dirname(fpath)
else:
    forms.alert('One CAD Link instance must be selected',exitscript=True)

os.startfile(f_path)
