
#pylint: disable=C0103,E0401,C0111
from pyrevit import revit, DB
from pyrevit import script
from pyrevit import forms
from Autodesk.Revit.DB import View3D, ViewSection ,ViewPlan, ViewCropRegionShapeManager ,CurveLoop, Line, Transaction, BoundingBoxXYZ, FilteredElementCollector, BuiltInCategory, ElementCategoryFilter, LinkElementId, UV, LocationPoint, Location, XYZ
from Autodesk.Revit.Creation import Document

from Autodesk.Revit.UI.Selection.Selection import PickBox 
from Autodesk.Revit.UI.Selection import PickBoxStyle, Selection

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

#Drag Mouse by select
pick= uidoc.Selection.PickBox(PickBoxStyle.Directional)


#Pick bouding box by Drag Mouse
offset = 15
pickBox = BoundingBoxXYZ()
pickBox.Min = pick.Min
pickBox.Max = pick.Max

bboxMinX = pickBox.Min.X 
bboxMinY = pickBox.Min.Y 
bboxMinZ = pickBox.Min.Z - offset
bboxMaxX = pickBox.Max.X 
bboxMaxY = pickBox.Max.Y 
bboxMaxZ = pickBox.Max.Z + offset


newBbox = DB.BoundingBoxXYZ()
newBbox.Min = DB.XYZ(bboxMinX, bboxMinY, bboxMinZ)
newBbox.Max = DB.XYZ(bboxMaxX, bboxMaxY, bboxMaxZ)

#Use view Plan View
view = doc.ActiveView
viewcrop = view.GetCropRegionShapeManager()

if type(view) is ViewSection:
#Creat CropView by Drag Mousse
#if view is ViewSection:


    pt0_sc = XYZ( pick.Min.X, pick.Min.Y, pick.Min.Z )
    pt1_sc = XYZ( pick.Min.X, pick.Min.Y, pick.Max.Z )
    pt2_sc = XYZ( pick.Min.X, pick.Max.Y, pick.Max.Z )
    pt3_sc = XYZ( pick.Min.X, pick.Max.Y, pick.Min.Z )

    #Edges in BBox coords

    edge0_sc = Line.CreateBound( pt0_sc, pt1_sc )
    edge1_sc = Line.CreateBound( pt1_sc, pt2_sc )
    edge2_sc= Line.CreateBound( pt2_sc, pt3_sc )
    edge3_sc = Line.CreateBound( pt3_sc, pt0_sc )

    #Create loop, still in BBox coords

    edges_sc = []

    edges_sc.append( edge0_sc )
    edges_sc.append( edge1_sc )
    edges_sc.append( edge2_sc )
    edges_sc.append( edge3_sc )
    #Create curveloop, still in BBox coords

    baseLoop_sc = DB.CurveLoop.Create( edges_sc )

    t1=Transaction(doc,"Crop ViewSection")
    t1.Start()
    #Remove non-rectangular boundary
    x1 = viewcrop.RemoveCropRegionShape()
    #Creat new Crop region
    p1 = viewcrop.SetCropShape(baseLoop_sc)

    t1.Commit()

elif type(view) is ViewPlan:
    pt0 = XYZ( pick.Min.X, pick.Min.Y, pick.Min.Z )
    pt1 = XYZ( pick.Max.X, pick.Min.Y, pick.Min.Z )
    pt2 = XYZ( pick.Max.X, pick.Max.Y, pick.Min.Z )
    pt3 = XYZ( pick.Min.X, pick.Max.Y, pick.Min.Z )

    #Edges in BBox coords

    edge0 = Line.CreateBound( pt0, pt1 )
    edge1 = Line.CreateBound( pt1, pt2 )
    edge2 = Line.CreateBound( pt2, pt3 )
    edge3 = Line.CreateBound( pt3, pt0 )

    #Create loop, still in BBox coords

    edges = []

    edges.append( edge0 )
    edges.append( edge1 )
    edges.append( edge2 )
    edges.append( edge3 )
    #Create curveloop, still in BBox coords
    baseLoop = DB.CurveLoop.Create( edges )

    t=Transaction(doc,"Crop ViewPlan")
    t.Start()

    #Remove non-rectangular boundary
    new_sc = View3D.GetSectionBox() 
    sc = new_sc.SetSectionBox(newBbox)

    #Creat new Crop region
    

    t.Commit()
#print(baseLoop)