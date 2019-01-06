#!/usr/bin/perl
#
# Banish 1.4.7
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
# $Id: Banish.cgi,v 1.4.7 2008/03/18 20:13 Sid McLaurin
#
# Ported to IPFire 29/12/2018 by Rob Brewer
 
use strict;

# GeoIP Mod
use Geo::IP::PurePerl;
use Getopt::Std;

# enable only the following on debugging purpose
#use warnings;
#use CGI::Carp 'fatalsToBrowser';

require '/var/ipfire/general-functions.pl';
require '/var/ipfire/Banish/Banish-functions.pl';
require "${General::swroot}/lang.pl";
require "${General::swroot}/header.pl";

#workaround to suppress a warning when a variable is used only once
my @dummy = ( ${Header::colouryellow} );
undef (@dummy);

my %cgiparams=();
my %checked=();
my %selected=();
my %settings=();
my %netsettings;

# Load Network Settings
&General::readhash("${General::swroot}/ethernet/settings", \%netsettings);

my $errormessage = '';
my $filename = "${General::swroot}/Banish/Banish_config";
my $outfilename = "${General::swroot}/Banish/ip_Banishlist";
my $removefilename = "${General::swroot}/Banish/rm_Banishlist";
my $changed = 'no';
my $size = '';
my $filter_changed = '';
my $start = 0;
my $count = 0;
my $version = "Port of Banish 1.4.7 to IPFire";
my $viewsize = '0';

# Select array for Display Settings
my @VS = ('15','50','100','150','250','500');
$settings{'DISPLAY_AMOUNT'} = '50';
$settings{'ACTION'} = '';
$settings{'APPLY'} = '';

&Header::showhttpheaders();

$cgiparams{'ENABLED'} = 'off';
$cgiparams{'ACTION'} = '';
$cgiparams{'SRC'} = '';
$cgiparams{'REMARK'} ='';
$cgiparams{'CURR_SRC'} = '';
$cgiparams{'START'} = 0;
$cgiparams{'FILTER'} = '';

# Get Current Configuration
&Header::getcgihash(\%cgiparams);
open(FILE, $filename) or die 'Unable to open config file.';
	my @current = <FILE>;
close(FILE);

# Get amount of filter matching entries if applicable
if ($cgiparams{'FILTER'} ne '')
{
	$size = grep $cgiparams{'FILTER'}, @current;
} else {
		$size = @current;
}

# Get Current Settings
&Header::getcgihash(\%settings);

# Save Banish Settings
if ($settings{'ACTION'} eq $Lang::tr{'save'}) {
	
	&General::writehash("/var/ipfire/Banish/Banish_settings", \%settings);
	$cgiparams{'START'} = 0;
	
	# Log saving of Banish settings to syslog
	system('/usr/bin/logger', '-t', 'banish', $Lang::tr{'Banish settings saved'});
}

&General::readhash("/var/ipfire/Banish/Banish_settings", \%settings);
$checked{'ENABLED'}{'off'} = '';
$checked{'ENABLED'}{'on'} = '';
$checked{'ENABLED'}{$cgiparams{'ENABLED'}} = "checked='checked'";
map ($selected{'DISPLAY_AMOUNT'}{$_} = '', @VS);
$selected{'DISPLAY_AMOUNT'}{$settings{'DISPLAY_AMOUNT'}} = "selected='selected'";

# Set Entry Display Amount
if ($settings{'DISPLAY_AMOUNT'} ne '')
{
	$viewsize = $settings{'DISPLAY_AMOUNT'};
} else {
	$viewsize = 50;
}

# Sort Banished Resources
if ($cgiparams{'ACTION'} eq $Lang::tr{'Banish sort by ip/network'})
{

	open(INFILE, $filename) or die 'Unable to open config file.';
		my @in = <INFILE>;
	close(INFILE);
	
	# Sort FQDN entries
	my @sorted = sort { lc($a) cmp lc($b) } @in;

	
	# Sort IP entries
	my @out = sort {

    	pack('C4' => $a =~

      	/(\d+)\.(\d+)\.(\d+)\.(\d+)/)

    	cmp

    	pack('C4' => $b =~

      	/(\d+)\.(\d+)\.(\d+)\.(\d+)/)

  	} @sorted;

	open(OUTFILE, ">$filename") or die 'Unable to open ip list file.';
		flock OUTFILE, 2;
	foreach my $line (@out)
	{
			print OUTFILE "$line";
	};
	close(OUTFILE);
}

# Sort entries by remarks
if ($cgiparams{'ACTION'} eq $Lang::tr{'Banish sort by remark'})
{
	
	my $ip1 = '';
	my $enabled1 = '';
	my $remark1 = '';
	my $ip2 = '';
	my $enabled2 = '';
	my $remark2 = '';

	open(INFILE, $filename) or die 'Unable to open config file.';
		my @in = <INFILE>;
	close(INFILE);

	# Sort entries
	my @out = sort byremark @in;

	sub byremark {

		($ip1, $enabled1, $remark1) = split(/\,/, $a);
		($ip2, $enabled2, $remark2) = split(/\,/, $b);
		return (lc($remark1) cmp lc($remark2));
	}

	open(OUTFILE, ">$filename") or die 'Unable to open config file.';
		flock OUTFILE, 2;
		foreach my $line (@out)
		{
			print OUTFILE "$line";
		};
	close(OUTFILE);
}

# Sort entries by the ones that are enbabled
if ($cgiparams{'ACTION'} eq $Lang::tr{'Banish sort by enabled'})
{
	my $ip1 = '';
	my $enabled1 = '';
	my $remark1 = '';
	my $ip2 = '';
	my $enabled2 = '';
	my $remark2 = '';

	open(INFILE, $filename) or die 'Unable to open config file.';
		my @in = <INFILE>;
	close(INFILE);

	# Sort entries
	my @out = sort byenable @in;

	sub byenable {

		($ip1, $enabled1, $remark1) = split(/\,/, $a);
		($ip2, $enabled2, $remark2) = split(/\,/, $b);
		return ($enabled2 cmp $enabled1);
	}
	
	open(OUTFILE, ">$filename") or die 'Unable to open config file.';
		flock OUTFILE, 2;
	foreach my $line (@out)
	{
			print OUTFILE "$line";
	};
	close(OUTFILE);
}

# Apply Filter Settings
if ($cgiparams{'ACTION'} eq $Lang::tr{'apply'}) {
	$cgiparams{'START'} = 0;
	
	# Log application of filter to syslog
	system('/usr/bin/logger', '-t', 'banish', $Lang::tr{'Banish display filter applied'}.$cgiparams{'FILTER'});

}

# Modify Banish config
if ($cgiparams{'ACTION'} eq $Lang::tr{'add'})
{
	# User Entry Error Handling
	
	# Check for blank resource entry
	if ($cgiparams{'SRC'} eq '') 
	{
		$errormessage = $Lang::tr{'source ip bad'}; 
	}
	# Don't lock yourself out!
	elsif ($cgiparams{'SRC'} eq '0.0.0.0/0')
	{
    	$errormessage = $Lang::tr{'source ip bad'};
	}
	# Check for IP Address or CDIR resource entry
	elsif(&General::validipormask($cgiparams{'SRC'})ne '1')

	{
		# Check for FQDN resouce entry
		# Use Banish version because IPFire version is in error rwb - 29/12/18
		if(&Banish::validfqdn($cgiparams{'SRC'})ne '1')
		{
			# Check for MAC Address entry
			if(&General::validmac($cgiparams{'SRC'})ne '1')
			{
				# Check for IP Range entry
				if(&Banish::validiprange($cgiparams{'SRC'})ne '1')
				{
                                    #added to check for valid IP rwb - 10/12/18
                                    if(&General::validip($cgiparams{'SRC'})ne '1')
                                    {
					$errormessage = $Lang::tr{'Banish invalid resource'};
					
				     }
				}				
				
			}
		}
	}
	# Check for ',' in remark entry
	elsif ($cgiparams{'REMARK'} =~ /,/)
	{
		$errormessage = $Lang::tr{'Banish invalid comment'};
	}
	
	if ( ! $errormessage)
	{
	   	# Load User Input Values
	   	$cgiparams{'REMARK'} = &Header::cleanhtml($cgiparams{'REMARK'});
		$cgiparams{'CURR_SRC'} = $cgiparams{'SRC'};
		
		# Add New rule
		if($cgiparams{'EDITING'} eq 'no') {
			system("/bin/cp $outfilename $removefilename");
			open(FILE,">>$filename") or die 'Unable to open config file.';
				flock FILE, 2;
			print FILE "$cgiparams{'SRC'},$cgiparams{'ENABLED'},$cgiparams{'REMARK'}\n";
			
			open(IP_FILE, ">>$outfilename") or die 'Unable to open banish file.';
				flock IP_FILE, 2;
			if ($cgiparams{'ENABLED'} eq 'on')
			{
				print IP_FILE "$cgiparams{'SRC'}\n";
			}
		# Edit Rule	
		} else {
			system("/bin/cp $outfilename $removefilename");
			open(FILE, ">$filename") or die 'Unable to open config file.';
				flock FILE, 2;
			open(IP_FILE, ">$outfilename") or die 'Unable to open banish file.';
				flock IP_FILE, 2;
			
			# Write resource to the Banish List
			my $id = 0;
			foreach my $line (@current)
			{
				$id++;
				if ($cgiparams{'EDITING'} eq $id) {
					print FILE "$cgiparams{'SRC'},$cgiparams{'ENABLED'},$cgiparams{'REMARK'}\n";
					chomp($line);
					my @temp = split(/\,/,$line);
					if ($cgiparams{'ENABLED'} eq 'on')
					{
						print IP_FILE "$temp[0]\n";
					}
				} else { 
					print FILE "$line"; 
					chomp($line);
					my @temp = split(/\,/,$line);
					if ($temp[1] eq 'on')
					{
						print IP_FILE "$temp[0]\n";
					}
				}
			}
		}
		close(FILE);
		close(IP_FILE);
		
		# Apply Banish Rules
		system('/usr/local/bin/Banish_Sort.pl');
		
		# Log rule addition/modification activity to syslog
		if($cgiparams{'EDITING'} eq 'no') 
		{
			system('/usr/bin/logger', '-t', 'banish', $Lang::tr{'Banish rule added'}.$cgiparams{'CURR_SRC'});
		}
		else {	
			system('/usr/bin/logger', '-t', 'banish', $Lang::tr{'Banish rule modified'}.$cgiparams{'CURR_SRC'});	
		}
		
		# Save and re-apply start & filter variables
		my $sid = $cgiparams{'START'};
		$filter_changed = $cgiparams{'FILTER'};
		undef %cgiparams;
		$changed = 'yes';
		$cgiparams{'START'} = $sid;
		$cgiparams{'FILTER'} = $filter_changed;
	} else {
		# stay on edit mode if an error occur
		if ($cgiparams{'EDITING'} ne 'no')
		{
			$cgiparams{'ACTION'} = $Lang::tr{'edit'};
			$cgiparams{'ID'} = $cgiparams{'EDITING'};
		}
	}
}

# Remove rule from Banish Configuration & List
if ($cgiparams{'ACTION'} eq $Lang::tr{'remove'})
{
	system("/bin/cp $outfilename $removefilename");
	my $id = 0;
	open(FILE, ">$filename") or die 'Unable to open config file.';
		flock FILE, 2;
	open(IP_FILE, ">$outfilename") or die 'Unable to open banish file.';
		flock IP_FILE, 2;
	
	foreach my $line (@current)
	{
		$id++;
		unless ($cgiparams{'ID'} eq $id) 
		{ 
			print FILE "$line"; 
			chomp($line);
			my @temp = split(/\,/,$line);
			if ($temp[1] eq 'on')
			{
				print IP_FILE "$temp[0]\n";
			}
		}
		if ($cgiparams{'ID'} eq $id)
		{
			my @temp = split(/\,/,$line);
			$cgiparams{'CURR_SRC'} = $temp[0];
		}
	}
	close(FILE);
	close(IP_FILE);
	
	# Apply Banish rules
	system('/usr/local/bin/Banish_Sort.pl');
	# Log rule removal to syslog
	system('/usr/bin/logger', '-t', 'banish', $Lang::tr{'Banish rule removed'}.$cgiparams{'CURR_SRC'});
}

# Toggle rule on/off
if ($cgiparams{'ACTION'} eq $Lang::tr{'toggle enable disable'})
{
	system("/bin/cp $outfilename $removefilename");
	open(FILE, ">$filename") or die 'Unable to open config file.';
	flock FILE, 2;
	open(IP_FILE, ">$outfilename") or die 'Unable to open banish file.';
	flock IP_FILE, 2;
	my $id = 0;
	foreach my $line (@current)
	{
		$id++;
		unless ($cgiparams{'ID'} eq $id) { 
		print FILE "$line"; 
		chomp($line);
		my @temp = split(/\,/,$line);
		if ($temp[1] eq 'on')
			{
				print IP_FILE "$temp[0]\n";
				
			}
		}
		else
		{
			chomp($line);
			my @temp = split(/\,/,$line);
			print FILE "$temp[0],$cgiparams{'ENABLE'},$temp[2]\n";
			$cgiparams{'CURR_SRC'} = $temp[0];
			if ($cgiparams{'ENABLE'} eq 'on')
			{
				print IP_FILE "$temp[0]\n";
				
			}
		}
	}
	close(FILE);
	close(IP_FILE);
	
	# Apply Banish rules
	system('/usr/local/bin/Banish_Sort.pl');
	# Log rule toggle event to syslog
	system('/usr/bin/logger', '-t', 'banish', $Lang::tr{'Banish rule toggled'}."'".$cgiparams{'ENABLE'}."' for ".$cgiparams{'CURR_SRC'});
	
}

# Load rule for edit
if ($cgiparams{'ACTION'} eq $Lang::tr{'edit'})
{
	my $id = 0;
	foreach my $line (@current)
	{
		$id++;
		if ($cgiparams{'ID'} eq $id)
		{
			chomp($line);
			my @temp = split(/\,/,$line);
			$cgiparams{'SRC'} = $temp[0];
			$cgiparams{'ENABLED'} = $temp[1];
			$cgiparams{'REMARK'} = $temp[2];
		}
	}
}

if ($cgiparams{'ACTION'} eq '')
{
	$cgiparams{'ENABLED'} = 'on';
}
&General::readhash("/var/ipfire/Banish/Banish_settings", \%settings);
$checked{'ENABLED'}{'off'} = '';
$checked{'ENABLED'}{'on'} = '';
$checked{'ENABLED'}{$cgiparams{'ENABLED'}} = "checked='checked'";

# Display User Interface
&Header::openpage($Lang::tr{'Banish configuration'}, 1, '');

&Header::openbigbox('100%', 'left', '', $errormessage);

if ($errormessage) {
	&Header::openbox('100%', 'left', $Lang::tr{'error messages'});
	print "<class name='base'>$errormessage\n";
	print "&nbsp;</class>\n";
	&Header::closebox();
}
# Credits Comments
print "\n\n\t<!-- Banish Firewall Addon for IPCop -->\n";
print 	  "\t<!--    Developed by Sid McLaurin    -->\n";
print	  "\t<!--        SID Solutions            -->\n";
print	  "\t<!--     http://sidsolutions.net     -->\n\n";


# Banish Logo site Link & version number
print "\t<!-- Banish Logo site Link				-->\n";
print "\t<center><a href='$Lang::tr{'Banish Url'}' title='$Lang::tr{'Banish Url Alt'}' target='_blank' alt='$Lang::tr{'Banish Url Alt'}'><img src='/images/Banish/$Lang::tr{'Banish Logo'}' alt='$Lang::tr{'Banish title'}' border='0'></a></center><br>\n";
print "\t<center><font color='#ce0632'><b>$version</b></font></center><br>\n";

print "<br>\n";

# Banish Settings Interface
&Header::openbox('100%', 'left', $Lang::tr{'Banish Viewing Options'});
print "<form name='settings' method='post' action='$ENV{'SCRIPT_NAME'}'>";
print <<END
	
	<!-- Banish Settings Interface -->
	<table width='100%'>
		<tr>
			<td class='base'>$Lang::tr{'Banish Display Setting'}:&nbsp;
			<select name='DISPLAY_AMOUNT'>
END
;
foreach my $vs (@VS) {
    print "\t<option value='$vs' $selected{'DISPLAY_AMOUNT'}{$vs}>$vs</option>\n";
}
print <<END
			</select></td>
			<td width='30%' align='center' class='base'><input type='submit' name='ACTION' value='$Lang::tr{'save'}' /></td>
		</tr>
	</table>
	</form>
END
;
&Header::closebox();




# Banish User Input Interface 
print "\t<form method='post' action='$ENV{'SCRIPT_NAME'}'>\n\n";

my $buttontext = $Lang::tr{'add'};
if ($cgiparams{'ACTION'} eq $Lang::tr{'edit'}) {
	&Header::openbox('100%', 'left', $Lang::tr{'edit a rule'});
	$buttontext = $Lang::tr{'update'};
} else {
	&Header::openbox('100%', 'left', $Lang::tr{'add a new rule'});
}

print <<END
	
	<!-- Banish User Input Interface -->
	<table width='100%'>
		<tr>
			<td class='base'><font color='${Header::colourred}'>$Lang::tr{'Banish banishIP'}</font></td>
			<td><input type='text' name='SRC' value='$cgiparams{'SRC'}' size='32' /></td>
			<td width='10%' class='base'>$Lang::tr{'enabled'}<input type='checkbox' name='ENABLED' $checked{'ENABLED'}{'on'} /></td>
			<td width ='10%' class='base'>
				<font class='boldbase'>$Lang::tr{'remark'}:</font>&nbsp;<img src='/blob.gif' alt='*' /></td>
			<td><input type='text' name='REMARK' value='$cgiparams{'REMARK'}' size='32' /></td>
			<td><input type='hidden' name='ACTION' value='$Lang::tr{'add'}' />
				<input type='submit' name='SUBMIT' value='$buttontext' /></td>
		</tr>
	</table>
	<input type='hidden' name='START' value='$cgiparams{'START'}' />
	<input type='hidden' name='FILTER' value='$cgiparams{'FILTER'}' />
END
;

if ($cgiparams{'ACTION'} eq $Lang::tr{'edit'}) {
	print "<input type='hidden' name='EDITING' value='$cgiparams{'ID'}' />\n";
} else {
	print "<input type='hidden' name='EDITING' value='no' />\n";
}

&Header::closebox();
print "</form>\n";


# Search Filter Input
if ($cgiparams{'FILTER'} eq '.*')
{
	$cgiparams{'FILTER'} ='';
}
print <<END	
	<br>
	<br>
	<!-- Banish Display Filter -->
	<center>
	<form name='settings' method='post' action='$ENV{'SCRIPT_NAME'}'>
	<table>
		<tr>
			<td><b>$Lang::tr{'Banish Filter by'}:<b>&nbsp<img src='/blob.gif' alt='*' align='top'/>&nbsp<input type="text" name="FILTER" title='$Lang::tr{'Banish Filter Title'}' onKeyPress="checkEnter(event)" size='32' value='$cgiparams{'FILTER'}'>
			<input type='submit' name='ACTION' value='$Lang::tr{'apply'}'>
			</td>
		</tr>
	<input type='hidden' name='START' value='$cgiparams{'START'}' />
	<input type='hidden' name='SIZE' value='$cgiparams{'SIZE'}' />
	</table>
	</form>
	</center>

END
;


# Banish Current Entries
&Header::openbox('100%', 'left', $Lang::tr{'current rules'});

# Display Banish entries per page
$start = $cgiparams{'START'};
if ($settings{'DISPLAY_AMOUNT'} ne '')
{
	$viewsize = $settings{'DISPLAY_AMOUNT'};
} else {
	$viewsize = 50;
}
$cgiparams{'START'} = $size - $viewsize if ($cgiparams{'START'} >= $size - $viewsize);
$cgiparams{'START'} = 0 if ($cgiparams{'START'} < 0);
	
my $prev;

if ($cgiparams{'START'} == 0) {
		$prev = -1;
	} else {
		$prev = $cgiparams{'START'} - $viewsize;
		$prev = 0 if ( $prev < 0);
}
				    
my $next;

if ($cgiparams{'START'} == $size - $viewsize) {
        $next = -1;
    } else {
        $next = $cgiparams{'START'} + $viewsize;
        $next = $size - $viewsize if ($next >= $size - $viewsize);
}

# Next and Previous Page Icons
print <<END
<!-- Banish Next & Previous Page Links -->
<table width='100%'>
<tr>
END
;

print "<td align='center' width='50%'>";
if ($prev != -1) {
	print "<form method='post' name='the_form1' action='$ENV{'SCRIPT_NAME'}'><input type='hidden' name='START' value='$prev' />
<input type='hidden' name='ACTION' value='DISPLAY' /><input type='hidden' name='FILTER' value='$cgiparams{'FILTER'}' /><input type='image' name='' src='/images/Banish/back.gif' title='$Lang::tr{'Banish Previous Page'}' alt='$Lang::tr{'Banish Previous Page'}' /></form>"; }
else {
	print ""; }
print "</td>\n";

print "<td align='center' width='50%'>";
if ($next >= 0) {
	print "<form method='post' name='the_form2' action='$ENV{'SCRIPT_NAME'}'><input type='hidden' name='START' value='$next' />
<input type='hidden' name='ACTION' value='DISPLAY' /><input type='hidden' name='FILTER' value='$cgiparams{'FILTER'}' /><input type='image' name='' src='/images/Banish/forward.gif' title='$Lang::tr{'Banish Next Page'}' alt='$Lang::tr{'Banish Next Page'}' /></form>"; }
else {
	print ""; }
print "</td>\n";

print <<END
</tr>
</table>
END
;

# Banish Sort Forms
print <<END
	
	<!-- Banish Sort Forms -->
	<table width='100%'>
		<tr>
			<td width='20%' class='boldbase' align='left'>
				<form method='post' action='$ENV{'SCRIPT_NAME'}'>
					<b>$Lang::tr{'Banish banishIP'}</b>
					<input type='image' name='SORT' src='/images/Banish/sort.gif' title='$Lang::tr{'Banish sort by ip/network'}' alt='$Lang::tr{'Banish sort by ip/network'}'>
					<input type='hidden' name='ACTION' value='$Lang::tr{'Banish sort by ip/network'}' />
					<input type='hidden' name='START' value='$cgiparams{'START'}' />
					<input type='hidden' name='FILTER' value='$cgiparams{'FILTER'}' />
				</form>
			</td>
			<td width='5%' align='center' class='boldbase'><b>$Lang::tr{'Banish flag'}</b></td>
			<td width='30%' class='boldbase' align='left'>
				<form method='post' action='$ENV{'SCRIPT_NAME'}'>
					<b>$Lang::tr{'remark'}</b>
					<input type='image' name='SORT' src='/images/Banish/sort.gif' title='$Lang::tr{'Banish sort by remark'}' alt='$Lang::tr{'Banish sort by remark'}'>
					<input type='hidden' name='ACTION' value='$Lang::tr{'Banish sort by remark'}' />
					<input type='hidden' name='START' value='$cgiparams{'START'}' />
					<input type='hidden' name='FILTER' value='$cgiparams{'FILTER'}' />
				</form>
			</td>
			<td width='5%' class='boldbase' colspan='3' align='center'>
				<form method='post' action='$ENV{'SCRIPT_NAME'}'>
					<b>$Lang::tr{'action'}</b>
					<input type='image' name='SORT' src='/images/Banish/sort.gif' title='$Lang::tr{'Banish sort by enabled'}' alt='$Lang::tr{'Banish sort by enabled'}'>
					<input type='hidden' name='ACTION' value='$Lang::tr{'Banish sort by enabled'}' />
					<input type='hidden' name='START' value='$cgiparams{'START'}' />
					<input type='hidden' name='FILTER' value='$cgiparams{'FILTER'}' />
				</form>
			</td>
		</tr>
		
	<!-- Banish Rules -->
END
;

# If something has happened re-read config and reset amount of entries
if($cgiparams{'ACTION'} ne '' or $changed ne 'no')
{
	open(FILE, $filename) or die 'Unable to open config file.';
		@current = <FILE>;
	close(FILE);
	if ($cgiparams{'FILTER'} ne '')
	{
		$size = grep $cgiparams{'FILTER'}, @current;
	} else {
		$size = @current;
	}
}

# Display Banish Rules
my $id = 0;
my $lines = 0;

foreach my $line (@current)
{
	$id++;
	chomp($line);
	
	# Apply filter if present
	if ($cgiparams{'FILTER'} eq '')
	{	
		$cgiparams{'FILTER'} = '.*';
	}
	if($line =~ (/$cgiparams{'FILTER'}/i))
	{
		$count++;
		my @temp = split(/\,/,$line);
		my $gif = '';
		my $gdesc = '';
		my $toggle = '';
		
		# Display amount entries per setting
		$lines++;
		if ($lines <= ($start + $viewsize)&& $lines > $start)
		{
			if($cgiparams{'ACTION'} eq $Lang::tr{'edit'} && $cgiparams{'ID'} eq $id) {
				print "\t\t<tr bgcolor='${Header::colouryellow}'>\n"; }
			elsif ($count % 2) {
				print "\t\t<tr bgcolor='${Header::table1colour}'>\n"; }
			else {
				print "\t\t<tr bgcolor='${Header::table2colour}'>\n"; }
			if ($temp[1] eq 'on') { $gif='on.gif'; $toggle='off'; $gdesc=$Lang::tr{'click to disable'};}
			else { $gif='off.gif'; $toggle='on'; $gdesc=$Lang::tr{'click to enable'}; }
			$temp[2] = '' unless defined $temp[2];
	
			## GeopIP  Mod
    		my $addr = "$temp[0]";
    		my $gi = Geo::IP::PurePerl->new();

    		# CDIR to IP for Whois lookup
    		if ($addr =~ /\/\d+/)
    		{
    			$addr =~ s/\/\d+//;
        		$addr =~ "s/\d$/2 + $1/";
    		}
    		
    		# IP Range to IP for Whois lookup
    		if ($addr =~ /\-(\d+)\.(\d+)\.(\d+)\.(\d+)/)
    		{
    			$addr =~ s/\-(\d+)\.(\d+)\.(\d+)\.(\d+)//;
        		$addr =~ "s/\d$/2 + $1/";
    		}
    		
    		# Resolve domain to IP for Whois lookup
    		elsif(&General::validipormask($addr)ne '1')
    		{
    			my @hostlookup = qx(/usr/bin/host $addr);
        		my $displayAddress = '';
        		foreach my $line (@hostlookup)
        		{
        			chomp($line);
            		if ($line =~ /has address/)
            		{
            			(my $before, $displayAddress) = split(/has address/, $line);
            		}
        		}
        		$displayAddress =~ s/\s//;
        		$addr = $displayAddress;
     		}

			# Get flag code
    		my $ccode = $gi->country_code_by_name($addr);
# Change to uppercase for ipfire (lc to uc) rwb 10/12/18
    		my $fcode = uc($ccode);
	
			if ( ! -z "$filename") {
	print <<END
			<td align='left'><a href='/cgi-bin/ipinfo.cgi?ip=$addr'>$temp[0]</a></td>
			<td align='center'><a href='/cgi-bin/country.cgi#$fcode'><img src='/images/flags/$fcode.png' border='0' align='absmiddle' alt='$ccode'></a></td> 
			<td align='left'>&nbsp;$temp[2]</td>
			<td align='center'>
				<form method='post' name='frma$id' action='$ENV{'SCRIPT_NAME'}'>
					<input type='image' name='$Lang::tr{'toggle enable disable'}' src='/images/$gif' title='$gdesc' alt='$gdesc' />
					<input type='hidden' name='ID' value='$id' />
					<input type='hidden' name='ENABLE' value='$toggle' />
					<input type='hidden' name='ACTION' value='$Lang::tr{'toggle enable disable'}' />
					<input type='hidden' name='START' value='$cgiparams{'START'}' />
                    <input type='hidden' name='FILTER' value='$cgiparams{'FILTER'}' />
				</form>
			</td>
			<td align='center'>
				<form method='post' name='frmb$id' action='$ENV{'SCRIPT_NAME'}'>
					<input type='image' name='$Lang::tr{'edit'}' src='/images/edit.gif' title='$Lang::tr{'edit'}' alt='$Lang::tr{'edit'}' />
					<input type='hidden' name='ID' value='$id' />
					<input type='hidden' name='ACTION' value='$Lang::tr{'edit'}' />
					<input type='hidden' name='START' value='$cgiparams{'START'}' />
                    <input type='hidden' name='FILTER' value='$cgiparams{'FILTER'}' />
				</form>
			</td>
			<td align='center'>
				<form method='post' name='frmc$id' action='$ENV{'SCRIPT_NAME'}'>
					<input type='image' name='$Lang::tr{'remove'}' src='/images/delete.gif' title='$Lang::tr{'remove'}' alt='$Lang::tr{'remove'}' />
					<input type='hidden' name='ID' value='$id' />
					<input type='hidden' name='ACTION' value='$Lang::tr{'remove'}' />
					<input type='hidden' name='START' value='$cgiparams{'START'}' />
                    <input type='hidden' name='FILTER' value='$cgiparams{'FILTER'}' />
				</form>
			</td>
		</tr>
END
} 
;
	}
	;
	}
}
print "\t</table>\n";

# Next and Previous Page Icons
print <<END
<!-- Banish Next & Previous Page Links -->
<table width='100%'>
<tr>
END
;

print "<td align='center' width='50%'>";
if ($prev != -1) {
	print "<form method='post' name='the_form1' action='$ENV{'SCRIPT_NAME'}'><input type='hidden' name='START' value='$prev' />
<input type='hidden' name='ACTION' value='DISPLAY' /><input type='hidden' name='FILTER' value='$cgiparams{'FILTER'}' /><input type='image' name='' src='/images/Banish/back.gif' title='$Lang::tr{'Banish Previous Page'}' alt='$Lang::tr{'Banish Previous Page'}' /></form>"; }
else {
	print ""; }
print "</td>\n";

print "<td align='center' width='50%'>";
if ($next >= 0) {
	print "<form method='post' name='the_form2' action='$ENV{'SCRIPT_NAME'}'><input type='hidden' name='START' value='$next' />
<input type='hidden' name='ACTION' value='DISPLAY' /><input type='hidden' name='FILTER' value='$cgiparams{'FILTER'}' /><input type='image' name='' src='/images/Banish/forward.gif' title='$Lang::tr{'Banish Next Page'}' alt='$Lang::tr{'Banish Next Page'}' /></form>"; }
else {
	print ""; }
print "</td>\n";

print <<END
</tr>
</table>
END
;

# If the banish file contains entries, print Key to action icons
if ( ! -z "$filename") {
print <<END

	<!-- Icon Legend -->
	<fieldset>
	<legend>&nbsp;<b>$Lang::tr{'legend'}:</b>&nbsp;</legend>
	<table>
		<tr>
			<td>&nbsp; <img src='/blob.gif' alt='*' /></td>
			<td class='base'>$Lang::tr{'this field may be blank'}</td>
			<td>&nbsp; &nbsp; <img src='/images/Banish/back.gif' alt='$Lang::tr{'Banish Previous Page'}' /></td>
			<td class='base'>$Lang::tr{'Banish Previous Page'}</td>
			<td>&nbsp; &nbsp; <img src='/images/Banish/forward.gif' alt='$Lang::tr{'Banish Next Page'}' /></td>
			<td class='base'>$Lang::tr{'Banish Next Page'}</td>
			<td>&nbsp; <img src='/images/Banish/sort.gif' alt='$Lang::tr{'Banish click to sort'}' /></td>
			<td class='base'>$Lang::tr{'Banish click to sort'}</td>
			<td>&nbsp; &nbsp; <img src='/images/on.gif' alt='$Lang::tr{'click to disable'}' /></td>
			<td class='base'>$Lang::tr{'click to disable'}</td>
			<td>&nbsp; &nbsp; <img src='/images/off.gif' alt='$Lang::tr{'click to enable'}' /></td>
			<td class='base'>$Lang::tr{'click to enable'}</td>
			<td>&nbsp; &nbsp; <img src='/images/edit.gif' alt='$Lang::tr{'edit'}' /></td>
			<td class='base'>$Lang::tr{'edit'}</td>
			<td>&nbsp; &nbsp; <img src='/images/delete.gif' alt='$Lang::tr{'remove'}' /></td>
			<td class='base'>$Lang::tr{'remove'}</td>
		</tr>
	</table>
	</fieldset>
END
;
}

&Header::closebox();

&Header::closebigbox();

&Header::closepage();
