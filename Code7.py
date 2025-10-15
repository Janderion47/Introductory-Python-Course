def cm(datain): # Calculate Mean
    suma = 0
    count=int(0)
    for i in datain:
        suma+=i
        count+=1
    
    return suma/count

def make_prediction(data_point, m, yint):
    return (data_point*m)+yint

data_points = [
    (2000, 72.5),
    (2001, 73.1),
    (2002, 73.8),
    (2003, 74.2),
    (2004, 74.7),
    (2005, 75.3),
    (2006, 75.9),
    (2007, 76.5),
    (2008, 76.9),
    (2009, 77.4),
    (2010, 78.0),
    (2011, 78.5),
    (2012, 79.0),
    (2013, 79.5),
    (2014, 80.0),
    (2015, 80.5),
    (2016, 81.0),
    (2017, 81.5),
    (2018, 82.0),
    (2019, 82.5)]

x_items = []
y_items = []
for i in data_points:
    x_items.append(i[0])
    y_items.append(i[1])

x_mean = cm(x_items)
y_mean = cm(y_items)

linreg_numer = 0
linreg_denom = 0
for i in data_points:
    linreg_numer+=(i[0]-x_mean)*(i[1]-y_mean)
    linreg_denom+=((i[0]-x_mean)**2)

linreg_slope = linreg_numer/linreg_denom
linreg_int = y_mean - (linreg_slope*x_mean)

newdata = float(input("New 'x' value to predict the 'y'?"))
print(make_prediction(newdata,linreg_slope,linreg_int))
