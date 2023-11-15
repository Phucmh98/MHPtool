__doc__ = 'Create Floors From Selected Rooms'
__author__ = 'Phuc'

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, ElementCategoryFilter, Transaction
from Autodesk.Revit.UI.Selection.Selection import PickObjects
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.DB.FilteredElementCollector import WherePasses, WhereElementIsNotElementType
from pyrevit import forms
from pyrevit import revit, DB
from Autodesk.Revit.DB.Architecture import Room
import rpw
from rpw import doc, uidoc, DB, UI, db, ui
import sys
import os
from collections import namedtuple


#Selection Rooms
selection = ui.Selection()

selected_rooms = [e for e in selection.elements if isinstance(e, Room)]

if not selected_rooms:
    UI.TaskDialog.Show('Create Floor', 'Please select at least one Room.')
    sys.exit()

floor_types = rpw.db.Collector(of_category='OST_Floors', is_type=True).elements
#rpw floor type
floor_type_options = {DB.Element.Name.GetValue(t): t for t in floor_types} 
#rpw select floor type
floor_type = ui.forms.SelectFromList('Create Floor', floor_type_options,
                                     description='Select Floor Type')
floor_type_id = floor_type.Id


@rpw.db.Transaction.ensure('Create Floor')
def make_floor(new_floor):
    floor_curves = DB.CurveArray()
    for boundary_segment in new_floor.boundary:
        try:
            floor_curves.Append(boundary_segment.Curve)       # 2015, dep 2016
        except AttributeError:
            floor_curves.Append(boundary_segment.GetCurve())  # 2017

    floorType = doc.GetElement(new_floor.floor_type_id)
    level = doc.GetElement(new_floor.level_id)
    normal_plane = DB.XYZ.BasisZ
    doc.Create.NewFloor(floor_curves, floorType, level, False, normal_plane)


NewFloor = namedtuple('NewFloor', ['floor_type_id', 'boundary', 'level_id'])
new_floors = []
room_boundary_options = DB.SpatialElementBoundaryOptions()

for room in selected_rooms:
    room_level_id = room.Level.Id
    # List of Boundary Segment comes in an array by itself.
    room_boundary = room.GetBoundarySegments(room_boundary_options)[0]
    new_floor = NewFloor(floor_type_id=floor_type_id, boundary=room_boundary,
                         level_id=room_level_id)
    new_floors.append(new_floor)

for new_floor in new_floors:
    make_floor(new_floor)
