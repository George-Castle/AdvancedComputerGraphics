import matplotlib.pyplot as plt
import math
import numpy as np


ni_air = 1.45
nt_mat = 1.0
xmax = 91


critical = math.degrees(math.asin(nt_mat/ni_air)) # calc critical angle using equation from slides
xaxis = np.arange(int(critical)+2)
Rp = np.arange(int(critical)+2)
Rs = np.arange(int(critical)+2)

for x in range(int(critical)+2):
    if (x < critical):
        rad_x = math.radians(x)
        xaxis[x] = x #set x axis degrees of incidence values
    elif (x == int(critical)+1): #integer values loop index - to get the final value the loop must go beyond critical value
        rad_x = math.radians(critical)
        xaxis[x] = critical
    #snells law
    incident = math.degrees(ni_air * math.sin(rad_x))
    trans_angle = math.asin(math.radians(incident/nt_mat))

    #fresnel reflectance equations

    #parallel
    para_top = (nt_mat * math.cos(rad_x)) - (ni_air * math.cos(trans_angle))
    para_bottom = (nt_mat * math.cos(rad_x)) + (ni_air * math.cos(trans_angle))
    div = math.degrees(para_top) / math.degrees(para_bottom)
    parallel = abs(div) ** 2

    #perpendicular
    perp_top = (ni_air * math.cos(rad_x)) - (nt_mat * math.cos(trans_angle))
    perp_bottom = (ni_air * math.cos(rad_x)) + (nt_mat * math.cos(trans_angle))
    div = math.degrees(perp_top) / math.degrees(perp_bottom)
    perpendicular = abs(div) ** 2

    
        
    
    Rp[x] = (parallel)*100 # multiply by 100 to show as percentage values as was shown in the slides
    Rs[x] = (perpendicular)*100

brewsters = math.degrees(math.atan(nt_mat/ni_air)) # calc brewsters angle using equation from slides
plt.plot(xaxis, Rp)
plt.plot(xaxis, Rs)
plt.axvline(x=int(brewsters), color='g', linestyle='--')
plt.axvline(x=int(critical), color='r', linestyle='--')
plt.title('n1 = 1.45, n2 = 1.0')
plt.text(13.0, 90.8,'Rp at normal = ' + str(int(Rp[0])) + '%',
     horizontalalignment='center',
     verticalalignment='center')
plt.text(13.0, 95.9,'Rs at normal = ' + str(int(Rs[0])) + '%',
     horizontalalignment='center',
     verticalalignment='center')
plt.xlabel('Angle of incidence (°)')
plt.ylabel('Reflection coefficient (%)')
plt.legend(['Rp', 'Rs', 'Brewsters = ' + str(int(brewsters)) + '°', 'critical = ' + str(int(critical)) + '°'])
plt.axis([0, 90, 0, 100]) 
plt.show()

