""" Spatially appends attributes from one layer to another if the
    two layers have a spatial relationship
    Author: Mitch Holley
    Date: 8/20/2018
    Version: 2.7.10
    Type: ESRI Custom Script Tool
"""


import arcpy
import sys

inputFeatures = arcpy.GetParameterAsText(0) #input: feature layer
inputField = arcpy.GetParameterAsText(1) #input: field (obtained from: feature layer)
targetFeatures = arcpy.GetParameterAsText(2) #input: feature layer
targetField = arcpy.GetParameterAsText(3) #input: field (obtained from: target field)
relation = arcpy.GetParameterAsText(4) #input: string (list of values) | CONTAINS, CROSSES, IDENTICAL, OVERLAPS, COMPLETELY WITHIN


#relationship dictionary
relDict = {'CONTAINS': 'contains',
           'CROSSES': 'crosses',
           'IDENTICAL': 'equals',
           'OVERLAPS': 'overlaps',
           'COMPLETELY WITHIN': 'within'}

#get relationship string as generator
rel = relDict[relation]

#invalid relationships [type, inputFeautres, targetFeatures]
invalid = (['contains','point','polyline'],
           ['contains','point','polygon'],
           ['contains','polyline','polygon'],
           ['crosses','point','point'],
           ['crosses','point','polyline'],
           ['crosses','point','polygon'],
           ['crosses','polyline','point'],
           ['crosses','polygon','point'],
           ['crosses','polygon','polygon'],
           ['equals','point','polyline'],
           ['equals','point','polygon'],
           ['equals','polyline','point'],
           ['equals','polyline','polygon'],
           ['equals','polygon','point'],
           ['equals','polygon','polyline'],
           ['overlaps','point','polyline'],
           ['overlaps','point','polygon'],
           ['overlaps','polyline','point'],
           ['overlaps','polyline','polygon'],
           ['overlaps','polygon','point'],
           ['overlaps','polygon','polyline'],
           ['within','polyline','point'],
           ['within','polygon','point'],
           ['within','polygon','polygon']
           )

relList = [rel,
           str(arcpy.Describe(inputFeatures).shapeType).lower(),
           str(arcpy.Describe(targetFeatures).shapeType).lower()
           ]

if relList in invalid:
    arcpy.AddError("ERROR: Invalid relationship type- {0} {1} {2}".format(relList[1].upper(),
                                                                          relList[0].upper(),
                                                                          relList[2].upper())
                   )
    sys.exit(0)
    

#dictionary of geometry generators and input field string
inputDict = {row[0]:row[1] for row in arcpy.da.SearchCursor(inputFeatures,
                                                            ['SHAPE@',inputField])}

#loop over target features geometry to analyze, if relationship found, paste values
updateCount = 0
if rel == 'contains':
    with arcpy.da.UpdateCursor(targetFeatures, ['SHAPE@',targetField]) as cursor:
        for c, row in enumerate(cursor, 1):
            for i in inputDict:
                if i.contains(row[0]): #using arcpy contain fuction for spatial analysis
                    if row[1] in (None,''):
                        row[1] = inputDict[i]
                    else:
                        row[1] = "{0}{1}".format(row[1], inputDict[i])
                    cursor.updateRow(row)
                    updateCount += 1
    del cursor

if rel == 'crosses':
    with arcpy.da.UpdateCursor(targetFeatures, ['SHAPE@',targetField]) as cursor:
        for c, row in enumerate(cursor, 1):
            for i in inputDict:
                if i.crosses(row[0]): #using arcpy crosses fuction for spatial analysis
                    if row[1] in (None,''):
                        row[1] = inputDict[i]
                    else:
                        row[1] = "{0}{1}".format(row[1], inputDict[i])
                    cursor.updateRow(row)
                    updateCount += 1
    del cursor
    
if rel == 'equals':
    with arcpy.da.UpdateCursor(targetFeatures, ['SHAPE@',targetField]) as cursor:
        for c, row in enumerate(cursor, 1):
            for i in inputDict:
                if i.equals(row[0]): #using arcpy equals fuction for spatial analysis
                    if row[1] in (None,''):
                        row[1] = inputDict[i]
                    else:
                        row[1] = "{0}{1}".format(row[1], inputDict[i])
                    cursor.updateRow(row)
                    updateCount += 1
    del cursor

if rel == 'overlaps':
    with arcpy.da.UpdateCursor(targetFeatures, ['SHAPE@',targetField]) as cursor:
        for c, row in enumerate(cursor, 1):
            for i in inputDict:
                if i.overlaps(row[0]): #using arcpy overlaps fuction for spatial analysis
                    if row[1] in (None,''):
                        row[1] = inputDict[i]
                    else:
                        row[1] = "{0}{1}".format(row[1], inputDict[i])
                    cursor.updateRow(row)
                    updateCount += 1
    del cursor

if rel == 'within':
    with arcpy.da.UpdateCursor(targetFeatures, ['SHAPE@',targetField]) as cursor:
        for c, row in enumerate(cursor, 1):
            for i in inputDict:
                if i.within(row[0]): #using arcpy within fuction for spatial analysis
                    if row[1] in (None,''):
                        row[1] = inputDict[i]
                    else:
                        row[1] = "{0}{1}".format(row[1], inputDict[i])
                    cursor.updateRow(row)
                    updateCount += 1
    del cursor
        
msg = "{0} input features had a relation with the target features.".format(updateCount)
arcpy.AddMessage(msg)
