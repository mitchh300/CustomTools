## Author:  Mitch Holley
## Date:    08/30/2016
## Version: 2.7.8
## 
## This script is meant to be imported into an ArcGIS script. The purpose of the tool is to delete duplicate
## records in a specific field.  A checkbox is included in the script to check for duplicate geometries.
## Both a specific field AND the duplicate geometry checkbox should not be selected at one time. This tool was
## built as a replacement for the 'Delete Identical (Data Management)' tool found in the ArcGIS Advanced License package.
##EDITS: 
##9/12/2016 - After some testing, using sets was found to be much faster than lists. All old lists were convereted to sets().

import arcpy

#Get feature from user
feature = arcpy.GetParameterAsText(0)

#Get field from user
field = arcpy.GetParameterAsText(1)

#Boolean used for check box
ischecked = arcpy.GetParameterAsText(2)

#Lists
field_list = set()
shapes = set()

#Count for messages
count = 0

if str(ischecked) == 'true':
    with arcpy.da.UpdateCursor(feature, ['SHAPE@XY']) as cursor:
        for row in cursor:
            if row[0] not in shapes:
                shapes.add(row[0])
            else:
                count+=1
                cursor.deleteRow()
                arcpy.AddMessage('\n'+str(count) + ' duplicate geometries removed.\n')
else:
    with arcpy.da.UpdateCursor(feature, [field]) as cursor:
        for row in cursor:
            if row[0] not in field_list:
                field_list.add(row[0])
            else:
                count+=1
                cursor.deleteRow()
                arcpy.AddMessage('\n'+str(count) + ' duplicates removed from the ' + str(field) + ' field.\n')
