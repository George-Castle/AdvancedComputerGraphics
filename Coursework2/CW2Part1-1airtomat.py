import matplotlib.pyplot as plt
import math
import numpy as np


ni_air = 1.0
nt_mat = 1.45
xmax = 91
Rp = np.arange(91)
Rs = np.arange(91)
xaxis = np.arange(91)

for x in range(xmax):
    rad_x = math.radians(x) #pyhton uses radians by default
    #snells law
    incident = ni_air * math.sin(rad_x)
    trans_angle = math.asin(incident/nt_mat) # rearranged to calculate transmission angle
    
    #fresnel reflectance equations

    #parallel polarised light
    para_top = (nt_mat * math.cos(rad_x)) - (ni_air * math.cos(trans_angle))
    para_bottom = (nt_mat * math.cos(rad_x)) + (ni_air * math.cos(trans_angle))
    div = math.degrees(para_top) / math.degrees(para_bottom)
    parallel = abs(div) ** 2

    #perpendicular polarised light
    perp_top = (ni_air * math.cos(rad_x)) - (nt_mat * math.cos(trans_angle))
    perp_bottom = (ni_air * math.cos(rad_x)) + (nt_mat * math.cos(trans_angle))
    div = math.degrees(perp_top) / math.degrees(perp_bottom)
    perpendicular = abs(div) ** 2

    Rp[x] = (parallel)*100 # multiply by 100 to show as percentage values as was shown in the slides
    Rs[x] = (perpendicular)*100

brewsters = math.degrees(math.atan(nt_mat/ni_air)) # calcualte the brewsters angle

plt.plot(xaxis, Rp)
plt.plot(xaxis, Rs)
plt.axvline(x=int(brewsters), color='g', linestyle='--')
plt.title('n1 = 1.0, n2 = 1.45')
#reflectance of both components at normal incidence (0 degrees)
plt.text(13.0, 70.8,'Rp at normal = ' + str(int(Rp[0])) + '%',
     horizontalalignment='center',
     verticalalignment='center')
plt.text(13.0, 75.9,'Rs at normal = ' + str(int(Rs[0])) + '%',
     horizontalalignment='center',
     verticalalignment='center')
plt.xlabel('Angle of incidence (°)')
plt.ylabel('Reflection coefficient (%)')
plt.legend(['Rp', 'Rs', 'Brewsters = ' + str(int(brewsters)) + '°'])
plt.axis([0, 90, 0, 100]) 
plt.show()

