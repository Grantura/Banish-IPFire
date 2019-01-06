#!/usr/bin/perl -w
#
# Banish 1.4.7 IP Sort & iptables reload
#
# Sort the IP address on the Banish list,
# write sorted IPs back to the Banish list
# and reload iptables
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
# $Id: Banish_Sort.pl,v 1.4.7 2008/03/18 14:08 Sid McLaurin
#
# Ported to IPFire by Rob Brewer [ granturav8@gmail.com ] - 29/12/2018

# List of banished IPS/networks
$filename = "/var/ipfire/Banish/ip_Banishlist";

# Open Banish list file and read in contents
open(INFILE, $filename) or die 'Unable to open Banish list file.';
@in = <INFILE>;
close(INFILE);

# Sort IPs
@out = sort {

    pack('C4' => $a =~

      /(\d+)\.(\d+)\.(\d+)\.(\d+)/)

    cmp

    pack('C4' => $b =~

      /(\d+)\.(\d+)\.(\d+)\.(\d+)/)

  } @in;

# Write sorted list to Banish list file
open(OUTFILE, ">$filename") or die 'Unable to open Banish list file.';
flock OUTFILE, 2;
	foreach $line (@out)
	{
		print OUTFILE "$line";
	};
close(OUTFILE);

# Reload iptables rules
# For IPFire now use sysinit rwb - 19/12/18
exec('sudo /usr/local/bin/banish reload');

