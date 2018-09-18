"""
   Date: 9/14/2018
   Author: Mitch Holley
   Version: 3.6.5

   Edits:

   Sources: https://joelmccune.com/arcgis-to-pandas-data-frame/
            https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.rename.html
            https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_excel.html
"""

import arcpy
import os
from openpyxl import Workbook
import pandas as pd
from pandas import DataFrame


def fc_to_pd_dataframe(feature_class, field_list):
    """
    Loads data into a Pandas Data Frame for subsequent analysis.
    
    feature_class = Input ArcGIS Feature Class
    field_list = Fields for input
    return: Pandas DataFrame object
    """
    
    return DataFrame(arcpy.da.FeatureClassToNumPyArray(
                     in_table=feature_class,
                     field_names=field_list,
                     skip_nulls=False,
                     null_value=-99999))


def FeatureClassesToExcel(inputData, outputLocation, aliased):
    """ Exports feature classes to Excel worksheets and
        combines them in to a single workbook.

        inputLoc = Input geodatabase or folder containing shapefiles
        outputLoc = Ouput location to where the Excel file will be saved
        aliased = 'true' or 'false' - will use field aliases if true
    """

    #time variables
    today = datetime.datetime.now().strftime("%m%d%Y")
    
    #set workspace
    arcpy.env.workspace = inputData
    
    #list all necessary feature classes
    features = arcpy.ListFeatureClasses()

    #create the output Excel file
    filename = "FeatureClassesToExcel_{}.xlsx".format(today)
    outFile = os.path.join(outputLocation, filename)
    wb = Workbook()

    #check if outFile exists, delete if necessary
    if os.path.exists(outFile):
        os.remove(outFile)

    #save Excel file to be accessed by Panadas in next line    
    wb.save(outFile)

    #pandas Excel variables
    writer = pd.ExcelWriter(outFile)

    #load feature class data input panda df
    arcpy.AddMessage("Processing {} feature classes...".format(len(features)))
    for feature in features:
        fc_path = os.path.join(inputWkspc, feature)
        exclude = ['Shape','FID','OID']
        fields = [x.name for x in arcpy.ListFields(feature) if x.name not in exclude]

        #convert to pandas dataframe
        df = fc_to_pd_dataframe(feature, fields)

        if aliased == 'true':
            #compile dictionary of comment / alias field name
            aliases = [x.aliasName for x in arcpy.ListFields(feature) if x.name not in exclude]
            newColumns = dict(zip(fields, aliases)) #fancy method to create dict from two lists
            
            #change pandas df column names with one fell swoop
            df = df.rename(columns=newColumns)
        
        #save dataframe to Excel sheet
        df.to_excel(excel_writer=writer,
                    sheet_name=str(feature),
                    index=False,
                    freeze_panes=(1,1)) #freeze panes (to look cool)
        arcpy.AddMessage("{} processed".format(feature))


    #save file
    writer.save()
    arcpy.AddMessage("\nOutput location: {}\n".format(outFile))
    del df, writer


if __name__ == '__main__':
    
    #script tool parameters
    inputWkspc = arcpy.GetParameterAsText(0)
    output = arcpy.GetParameterAsText(1)
    aliased = arcpy.GetParameterAsText(2)
    FeatureClassesToExcel(inputWkspc, output, aliased)
