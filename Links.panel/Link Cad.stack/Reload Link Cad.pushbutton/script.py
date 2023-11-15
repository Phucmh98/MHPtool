#open Link Cad
import os
from Autodesk.Revit.DB import ExternalFileUtils, ModelPathUtils, Transaction
from pyrevit import revit, forms

doc     = __revit__.ActiveUIDocument.Document
uidoc   = __revit__.ActiveUIDocument


#Reload Selected DWG

#select Link Cad
el = revit.get_selection().first
if el != None and el.GetType().FullName == 'Autodesk.Revit.DB.ImportInstance':
    t = Transaction(doc,"Reload DWG")
    t.Start()
    cadLink = revit.doc.GetElement(el.GetTypeId())
    cadLink.Reload()
    t.Commit()
else:
    forms.alert('One CAD Link instance must be selected',exitscript=True)

