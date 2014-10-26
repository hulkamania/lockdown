ROOT= /
BASE= /usr/local
LIB_DIR= $(BASE)/lockdown/lib
BIN_DIR= $(BASE)/lockdown/bin
CONF_DIR= $(BASE)/lockdown/conf
LIB_LOCKDOWN= src/connassert.py src/conninfo.py src/connlog.py src/conntables.py src/common.py
LIB_TEST= src/perf_test.py
LIB_LDUI= src/logreader.py src/violation.py
BINS= src/lockdown src/log_analyzer src/violation_tool uninstall.sh
PYTHON=`which python`
PY_VER=`python --version 2>&1 | cut -d'.' -f1`

build :
	# prepare the library directory for the lockdown software
	@mkdir -p build$(LIB_DIR)/lockdown/test
	@touch    build$(LIB_DIR)/lockdown/__init__.py
	@touch    build$(LIB_DIR)/lockdown/test/__init__.py
	@cp $(LIB_LOCKDOWN) build$(LIB_DIR)/lockdown/
	@cp $(LIB_TEST)     build$(LIB_DIR)/lockdown/test/
	# prepare the base libraries 
	@touch build$(LIB_DIR)/__init__.py
	@cp    src/daemonize.py build$(LIB_DIR)/
	# prepare the library directory for the helper software
	@mkdir -p build$(LIB_DIR)/ldui
	@touch    build$(LIB_DIR)/ldui/__init__.py
	@cp $(LIB_LDUI)         build$(LIB_DIR)/ldui/
	@cp src/_ldui_common.py build$(LIB_DIR)/ldui/common.py
	# prepare the binaries
	@mkdir -p build$(BIN_DIR)
	@cp $(BINS) build$(BIN_DIR)/
	@sed -i 's#<BASE>#'$(BASE)'#g' build$(BIN_DIR)/uninstall.sh
	@mkdir -p build/sbin
	@cp src/lockdown.bin     build/sbin/lockdown
	@cp src/log_analyzer.bin build/sbin/log_analyzer
	@sed -i 's#<BASE>#'$(BASE)'#g' build/sbin/lockdown
	@sed -i 's#<BASE>#'$(BASE)'#g' build/sbin/log_analyzer
	# setup the default configuration files
	@mkdir -p build$(BASE)/lockdown/conf
	@cp -r conf/* build$(BASE)/lockdown/conf/

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
	@cp -r build/* $(ROOT)
	@mkdir -p $(ROOT)/$(BASE)/lockdown/log
	# add binaries
	@chmod 750 $(ROOT)/sbin/lockdown
	@chmod 750 $(ROOT)/sbin/log_analyzer
	@chmod 750 $(ROOT)/$(BIN_DIR)/uninstall.sh
