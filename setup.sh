#/bin/bash

#ToDo
# - Install/verify MS cert 
# - make it install red hat cert
#
#
#
#


#V1.2
currTime=$(date +%s)
warnCount="0"


#Color set up
Color_Off='\033[0m'		# Text Reset
errText='\033[0;31m'	# Red
okText='\033[0;32m'		# Green
warnText='\033[0;33m'	# Yellow
err='\033[1;31m'		# BOLD Red
ok='\033[1;32m'			# BOLD Green
warn='\033[1;33m'		# BOLD Yellow
info='\033[1m'			# BOLD

#download and update required packages
echo -e "${info}INFO:${Color_Off} Installing and updating required packages"
sudo yum update
sudo yum install coreutils osslsigncode ncurses-compat-libs python3 ca-certificates
#coreutils contains sha256sum and sha512sum
warnCount=$(expr $warnCount + $?)


#install OVF tool
echo -e "${info}INFO:${Color_Off} Installing VMWare OVFtool 4.3.0-15755677"
vmware=$(head ovftool/VMware-ovftool-4.3.0-15755677-lin.x86_64.bundle)
if [ -z "$vmware" ]
then
	echo -e "${warn}WARNING:${warnText} Could not find VMWare OVFtool please install manually${Color_Off}"
	#adding to warn count
	((warnCount=warnCount+1))
else
	echo -e "${info}INFO:${Color_Off} Running OVFtool install script"
	sudo bash ./ovftool/VMware-ovftool-4.3.0-15755677-lin.x86_64.bundle
fi

# Verifying certificate
# Red Hat
redhatKey=$(cat /etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release | grep -iE "567E *347A *D004 *4ADE *55BA *8A5F *199E *2F91 *FD43 *1D51" | wc -l)
if [[ $redhatKey = 0 ]];
then
	echo -e "${info}INFO:${Color_Off} Installing Red Hat Key"
	sudo cp ./setupDependencies/certificates/RPM-GPG-KEY-redhat-release /etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release
else
	echo -e "${info}INFO:${Color_Off} Found Red Hat key"
fi



# Status of the set up
if [[ $warnCount -eq "0" ]];
then
	echo -e "${ok}OK:${okText} Set up ran successfully!${Color_Off}"
else
	echo -e "${err}ERROR:${errText} Set up not completed successfully!${Color_Off}"
fi
echo -e "${info}INFO:${Color_Off} Execution took: $(expr $(date +%s) - $currTime) seconds"