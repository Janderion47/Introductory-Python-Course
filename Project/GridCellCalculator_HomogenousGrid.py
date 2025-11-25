from uncertainties import ufloat
from uncertainties.umath import sin, cos, atan2, sqrt, acos
from math import pi
import pandas as pd
from mpl_toolkits.basemap import Basemap
import csv
import time
import matplotlib.pyplot as plt

start = time.time()

def HaversineWithUncert(point1,point2,unitmeasure="m"): # Calculates distance between two points in meters
    # point1 and point2 are both formatted as [lat,lon] where both values may be uncertainties' ufloat()
    # Copied code from https://web.archive.org/web/20250916155915/http://www.movable-type.co.uk/scripts/latlong.html
    EarthRadius = ufloat(6371e3,1e1) # meters
    phi1 = point1[0]*pi/180 # deg to rad
    phi2 = point2[0]*pi/180 # deg to rad
    d_phi = (point2[0]-point1[0])*pi/180 # difference; deg to rad
    d_gamma=(point2[1]-point1[1])*pi/180 # difference; deg to rad

    apple= (sin(d_phi/2)**2)+(cos(phi1)*cos(phi2)*sin(d_gamma/2)**2)
    coconut=2*atan2(sqrt(apple),(sqrt(1-apple)))
    Distanc = EarthRadius*coconut # meters
    if unitmeasure == "m":
        return Distanc
    elif unitmeasure =="km":
        return Distanc/1000
    elif unitmeasure in ["mile","miles","mi"]:
        return Distanc/1609.344

def SurfaceAreaSphericalCap(lat,r): # Derived from its wikipedia page
    sArea = 2*pi*(r**2)*(1-cos((90-lat)*pi/180))
    return sArea

def SurfaceAreaSphericalQuadralateral(North,South,East,West,radius=ufloat(6371e3,1e1),unitmeasure="m2"):
    # NSEW are all lat-lon values in degrees of all of the boundaries
    sAreaN = SurfaceAreaSphericalCap(North,r=radius)
    sAreaS = SurfaceAreaSphericalCap(South,r=radius)
    EW_proportion = (East-West)/360
    sAreaFinal = (sAreaS-sAreaN)*EW_proportion
    if unitmeasure == "m2":
        return sAreaFinal
    elif unitmeasure =="km2":
        return sAreaFinal/(1000**2)
    elif unitmeasure in ["mile2","miles2","mi2"]:
        return sAreaFinal/(1609.344**2)
    
def NorthLatDegFromSASQ(South,East,West,AreaWanted,radius=ufloat(6371e3,1e1)):
    sAreaS = SurfaceAreaSphericalCap(South,r=radius)
    EW_proportion = (East-West)/360
    latN = 90 - (acos(1 - ( (sAreaS - (AreaWanted / EW_proportion))) / (2*pi*(radius**2)) )) *180/pi
    return latN

def MH_to_GPS(locator): # Converting Maidenhead locator to GPS coordinates
    locator = locator.upper() # Makes sure all letters are capital
    
    scope = None # Values correspond to how specific the grid area is
    if len(locator) == 4: # 2 Layers 
        scope = "Basic"
    elif len(locator) == 6:
        scope = "Usual"
    elif len(locator) == 8:
        scope = "Extra"
    elif len(locator) > 8:
        raise Exception("Whatever you put is too long.")
    else:
        raise Exception("Not a valid Maidenhead locator.")

    scopedict = {
        "Basic": [0.5],
        "Usual": [0,0.5],
        "Extra": [0,0,0.5]
    }
    uncert = scopedict[scope] # Uncertainty depends on how specific the grid area is
    
    LtN = { # Letters to Numbers
        "A":0, "B":1, "C":2, "D":3, "E":4, "F":5, "G":6, "H":7,
        "I":8, "J":9, "K":10,"L":11,"M":12,"N":13,"O":14,"P":15,
        "Q":16,"R":17,"S":18,"T":19,"U":20,"V":21,"W":22,"X":23
        }
    
    # Each (lon)gitude and (lat)itude variable is calculated in units of degrees.
    # Each lon and lat are underestimates, but the addition of the uncertainty
    # in the most specific scope specificity of location makes the sum of the
    # variables the most accurate.
    lon1 = LtN[locator[0]]*360/18
    lat1 = LtN[locator[1]]*180/18
    lon2 = ufloat(int(locator[2])+uncert[0],uncert[0])*(360/18)/10
    lat2 = ufloat(int(locator[3])+uncert[0],uncert[0])*(180/18)/10
    
    lon3 = 0
    lat3 = 0
    try: # Tries to do this, unless the locator isn't long enough and it raises the 'except'
        lon3 = ufloat(LtN[locator[4]]+uncert[1],uncert[1])*((360/18)/10)/24
        lat3 = ufloat(LtN[locator[5]]+uncert[1],uncert[1])*((180/18)/10)/24
    except IndexError:
        pass

    lon4 = 0
    lat4 = 0
    try: # Tries to do this, unless the locator isn't long enough and it raises the 'except'
        lon4 = ufloat(int(locator[6])+uncert[2],uncert[2])*(((360/18)/10)/24)/10
        lat4 = ufloat(int(locator[7])+uncert[2],uncert[2])*(((180/18)/10)/24)/10
    except IndexError:
        pass
    
    final_lon = lon1+lon2+lon3+lon4 - 180 # The -180 converts to real value
    final_lat = lat1+lat2+lat3+lat4 - 90  # The -90 converts to real value
    return final_lat, final_lon


def timef(tofix): # Formats time in seconds
    fixed = format(tofix,".5f",)
    return fixed

class GridCell:
    def __init__(self,bN,bS,bW,bE,shelterGPSuncert):
        self.centroid = (ufloat((bN + bS)/2,(bN-bS)/2),ufloat((bE + bW)/2,(bE - bW)/2)) # lat & lon
        self.shelterGPS_uncert = shelterGPSuncert
    
    def distAllRadios(self):
        distances = list()
        
        df = pd.read_csv("Repeaters.csv",header=0,usecols=["Repeaters","Maidenhead Locator"])
        
        
        for index, row in df.iterrows():
            #print(row["Repeaters"],row["Maidenhead Locator"])
            rept_dist = HaversineWithUncert([self.centroid[0],
                                             self.centroid[1]],
                                            MH_to_GPS(row["Maidenhead Locator"]),
                                            unitmeasure="mi").nominal_value # Distances in miles
            distances.append([rept_dist,row["Repeaters"]])
        
        self.repeaterdistances = distances
        
        dist_low = None
        name = None
        
        for repeater in distances:
            if name == None:
                dist_low = repeater[0]
                name = repeater[1]
            elif repeater[0] < dist_low:
                dist_low = repeater[0]
                name = repeater[1]
        
        self.repeater_closest = [name,dist_low]
        
    
    def sizeCell(self):
        xval = self.centroid[1].std_dev
        yval = self.centroid[0].std_dev
        xyratio = xval/yval
        
        arae = SurfaceAreaSphericalQuadralateral(self.centroid[0].nominal_value+self.centroid[0].std_dev,
                                                 self.centroid[0].nominal_value-self.centroid[0].std_dev,
                                                 self.centroid[1].nominal_value+self.centroid[1].std_dev,
                                                 self.centroid[1].nominal_value-self.centroid[1].std_dev)
        
        return xyratio, arae
    
    def distAllShelters(self):
        distances = list()
        
        df = pd.read_csv("Shelters.csv",header=0,usecols=["Name","Latitude NS","Longitude EW"])
        
        
        for index, row in df.iterrows():
            #print(row["Repeaters"],row["Maidenhead Locator"])
            shel_dist = HaversineWithUncert([self.centroid[0],
                                             self.centroid[1]],
                                            [ufloat(row["Latitude NS"],self.shelterGPS_uncert),
                                             ufloat(row["Longitude EW"],self.shelterGPS_uncert)],
                                            unitmeasure="mi")
            distances.append([shel_dist,row["Name"]])
        
        self.shelterdistances = distances
        
        def nomval(inp):
            return inp[0].nominal_value
        
        sort_dist = sorted(distances,key=nomval,reverse=True)
        self.shelter_closest = [sort_dist[-1][1],sort_dist[-1][0]]


if __name__ == "__main__":
    desiredGridCellArea = 500**2 # Square meters; m2
    grid_x = 120 # Pertains to cutting up the longitude
    shelter_gps_uncert = 0.0000005 # Derived from the gps website is assumed 0.00000005
    
    maxNorth= ufloat(28.1724342,0.0000001)
    minSouth= ufloat(27.6463871,0.0000001)
    maxWest = ufloat(-82.6511685,0.0000001)
    minEast = ufloat(-82.0553083,0.0000001)
    
    # Mapping Coefficients
    center_lat = (maxNorth.nominal_value+minSouth.nominal_value)/2
    center_lon = (maxWest.nominal_value+minEast.nominal_value)/2
    
    EW_range_deg = -(maxWest - minEast)
    NS_range_deg = maxNorth - minSouth
    delta_x = EW_range_deg/grid_x
    
    EW_r_dist_at_borderS = HaversineWithUncert([minSouth,maxWest],
                                               [minSouth,minEast],
                                               unitmeasure="km")
    EW_r_dist_at_borderN = HaversineWithUncert([maxNorth,maxWest],
                                               [maxNorth,minEast],
                                               unitmeasure="km")
    AreaOfTestSphericalQuadralateral = SurfaceAreaSphericalQuadralateral(maxNorth, minSouth, minEast, maxWest,unitmeasure="km2")
    
    #print(EW_r_dist_at_borderS/60)
    #print(EW_r_dist_at_borderN)
    #print(AreaOfTestSphericalQuadralateral)
    
    print(f"{timef(time.time()-start)} sec: Loading up the map")
    bm = Basemap(width=65000,height=65000,projection='aeqd',
                lat_0=center_lat,lon_0=center_lon,resolution="f")
    print(f"{timef(time.time()-start)} sec: Map loaded")
    
    plt.figure(figsize=(50,50))
    AllCells = list()
    
    savedSbound = minSouth
    while savedSbound.nominal_value+savedSbound.std_dev < maxNorth:
        Nbound = NorthLatDegFromSASQ(savedSbound, delta_x, 0, desiredGridCellArea)
        Sbound = savedSbound
        for StepsFromWest in range(grid_x):
            Wbound = maxWest + (StepsFromWest*delta_x)
            Ebound = maxWest + ((StepsFromWest+1)*delta_x)
            
            
            xavg = (Wbound+Ebound)/2
            yavg = (Nbound+Sbound)/2
            
            xpt, ypt = bm(xavg.nominal_value,yavg.nominal_value)
            if (bm.is_land(xpt,ypt) == True) and not ((xavg.nominal_value+xavg.std_dev < -82.575) and (yavg.nominal_value+yavg.std_dev < 27.95)):
                # Checks if the centroid of the grid cell is on land, and is not in the region of Pinellas County, FL.
                cell = GridCell(Nbound.nominal_value,Sbound.nominal_value,
                                         Wbound.nominal_value,Ebound.nominal_value,
                                         shelter_gps_uncert)
                AllCells.append(cell)
                plt.plot(cell.centroid[1].nominal_value,cell.centroid[0].nominal_value, ".g")
                print(cell.sizeCell())
                #print(f"Cell added at map location {xpt},{ypt}")
            else:
                pass
        
        print((maxNorth-savedSbound)*100/NS_range_deg, "% of area remaining to check")
        savedSbound = Nbound
    
    setsize = len(AllCells)
    print(f"There are {setsize} land cells.")
    print(f"Based on this, estimate of the land area of Hillsborough County, FL: {setsize*desiredGridCellArea} square meters.")
    print(f"Or {setsize*desiredGridCellArea/1000000} square kilometers.")
    
    # The following lines were necessary for testing the arrangement of grid
    # cells on the map. These coincide with the 'plt' calls all above.
    plt.title(f"Cells {desiredGridCellArea/1000000} square kilometers, \ncutting the grid into {grid_x} columns.")
    #plt.vlines(-82.575,ymin=minSouth.nominal_value,ymax=maxNorth.nominal_value)
    #plt.hlines(27.95,xmin=maxWest.nominal_value,xmax=minEast.nominal_value)
    #plt.legend()
    plt.show()
    
    
    print(f"{timef(time.time()-start)} sec: Beginning to calculate distances and write them to csv")
    csvname = f"HillsboroughCoFL_DistToHurricaneShelters_x{grid_x}_a{int(desiredGridCellArea)}m2_{time.time()}.csv"
    fieldnames = ["Lat","Lon","Distance","uLat","uLon","uDist"]
    with open(csvname, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        stepCells = 1
        for cell in AllCells:
            cell.distAllShelters()
            line = {
                "Lat": cell.centroid[0].nominal_value,
                "Lon": cell.centroid[1].nominal_value,
                "Distance":cell.shelter_closest[1].nominal_value,
                "uLat":cell.centroid[0].std_dev,
                "uLon":cell.centroid[1].std_dev,
                "uDist": cell.shelter_closest[1].std_dev
                }
            writer.writerow(line)
            if stepCells % 10 == 0:
                print(stepCells*100/setsize,"% though calculating distances")
            
            stepCells +=1
    
    
    

end = time.time()
end -= start
print(f"This took {end} seconds to complete. \nAlso known as {end/60} minutes or {end/3600} hours")
