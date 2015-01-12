Name: lockdown
Version: 0
Release: 9
Summary: Filter outgoing connections based on originating binary
License: GPLv2
Distribution: Fedora
Group: Applications/System

%define _rpmdir .
%define _rpmfilename %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm
%define _unpackaged_files_terminate_build 0

%description
Firewall tool used to filter outgoing connections based on which binary is
initiating the connection.

%files
%defattr(-,root,root,-)
"/sbin/lockdown"
"/sbin/log_analyzer"
"/usr/local/lockdown/bin/lockdown"
"/usr/local/lockdown/bin/log_analyzer"
"/usr/local/lockdown/bin/logger"
"/usr/local/lockdown/bin/uninstall.sh"
"/usr/local/lockdown/bin/violation_tool"
"/usr/local/lockdown/conf/main.conf"
"/usr/local/lockdown/conf/tcp.conf"
"/usr/local/lockdown/conf/test"
"/usr/local/lockdown/conf/test/test_hosts.json"
"/usr/local/lockdown/conf/udp.conf"
"/usr/local/lockdown/lib/__init__.py"
"/usr/local/lockdown/lib/daemonize.py"
"/usr/local/lockdown/lib/ldui"
"/usr/local/lockdown/lib/ldui/__init__.py"
"/usr/local/lockdown/lib/ldui/common.py"
"/usr/local/lockdown/lib/ldui/logreader.py"
"/usr/local/lockdown/lib/ldui/violation.py"
"/usr/local/lockdown/lib/lockdown"
"/usr/local/lockdown/lib/lockdown/__init__.py"
"/usr/local/lockdown/lib/lockdown/common.py"
"/usr/local/lockdown/lib/lockdown/connassert.py"
"/usr/local/lockdown/lib/lockdown/conninfo.py"
"/usr/local/lockdown/lib/lockdown/connlog.py"
"/usr/local/lockdown/lib/lockdown/conntables.py"
"/usr/local/lockdown/lib/lockdown/test"
"/usr/local/lockdown/lib/lockdown/test/__init__.py"
"/usr/local/lockdown/lib/lockdown/test/perf_test.py"
"/usr/local/lockdown/log"
"/usr/share/doc/lockdown"
"/usr/share/doc/lockdown/CHANGES"
"/usr/share/doc/lockdown/LICENSE"
"/usr/share/doc/lockdown/README.md"
