lockdown
========
Outgoing connection firewall based on originating binary.

This is the first version. Open to be tested, critized, whatever.

Feel free to drop comments/suggestions/ideas at lockdown.tables<at>gmail.com but
please don't write just to tell me my Makefile is crude, I know it is crude. If you
really want to criticize it, please be good enough to offer improvement suggestions.

Block/allow outgoing connections based on what binary (and which user) made the connection.

requirements
============
* iptables
* python 2.x
* dpkt (https://code.google.com/p/dpkt/)
* nfqueue
* nfqueue python bindings v2.0.10 (debian variants python-nfqueue 0.4-6)
* python-inet_diag (tarball provided)

installation
============
1. install requirements
2. make build; sudo make install

uninstall
=========
uninstall.sh in this directory

usage
=====
```bash
/sbin/lockdown     # start the firewall daemon (as root)
/sbin/log_analyzer # read information from the log files
```
configuration
=============
/opt/lockdown/conf/main.conf:

property | description
-------- | -----------
log_only | do not block any connections
violation_handler | TODO future releases
default | default action for non TCP/UDP connections, 1=ALLOW, 0=BLOCK

/opt/lockdown/conf/{tcp, udp}.conf:
```json
"<user>" : {
        "<binary path>" : {
                { "port" : <minimum or only port>, "max" : <maximum port>, "destination" : [ "<destination IP or networks>", ] },
        ...
```
