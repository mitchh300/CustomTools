import arcpy

#arctoolbox variables
features = arcpy.GetParameterAsText(0)#"Input Layer", [Feature Layer], Required, Filter:Point-FeatureClass 
sourceX = arcpy.GetParameterAsText(1)#"SourceX Field", [Field], Required, Filter:Double-Field, ObtainedFrom: Input Layer
sourceY = arcpy.GetParameterAsText(2)#"SourceY Field", [Field], Required, Filter:Double-Field, ObtainedFrom: Input Layer

#mxd properties
mxd = arcpy.mapping.MapDocument('CURRENT')
df = arcpy.mapping.ListDataFrames(mxd, 'Layers')[0]

#Function that checks if floats are within a range
def float_range(x,y,sourceX,sourceY):
    xMin = sourceX - 0.002
    xMax = sourceX + 0.002
    yMin = sourceY - 0.002
    yMax = sourceY + 0.002
    if (xMin <= x) and (xMax >= x):
        if (yMin <= y) and (yMax >= y):
            return True
        else:
            return False
    else:
        return False

#Compare inFeatures geometry if sourceX/sourceY is selected
outside = set()
try:
    with arcpy.da.SearchCursor(features,['OBJECTID',sourceX,sourceY,'SHAPE@X','SHAPE@Y'],"Source_X IS NOT NULL") as cursor:
        for row in cursor:
            results = float_range(row[3],row[4],row[1],row[2])
            if results == False:
                outside.add(row[0])
            else:
                pass
    del cursor
    if len(outside) > 0:
        if len(outside) == 1:
            qry = "OBJECTID = {}".format(int(list(outside)[0]))
        else:
            qry = "OBJECTID IN {}".format(tuple(outside))
        arcpy.AddMessage("\nThe following %s features need checking against their source X,Y values:\n"%str(len(outside)))
        arcpy.AddMessage(qry)
        arcpy.SelectLayerByAttribute_management(features,"NEW_SELECTION",qry)
        df.zoomToSelectedFeatures()
        arcpy.RefreshActiveView()
    else:
        arcpy.AddMessage("All feature geometries are near their source.")
        
except arcpy.ExecuteError:
    arcpy.AddError(arcpy.GetMeesages(2))
arcpy.AddMessage("\n")
    
