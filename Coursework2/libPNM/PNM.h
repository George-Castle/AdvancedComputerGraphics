#ifndef __LOADPNM_H__
#define __LOADPNM_H__

#ifdef __linux__
	#ifdef __cplusplus
		#define EXPORT extern "C"
	#else
		#define EXPORT
	#endif
#elif __unix__
	#ifdef __cplusplus
		#define EXPORT extern "C"
	#else
		#define EXPORT
	#endif
#elif __APPLE__
	#ifdef __cplusplus
		#define EXPORT extern "C"
	#else
		#define EXPORT
	#endif
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

