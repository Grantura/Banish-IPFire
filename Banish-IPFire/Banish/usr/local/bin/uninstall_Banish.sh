#!/bin/bash
#
# Banish 1.4.7 for IPCop 1.4.18+
# Banish uninstall script
# Version 1.4.7
#
# SID Solutions
# http://sidsolutions.net
# Copyright (c) 2005/07/10 Sid McLaurin 
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
# $Id: uninstall_Banish.sh,v 1.4.7 2008/03/18 14:08 Sid McLaurin
#
# Ported to PFire by Rob Brewer [ granturav8@gmail,com] 5/1/2019
#

# Print uninstall message to console
echo
/bin/echo -e "\033[1;32mBanish-IPFire 1.0.1 uninstall \033[0m"
/usr/bin/logger -t "banish" "Starting Banish-IPFire 1.0.1 Uninstall"
echo

# Remove Banish rules
echo -e "Flushing Banish rules................\c"
/bin/cp -p /var/ipfire/Banish/ip_Banishlist /var/ipfire/Banish/rm_Banishlist
/etc/rc.d/init.d/banish stop
echo -e "Done!\n"

# Change to /tmp directory
cd /tmp

# Remove files
echo -e "Removing files.......................\c"

/bin/rm /usr/local/bin/Banish_Sort.pl >/dev/null 2>&1
/bin/rm /usr/local/bin/banish >/dev/null 2>&1
/bin/rm /srv/web/ipfire/cgi-bin/BanishGeo.cgi >/dev/null 2>&1
/bin/rm /srv/web/ipfire/cgi-bin/Banish_Settings.cgi >/dev/null 2>&1
/bin/rm /srv/web/ipfire/cgi-bin/logs.cgi/Banishlog.dat >/dev/null 2>&1
/bin/rm /etc/rc.d/init.d/rc.banish >/dev/null 2>&1
/bin/rm -rf /srv/web/ipfire/html/images/Banish >/dev/null 2>&1
/bin/rm -rf /var/ipfire/Banish >/dev/null 2>&1
/bin/rm /etc/rc.d/rc0.d/K75banish
/bin/rm /etc/rc.d/rc3.d/S50banish
/bin/rm /etc/rc.d/rc6.d/K75banish
echo "Done!"


# Unappending files
echo -e "Restoring files......................\c"

# Removing Language entries
# English
/bin/rm /var/ipfire/addon-lang/Banish.en.pl

# Deutsch
/bin/rm /var/ipfire/addon-lang/Banish.de.pl

# French
/bin/rm /var/ipfire/addon-lang/Banish.fr.pl

# Italain
/bin/rm /var/ipfire/addon-lang/Banish.it.pl

# Spanish
/bin/rm /var/ipfire/addon-lang/Banish.es.pl

# Portuguese
/bin/rm /var/ipfire/addon-lang/Banish.pt.pl

# Netherlands
/bin/rm /var/ipfire/addon-lang/Banish.nl.pl

# Lang Script Cache Compliation
perl -e "require '/var/ipfire/lang.pl'; &Lang::BuildCacheLang"

# Remove whois tweak
/bin/cat /srv/web/ipfire/cgi-bin/ipinfo.cgi | sed -e '/Added for Banish/,/End Banish/d' > /tmp/ipinfo.cgi.tmp
/usr/bin/perl -pi.old -e "s/address \./addr \./g" ipinfo.cgi.tmp
/bin/cp /tmp/ipinfo.cgi.tmp /srv/web/ipfire/cgi-bin/ipinfo.cgi
/bin/rm /tmp/ipinfo.cgi.tmp
/bin/rm /tmp/ipinfo.cgi.tmp.old

# Remove firewall log tweak
/bin/cat /srv/web/ipfire/cgi-bin/logs.cgi/firewalllog.dat | sed -e '/Added for Banish/,/End Banish/d' > /tmp/firewalllog.dat.tmp
/bin/cp /tmp/firewalllog.dat.tmp /srv/web/ipfire/cgi-bin/logs.cgi/firewalllog.dat
/bin/rm /tmp/firewalllog.dat.tmp

# Remove system log tweak
/bin/cat /srv/web/ipfire/cgi-bin/logs.cgi/log.dat | sed -e '/Added for Banish/,/End Banish/d' > /tmp/log.dat.tmp
/bin/cp /tmp/log.dat.tmp /srv/web/ipfire/cgi-bin/logs.cgi/log.dat
/bin/rm /tmp/log.dat.tmp

# Remove sudoers tweak
/bin/cat /etc/sudoers | sed -e '/Added for Banish/,/End Banish/d' > /tmp/sudoers.tmp
/bin/cp /tmp/sudoers.tmp /etc/sudoers
/bin/rm /tmp/sudoers.tmp

echo "Done!"

# Remove backup directory
/bin/rm -rf /Banish >/dev/null 2>&1

# Remove uninstall script
rm -f /usr/local/bin/uninstall_Banish.sh

echo
echo -e "\033[1;32mBanish-IPFire 1.0.1 Uninstall Complete \033[0m"
/usr/bin/logger -t "banish" "Banish-IPFire-1.0.1 Uninstall Completed"
echo
