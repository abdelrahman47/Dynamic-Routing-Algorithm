#!/usr/bin/env python2.7


# Used libraries
from datetime import datetime , timedelta
now = datetime.utcnow()
from pyorbital.orbital import Orbital
from pyorbital import tlefile
import math
import timeit

# variables 
Sats      = []#[IR3,IR46,IR24,IR64,IR71,IR69,IR47]
Nodes     = []
names     = []
file  = "/home/debian/iridium.txt"
file1 = "/home/debian/globalstar.txt"
file2 = "/home/debian/iridium-NEXT.txt"
file3 = "/home/debian/spire.txt"
file4 = "/home/debian/planet.txt"
# Functions
class Node:
        
    def __init__(self, IR):
        self.IR    = IR
        self.Neib  = []
        
def Neighbours(Nodes):
    for i in range(len(Nodes)):
        for j in range(len(Nodes)):
                R_lon , R_lat, R_alt = Nodes[i].IR.get_lonlatalt(now)
                R_altm = R_alt * 1000
                R_x , R_y, R_z = geodetic2ecef(R_lat,R_lon,R_altm)
                R_xm = R_x /1000 
                R_ym = R_y /1000
                R_zm = R_z /1000
                
                N_lon , N_lat , N_alt = Nodes[j].IR.get_lonlatalt(now)
                N_altm = N_alt * 1000
                N_x, N_y, N_z = geodetic2ecef(N_lat,N_lon,N_altm)
                N_xm = N_x / 1000 
                N_ym = N_y / 1000
                N_zm = N_z / 1000
                
                dis = Distance_2_Sats(R_xm,R_ym,R_zm, N_xm,N_ym,N_zm)
                if dis <= 3000 and Nodes[i].IR.satellite_name.strip() != Nodes[j].IR.satellite_name.strip() :
                    Nodes[i].Neib.append(Nodes[j])
                    
def createNode(Sats):
        #Nodes.clear()
        for i in range(len(Sats)):
            n = Node(Sats[i])
            Nodes.append(n)
        
        Neighbours(Nodes)
        
def Send_To_Node(root, Dis_name):
    Route = 'Route = '+root.IR.satellite_name.strip() + "-"
    level = 0
    if Dis_name == root.IR.satellite_name:
        print("Source is Distination ")
        return None
    for i in range(len(root.Neib)):
        if Dis_name == root.Neib[i].IR.satellite_name.strip():
            Route +=  "-" + root.Neib[i].IR.satellite_name.strip() 
            print(Route)
            return None
    level += 1
    if level == 1:
        for i in range(len(root.Neib)):
            for j in range(len(root.Neib[i].Neib)):
                if Dis_name == root.Neib[i].Neib[j].IR.satellite_name.strip():
                    Route += "-" + root.Neib[i].IR.satellite_name.strip() + "--" + root.Neib[i].Neib[j].IR.satellite_name.strip() 
                    print(Route)
                    return None
    level += 1
    if level == 2:
        for i in range(len(root.Neib)):
            for j in range(len(root.Neib[i].Neib)):
                for k in range(len(root.Neib[i].Neib[j].Neib)):
                    if Dis_name == root.Neib[i].Neib[j].Neib[k].IR.satellite_name.strip():
                        Route += "-" + root.Neib[i].IR.satellite_name.strip() + "-" + root.Neib[i].Neib[j].IR.satellite_name.strip() + "--" + root.Neib[i].Neib[j].Neib[k].IR.satellite_name.strip() 
                        print(Route)
                        return None
    level += 1
    if level == 3:
        for i in range(len(root.Neib)):
            for j in range(len(root.Neib[i].Neib)):
                for k in range(len(root.Neib[i].Neib[j].Neib)):
                    for l in range(len(root.Neib[i].Neib[j].Neib[k].Neib)):
                        if Dis_name == root.Neib[i].Neib[j].Neib[k].Neib[l].IR.satellite_name.strip():
                            Route += "-" + root.Neib[i].IR.satellite_name.strip() + "-" + root.Neib[i].Neib[j].IR.satellite_name.strip() + "--" + root.Neib[i].Neib[j].Neib[k].IR.satellite_name.strip() +  "--" + root.Neib[i].Neib[j].Neib[k].Neib[l].IR.satellite_name.strip() 
                            print(Route)
                            return None
    level += 1
    print("Distination Not Found")
    
def Distance_2_Sats(x1, y1, z1, x2, y2, z2):
    distance = math.sqrt(((x1 - x2)**2) + ((y1 - y2)**2) + ((z1 - z2)**2))
    return distance

def geodetic2ecef(lat,lon,alt):
    # WGS84 model
    semimajor_axis = 6378137
    flattening = 1 / 298.2572235630
    semiminor_axis = semimajor_axis * (1 - flattening)
    lat = math.radians(lat)
    lon = math.radians(lon)
    
    N = semimajor_axis**2 / math.sqrt(semimajor_axis**2 * math.cos(lat)**2 + semiminor_axis**2 * math.sin(lat)**2)
    x = (N + alt) * math.cos(lat) * math.cos(lon)
    y = (N + alt) * math.cos(lat) * math.sin(lon)
    z = (N * (semiminor_axis / semimajor_axis)**2 + alt) * math.sin(lat)
    return x, y, z





# Main Algorithm

f  = open(file)
f1 = open(file1)
f2 = open(file2)
f3 = open(file3)
f4 = open(file4)
#IRIDIUM
for x in f.readlines():
    if "." in x:
        continue
    else:
        names.append(x)
        IR = Orbital(x,tle_file=file)
        Sats.append(IR)
#gLOBAL-STAR        
for x in f1.readlines():
    if "." in x:
        continue
    else:
        names.append(x)
        IR = Orbital(x,tle_file=file1)
        Sats.append(IR)
#IRIDIUM-NEXT        
for x in f2.readlines():
    if "." in x:
        continue
    else:
        names.append(x)
        IR = Orbital(x,tle_file=file2)
        Sats.append(IR)
#SPIRE        
for x in f3.readlines():
    if "." in x:
        continue
    else:
        names.append(x)
        IR = Orbital(x,tle_file=file3)
        Sats.append(IR) 
#PLANET
for x in f4.readlines():
    if "." in x:
        continue
    if "FL" in x:
        names.append(x)
        IR = Orbital(x,tle_file=file4)
        Sats.append(IR) 
        
num = []
for i in range(500):
    num.append(Sats[i])		
		
				
		
createNode(num)  
print(len(Sats))
print(len(num))
Src = "IRIDIUM 921" #Source
Dis = "IRIDIUM " #Destination


for i in range(len(Nodes)):
    if Src == Nodes[i].IR.satellite_name.strip():
        print(Nodes[i].IR.satellite_name.strip() ,'index', i)
        root = Nodes[i]

        
        
#Send_To_Node(root,Dis)
time = [] 

for i in range(1000):
	start = timeit.default_timer()
	Send_To_Node(root,Dis)
	stop = timeit.default_timer()
	total = stop - start 
	time.append(total)
	print(total)

f = open("runtimeFun.txt","w")
for i in time:
	f.write(str(i))
	f.write("\n")
f.close()
# In[ ]: