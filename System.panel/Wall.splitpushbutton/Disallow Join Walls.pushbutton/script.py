__title__="Disallow Join\nWall"
__doc__ = 'Disallow Join by selected Wall in View'
__author__ = 'Phuc'


from Autodesk.Revit.DB import  WallUtils ,Element,UnitUtils,DisplayUnitType,Transaction, FilteredElementCollector, BuiltInCategory, ElementCategoryFilter, LinkElementId, UV, LocationPoint, Location, XYZ
from Autodesk.Revit.UI.Selection.Selection import PickObject
from Autodesk.Revit.UI.Selection import ObjectType
import rpw
from rpw import DB,ui
from phuc import select
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document



selection = select.select_with_cat_filter(DB.BuiltInCategory.OST_Walls, "Pick Wall form View")


t = Transaction(doc, "Disallow selected wall")
t.Start()
for i in selection:
    unjoin_wall_start= WallUtils.DisallowWallJoinAtEnd(i,0)
    unjoin_wall_end= WallUtils.DisallowWallJoinAtEnd(i,1)
t.Commit()