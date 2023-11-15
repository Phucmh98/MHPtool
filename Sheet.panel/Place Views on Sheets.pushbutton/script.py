"""Add selected view to selected sheets."""

from pyrevit import revit, DB
from pyrevit import forms
from pyrevit import script
from Autodesk.Revit.DB import (BuiltInParameter,
                               Transaction,
                               ViewSheet,
                               Viewport,
                               XYZ)




selected_views = forms.select_views(use_selection=True)
if not selected_views:
    forms.alert("No views selected. Please try again.", exitscript = True)


dest_sheets = forms.select_sheets(include_placeholder=False)
if not dest_sheets:
    forms.alert("No views Sheets. Please try again.", exitscript = True)

if len(selected_views) != len(dest_sheets):
        forms.alert('Please Selected Views = Selected Sheets.')
     
    
    #>>>>>>>>>> FILTER VIEWS ALREADY ON SHEETS
selected_views_already_on_sheet = [view for view in selected_views if view.get_Parameter(BuiltInParameter.VIEWER_SHEET_NUMBER).AsString() != '---']
selected_views                  = [view for view in selected_views if view.get_Parameter(BuiltInParameter.VIEWER_SHEET_NUMBER).AsString() == '---']
    
    #>>>>>>>>>> PRINT VIEWS NOT ON SHEETS
    #fixme add equal spacing

if selected_views_already_on_sheet:
    print("="*10 + " Views that are already placed on sheets:" + "="*10)
    for view in selected_views_already_on_sheet:
        print('View [{}] - Sheet [{}]'.format(view.Name, view.get_Parameter(BuiltInParameter.VIEWER_SHEET_NUMBER).AsString()))
    
#>>>>>>>>>> MAIN LOOP
print("="*10 +" Placing {} views on sheets.".format(len(selected_views))+"="*10)
#Main Start code
if dest_sheets:

    with revit.Transaction("Add Views to Sheets"):
        for sheet, selected_view in zip(dest_sheets, selected_views):
                #selected_view in selected_views:
                #for selected_view in selected_views:
                #for sheet in dest_sheets:

                    
            DB.Viewport.Create(revit.doc,
                                           sheet.Id,
                                           selected_view.Id,
                                           DB.XYZ(0, 0, 0))
                    #except Exception as place_err:
                        #logger.debug('Error placing view on sheet: {} -> {}'
                                     #.format(selected_view.Id, sheet.Id))
                    
            print('Created sheet: [{}] - [{}]'.format(sheet.Name, selected_view.Name))                    
else:
    forms.alert('No views selected.')
