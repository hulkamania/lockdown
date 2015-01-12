lockdown
========
Block/allow outgoing connections based on what binary (and which user) made the connection.

This is the first version. Open to be tested, critized, whatever.

Feel free to drop comments/suggestions/ideas at lockdown.tables<at>gmail.com


requirements
============
* iptables
* python 2.x
* python-ipaddr
* dpkt (https://code.google.com/p/dpkt/)
** deb : python-dpkt
** rpm : python-dpkt
* nfqueue
** deb : libnetfilter-queue
** rpm : libnetfilter-queue
* nfqueue python bindings
** deb : python-nfqueue
** rpm : python-nfqueue-0.4-7.x86_64.rpm (provided in depends/rpm)
* python-inet_diag
** deb : python-inet-diag_0.1-2_amd64.deb (provided in depends/deb)
** rpm : python-inet_diag-0.1-1.fc21.x86_64.rpm (provided in depends/rpm)

installation
============
1. install requirements
2. a. install .rpm or .deb (provided in packages) OR
   b. make build; sudo make install

uninstall
=========
uninstall.sh in <install directory>/bin/

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

known issues
============

fixed issues
============
FIXED (v0.9) when running the lookup for the process making a DNS request a major performance hit is seen (1-2 seconds), due to this DNS traffic is currently whitelisted
