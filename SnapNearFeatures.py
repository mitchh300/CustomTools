## Author: Mitch Holley
## Date: 01/26/2017
## Version: 2.7.8
## ArcGIS Version: 10.3.1
"""
This tool snaps multiple target features to input features based on a user specified SQL criteria and search radius.
Import this script into an ArcGIS Toolbox.
Note: The tool creates a scratch geodatabases in the ArcGIS default location on the machine this is run.
"""
import arcpy, os

#Set scratch workspace environments
workspace=arcpy.env.scratchGDB
outputWorkspace = workspace
arcpy.env.overwriteOutput = True

#Scratch workspace spatial join feature
spatialJoinFC = outputWorkspace + '/' + "SnapFeatures_SpatialJoin"

#Get parameters
inputFeatures = arcpy.GetParameterAsText(0) #Data Type = Feature Class, Required
targetFeatures = arcpy.GetParameterAsText(1) #Data Type = Feature Class, Required
inputQry = arcpy.GetParameterAsText(2)#Data Type = SQL Expression, Optional, Obtained from: InputFeatures
targetQry = arcpy.GetParameterAsText(3)#Data Type = SQL Expression, Optional, Obtained from: TargetFeatures
searchRadius = arcpy.GetParameterAsText(4)#Data Type = Linear Unit, Required
uniqueID = arcpy.GetParameterAsText(5)#Data Type = Field, Required, Obtained from: TargetFeatures
arcpy.AddFieldDelimiters(targetFeatures, uniqueID)

#Apply SQL query to both features
arcpy.MakeFeatureLayer_management(inputFeatures, "inputLayer", inputQry)
arcpy.MakeFeatureLayer_management(targetFeatures, "targetLayer", targetQry)

#Preform spatial join
arcpy.SpatialJoin_analysis("inputLayer", "targetLayer", spatialJoinFC, "JOIN_ONE_TO_ONE", "KEEP_ALL", "", "CLOSEST", searchRadius, "")

#Search through spatial join features and grab spatial geometry tokens 
tokens = []
with arcpy.da.SearchCursor(spatialJoinFC, ['%s_1' % uniqueID, 'SHAPE@X','SHAPE@Y'])  as cursor:
    for row in cursor:
        tokens.append(str(row[0]) + '|' + str(row[1]) + '|' + str(row[2]))
arcpy.AddMessage("\nGrabbed geometry tokens from input features.")

#Update geometry tokens based on token list
count = 0
with arcpy.da.UpdateCursor(targetFeatures, [uniqueID,'SHAPE@X','SHAPE@Y']) as cursor:
    for row in cursor:
        for x in tokens:
            if x.split('|')[0] == str(row[0]):
                row[1] = float(x.split('|')[1])
                row[2] = float(x.split('|')[2])
                count += 1
                cursor.updateRow(row)
arcpy.AddMessage("\n%s features were snapped to input features locations.\n" % count)
