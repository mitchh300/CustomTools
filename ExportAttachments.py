## Code found here: http://support.esri.com/technical-article/000011912
## This script is meant to be imported in an ArcToolbox as a script tool.  The script exports feature class attachments
## specifically .jpg images. The exported attachments are saved to a folder the user specifies. 

import arcpy
from arcpy import da
import os

#Get input ATTACH table from user
inTable = arcpy.GetParameterAsText(0)

#Get output folder location from user
fileLocation = arcpy.GetParameterAsText(1)

#Search through input table and extract attachments to specified folder
#may need to change 'REL_OBJECTID' to the related OID from the FC with attachments
with da.SearchCursor(inTable, ['DATA','REL_OBJECTID']) as cursor: 
    for item in cursor:
        attachment = item[0]
        filename = str(item[1]) + '.jpg' #Edit name of output file by specifying in the SearchCursor, edit data type if needed
        if object is None:
            pass
        else:
            open(fileLocation + os.sep + filename, 'wb').write(attachment.tobytes())
            del item
            del attachment

