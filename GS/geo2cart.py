import math

def geo2cart(pos):
    #This function transforms geodesian to cartesian earth-centered coordinates
    #Geodesian coordinates must be given in radians and cart. coord. shown in m.
    #Definition of ellipsoidal Earth model WGS-84 (used for GPS)
    f=1/298.257224
    re=6378.137*1e3 
    #the order will be determined by the gps output
    h=pos[0]
    phi=pos[1]
    lam=pos[2]
    phi=phi*math.pi/180
    lam=lam*math.pi/180

    x=(h+re/math.sqrt(1-f*(2-f)*math.sin(phi)**2))*math.cos(phi)*math.cos(lam)
    y=(h+re/math.sqrt(1-f*(2-f)*math.sin(phi)**2))*math.cos(phi)*math.sin(lam)
    z=(h+(re*(1-f)**2)/math.sqrt(1-f*(2-f)*math.sin(phi)**2))*math.sin(phi)
    
    return [x,y,z]