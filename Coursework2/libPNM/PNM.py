import ctypes
import numpy as np
import os

try:
    libPNM = ctypes.cdll.LoadLibrary('./PNM.dll')
except OSError:
    try:
        libPNM = ctypes.cdll.LoadLibrary('./libPNM.so')
    except OSError:
        err_msg = "Attempted to load PNM.dll and libPNM.so, but could not load either. Have you correctly compiled the libraries?"
        err_msg += "\n\tCommand for compiling using Visual Studio (Windows):     \"nmake /F WINDOWS_MAKEFILE python\""
        err_msg += "\n\tCommand for compiling using gcc on unix (Linux and Mac): \"make --file UNIX_MAKEFILE python\""
        raise OSError(err_msg)
    except:
        raise
except:
    raise
    
    

libPNM.loadPPM.restype  = ctypes.POINTER(ctypes.c_ubyte)
libPNM.loadPPM.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint)]
libPNM.writePPM.restype = None
libPNM.writePPM.argtypes = [ctypes.c_char_p, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]

libPNM.loadPFM.restype = ctypes.POINTER(ctypes.c_float)
libPNM.loadPFM.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint)]
libPNM.writePFM.restype = None
libPNM.writePFM.argtypes = [ctypes.c_char_p, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]

def loadPPM(fileName):
    width       = ctypes.c_uint()
    height      = ctypes.c_uint()
    nComponents = ctypes.c_uint()
    if not os.path.exists(fileName):
        raise IOError('No such file or directory: ' + fileName)
    data_ptr = libPNM.loadPPM(fileName.encode('utf-8'), ctypes.byref(width), ctypes.byref(height), ctypes.byref(nComponents))
    return np.ctypeslib.as_array(data_ptr, shape=(height.value, width.value, nComponents.value))

def writePPM(fileName, im):
    if not im.dtype == np.uint8:
        raise TypeError('PPM images must be of type uint8: ' + str(im.dtype) + ' found instead')
    height, width, nComponents = im.shape
    data_ptr = np.ctypeslib.as_ctypes(im)
    libPNM.writePPM(fileName.encode('utf-8'), width, height, nComponents, data_ptr)

def loadPFM(fileName):
    width       = ctypes.c_uint()
    height      = ctypes.c_uint()
    nComponents = ctypes.c_uint()
    if not os.path.exists(fileName):
        raise IOError('No such file or directory: ' + fileName)
    data_ptr = libPNM.loadPFM(fileName.encode('utf-8'), ctypes.byref(width), ctypes.byref(height), ctypes.byref(nComponents))
    return np.ctypeslib.as_array(data_ptr, shape=(height.value, width.value, nComponents.value))

def writePFM(fileName, im):
    if not (im.dtype == np.float32 or im.dtype == np.float64):
        raise TypeError('PFM images must be of type float32 or float64: ' + str(im.dtype) + ' found instead')
    if not len(im.shape) == 3:
        h,w = im.shape
        tmp = im
        im = np.empty(shape=(h,w,3), dtype=np.float32)
        im[:,:,0] = im[:,:,1] = im[:,:,2] = tmp
        print(im.shape)
    height,width,nComponents = im.shape
    data_ptr = np.ctypeslib.as_ctypes(np.float32(im))
    libPNM.writePFM(fileName.encode('utf-8'), width, height, nComponents, data_ptr)
