#!/usr/bin/env python

# opPtimizer: optimization framework for AI  
# Copyright (c) 2019 Artur Bak. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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