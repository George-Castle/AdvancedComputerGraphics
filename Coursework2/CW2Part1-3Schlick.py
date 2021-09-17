import matplotlib.pyplot as plt
import math
import numpy as np

ni_air = 1.0
nt_mat = 1.45
xmax = 91
Fp = np.arange(91)
xaxis = np.arange(91)
Sp = np.arange(91)
for x in range(xmax):
    rad_x = math.radians(x)
    #snells law
    incident = math.degrees(ni_air * math.sin(rad_x))
    trans_angle = math.asin(math.radians(incident/nt_mat))
    
    #polarisation dielectric fresnel reflectance equations

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

    

    Fp[x] = ((parallel*100)+(perpendicular*100))/2 # unpolarised Fresnel reflectance
    Sp[x] = (Fp[0]) + ((100 - Fp[0])*((1 - math.cos(rad_x))**5)) # Schlicks approximation scaled to percentage to work with array values

plt.plot(Sp)
plt.plot(Fp)


plt.title("Schlick's")
plt.xlabel('Angle of incidence (°)')
plt.ylabel('Reflection coefficient (%)')
plt.legend(['Schlick', 'Fresnel'])
plt.show()

