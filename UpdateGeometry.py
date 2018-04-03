""" Version: 2.7.11
    Description: Updates point geometry from source feature class to target feature class
                 based on a unique ID match
    Notes: Both source and target feature must be point features
"""
import arcpy
impory sys

source = r'... path to source feature class...'
target = r'...path to target feature class...'
uniqueID = "UNIQUEID" #GUID or unique identifier of dataset rows

#build dict of source ids and shape geometry
source_keys = {row[0]:row[1] for row in arcpy.da.SearchCursor(source, [uniqueID,'SHAPE@XY'])}

#ensure source and target are points
souceDesc = arcpy.Describe(source)
targetDesc = arcpy.Describe(target)
if sourceDesc.shapeType != 'Point':
    print "Source geometry is not point geometry"
    sys.exit(0)
    
if targetDesc.shapeType != 'Point':
    print "Target dataset is not point geometry"
    sys.exit(0)

#update target geometry to source if found in source_keys dictionary
with arcpy.da.UpdateCursor(target, [uniqueID,'SHAPE@XY']) as cursor:
    for row in cursor:
        if row[0] in source_keys:
            row[1] = source_keys[row[0]]
            cursor.updateRow(row)
del cursor
