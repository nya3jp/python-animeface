####################################################################
#  CLAPACK make include file.                                      #
#  CLAPACK, Version 3.1.1.1                                        #
#  October 2008                                                    #
####################################################################
#
#  The machine (platform) identifier to append to the library names
#
PLAT = _nvxs
#  
#  Modify the CC and CFLAGS definitions to refer to the
#  compiler and desired compiler options for your machine.  NOOPT
#  refers to the compiler options desired when NO OPTIMIZATION is
#  selected.  Define LOADER and LOADOPTS to refer to the loader and
#  desired load options for your machine.
#
#######################################################
# This is used to compile C libary
CC        = gcc
# if no wrapping of the blas library is needed, uncomment next line
#CC        = gcc -DNO_BLAS_WRAP
CFLAGS    = -O3 -fPIC -Wno-error=implicit-function-declaration -Wno-error=implicit-int
LOADER    = gcc
LOADOPTS  =
ifeq ($(shell uname -s),Linux)
  LOADOPTS += -Wl,--allow-multiple-definition
endif
NOOPT     = -O0 -fPIC
DRVCFLAGS = $(CFLAGS)
F2CCFLAGS = $(CFLAGS)
#######################################################################
#
#  The archiver and the flag(s) to use when building archive (library)
#  If you system has no ranlib, set RANLIB = echo.
#
ARCH     = ar
ARCHFLAGS= cr
RANLIB   = ranlib
#
#  The location of the libraries to which you will link.  (The 
#  machine-specific, optimized BLAS library should be used whenever
#  possible.)
#

# Using reference BLAS
BLASLIB      = ../../libblas$(PLAT).a
# Using Vectib
#BLASLIB = -framework vecLib
# Using Fortran BLAS interface of ATLAS without wrapper (CLAPACK has to be compiled with -DNO_BLAS_WRAP)
#BLASLIB = -lf77blas -latlas
# Using Fortran BLAS interface of ATLAS with wrapper
#BLASLIB = ../../libfblaswr.a -lf77blas -latlas
# Using CBLAS interface of ATLAS with wrapper
#BLASLIB = ../../libcblaswr.a -lcblas -latlas
# Using Goto without wrapper (CLAPACK has to be compiled with -DNO_BLAS_WRAP)
#BLASLIB = -lgoto -lpthread
# Using Goto with wrapper
#BLASLIB = ../../libfblaswr.a -lgoto -lpthread 
LAPACKLIB    = liblapack$(PLAT).a
F2CLIB       = ../../F2CLIBS/libf2c.a
TMGLIB       = libtmglib$(PLAT).a
EIGSRCLIB    = eigsrc$(PLAT).a
LINSRCLIB    = linsrc$(PLAT).a

