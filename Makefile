ROOT?= /
BUILD_DIR?= build
BASE?= /usr/local
DOC_DIR= /usr/share/doc
LIB_DIR= $(BASE)/lockdown/lib
BIN_DIR= $(BASE)/lockdown/bin
CONF_DIR= $(BASE)/lockdown/conf
LIB_LOCKDOWN= src/connassert.py src/conninfo.py src/connlog.py src/conntables.py src/common.py
LIB_TEST= src/perf_test.py
LIB_LDUI= src/logreader.py src/violation.py
BINS= src/lockdown src/log_analyzer src/violation_tool src/logger uninstall.sh
PYTHON=`which python`
PY_VER=`python --version 2>&1 | cut -d'.' -f1`

build :
	# prepare the library directory for the lockdown software
	@mkdir -p $(BUILD_DIR)$(LIB_DIR)/lockdown/test
	@touch    $(BUILD_DIR)$(LIB_DIR)/lockdown/__init__.py
	@touch    $(BUILD_DIR)$(LIB_DIR)/lockdown/test/__init__.py
	@cp $(LIB_LOCKDOWN) $(BUILD_DIR)$(LIB_DIR)/lockdown/
	@cp $(LIB_TEST)     $(BUILD_DIR)$(LIB_DIR)/lockdown/test/
	# prepare the base libraries 
	@touch $(BUILD_DIR)$(LIB_DIR)/__init__.py
	@cp    src/daemonize.py $(BUILD_DIR)$(LIB_DIR)/
	# prepare the library directory for the helper software
	@mkdir -p $(BUILD_DIR)$(LIB_DIR)/ldui
	@touch    $(BUILD_DIR)$(LIB_DIR)/ldui/__init__.py
	@cp $(LIB_LDUI)         $(BUILD_DIR)$(LIB_DIR)/ldui/
	@cp src/_ldui_common.py $(BUILD_DIR)$(LIB_DIR)/ldui/common.py
	# prepare the binaries
	@mkdir -p $(BUILD_DIR)$(BIN_DIR)
	@cp $(BINS) $(BUILD_DIR)$(BIN_DIR)/
	@sed -i 's#<BASE>#'$(BASE)'#g' $(BUILD_DIR)$(BIN_DIR)/uninstall.sh
	@mkdir -p $(BUILD_DIR)/sbin
	@cp src/lockdown.bin     $(BUILD_DIR)/sbin/lockdown
	@cp src/log_analyzer.bin $(BUILD_DIR)/sbin/log_analyzer
	@sed -i 's#<BASE>#'$(BASE)'#g' $(BUILD_DIR)/sbin/lockdown
	@sed -i 's#<BASE>#'$(BASE)'#g' $(BUILD_DIR)/sbin/log_analyzer
	@chmod 750 $(BUILD_DIR)/sbin/lockdown
	@chmod 750 $(BUILD_DIR)/sbin/log_analyzer
	@chmod 750 $(BUILD_DIR)/$(BIN_DIR)/uninstall.sh
	# setup the default configuration files
	@mkdir -p $(BUILD_DIR)$(BASE)/lockdown/conf
	@cp -r conf/* $(BUILD_DIR)$(BASE)/lockdown/conf/
	# setup the documentation
	@mkdir -p $(BUILD_DIR)$(DOC_DIR)/lockdown
	@cp CHANGES   $(BUILD_DIR)$(DOC_DIR)/lockdown/.
	@cp LICENSE   $(BUILD_DIR)$(DOC_DIR)/lockdown/.
	@cp README.md $(BUILD_DIR)$(DOC_DIR)/lockdown/.
	# create the log dir
	@mkdir -p $(BUILD_DIR)/$(BASE)/lockdown/log

clean :
	# remove build
	@rm -rf build

install :
	# check python
	@if [ "$(PYTHON)" = "" ]; then \
		echo "python not found"; \
		exit 1; \
	elif [ "$(PY_VER)" != "Python 2" ]; then \
		echo "Python 2 required"; \
		exit 2; \
	fi
	# check build
	@if [ ! -d build ]; then \
		echo "please run 'make build' first"; \
		exit 3; \
	fi
	# install software
	@cp -r build/sbin/* $(ROOT)/sbin/.
	@if [ ! -d $(ROOT)/$(BASE)/lockdown ]; then \
		mkdir $(ROOT)/${BASE}/lockdown; \
	fi
	@cp -r build/${BASE}/lockdown/bin $(ROOT)/${BASE}/lockdown/.
	@cp -r build/${BASE}/lockdown/lib $(ROOT)/${BASE}/lockdown/.
	@if [ ! -d $(ROOT)/$(BASE)/lockdown/conf ]; then \
		cp -r build/${BASE}/lockdown/conf $(ROOT)/${BASE}/lockdown/.; \
	fi
	@cp -r build/${BASE}/lockdown/conf/test $(ROOT)/${BASE}/lockdown/conf/.
	@if [ ! -d $(ROOT)/$(BASE)/lockdown/log ]; then \
		mkdir $(ROOT)/${BASE}/lockdown/log; \
	fi
	# copy documentation
	@cp -r $(BUILD_DIR)$(DOC_DIR)/* $(ROOT)$(DOC_DIR)

rpm-build :
	@mkdir -p rpmbuild/BUILD
	@mkdir -p rpmbuild/RPMS/i386
	@mkdir -p rpmbuild/SOURCES
	@mkdir -p rpmbuild/SPECS
	@mkdir -p rpmbuild/SRPMS
	export BUILD_DIR=rpmbuild/BUILD;$(MAKE) build
	@rpmbuild --buildroot $(shell pwd)/rpmbuild/BUILD -ba lockdown.spec
	@rm -rf rpmbuild
