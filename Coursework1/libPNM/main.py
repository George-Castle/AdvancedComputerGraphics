import sys
import math
import numpy as np
from PNM import *

def CreateCircle(in_path, out_path):
    img_in = loadPFM(in_path)
    height,width,_ = img_in.shape
    a = width/2
    b = height/2
    for y in range(height):
        for x in range(width):
            if abs(((x - a)**2) + ((y - b)**2)) > (255**2): #when out the bounds of the circle
                img_in[y,x,:] = 0.0
            else:
                img_in[y,x,0] = x/511 # normalise using division to val between 0 and 1
                img_in[y,x,1] = 1-(y/511) # invert y axis and normalise 
                img_in[y,x,2] = (math.sqrt((255**2)-((y - b)**2)-((x - a)**2))) / 255.5 # calc z value from sphere equation

    writePFM(out_path, img_in)

def CreateNormalMap(in_path, out_path):
    img_in = loadPFM(in_path)
    height,width,_ = img_in.shape
    a = width/2
    b = height/2
    for y in range(height):
        for x in range(width):
            if abs(((x - a)**2) + ((y - b)**2)) > (255**2): #when out the bounds of the circle
                img_in[y,x,:] = 0.0
            else:
                nx = (x - 255)/255 #normalise x and y
                ny = (y - 255)/(-255)
                z = (math.sqrt((255**2)-((y - b)**2)-((x - a)**2))) # calc and normalise z
                nz = (z)/255
                rx = nx/(math.sqrt((nx**2)+(ny**2)+((nz + 1)**2)))
                ry = ny/(math.sqrt((nx**2)+(ny**2)+((nz + 1)**2)))
                rz = nz/(math.sqrt((nx**2)+(ny**2)+((nz + 1)**2)))
                img_in[y,x,0] = (rx*0.5) + 0.5
                img_in[y,x,1] = (ry*0.5) + 0.5 
                img_in[y,x,2] = (rz*0.5) + 0.5

    writePFM(out_path, img_in)

def Gamma(in_path, out_path):
    img_in = loadPFM(in_path)
    gamma = 0.5
    g = pow(img_in,1/gamma)
    writePFM(out_path, g)

def CreateLatLongMap(in_path_ref, in_path_urban, out_path):
    img_ref = loadPFM(in_path_ref)
    img_urban = loadPFM(in_path_urban)
    height,width,_ = img_ref.shape
    latitude,longitude,_ = img_urban.shape
    img_out = np.empty(shape=(width, height, 3), dtype=np.float32)

    a = width/2
    b = height/2

    for y in range(height):
        for x in range(width):
            if abs(((x - a)**2) + ((y - b)**2)) > (255**2): #when out the bounds of the circle
                img_out[y,x,:] = 0.0
            else:
                nx = img_ref[y,x,0]
                ny = img_ref[y,x,1]
                nz = img_ref[y,x,2]
                nmx = (nx - 0.5)/0.5 # normalise to -1 -> 1 range
                nmy = (ny - 0.5)/0.5
             
                theta = math.acos(-nmy)
                phi = math.atan2(nz, nmx)

                phi1 = (phi + (math.pi/2))/(2*math.pi) #convert to 0 to 1 range
                theta1 = (theta)/(math.pi)
                plong = int(phi1 * (longitude))-1 # minus one to stay within array bounds
                tlat = (latitude-1) - int(theta1 * (latitude)) # latitude minus to invert y axis

                img_out[y,x,0] = img_urban[tlat,plong,0]
                img_out[y,x,1] = img_urban[tlat,plong,1]
                img_out[y,x,2] = img_urban[tlat,plong,2]
    writePFM(out_path, img_out)


def CreateReflectionMap(in_path, out_path):
    img_in = loadPFM(in_path)
    height,width,_ = img_in.shape
    a = width/2
    b = height/2
    for y in range(height):
        for x in range(width):
            if abs(((x - a)**2) + ((y - b)**2)) > (255**2): #when out of the bounds of the circle
                img_in[y,x,:] = 0.0
            else:
                nx = (x - a)/a #normalise x and y to -1 to 1 range
                ny = (y - b)/(-b)
                z = (math.sqrt((a**2)-((y - b)**2)-((x - a)**2))) # calc and normalise z
                nz = (z)/a
                rx = (2 * nz * nx) # find reflection vector using r = 2*(n.v)*n-v
                ry = (2 * nz * ny)
                rz = (2 * nz * nz) - 1
                img_in[y,x,0] = (rx*0.5) + 0.5
                img_in[y,x,1] = (ry*0.5) + 0.5 
                img_in[y,x,2] = rz

    writePFM(out_path, img_in)

def CreateAndSavePFM(out_path):
    width = 512
    height = 512
    numComponents = 3

    img_out = np.empty(shape=(width, height, numComponents), dtype=np.float32)
    
    for y in range(height):
        for x in range(width):
            img_out[y,x,:] = 1.0

    writePFM(out_path, img_out)

def LoadAndSavePPM(in_path, out_path):
    img_in = loadPPM(in_path)
    img_out = np.empty(shape=img_in.shape, dtype=img_in.dtype)
    height,width,_ = img_in.shape # Retrieve height and width
    for y in range(height):
        for x in range(width):
            img_out[y,x,:] = img_in[y,x,:] # Copy pixels

    writePPM(out_path, img_out)

def LoadAndSavePFM(in_path, out_path):
    img_in = loadPFM(in_path)
    img_out = np.empty(shape=img_in.shape, dtype=img_in.dtype)
    height,width,_ = img_in.shape # Retrieve height and width
    for y in range(height):
        for x in range(width):
            img_out[y,x,:] = img_in[y,x,:] # Copy pixels

    writePFM(out_path, img_out)

def LoadPPMAndSavePFM(in_path, out_path):
    img_in = loadPPM(in_path)
    img_out = np.empty(shape=img_in.shape, dtype=np.float32)
    height,width,_ = img_in.shape
    for y in range(height):
        for x in range(width):
            img_out[y,x,:] = img_in[y,x,:]/255.0

    writePFM(out_path, img_out)
            
def LoadPFMAndSavePPM(in_path, out_path):
    img_in = loadPFM(in_path)
    img_out = np.empty(shape=img_in.shape, dtype=np.float32)
    height,width,_ = img_in.shape
    for y in range(height):
        for x in range(width):
            img_out[y,x,:] = img_in[y,x,:] * 255.0

    writePPM(out_path, img_out.astype(np.uint8))

if '__main__' == __name__:
    path = 'C:/Users/georg/OneDrive/Desktop/MSc-Stuff/Advanced-Computer-Graphics/70001-Assignment1/UrbanProbe/'
    CreateAndSavePFM(path + 'start.pfm')
    CreateCircle(path + 'start.pfm', path + 'spherical_coord_map.pfm')
    CreateNormalMap(path + 'start.pfm', path + 'normal_map.pfm')
    CreateReflectionMap(path + 'start.pfm', path + 'reflection_map.pfm')
    CreateLatLongMap(path + 'reflection_map.pfm', path + 'urbanEM_latlong.pfm', path + 'urbanEM_sphere.pfm')
    #LoadAndSavePPM(path + 'urbanEM_latlong.ppm', path + 'test.ppm')
    LoadPPMAndSavePFM(path + 'urbanEM_latlong.ppm', path + 'urbanEM_latlong.pfm')
    #LoadAndSavePFM(path + '9.pfm', path + 'test2.pfm')
    Gamma(path + 'urbanEM_sphere.pfm', path + 'gamma_sphere.pfm')
    LoadPFMAndSavePPM(path + 'gamma_sphere.pfm', path + 'gamma_sphere.ppm')
    LoadPFMAndSavePPM(path + 'spherical_coord_map.pfm', path + 'spherical_coord_map.ppm')
    LoadPFMAndSavePPM(path + 'normal_map.pfm', path + 'normal_map.ppm')
    LoadPFMAndSavePPM(path + 'reflection_map.pfm', path + 'reflection_map.ppm')
    LoadPFMAndSavePPM(path + 'urbanEM_sphere.pfm', path + 'urbanEM_sphere.ppm')

    pass
