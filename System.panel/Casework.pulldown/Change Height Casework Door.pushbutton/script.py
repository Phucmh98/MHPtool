__title__="Casework\nDoors"
__doc__ = 'Change Height Caseworks of Doors form Height of Walls'
__author__ = 'Phuc'
from pyrevit import revit, DB, script, forms
from rpw.ui.forms import FlexForm, Label, TextBox, Button, ComboBox, CheckBox, Separator,Alert
from Autodesk.Revit.DB import  FamilyInstance,FamilySymbol,Element,UnitUtils,DisplayUnitType,Transaction, FilteredElementCollector, BuiltInCategory, ElementCategoryFilter, LinkElementId, UV, LocationPoint, Location, XYZ
from phuc import select
from pyrevit.forms import ProgressBar
from Autodesk.Revit.UI import UIDocument

doc = __revit__.ActiveUIDocument.Document

output = script.get_output()
logger = script.get_logger()  # helps to debug script, not used
#Select casework by filter
selection = select.select_with_cat_filter(DB.BuiltInCategory.OST_Doors, "Pick Casework form View")
#print('{} Casework will be change'.format(len(selection)))
#print('='*30)
#main code

t = Transaction(doc, "Py: New Change Casework")
max_value = len(selection)
t.Start()
#count = 0
with ProgressBar(title = 'Casework Changed: ({value} of {max_value})' ,cancellable=True) as pb:
    for i,n  in zip(selection, range(0, max_value)) :
        if pb.cancelled:
            break
        else:
            #id form selected
            eleid = i.Id
            #get element id
            ele = doc.GetElement(eleid)
            wall_host =ele.Host

            param_height = wall_host.LookupParameter("Unconnected Height").AsDouble()
            #param_bassoffset = wall_host.LookupParameter("Base Offset").AsDouble()
            #total parameter 
            #q= param_height + param_bassoffset

            #get parameter form casework
            param_e = ele.LookupParameter("CEN_L_BoTru") #revit 2019
            
            if not param_e:
                continue
            #param = ele.LookupParameter("Length")
            
            #set parameter to casework
            #param.Set(param_height)
            param_e.Set(param_height)    
            #count = count + 1  
                             
            pb.update_progress(n, max_value)
             
        #print('Casework Changed: ' + i.Name + ' [{}]/[{}]'.format(count, len(selection)))
t.Commit()

Alert('{} Casework Changed Success'.format(len(selection)), title="Casework Changed", header="Complete")