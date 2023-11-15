#open Link Cad

from Autodesk.Revit.DB import ExternalFileUtils, ModelPathUtils, Transaction
from pyrevit import revit, forms

doc     = __revit__.ActiveUIDocument.Document
uidoc   = __revit__.ActiveUIDocument


#Reload Selected DWG

#select Link Cad
el = revit.get_selection().first
if el != None and el.GetType().FullName == 'Autodesk.Revit.DB.RevitLinkInstance':
   # t = Transaction(doc,"Reload Revit Link")
    #t.Start()
    revitLink = revit.doc.GetElement(el.GetTypeId())
    print(revitLink)
    revitLink.Reload()
    #t.Commit()
else:
    forms.alert('One Revit Link instance must be selected',exitscript=True)

