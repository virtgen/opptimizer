# opPtimizer: optimization framework for AI   
# Copyright (c) 2019 Artur Bak

include ../../make/config.mk

HEADER_DIR=inc
SRC_DIR=src
OBJ_DIR=_obj
LIB_DIR=lib

HEADERS = $(wildcard $(HEADER_DIR)/*.h $(HEADER_DIR)/*.hxx) 
SOURCES = $(wildcard $(SRC_DIR)/*.cpp)
OBJECTS = $(patsubst $(SRC_DIR)/%.cpp, $(OBJ_DIR)/$(PLATFORM)/%.o, $(SOURCES))


all: $(OBJECTS)
	ar rvs ./lib/$(PLATFORM)/libext.a $(OBJECTS)

$(OBJ_DIR)/$(PLATFORM)/%.o: $(SRC_DIR)/%.cpp $(HEADERS) ./$(OBJ_DIR)/$(PLATFORM) ./$(LIB_DIR)/$(PLATFORM)
	$(CC) -Iinc -lstdc++ -c $< -o $@

$(OBJ_DIR):
	echo Create objects directory $(OBJ_DIR)
	mkdir $(OBJ_DIR)

$(OBJ_DIR)/$(PLATFORM): $(OBJ_DIR)
	echo Create output directory $(PLATFORM)
	mkdir $(OBJ_DIR)/$(PLATFORM)

clean: cleanobj
	echo Removing library directory files in $(LIB_DIR)
	rm -Rf $(LIB_DIR)

cleanobj:
	echo Removing temporary files in $(OBJ_DIR)
	rm -Rf $(OBJ_DIR)

$(LIB_DIR):
	echo Create library directory $(LIB_DIR)
	mkdir $(LIB_DIR)

$(LIB_DIR)/$(PLATFORM): $(LIB_DIR)
	echo Create output directory $(PLATFORM)
	mkdir $(LIB_DIR)/$(PLATFORM)

#clean:
#    rm -Rf $(OBJ_DIR)
    
test:
	echo HEADERS $(HEADERS)
	echo SOURCES $(SOURCES)
	echo OBJECTS $(OBJECTS)

