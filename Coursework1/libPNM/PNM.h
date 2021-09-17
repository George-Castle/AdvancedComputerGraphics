#ifndef __LOADPNM_H__
#define __LOADPNM_H__

#ifdef __linux__
	#define EXPORT extern "C"
#elif __unix__
	#define EXPORT extern "C"
#elif __APPLE__
	#define EXPORT extern "C"
#else
	#define EXPORT __declspec(dllexport)
#endif

#include <stdio.h>
#include <stdlib.h>

EXPORT unsigned char *
loadPPM( const char *filename,
	 unsigned int *width, unsigned int *height,
	 unsigned int *numComponents );

EXPORT void
writePPM( const char *filename,
          unsigned int width, unsigned int height,
          unsigned int numComponents,
          unsigned char* imageData );
   

EXPORT float *
loadPFM( const char *filename,
	 unsigned int *width, unsigned int *height,
	 unsigned int *numComponents );

EXPORT void
writePFM( const char *filename,
          unsigned int width, unsigned int height,
          unsigned int numComponents,
          float* imageData );

   
#endif

