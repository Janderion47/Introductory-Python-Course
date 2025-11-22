from uncertainties import ufloat
from uncertainties.umath import sin, cos, atan2, sqrt
from math import pi
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
        

if __name__ == "__main__":
    lat_0 = 27.91
    lon_0 = -82.35
    
    bm = Basemap(width=28000000,height=28000000,projection="aeqd",lat_0=lat_0,lon_0=lon_0,resolution="f")   # default: projection='cyl'
    #print(bm.is_land(99.675, 13.104))
    #print(bm.is_land(100.539, 13.104))
    
    shelter_gps_uncert = 0.0000005 # Derived from the gps website is assumed 0.00000005
    
    grid_x_n = 100 # Pertains to cutting up the longitude
    grid_y_n = 100 # Pertains to cutting up the latitude
    maxNorth= ufloat(28.1724342,0.0000001)
    minSouth= ufloat(27.6463871,0.0000001)
    maxWest = ufloat(-82.6511685,0.0000001)
    minEast = ufloat(-82.0553083,0.0000001)
    
    rangeNS = maxNorth - minSouth
    rangeEW = maxWest - minEast
    
    delta_y = rangeNS / grid_y_n
    delta_x = rangeEW / grid_x_n
    
    AllCells = list()
    
    for i in range(grid_x_n): # Creates the grid of geographic cells
        for j in range(grid_y_n):
            Sbound = minSouth.nominal_value + (j*delta_y.nominal_value)
            Nbound = minSouth.nominal_value + ((j+1)*delta_y.nominal_value)
            Wbound = maxWest.nominal_value + (i*delta_x.nominal_value)
            Ebound = maxWest.nominal_value + ((i+1)*delta_x.nominal_value)
            xpt, ypt = bm((Wbound+Ebound)/2,(Nbound+Sbound)/2)
            if bm.is_land(xpt,ypt) == True:
                AllCells.append(GridCell(Nbound,Sbound,Wbound,Ebound,shelter_gps_uncert))
                print("Land")
            else:
                pass
    
    #TODO He will be back tomorrow or tuesday
    print(f"Number of cells not in water: {len(AllCells)}")
    
    setAllRepeaterDist = list()
    setAllShelterDist = list()
    
    for CellInGrid in AllCells: # Actually performs the fun
        CellInGrid.distAllRadios()
        CellInGrid.distAllShelters()
        
        setAllRepeaterDist.append(CellInGrid.repeater_closest[1])
        setAllShelterDist.append(CellInGrid.shelter_closest[1])
        
        #print(setAllRepeaterDist.append(CellInGrid.repeater_closest[1]))
    
    percentiles_to_calc = [0,10,20,30,40,50,60,70,80,90,100]
    calculated_percentiles_rept = np.percentile(setAllRepeaterDist, percentiles_to_calc)
    calculated_percentiles_shel = np.percentile(setAllShelterDist, percentiles_to_calc)
    print(calculated_percentiles_rept)
    print(calculated_percentiles_shel)
    
    plt.scatter(np.array(percentiles_to_calc), np.array(calculated_percentiles_shel))
    plt.show()

timeend = time.time()
print(f"Took {timeend-timestart} seconds to finish.")
   