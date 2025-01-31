# 设置通用变量
SOURCE_PATH = $(PWD)
BIN_DIR = $(SOURCE_PATH)/bin

ABC_PATH = $(SOURCE_PATH)/abc
AIGER_PATH = $(SOURCE_PATH)/aiger
CAR_PATH = $(SOURCE_PATH)/simplecar-tcad
IC3_PATH = $(SOURCE_PATH)/IC3ref

TOOL_DIRS = \
    $(SOURCE_PATH)/tool/pdr-feedback/bin/ \
	$(SOURCE_PATH)/tool/backward-car-feedback/bin/ \
	$(SOURCE_PATH)/tool/forward-car-feedback/bin/ \
	$(SOURCE_PATH)/tool/ic3ref-feedback/bin/ \
    $(SOURCE_PATH)/tool/tool-compare/aigen/bin/ \
    $(SOURCE_PATH)/tool/tool-compare/aigfuzz/bin/ \
    $(SOURCE_PATH)/tool/tool-compare/aigrow-no-feedback/bin/ \
    $(SOURCE_PATH)/tool/tool-compare/aigrow-single-thread/pdr-feedback/bin/ \
	$(SOURCE_PATH)/tool/tool-compare/aigrow-single-thread/backward-car-feedback/bin/ \
	$(SOURCE_PATH)/tool/tool-compare/aigrow-single-thread/forward-car-feedback/bin/ \
	$(SOURCE_PATH)/tool/tool-compare/aigrow-single-thread/ic3ref-feedback/bin/

.PHONY: abc aiger simplecar ic3
all: abc aiger simplecar ic3

abc:
	tar -zxf $(SOURCE_PATH)/packages/checkers/abc.tar.gz -C $(SOURCE_PATH)
	cd $(ABC_PATH) && $(MAKE) ABC_USE_NO_READLINE=1 ABC_MAKE_NO_DEPS=1
	mkdir -p $(BIN_DIR)
	mv $(ABC_PATH)/abc $(BIN_DIR)/abc
	$(foreach dir, $(TOOL_DIRS), mkdir -p $(dir) && ln -sf $(BIN_DIR)/abc $(dir)abc;)

aiger:
	tar -zxf $(SOURCE_PATH)/packages/checkers/aiger.tar.gz -C $(SOURCE_PATH)
	cd $(AIGER_PATH) && ./configure.sh && $(MAKE)
	mkdir -p $(BIN_DIR)
	mv $(AIGER_PATH)/aigtoaig $(BIN_DIR)/aigtoaig
	mv $(AIGER_PATH)/aigfuzz $(BIN_DIR)/aigfuzz
	$(foreach dir, $(TOOL_DIRS), mkdir -p $(dir) && ln -sf $(BIN_DIR)/aigtoaig $(dir)aigtoaig;)
	$(foreach dir, $(TOOL_DIRS), mkdir -p $(dir) && ln -sf $(BIN_DIR)/aigfuzz $(dir)aigfuzz;)

simplecar:
	tar -zxf ${SOURCE_PATH}/packages/checkers/simplecar.tar.gz -C $(SOURCE_PATH)
	cd $(CAR_PATH) && $(MAKE)
	mkdir -p $(BIN_DIR)
	mv $(CAR_PATH)/simplecar $(BIN_DIR)/simplecar
	$(foreach dir, $(TOOL_DIRS), mkdir -p $(dir) && ln -sf $(BIN_DIR)/simplecar $(dir)simplecar;)

ic3:
# from https://github.com/arbrad/IC3ref.git
	tar -zxf ${SOURCE_PATH}/packages/checkers/IC3ref.tar.gz -C $(SOURCE_PATH)
	cd ${IC3_PATH}/minisat && $(MAKE)
# from https://github.com/agurfinkel/minisat
	cp ${SOURCE_PATH}/packages/checkers/aiger.tar.gz ${IC3_PATH}
	tar -zxf ${IC3_PATH}/aiger.tar.gz -C ${IC3_PATH}
	cd ${IC3_PATH} && $(MAKE)
	mkdir -p $(BIN_DIR)
	mv $(IC3_PATH)/IC3 $(BIN_DIR)/IC3
	$(foreach dir, $(TOOL_DIRS), ln -sf $(BIN_DIR)/IC3 $(dir)IC3;)

clean:
	echo "After you know there exists a rm -rf, change me to rm -rf manually."
	rm -f $(ABC_PATH) $(AIGER_PATH) $(BIN_DIR) ${CAR_PATH} ${IC3_PATH}
	$(foreach dir, $(TOOL_DIRS), rm -rf $(dir)/abc;)
	$(foreach dir, $(TOOL_DIRS), rm -rf $(dir)/aig*;)
	$(foreach dir, $(TOOL_DIRS), rm -rf $(dir)/IC3;)
	$(foreach dir, $(TOOL_DIRS), rm -rf $(dir)/simplecar*;)
