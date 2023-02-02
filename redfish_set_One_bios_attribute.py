#
# redfish_set_One_bios_attribute.py
# Set a single BIOS attributes to a new value
# Synopsis:
# redfish_set_one_bios_attribute.py <iDRAC IP> <user> <password>
# <Attribute name> <New value>
#
import requests, json, sys, re, time
from datetime import datetime
try:
    idrac_ip = sys.argv[1]
    idrac_username = sys.argv[2]
    idrac_password = sys.argv[3]
    attribute_name = sys.argv[4]
    pending_value = sys.argv[5]
except:
    print "- FAIL: You must pass in script name along with iDRAC IP / iDRAC username / iDRAC password / attribute name / attribute value. Example: \"script_name.py 192.168.0.120 root calvin MemTest Enabled\""
    sys.exit()
### Function to get BIOS attribute current value
def get_attribute_current_value():
    global current_value
    response = requests.get('https://%s/redfish/v1/Systems/System.Embedded.1/Bios' % idrac_ip,verify=False,auth=(idrac_username, idrac_password))
    data = response.json()
    current_value = data[u'Attributes'][attribute_name]
    if current_value == pending_value:
        answer = raw_input("\n- WARNING, %s is already set to %s, do you still want to set the attribute? Type (y) or (n): " % (attribute_name, current_value))
        if answer == "n":
            sys.exit()
        else:
            pass
            
### Function to set BIOS attribute pending value
def set_bios_attribute():
    print "\n- WARNING: Current value for %s is: %s, setting to: %s\n" % (attribute_name, current_value, pending_value)
    time.sleep(2)
    url = 'https://%s/redfish/v1/Systems/System.Embedded.1/Bios/Settings' % idrac_ip
    payload = {"Attributes":{attribute_name:pending_value}}
    headers = {'content-type': 'application/json'}
    response = requests.patch(url, data=json.dumps(payload), headers=headers, verify=False,auth=(idrac_username, idrac_password))
    statusCode = response.status_code
    if statusCode == 200:
        print "\n- PASS: Command passed to set BIOS attribute %s pending value to %s\n" % (attribute_name, pending_value)
    else:
        print "\n- FAIL, Command failed, errror code is %s" % statusCode
        detail_message=str(response.__dict__)
        print detail_message
        sys.exit()
    d=str(response.__dict__)
### Function to create BIOS target config job
def create_bios_config_job():
    global job_id
    url = 'https://%s/redfish/v1/Managers/iDRAC.Embedded.1/Jobs' % idrac_ip
    #payload = {"Target":"BIOS.Setup.1-1","RebootJobType":"PowerCycle"}
    payload = {"TargetSettingsURI":"/redfish/v1/Systems/System.Embedded.1/Bios/Settings"}
    headers = {'content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False,auth=(idrac_username, idrac_password))
    statusCode = response.status_code
    #print "Status Code: {0}".format(response.status_code)
    #print "Extended Info Message: {0}".format(response.json())
    if statusCode == 200:
        print "\n- PASS: Command passed to create target config job, status code 200 returned.\n"
    else:
        print "\n- FAIL, Command failed, status code is %s\n" % statusCode
        detail_message=str(response.__dict__)
        print detail_message
        sys.exit()
    d=str(response.__dict__)
    z=re.search("JID_.+?,",d).group()
    job_id=re.sub("[,']","",z)
    print "- WARNING: %s job ID successfully created\n" % job_id
### Function to verify job is marked as scheduled before rebooting the server
def get_job_status():
    while True:
        req = requests.get('https://%s/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/%s' % (idrac_ip, job_id), auth=(idrac_username, idrac_password), verify=False)
        statusCode = req.status_code
        if statusCode == 200:
            print "\n- PASS, Command passed to check job status, code 200 returned\n"
            time.sleep(20)
        else:
            print "\n- FAIL, Command failed to check job status, return code is %s" % statusCode
            print "Extended Info Message: {0}".format(req.json())
            sys.exit()
        data = req.json()
        if data[u'Message'] == "Task successfully scheduled.":
            print " JobID = "+data[u'Id']
            print " Name = "+data[u'Name']
            print " Message = "+data[u'Message']
            print " PercentComplete = "+str(data[u'PercentComplete'])+"\n"
            break
        else:
            print "\n- WARNING: JobStatus not scheduled, current status is: %s\n" % data[u'Message']
### Function to reboot the server
def reboot_server():
    url = 'https://%s/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset' % idrac_ip
    payload = {'ResetType': 'ForceOff'}
    headers = {'content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False, auth=(idrac_username,idrac_password))
    statusCode = response.status_code
    if statusCode == 204:
        print "\n- PASS, Command passed to power OFF server, code return is %s\n" % statusCode
    else:
        print "\n- FAIL, Command failed to power OFF server, status code is: %s\n" % statusCode
        print "Extended Info Message: {0}".format(response.json())
        sys.exit()
    time.sleep(10)
    payload = {'ResetType': 'On'}
    headers = {'content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False, auth=('root','calvin'))
    statusCode = response.status_code
    if statusCode == 204:
        print "\n- PASS, Command passed to power ON server, code return is %s\n" % statusCode
    else:
        print "\n- FAIL, Command failed to power ON server, status code is: %s\n" % statusCode
        print "Extended Info Message: {0}".format(response.json())
        sys.exit()

### Function to loop checking the job status until marked completed or failed
def loop_job_status():
    start_time=datetime.now()
    while True:
        req = requests.get('https://%s/redfish/v1/Managers/iDRAC.Embedded.1/Jobs/%s' % (idrac_ip, job_id), auth=(idrac_username, idrac_password), verify=False)
        current_time=(datetime.now()-start_time)
        statusCode = req.status_code
        if statusCode == 200:
            print "\n- PASS, Command passed to check job status, code 200 returned\n"
        else:
            print "\n- FAIL, Command failed to check job status, return code is %s" % statusCode
            print "Extended Info Message: {0}".format(req.json())
            sys.exit()
        data = req.json()
        if str(current_time)[0:7] >= "0:30:00":
            print "\n- FAIL: Timeout of 30 minutes has been hit, script stopped\n"
            sys.exit()
        elif "Fail" in data[u'Message'] or "fail" in data[u'Message']:
            print "- FAIL: %s failed" % job_id
            sys.exit()
        elif data[u'Message'] == "Job completed successfully.":
            print "\n JobID = "+data[u'Id']
            print " Name = "+data[u'Name']
            print " Message = "+data[u'Message']
            print " PercentComplete = "+str(data[u'PercentComplete'])+"\n"
            break
        else:
            print "- WARNING, JobStatus not completed, current status is: \"%s\", current job polling time is: %s\n" % (data[u'Message'],str(current_time)[0:7])
            time.sleep(30)
### Function to check attribute new current value
def get_new_current_value():
    response = requests.get('https://%s/redfish/v1/Systems/System.Embedded.1/Bios' % idrac_ip,verify=False,auth=(idrac_username, idrac_password))
    data = response.json()
    current_value_new = data[u'Attributes'][attribute_name]
    if current_value_new == pending_value:
        print "\n- PASS, BIOS attribute \"%s\" new current value is: %s" % (attribute_name, pending_value)
    else:
        print "n\- FAIL, BIOS attribute \"%s\" attribute not set to: %s" % (attribute_name, current_value)
        sys.exit()
### Run code
get_attribute_current_value()
set_bios_attribute()
create_bios_config_job()
get_job_status()
reboot_server()
loop_job_status()
get_new_current_value()