import matplotlib.pyplot as plt
import sys
import numpy as np
import math
import random
from PNM import *

def NormalisePFMVals(img):
    height,width,_ = img.shape 
    for y in range(height):
        for x in range(width):
            if img[y,x,0] > 1.0:
                img[y,x,0] = 1.0
            if img[y,x,1] > 1.0:
                img[y,x,1] = 1.0
            if img[y,x,2] > 1.0:
                img[y,x,2] = 1.0
    return(img)



def PDFbuilder(samples, in_path, out_path, rgb_out):
    img = loadPFM(in_path)
    img_in = NormalisePFMVals(img)
    
    img_out = np.empty(shape=img_in.shape, dtype=img_in.dtype)
    img_in_copy = np.empty(shape=img_in.shape, dtype=img_in.dtype)
    rgb_sample_img = np.empty(shape=img_in.shape, dtype=img_in.dtype)
    
    height,width,_ = img_in.shape # Retrieve height and width
    PDFY = np.arange(height)
    CDFY = np.arange(height)
    
    xacc = 0
    xmax = 0
    xmin = 10000
    

    # LOOP FOR CALCULATING INTENSITY VAL OF EACH PIXEL IN PFM ARRAY
    for y in range(height):
        xacc = 0
        for x in range(width):
            intensity = (img_in[y,x,0] + img_in[y,x,1] + img_in[y,x,2])/3 
            xacc = xacc + intensity # accumulating intensity of each pixel in scan line
            img_in_copy[y,x,:] = img_in[y,x,:]
            rgb_sample_img[y,x,:] =  0.0
            img_out[y,x,:] = intensity
        if (xacc > xmax):
            xmax = xacc
        if (xacc < xmin):
            xmin = xacc
        PDFY[y] = xacc #1D array of scan line intensity totals

    #PLOT CODE
    #plt.title("1D vertical PDF of horizontal scan lines")
    #plt.ylabel('Accumulation of energy in scan line')
    #plt.xlabel('Pixel row index (0 - 512)')
    #norm = ((PDFY - xmin)/(xmax - xmin))
    #plt.plot(norm)
    #plt.show()

    # LOOP FOR ADDING SINE MODULATION TO SCAN LINE PDFS AND CREATING CDF
    for y in range(height):
        y_theta = (y/height) * math.pi #convert to spherical coords
        sin_modulation = math.sin(y_theta) # calc sine theta pole weighting

        PDFY[y] = ((PDFY[y] - xmin)/(xmax - xmin))*100 # normalise to 0-100 range 
        if y > 0:
            CDFY[y] = CDFY[y-1] + (PDFY[y]*sin_modulation) # calc CDF with sine modulation
        else:
            CDFY[0] = PDFY[0]

    # LOOP FOR NORMALISING CDF
    for y in range(height):
        CDFY[y] = ((CDFY[y] - CDFY[0])/(CDFY[height-1] - CDFY[0]))*100 # normalise CDF to 0-100 range

    # GENERATE RANDOM SAMPLE NUMBERS AND USE TO FIND ROWS
    sample_num = int(math.sqrt(samples))
    sample_array = np.arange(sample_num)
    row_samp_matrix = np.empty(shape=(sample_num, sample_num), dtype=np.float32)

    for s in range(sample_num):
        sample_array[s] = find_nearest(CDFY, random.randint(0,100)) # find row from inverse CDF y index (THETA INDEX)
        row_array = np.arange(width)
        row_array = img_out[sample_array[s], :, 1] # summed pixel intensity values from first loop
        row_samp_matrix[s, :] = createCDFofRow(row_array, sample_num) # x index (PHI INDEX)


    for y in range(len(sample_array)):
        for x in range(len(sample_array)):
            y_index = sample_array[y]
            x_index = int(row_samp_matrix[y, x])
            if((y_index-2) >= 0 and (y_index-2) < height-3):
                if((x_index-2) >= 0 and (x_index-2) < width-3):
                    for vert in range(5):   # make 5x5 blue pixel square if within array bounds
                        for horiz in range(5):
                            rgb_sample_img[((y_index-2)+vert), ((x_index-2)+horiz), 0] = img_in[((y_index-2)+vert), ((x_index-2)+horiz), 0] # image with black and rgb vals
                            rgb_sample_img[((y_index-2)+vert), ((x_index-2)+horiz), 1] = img_in[((y_index-2)+vert), ((x_index-2)+horiz), 1]
                            rgb_sample_img[((y_index-2)+vert), ((x_index-2)+horiz), 2] = img_in[((y_index-2)+vert), ((x_index-2)+horiz), 2]
                            img_in_copy[((y_index-2)+vert), ((x_index-2)+horiz), 0] = 0.0
                            img_in_copy[((y_index-2)+vert), ((x_index-2)+horiz), 1] = 0.0
                            img_in_copy[((y_index-2)+vert), ((x_index-2)+horiz), 2] = 1.0
                else: # if unable to make 5x5 square just change iduvidual pixel colour
                    rgb_sample_img[y_index, x_index, 0] = img_in[y_index, x_index, 0]
                    rgb_sample_img[y_index, x_index, 1] = img_in[y_index, x_index, 1]
                    rgb_sample_img[y_index, x_index, 2] = img_in[y_index, x_index, 2]
                    img_in_copy[y_index, x_index, 0] = 0.0
                    img_in_copy[y_index, x_index, 1] = 0.0
                    img_in_copy[y_index, x_index, 2] = 1.0
            else: # if unable to make 5x5 square just change iduvidual pixel colour
                rgb_sample_img[y_index, x_index, 0] = img_in[y_index, x_index, 0]
                rgb_sample_img[y_index, x_index, 1] = img_in[y_index, x_index, 1]
                rgb_sample_img[y_index, x_index, 2] = img_in[y_index, x_index, 2]
                img_in_copy[y_index, x_index, 0] = 0.0
                img_in_copy[y_index, x_index, 1] = 0.0
                img_in_copy[y_index, x_index, 2] = 1.0
    #PLOT CODE
    #g = CDFY/100
    #plt.plot(g)
    #plt.title("CDF of horizontal scan lines with sine modulation")
    #plt.ylabel('Accumulation of row intensity totals')
    #plt.xlabel('Pixel row index (0 - 512)')
    #plt.plot(PDFY)
    #plt.show()
    writePFM(out_path, img_in_copy)
    writePFM(rgb_out, rgb_sample_img)


def createCDFofRow(row_array, sample_num):
    for x in range(len(row_array)):
        if x > 0:
            row_array[x] = row_array[x-1] + (row_array[x]) # calc CDF 
    #normalisation loop
    for y in range(len(row_array)):
        row_array[y] = ((row_array[y] - row_array[0])/(row_array[len(row_array)-1] - row_array[0]))*100 # normalise CDF to 0-100 range

    # GENERATE RANDOM SAMPLE NUMBERS AND USE TO FIND ROWS
    sample_array = np.arange(sample_num)
    for s in range(sample_num):
        sample_array[s] = find_nearest(row_array, random.randint(0,100)) # find row from inverse CDF 
    
    return(sample_array)
       

def find_nearest(array,value): # equivalent of numerical look up table
    idx = np.searchsorted(array, value, side="left")
    if idx > 0 and (idx == len(array) or math.fabs(value - array[idx-1]) < math.fabs(value - array[idx])):
        return idx-1 # return index of closest bin
    else:
        return idx

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

def Gamma(in_path, out_path):
    img_in = loadPFM(in_path)
    gamma = 2.1
    g = pow(img_in,1/gamma)
    writePFM(out_path, g)

path = 'C:/Users/georg/OneDrive/Desktop/MSc-Stuff/Advanced-Computer-Graphics/70001-Assignment2/GraceCathedral/'
if '__main__' == __name__:
    PDFbuilder(1024, path + 'grace_latlong.pfm', path + 'grace_samples_blue.pfm', path + 'grace_samples_rgb.pfm')
    Gamma(path + 'grace_samples_blue.pfm', path + 'gamma_samples_blue.pfm')
    Gamma(path + 'grace_samples_rgb.pfm', path + 'gamma_samples_rgb.pfm')
    LoadPFMAndSavePPM(path + 'grace_samples_blue.pfm', path + 'no_gamma.ppm')
    LoadPFMAndSavePPM(path + 'gamma_samples_rgb.pfm', path + 'gamma_rgb_out.ppm')
    LoadPFMAndSavePPM(path + 'gamma_samples_blue.pfm', path + 'gamma_samples.ppm')
    pass
