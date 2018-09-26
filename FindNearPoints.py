import arcpy
import numpy
import scipy
from scipy import spatial


#inputs
inFeatures = arcpy.GetParameterAsText(0) #input features (type: feature class, required)
targetFeatures = arcpy.GetParameterAsText(1) #near features (type: feature class, required)
toReturn = arcpy.GetParameter(2) #number of near features to return (type: long, optional, default:2)
outLocation = arcpy.GetParameterAsText(3) #output table location (type: workspace, required)
snapped = arcpy.GetParameterAsText(4) #return snapped features (type: boolean, default:false)

#mapping variables
mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd)[0]

#uniqueID
OID = arcpy.Describe(inFeatures).OIDFieldName
nearOID = arcpy.Describe(targetFeatures).OIDFieldName

#list of X,Y coordinates
fields = ['OID@','SHAPE@X','SHAPE@Y']
inXY = {row[0]: (round(row[1],4),round(row[2],4)) for row in arcpy.da.SearchCursor(inFeatures,fields)}
targetXY = ((int(row[0]),round(row[1],4),round(row[2],4)) for row in arcpy.da.SearchCursor(targetFeatures,fields))

#convert to array
pntArray = numpy.array(list(targetXY))

#built KDTree
tree = scipy.spatial.cKDTree(pntArray[:, [1,2]]) #specify only last x,y columns

#list to add to then create array from later
listArray = []

#loop over orig points, convert each to array and compare
count = 0
if snapped == 'true':
    for k,p in inXY.iteritems():
        distances = []  #distance container
        xy = numpy.asarray(p)
        index = tree.query_ball_point(xy, r=100)
            
        for r in index:
            XA = xy.reshape(-1,2)
            XB = pntArray[r][1:].reshape(-1,2) #split array, reshape
            distance = scipy.spatial.distance.cdist(XA,XB,metric = 'euclidean')#get distances

            row = list(pntArray[r])
            row.insert(0, int(k)) #insert key value at [0] index
            row.append(round(float(distance),3)) #append distances to list
            del row[2:4] #delete x,y values since we don't need them anymore
            distances.append(tuple(row)) #append to master list
            
        f = sorted(distances, key = lambda x:x[-1]) #sort based on dist values
        for i in f[:toReturn]:
            listArray.append(i)

else:
    for k,p in inXY.iteritems():
        distances = []  #distance container
        xy = numpy.asarray(p)
        index = tree.query_ball_point(xy, r=100)
            
        for r in index:
            XA = xy.reshape(-1,2)
            XB = pntArray[r][1:].reshape(-1,2) #split array, reshape
            distance = scipy.spatial.distance.cdist(XA,XB,metric = 'euclidean')#get distances

            if numpy.all(pntArray[r][1:] != xy):#check to see if it's comparing itself
                row = list(pntArray[r])
                row.insert(0, int(k)) #insert key value at [0] index
                row.append(round(float(distance),3)) #append distances to list
                del row[2:4] #delete x,y values since we don't need them anymore
                distances.append(tuple(row)) #append to master list
            
        f = sorted(distances, key = lambda x:x[-1]) #sort based on dist values
        for i in f[:toReturn]:
            listArray.append(i)

if listArray:
    #format array to create table from
    dts = [('IN_{0}'.format(OID),'uint64'),('NEAR_{0}'.format(nearOID),'uint64'),('NEAR_DIST','<f8')]
    formArray = numpy.array(listArray, dtype = dts)

    #export to gdb table or dbfif '.gdb' in outLocation:
    if '.gdb' in outLocation:
        arcpy.da.NumPyArrayToTable(formArray, outLocation)
    else:
        arcpy.da.NumPyArrayToTable(formArray, outLocation + '.dbf')
        outLocation = outLocation + '.dbf'

    try:
        #mapping variables, add table to map
        mxd = arcpy.mapping.MapDocument("CURRENT")
        df = arcpy.mapping.ListDataFrames(mxd, "*")[0]
        table = arcpy.mapping.TableView(r'{0}'.format(outLocation))
        arcpy.mapping.AddTableView(df, table)
        arcpy.RefreshActiveView()
        arcpy.AddMessage("Output table added to map")
    except:
        pass
    
        arcpy.AddMessage("Output location:{0}".format(outLocation))
else:
    arcpy.AddWarning("No output table was made.")
