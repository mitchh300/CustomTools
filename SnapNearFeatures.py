## Author: Mitch Holley
## Date: 01/26/2017
## Version: 2.7.8
## ArcGIS Version: 10.3.1
"""
This tool snaps multiple target features to input features based on a user specified SQL criteria and search radius.
Import this script into an ArcGIS Toolbox.
Note: The tool uses the ArcGIS default scratch geodatabase.
"""
import arcpy
import os
import datetime

#date string
today = datetime.datetime.now().strftime('%m%d%Y')

#Set scratch workspace environments
workspace = arcpy.env.scratchGDB
outputWorkspace = workspace
arcpy.env.overwriteOutput = True

#Scratch workspace spatial join feature
spatialJoinFC = os.path.join(outputWorkspace, "SnapFeatures_SpatialJoin_{}".format(today))

#Get parameters
inputFeatures = arcpy.GetParameterAsText(0) #Data Type = Feature Class, Required
targetFeatures = arcpy.GetParameterAsText(1) #Data Type = Feature Class, Required
inputQry = arcpy.GetParameterAsText(2) #Data Type = SQL Expression, Optional, Obtained from: InputFeatures
targetQry = arcpy.GetParameterAsText(3) #Data Type = SQL Expression, Optional, Obtained from: TargetFeatures
searchRadius = arcpy.GetParameterAsText(4) #Data Type = Linear Unit, Required
uniqueID = arcpy.GetParameterAsText(5) #Data Type = Field, Required, Obtained from: TargetFeatures
arcpy.AddFieldDelimiters(targetFeatures, uniqueID)

#Apply SQL query to both features
arcpy.MakeFeatureLayer_management(inputFeatures, "inputLayer", inputQry)
arcpy.MakeFeatureLayer_management(targetFeatures, "targetLayer", targetQry)

#Preform spatial join
arcpy.SpatialJoin_analysis("inputLayer", "targetLayer", spatialJoinFC, "JOIN_ONE_TO_ONE", "KEEP_ALL", "", "CLOSEST", searchRadius, "")

#build dict from spatial join feature geometry tokens
uniqueID_1 = "{}_1".format(uniqueID)
excludeQry = "{} IS NOT NULL".format(uniqueID_1)
tCursor = arcpy.da.SearchCursor(spatialJoinFC, ["{}_1".format(uniqueID_1), "SHAPE@XY"], excludeQry)
tokens = {row[0]:row[1] for row in tCursor}

#Update geometry tokens based on token list
updateCount = 0
with arcpy.da.UpdateCursor(targetFeatures, [uniqueID,'SHAPE@XY']) as cursor:
    for iterCount, row in enumerate(cursor, 1):
        if row[0] in tokens:
            row[1] = tokens[row[0]]
            cursor.updateRow(row)
            updateCount += 1
           
del tCursor
del cursor
arcpy.AddMessage("\n{0}s features were snapped to input feature locations.\n".format(count))
