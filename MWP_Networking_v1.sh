#!/bin/bash
echo ""
echo -e "\033[33m CoD MWP Networking Script \033[0m "
echo ""
echo -e "\e[1;31mWARNING : This script is strictly meant for first time network setup on server and override all existing network files & configuration.\e[0m"
echo -e "if mistakenly executed than please terminate the process \033[33m (CTRL + C) \033[0m immediately."
echo ""
echo "####################################MWP IPv4 Plan###################################################"
echo "        NAME    bond0.1000_IP bond0.1000_MASK bond0.1000_GW bond1.1500_IP bond1.1500_MASK bond1.1500_GW"
cat --number MWP_IPv4_Plan
echo ""

echo "Enter MWP Server number for MWP IPv4 Networking configuration"
read n
##### MWP IPv4 Networking Configuration################
echo "Starting MWP IPv4 Networking Configuration"
touch MWP_IPv4_Plan_server
head -$n MWP_IPv4_Plan | tail -1 > MWP_IPv4_Plan_server
while read f1 f2 f3 f4 f5 f6 f7
do
       echo "Server Name is   : $f1"
       echo "" 
       echo "bond0.1000 IPv4 is    : $f2"
       echo "bond0.1000 Subnet is  : $f3"
       echo "bond0.1000 D-GW IP is : $f4"
       echo ""
       echo "bond1.1500 IPv4 is    : $f5"
       echo "bond1.1500 Subnet is  : $f6"
       echo "bond1.1500 GW is      : $f7"

done < MWP_IPv4_Plan_server
while true; do
    read -p 'Please Confirm MWP IPv4 Networking Configuration & Continue? yes/no: ' input
    case $input in
        [yY]*)
            echo 'Continuing'
            break
            ;;
        [nN]*)
            echo 'Ok, exiting'
            exit 1
            ;;
         *)
            echo 'Invalid input' >&2
    esac
done
mkdir /etc/sysconfig/network-scripts/backup
yes|cp -rvf /etc/sysconfig/network-scripts/ifcfg-* /etc/sysconfig/network-scripts/backup/
rm -rf /etc/sysconfig/network-scripts/ifcfg-eth*
rm -rf /etc/sysconfig/network-scripts/ifcfg-bond*
yes|cp -rvf MWP_Networking_Files/* /etc/sysconfig/network-scripts/ 
while read f1 f2 f3 f4 f5 f6 f7
do
       a="$f2"
       b="$f3"
       c="$f4"
       d="$f5"
       e="$f6"
       f="$f7"
done < MWP_IPv4_Plan_server

echo "IPADDR=$a" >> /etc/sysconfig/network-scripts/ifcfg-bond0.1000
echo "NETMASK=$b" >> /etc/sysconfig/network-scripts/ifcfg-bond0.1000
echo "GATEWAY=$c" >> /etc/sysconfig/network-scripts/ifcfg-bond0.1000

echo "IPADDR=$d" >> /etc/sysconfig/network-scripts/ifcfg-bond1.1500
echo "NETMASK=$e" >> /etc/sysconfig/network-scripts/ifcfg-bond1.1500


echo "######Completed MWP IPv4 Networking Configuration######"


systemctl stop NetworkManager
systemctl disable NetworkManager
echo "Restarting Network Service"
systemctl restart network
sleep 45s
echo "Network Service restart completed"
systemctl status network
echo "Pingining bond0.1000 GW"
ping -c3 $c
echo "Pingining bond1.1500 GW"
ping -c3 $f