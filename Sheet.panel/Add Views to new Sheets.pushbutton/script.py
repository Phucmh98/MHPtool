"""Place selected view to new sheets."""


from rpw.ui.forms import FlexForm, Label, ComboBox, TextBox, TextBox, Separator, Button, CheckBox
from rpw import revit, doc, uidoc, DB, UI, db, ui
from Autodesk.Revit.DB import (FilteredElementCollector, BuiltInCategory, 
                                BuiltInParameter, ViewSheet, Viewport, Transaction, XYZ)
from pyrevit import forms
from pyrevit import script
from rpw.ui.forms import SelectFromList
from Autodesk.Revit.UI.Selection import Selection
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument


#Get name Family type of Title Blocks and
all_title_blocks = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_TitleBlocks).WhereElementIsElementType().ToElements()
unique_title_blocks = {}
for tb in all_title_blocks:
    family_name = tb.FamilyName
    type_name = tb.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
    unique_title_blocks["{} - {}".format(family_name, type_name)] = tb.Id

#value = SelectFromList('Test Window', unique_title_blocks)

#Theme RPW choose
components = [Label('Select Title Blocks:'),
             ComboBox( 'titleblocks', unique_title_blocks),
              Label('Enter Prefix:'),
              TextBox('textbox1', Text= "00."),
              Label('Enter Start Count:'),
              TextBox('textbox2', Text= "0"),
             Separator(),
             Button('Create Sheets')]
form = FlexForm('Place Views On New Sheets', components)
#Show CommandSWitch RPW
form.show()

form.values

    
#Get values form Theme


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> MAIN
if __name__ == '__main__':

    #>>>>>>>>>> GET SELECTED VIEWS
    selected_views = forms.select_views(use_selection=True)
    if not selected_views:
        forms.alert("No views selected. Please try again.", exitscript = True)

    #>>>>>>>>>> FILTER VIEWS ALREADY ON SHEETS
    selected_views_already_on_sheet = [view for view in selected_views if view.get_Parameter(BuiltInParameter.VIEWER_SHEET_NUMBER).AsString() != '---']
    selected_views                  = [view for view in selected_views if view.get_Parameter(BuiltInParameter.VIEWER_SHEET_NUMBER).AsString() == '---']


    #>>>>>>>>>> PRINT VIEWS NOT ON SHEETS
    #fixme add equal spacing
    if selected_views_already_on_sheet:
        print("="*10 + " Views that are already placed on sheets:"+"="*10)
        for view in selected_views_already_on_sheet:
            print('View [{}] - Sheet [{}]'.format(view.Name, view.get_Parameter(BuiltInParameter.VIEWER_SHEET_NUMBER).AsString()))

    #>>>>>>>>>> SELECT TITLEBLOCK
    selected_title_block = form.values.get('titleblocks')

    
    #Get Value form Theme
    prefix = form.values.get('textbox1')
    start_count = int(form.values.get('textbox2'))

    #>>>>>>>>>> MAIN LOOP

    print("="*15 +" Placing {} views on sheets.".format(len(selected_views))+ "="*15)

    t = Transaction(doc, "Py: New Sheets")
    t.Start()


    for view in selected_views:

        #>>>>>>>>>> CREATE SHEET
        Sheet = ViewSheet.Create(doc, selected_title_block)

        #>>>>>>>>>> SET SHEET NUMBER
        count = "{:02d}".format(start_count) # 1 -> 01...
        sheet_number = prefix + count

        fail_count = 0
        while True:
            fail_count += 1
            if fail_count > 10:
                break
            try:
                Sheet.SheetNumber = sheet_number
                break
            except:
                sheet_number += "*"
        start_count += 1

        #>>>>>>>>>> PLACE VIEW ON SHEET

        Viewport.Create(doc, Sheet.Id, view.Id, XYZ(0.6 , 0.55 , 0))
        Sheet.Name = view.Name
        print('Created sheet: {} - {}'.format(sheet_number, Sheet.Name))
    t.Commit()

