""" Version: 2.7.11
    Description: Updates point geometry from source feature class to target feature class
                 based on a unique ID match
    Notes: Both source and target feature must be point features
"""

source = r'... path to source feature class...'
target = r'...path to target feature class...'
uniqueID = "UNIQUEID"
source_keys = []

with arcpy.da.SearchCursor(source, [uniqueID,'SHAPE@X','SHAPE@Y']) as cursor:
    for row in cursor:
        source_keys.append(str(row[0])+'|'+str(row[1])+"|"+str(row[2]))

with arcpy.da.UpdateCursor(target, [uniqueID,'SHAPE@X','SHAPE@Y']) as cursor:
    for row in cursor:
        for s in source_keys:
            if str(row[0]) == s.split("|")[0]:
                row[1] = float(s.split("|")[1])
                row[2] = float(s.split("|")[2])
                cursor.updateRow(row)
