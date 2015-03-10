CC=g++
#TO ENABLE DEBUG MESSAGES ADD OPTION -DDEBUG
CFLAGSmdsutils=  -c -o3 -fPIC  -D_FILE_OFFSET_BITS=64 -D_LARGE_FILES -I. -I{MDSPLUS_DIR}/include
CFLAGSstreamutils= -c -o3 -fPIC  -D_FILE_OFFSET_BITS=64 -D_LARGE_FILES -I.
##############
LDFLAGSstreamutils = -shared -lrt -pthread
LDFLAGSmdsutils = -shared -lrt -pthread -L/usr/local/mdsplus/lib -lMdsObjectsCppShr -lMdsIpShr

SOURCESstreamutils=camstreamutils.cpp 
SOURCESmdsutils=cammdsutils.cpp 

INCstreamutils=libcamstreamutils.h 
INCmdsutils=libcammdsutils.h

OBJstreamutils=camstreamutils.o
OBJmdsutils=cammdsutils.o

SHAREDLIBstreamutils=libcamstreamutils.so 
SHAREDLIBmdsutils=libcammdsutils.so 

all: $(SHAREDLIBstreamutils) $(SHAREDLIBmdsutils) 
 
$(OBJstreamutils):$(SOURCESstreamutils)
	$(CC) $(CFLAGSstreamutils) $< -o $@

$(OBJmdsutils):$(SOURCESmdsutils)
	$(CC) $(CFLAGSmdsutils) $< -o $@

$(SHAREDLIBstreamutils):$(OBJstreamutils)
	$(CC) $(OBJstreamutils) -o $(SHAREDLIBstreamutils) $(LDFLAGSstreamutils) 

$(SHAREDLIBmdsutils):$(OBJmdsutils)
	$(CC) $(OBJmdsutils) -o $(SHAREDLIBmdsutils) $(LDFLAGSmdsutils) 

clean:
	rm $(OBJstreamutils)
	rm $(SHAREDLIBstreamutils)
	rm $(OBJmdsutils)
	rm $(SHAREDLIBmdsutils)	

