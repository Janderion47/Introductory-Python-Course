from uncertainties import ufloat
from uncertainties.umath import sin, cos, atan2, sqrt
from math import pi, ceil
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
import time

from mpl_toolkits.basemap import Basemap

timestart = time.time()
warnings.filterwarnings("ignore")


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

class GridCell:
    def __init__(self,bN,bS,bW,bE,shelterGPSuncert):
        self.centroid = (ufloat((bN + bS)/2,abs((bN+bS)/4)),ufloat((bE + bW)/2,abs(bE + bW)/4)) # lat & lon
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
        
    
    def distAllShelters(self):
        distances = list()
        
        df = pd.read_csv("Shelters.csv",header=0,usecols=["Name","Latitude NS","Longitude EW"])
        
        
        for index, row in df.iterrows():
            #print(row["Repeaters"],row["Maidenhead Locator"])
            shel_dist = HaversineWithUncert([self.centroid[0],
                                             self.centroid[1]],
                                            [ufloat(row["Latitude NS"],self.shelterGPS_uncert),
                                             ufloat(row["Longitude EW"],self.shelterGPS_uncert)],
                                            unitmeasure="mi").nominal_value
            distances.append([shel_dist,row["Name"]])
        
        self.shelterdistances = distances
        
        dist_low = None
        name = None
        
        for shelter in distances:
            if name == None:
                dist_low = shelter[0]
                name = shelter[1]
            elif shelter[0] < dist_low:
                dist_low = shelter[0]
                name = shelter[1]
        
        self.shelter_closest = [name,dist_low]
        

def timef(tofix): # Formats time in seconds
    fixed = format(tofix,".5f",)
    return fixed


if __name__ == "__main__":
    
    # Parameters
    shelter_gps_uncert = 0.0000005 # Derived from the gps website is assumed 0.00000005
    
    grid_x = 1000 # Pertains to cutting up the longitude
    grid_y = 1000 # Pertains to cutting up the latitude
    grid_n = grid_x * grid_y
    
    maxNorth= ufloat(28.1724342,0.0000001)
    minSouth= ufloat(27.6463871,0.0000001)
    maxWest = ufloat(-82.6511685,0.0000001)
    minEast = ufloat(-82.0553083,0.0000001)
    
    percentile_specificity = 500# 100 for all integers [0,100]
    
    # Mapping Coefficients
    center_lat = (maxNorth.nominal_value+minSouth.nominal_value)/2
    center_lon = (maxWest.nominal_value+minEast.nominal_value)/2
    
    # Starting up the mapping module.
    # Necessary for figuring out what grid cells are on land or on water.
    print(f"{timef(time.time()-timestart)} sec: Booting up the map")
    bm = Basemap(width=65000,height=65000,projection='aeqd',
                lat_0=center_lat,lon_0=center_lon,resolution="f")
    # width&height of 65000 chosen because it as closely as possible focuses
    # on the county.
    print(f"{timef(time.time()-timestart)} sec: Map done loading")
    
    
    # Calculations for cell lat-lon bounds
    rangeNS = abs(maxNorth - minSouth)
    rangeEW = abs(maxWest - minEast)
    delta_y = rangeNS / grid_y
    delta_x = rangeEW / grid_x
    
    
    AllCells = list()
    for i in range(grid_x): # Creates the grid of geographic cells
        for j in range(grid_y):
            Sbound = minSouth.nominal_value + (j*delta_y.nominal_value)
            Nbound = minSouth.nominal_value + ((j+1)*delta_y.nominal_value)
            Wbound = maxWest.nominal_value + (i*delta_x.nominal_value)
            Ebound = maxWest.nominal_value + ((i+1)*delta_x.nominal_value)
            
            xavg = (Wbound+Ebound)/2
            yavg = (Nbound+Sbound)/2
            
            xpt, ypt = bm(xavg,yavg)
            if (bm.is_land(xpt,ypt) == True) and not ((xavg < -82.575) and (yavg < 27.95)):
                # Checks if the centroid of the grid cell is on land, and is not in the region of Pinellas County, FL.
                AllCells.append(GridCell(Nbound,Sbound,
                                         Wbound,Ebound,
                                         shelter_gps_uncert))
            else:
                pass
            
        print(f"{(i+1)*100/grid_x}% of grid cells checked.")
        
        
    setsize = len(AllCells)
    print(f"The number of grid cells on land is {setsize} out of a possible {grid_n}; {len(AllCells)*100/(grid_n)}%")
    print(f"{timef(time.time()-timestart)} sec: Grid cells check done. Beginning to calculate distances of grid cells to the landmarks")
    
    #setAllRepeaterDist = list()
    setAllShelterDist = list()
    stepindex=1
    for CellInGrid in AllCells: # Actually performs the fun
        #CellInGrid.distAllRadios()
        CellInGrid.distAllShelters()
        
        #setAllRepeaterDist.append(CellInGrid.repeater_closest[1])
        setAllShelterDist.append(CellInGrid.shelter_closest[1])
        
        if stepindex % 10 == 0:
            print(f"{format(stepindex*100/setsize,'.4f')}% of cells' distances evaluated.")
        
        stepindex+=1
    
    print(f"{timef(time.time()-timestart)} sec: Distance calculations done. Beginning to calculate the percentiles")
    
    percentiles_to_calc = np.linspace(0, 100, percentile_specificity+1)
    
    #rept_dist_percentiles = np.percentile(setAllRepeaterDist,percentiles_to_calc)
    shel_dist_percentiles = np.percentile(setAllShelterDist,percentiles_to_calc)
    #print(f"Percentiles to calculate: {percentiles_to_calc}")
    #print(rept_dist_percentiles)
    print(shel_dist_percentiles)
    
    plt.figure(figsize=(10,7.5)) 
    #plt.plot(np.array(percentiles_to_calc),np.array(rept_dist_percentiles),label="Distance to Major Amateur Radio Repeaters")
    plt.plot(np.array(percentiles_to_calc),np.array(shel_dist_percentiles),label="Distance to Hurricane Shelters")
    plt.title(f"Percentiles of the Distances from land locations throughout Hillsborough County, FL. \n(Grid of {grid_x} by {grid_y})")
    plt.xlabel("Percentile")
    plt.ylabel("Value of the Percentile (miles)")
    plt.legend()
    plt.show()
    
    print("Summary:")
    print(f"Of a the {grid_x} by {grid_y} overlay of the county with a product of {grid_n} grid cells, only {setsize} cells were calculated to be over land and therefore usable.")
    print(f"25% of land in Hillsborough County is as close as {shel_dist_percentiles[ceil(percentile_specificity*.25)]} miles or nearer to a county hurricane shelter.")
    print(f"50% of land in Hillsborough County is as close as {shel_dist_percentiles[ceil(percentile_specificity*.5)]} miles or nearer to a county hurricane shelter.")
    print(f"75% of land in Hillsborough County is as close as {shel_dist_percentiles[ceil(percentile_specificity*.75)]} miles or nearer to a county hurricane shelter.")
    print(f"The maximum distance to a shelter is {shel_dist_percentiles[percentile_specificity]}.")


timeend = time.time()
print(f"Took {timef(timeend-timestart)} seconds or {timef(((timeend-timestart)/60))} minutes or {timef(((timeend-timestart)/3600))} hours to finish.")
   