BASE= opt/lockdown
PYTHON=`which python`
PY_VER=`python --version 2>&1 | cut -d'.' -f1`

build :
	# prepare the library directory for the lockdown software
	@mkdir -p build/${BASE}/lib/lockdown
	@touch build/${BASE}/lib/lockdown/__init__.py
	@cp src/connassert.py build/${BASE}/lib/lockdown
	@cp src/conninfo.py build/${BASE}/lib/lockdown/
	@cp src/connlog.py build/${BASE}/lib/lockdown/
	@cp src/conntables.py build/${BASE}/lib/lockdown/
	@cp src/common.py build/${BASE}/lib/lockdown/
	# prepare the base libraries 
	@touch build/${BASE}/lib/__init__.py
	@cp src/daemonize.py build/${BASE}/lib/
	# prepare the library directory for the helper software
	@mkdir -p build/${BASE}/lib/ldui
	@touch build/${BASE}/lib/ldui/__init__.py
	@cp src/logreader.py build/${BASE}/lib/ldui/
	@cp src/violation.py build/${BASE}/lib/ldui/
	@cp src/_ldui_common.py build/${BASE}/lib/ldui/common.py
	# prepare the binaries
	@mkdir -p build/${BASE}/bin
	@cp src/lockdown build/${BASE}/bin/
	@cp src/log_analyzer build/${BASE}/bin/
	@cp src/violation_tool build/${BASE}/bin/
	@cp src/lockdown.bin build/
	@cp src/log_analyzer.bin build/
	# setup the default configuration files
	@mkdir -p build/opt/lockdown/conf
	@cp conf/* build/opt/lockdown/conf/
clean :
	# remove build
	@rm -rf build

install :
	# check python
	@if [ "${PYTHON}" = "" ]; then \
		echo "python not found"; \
		exit 1; \
	elif [ "${PY_VER}" != "Python 2" ]; then \
		echo "Python 2 required"; \
		exit 2; \
	fi
	# check build
	@if [ ! -d build ]; then \
		echo "please run 'make build' first"; \
		exit 3; \
	fi
	# install software
	@cp -r build/opt /
	@mkdir -p /opt/lockdown/log
	# add binaries
	@cp build/lockdown.bin /sbin/lockdown
	@cp build/log_analyzer.bin /sbin/log_analyzer
	@chmod 750 /sbin/lockdown
	@chmod 750 /sbin/log_analyzer
