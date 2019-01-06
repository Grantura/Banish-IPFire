# Added for Banish
my $address = '';
# CDIR to IP for Whois lookup
if ($addr =~ /\/\d+/)
{
        $address = $addr;
        $addr =~ s/\/\d+//;
        $addr =~ s/\d$/2 + $1/;
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
    $address = $addr;
    $addr = $displayAddress;
} else {
        $address = $addr;
}
# End Banish 
