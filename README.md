# Banish-IPFire
This addon alows the administrator to generate a personal blocklst through menus on the IPFire GUI and to generate iptables rules to block by IP Address,CIDR, MAC Address or fully qualified domain name 
This is a port of Banish IPCop addon to IPFire. The Banish addon was written by Sid McLaurin but seems to have abandoned arround 2008 and I can no longer find any trace of the original author.

I am currently running the ported version of Banish on IPFire 2.21 (i586) - Core Update 125 on a PC Engines ‐ apu2.

# Banish Help
From SID Solutions Wikipedia
Contents

    1 Introduction
        1.1 Features
    2 Installing/Upgrading
    3 Usage
        3.1 Getting Started
        3.2 Add a new Banish Rule
        3.3 Enable/Disable Banish Rule
        3.4 Edit Banish Rule
        3.5 Remove Banish Rule
        3.6 Sort Banish Rules
            3.6.1 Sort by Banished Resource
            3.6.2 Sort by Remark
            3.6.3 Sort by Enabled Rules
        3.7 Links
        3.8 Whois Lookup
    4 Uninstall

Introduction

Banish is a IPCop firewall Addon Module that allows you to simply and completely block IP addresses, ranges of IPs, MAC Address or Fully Qualified Domain Names at the IPTables firewall level.
Features

    "Who is" lookups for Banish entries.

    Create meaningful Remarks about added Banish Rules.

    Toggle Enabled/Disabled or Remove rules.

    Sort by Banished Resources, Remarks or if rule is Enabled.

    Compatible with other IPCop firewall MODs.

    Added support for GeoIP IPCop Mod (GeoIP must be installed first).

    MAC Address block capability

Installing/Upgrading

Download the latest version here and copy to your /tmp. See How to remotely transfer files to and from your IPCop system for more information.

If you are having trouble downloading, click here.


Logon as root on your IPCop system. See How to logon remotely to your IPCop system


Extract installation files:

 tar xzvf current-banish.tar.gz

Or

 tar xzvf banish*tar.gz

Change to installation directory

 cd banish*

Execute installation script

 ./install_Banish.sh

Or

 sh install_Banish.sh

Usage
Getting Started

Select Banish from the Firewall menu of IPCop's Web Interface.


Image:Banish menu.png


This will bring up the Banish Administration Console.


Image:Banish console.png
Add a new Banish Rule

    Type in a valid IP Address,CIDR, MAC Address or fully qualified domain name in the Banished Resource field.
    Check the Enabled field.
    Optional:
    Type in a remark/comment about the Banished Resource in the Remark field.
    Click the Add button.


Image:Banish addition.png
Enable/Disable Banish Rule

You can toggle a Banish Rule between Enable and Disabled states by clicking on the Enable/Disable checkbox under the Action column.

Enabled

Image:Banish enabled.png


Disabled

Image:Banish disabled.png


Edit Banish Rule

Click on the Edit icon Image:Edit.gif under the Action column of the rule you wish to edit.

Banish Edit Mode


Image:Banish edit.png


Remove Banish Rule

Click on the Remove icon Image:Delete.gif under the Action column of the rule you wish to remove.


