# opPtimizer: optimization framework for AI   
# Copyright (c) 2019 Artur Bak

include ../../make/config.mk

SOURCES = $(wildcard *.cpp)
OBJECTS = $(patsubst %.cpp, $(PLATFORM)/%, $(SOURCES))
EXT_DIR=ext

all: $(OBJECTS)

$(PLATFORM)/%: %.cpp ./$(PLATFORM)
ifeq ($(PLATFORM),linux64)
	$(CC) $< -o $@ -lstdc++ -l$(EXT_DIR) -L../../$(EXT_DIR)/cpp/lib/$(PLATFORM) -I../../$(EXT_DIR)/cpp/inc
else ifeq ($(PLATFORM),macos)
	$(CC) $< -o $@ -lstdc++ -l$(EXT_DIR) -L../../$(EXT_DIR)/cpp/lib/$(PLATFORM) -I../../$(EXT_DIR)/cpp/inc
else ifeq ($(PLATFORM),win64)
	$(CC) $< -ldpext -o $@ -lstdc++ -L../../$(EXT_DIR)/cpp/lib/$(PLATFORM) -I../../$(EXT_DIR)/cpp/inc
endif

$(PLATFORM):
	echo Create output directory $(PLATFORM)
	mkdir $(PLATFORM)

clean:
	echo Removing binary output of odule in $(PLATFORM)
	rm -Rf $(PLATFORM)