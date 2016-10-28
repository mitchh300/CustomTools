""" Verision: 2.7.11
    Description: Calculates X Y values for a point feature class in a specified projected coordinate system.
    Notes: This code is a verion of a code posted to StackExchange by user crmackey. 
           See here: http://gis.stackexchange.com/questions/158923/calculating-geometry-for-feature-class-with-x-y-and-lat-long-values-in-different
"""


import arcpy

feature = r'...path to feature class...'

#This spatial reference is EPSG code 2278 [NAD83 / Texas South Central (US_FOOT)]
ref = arcpy.SpatialReference(2278)

with arcpy.da.UpdateCursor(feature, ['SHAPE@','POINT_X','POINT_Y']) as cursor:
    for row in cursor:
        pnt_proj = row[0].projectAs(ref)
        row[1] = [pnt_proj.centroid.X]
        row[2]= [pnt_proj.centroid.Y]
        cursor.updateRow(row)
