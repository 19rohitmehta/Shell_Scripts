#!/bin/bash
lseth | awk '{print$1}' | grep -v PCIID > /etc/sysconfig/eth-pci-order
echo ""
echo "PCI Order before Ethernet sorting"
cat /etc/sysconfig/eth-pci-order
echo ""
echo "Ethernet Order after sorting, will be refelected after reboot"
sorteth