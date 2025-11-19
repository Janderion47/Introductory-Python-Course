from uncertainties import ufloat
from uncertainties.umath import sin, cos, atan2, sqrt
from math import pi

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
        self.centroid = (ufloat((bN + bS)/2,((bN+bS)/4)),ufloat((bE + bW)/2,(bE + bW)/4)) # lat & lon
        
if __name__ == "__main__":
    test1 = GridCell(10,5,12,6)
    print(test1.centroid)