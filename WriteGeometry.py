cps_source = database + '/' + 'CPS_Poles_SOURCE'
source_keys = []

with arcpy.da.SearchCursor(cps_source, ['Facility_ID','SHAPE@X','SHAPE@Y']) as cursor:
    for row in cursor:
        source_keys.append(str(row[0])+'|'+str(row[1])+"|"+str(row[2]))

with arcpy.da.UpdateCursor(cps_poles, ['Facility_ID','SHAPE@X','SHAPE@Y']) as cursor:
    for row in cursor:
        for s in source_keys:
            if str(row[0]) == s.split("|")[0]:
                row[1] = float(s.split("|")[1])
                row[2] = float(s.split("|")[2])
                cursor.updateRow(row)
