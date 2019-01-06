#
# Banish 1.4.7 Functions
#
# Add the ability to block all access to IP and/or Networks
#
# SID Solutions
# Solid Innovative Designed Solutions
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
# $Id: Banish.cgi,v 1.4.7 2008/03/18 14:08 Sid McLaurin
#
# Ported to IPFire by Rob Brewer [granturav8@gmail.com] 5/1/2019


package Banish;

use strict;

$|=1; # line buffering

sub validIP
{
        my $ip = $_[0];

        if (!($ip =~ /^(\d+)\.(\d+)\.(\d+)\.(\d+)$/)) {
                return 0; }
        else
        {
                my @octets = ($1, $2, $3, $4);
                foreach $_ (@octets)
                {
                        if (/^0./) {
                                return 0; }
                        if ($_ < 0 || $_ > 255) {
                                return 0; }
                }
                return 1;
        }
}

sub validiprange
{
        my $iprange = $_[0];
		
		
        if (!($iprange =~ /\-/)) {
                return 0; }
        else
        {
        	my @ips = split('-',$iprange);
            
            if((&validIP($ips[0]))&& (&validIP($ips[1])))
			{
            	my @beginIP = split('\.',$ips[0]);
				my @endIP = split('\.',$ips[1]);
				my $i = 0;
				chomp(@beginIP);
				chomp(@endIP);
				my $a = 0;
                
                for ($i=0; $i<=3; $i++)
                {
                	if ($beginIP[$i]< $endIP[$i])
                	{
                		$a=$i;
                	}elsif (($beginIP[$i]>$endIP[$i]) &&($a<=0))
				{
					return 0;
				}
                }
                return 1;
        }else {
		return 0;
	}
	}
}
sub validfqdn
# ipfire's version is in error so Banish needs this modified vesion.
# modified to add adition test to confirm TL is only a-z or A-Z
# as per ipcop rwb 12/12/18

{
        my $part;
        my $tld;
     
        # Checks a fully qualified domain name against RFC1035
        my $fqdn = $_[0];
        my @parts = split (/\./, $fqdn);        # Split hostname at the '.'
        if (scalar(@parts) < 2) {               # At least two parts should
                return 0;}                      # exist in a FQDN
                                                # (i.e.hostname.domain)
        foreach $part (@parts) {
                # Each part should be at least one character in length
                # but no more than 63 characters
                if (length ($part) < 1 || length ($part) > 63) {
                        return 0;}
                # Only valid characters are a-z, A-Z, 0-9 and -
                if ($part !~ /^[a-zA-Z0-9-]*$/) {
                        return 0;}
                # First character can only be a letter or a digit
                if (substr ($part, 0, 1) !~ /^[a-zA-Z0-9]*$/) {
                        return 0;}
                # Last character can only be a letter or a digit
                if (substr ($part, -1, 1) !~ /^[a-zA-Z0-9]*$/) {
                        return 0;}
           # Store for additional check on TLD
           $tld = $part;
        } 

        # TLD valid characters are a-z, A-Z
        if ($tld !~ /^[a-zA-Z]*$/) {
        return 0;
        }
        return 1;
}
1;
