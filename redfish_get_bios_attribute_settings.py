#
# redfish_get_bios_attribute_settings.py
# Get BIOS attributes and current settings
# Print to STDOUT and save to file "bios_attributes.txt"
# Synopsis:
# redfish_get_bios_attribute_settings.py <iDRAC IP addr> <user> <password>
#
import requests, json, sys, re, time, os

try:
    idrac_ip = sys.argv[1]
    idrac_username = sys.argv[2]
    idrac_password = sys.argv[3]
except:
    print "- FAIL: You must pass in script name along with iDRAC IP / iDRAC username / iDRAC password"
sys.exit()
try:
    os.remove("bios_attributes.txt")
except:
    pass
#
# Function to get BIOS attributes /current settings
#
def get_bios_attributes():
    f=open("bios_attributes.txt","a")
    global current_value
	global pending_value
    response = requests.get('https://%s/redfish/v1/Systems/System.Embedded.1/Bios' % idrac_ip,verify=False,auth=(idrac_username,idrac_password))
    data = response.json()
    a="\n--- BIOS Attributes ---\n\n%-30s%-30s\n\n" % ("Attribute", "Value")
    print a
    f.writelines(a)
    for i in data[u'Attributes'].items():
        attribute_name = "%-30s" % (i[0])
        #print attribute_name
        f.writelines(attribute_name)
        attribute_value = "%-30s\n" % (i[1])
        #print attribute_value    
        f.writelines(attribute_value)
        print "%-30s%-30s" % (i[0],i[1])
    print "\n- Attributes are also captured in \"bios_attributes.txt\" file"
    f.close()
# Run Code
get_bios_attributes()