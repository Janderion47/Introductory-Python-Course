from uncertainties import ufloat
from uncertainties.umath import sin, cos, atan2, sqrt
from math import pi
import pandas as pd

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
    def __init__(self,bN,bS,bW,bE):
        self.centroid = (ufloat((bN.nominal_value + bS.nominal_value)/2,abs((bN.nominal_value+bS.nominal_value)/4)),ufloat((bE.nominal_value + bW.nominal_value)/2,abs(bE.nominal_value + bW.nominal_value)/4)) # lat & lon
    
    def distAllRadios(self):
        distances = list()
        
        df = pd.read_csv("Repeaters.csv",header=0,usecols=["Repeaters","Maidenhead Locator"])
        
        
        for index, row in df.iterrows():
            #print(row["Repeaters"],row["Maidenhead Locator"])
            rept_dist = HaversineWithUncert([self.centroid[0],self.centroid[1]],MH_to_GPS(row["Maidenhead Locator"]))
            distances.append([rept_dist,row["Repeaters"]])
        
        self.repeaterdistances = distances
    def distAllShelters(self):
        pass
        
if __name__ == "__main__":
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
            Sbound = minSouth + (j*delta_y)
            Nbound = minSouth + ((j+1)*delta_y)
            Wbound = maxWest + (i*delta_x)
            Ebound = maxWest + ((i+1)*delta_x)
            AllCells.append(GridCell(Nbound,Sbound,Wbound,Ebound))
    
    for u in AllCells: # Actually performs the fun
        u.distAllRadios()
        print(u.repeaterdistances)
    
    #test1 = GridCell(10,5,12,6)
    #print(test1.centroid)
    #TestHam = MH_to_GPS("EL87SI")
    #print(TestHam)