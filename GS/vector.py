from geo2cart import geo2cart


def vector(a,b):
    acart=geo2cart(a)
    bcart=geo2cart(b)
    vx=bcart[0]-acart[0]
    vy=bcart[1]-acart[1]
    vz=bcart[2]-acart[2]
    return [vx,vy,vz]