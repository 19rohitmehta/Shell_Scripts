import paramiko
import pdb

def bio_congig(serverIP,option):
    file = open('Logs_{}'.format(serverIP),'a+')
    #pdb.set_trace()
    try:
        connection = paramiko.SSHClient()
        connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # key=paramiko.RSAKey.from_private_key_file("/home/ubuntu/.ssh/known_hosts")
        connection.connect(hostname=serverIP, username="root", password="mavenirserver")

        def Idrac_config_checkbios():
            print(serverIP)
            print('Idrac_config_6152_checkbios')
            file.write('############' + serverIP + '###################' + '\n')
            file.write('############ Idrac_config_checkbios ###################' + '\n')
            fwupdate = "racadm getversion -f bios"
            fwupdate1 = "racadm jobqueue view"
            VD_commands = [fwupdate,fwupdate1]
            for commands in VD_commands:
                print(commands)
                stdin, stdout, stderr = connection.exec_command(commands)
                file.write('{}\n'.format(stdout.read()))
            file.write('############ Idrac_config_checkbios ###################' + '\n')

        def IPMIEnable():
            file.write('############' + serverIP + '###################' + '\n')
            file.write('############ IPMIEnable ###################' + '\n')
            print(serverIP)
            print('IPMIEnable')
            check_command = "racadm get iDRAC.IPMILan"
            Enable_cmd = "racadm set iDRAC.IPMILan.Enable 1"
            stdin, stdout, stderr = connection.exec_command(check_command)
            file.write('IPMI status before enabling {}\n'.format(stdout.read()))
            stdin, stdout, stderr = connection.exec_command(Enable_cmd)
            file.write('\n IPMI Enabled \n output after enabling :{}\n'.format(stdout.read()))

            stdin, stdout, stderr = connection.exec_command(check_command)
            print(stdout.read())
            file.write('\n IPMI Enabled \n output after enabling \n'.format(stdout.read()))
            file.write('############ IPMIEnable ###################' + '\n')


        def Raid_config_check():

            file.write('############' + serverIP + '###################' + '\n')
            file.write('############ Raid_config_check ###################' + '\n')
            print(serverIP)
            print('Raid_config_check')
            Verify = "racadm storage get vdisks"
            Verify_raid = "racadm storage get vdisks -o -p layout"
            stdin, stdout, stderr = connection.exec_command(Verify)
            print(stdout.read())
            file.write('###########' + stdout.read() + '################################################' + '\n')

            stdin, stdout, stderr = connection.exec_command(Verify_raid)
            print(stdout.read())
            file.write('###########' + stdout.read() + '################################################' + '\n')
            file.write('############ Raid_config_check ###################' + '\n')


        def Raid_config_compute_control(): # raid cingfig storage

            file.write('############' + serverIP + '###################' + '\n')
            file.write('############ Raid_config_compute ###################' + '\n')
            print(serverIP)
            print('Raid_config_compute')
            VD_create1 = "racadm storage createvd:RAID.Slot.5-1 -rl r10 -rp ra -pdkey:Disk.Bay.0:Enclosure.Internal.0-1:RAID.Slot.5-1,Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.5-1,Disk.Bay.2:Enclosure.Internal.0-1:RAID.Slot.5-1,Disk.Bay.3:Enclosure.Internal.0-1:RAID.Slot.5-1"
            # VD_create2 = "racadm storage createvd:RAID.Slot.5-1 -rl r1 -rp ra -pdkey:Disk.Bay.2:Enclosure.Internal.0-1:RAID.Slot.5-1,Disk.Bay.3:Enclosure.Internal.0-1:RAID.Slot.5-1"
            Job_create = "racadm jobqueue create RAID.Slot.5-1"
            #Poweraction = "racadm serveraction powercycle"
            Verify = "racadm storage get vdisks"
            stdin, stdout, stderr = connection.exec_command(Verify)
            file.write('###########' + stdout.read() + '################################################' + '\n')
            Verify_raid = "racadm storage get vdisks -o -p layout"
            stdin, stdout, stderr = connection.exec_command(Verify_raid)
            print(stdout.read())
            file.write('###########' + stdout.read() + '################################################' + '\n')
            VD_commands = [VD_create1, Job_create]

            for commands in VD_commands:
                print(commands)
                stdin, stdout, stderr = connection.exec_command(commands)
                file.write('###########' + stdout.read() + '################################################' + '\n')
                stdin, stdout, stderr = connection.exec_command(Verify_raid)
                file.write('###########' + stdout.read() + '################################################' + '\n')
                file.write('############ Raid_config_compute ###################' + '\n')

        def Raid_config_storage(): # raid cingfig storage

            file.write('############' + serverIP + '###################' + '\n')
            file.write('############ Raid_config_compute ###################' + '\n')
            print(serverIP)
            print('Raid_config_compute')
            VD_create1 = "racadm storage createvd:RAID.Slot.5-1 -rl r1 -rp ra -pdkey:Disk.Bay.0:Enclosure.Internal.0-1:RAID.Slot.5-1,Disk.Bay.1:Enclosure.Internal.0-1:RAID.Slot.5-1"
            VD_create2 = "racadm storage createvd:RAID.Slot.5-1 -rl r0 -rp ra -pdkey:Disk.Bay.2:Enclosure.Internal.0-1:RAID.Slot.5-1"
            VD_create3 = "racadm storage createvd:RAID.Slot.5-1 -rl r0 -rp ra -pdkey:Disk.Bay.3:Enclosure.Internal.0-1:RAID.Slot.5-1"
            VD_create4 = "racadm storage createvd:RAID.Slot.5-1 -rl r0 -rp ra -pdkey:Disk.Bay.4:Enclosure.Internal.0-1:RAID.Slot.5-1"
            VD_create5 = "racadm storage createvd:RAID.Slot.5-1 -rl r0 -rp ra -pdkey:Disk.Bay.5:Enclosure.Internal.0-1:RAID.Slot.5-1"
            VD_create6 = "racadm storage createvd:RAID.Slot.5-1 -rl r0 -rp ra -pdkey:Disk.Bay.6:Enclosure.Internal.0-1:RAID.Slot.5-1"
            VD_create7 = "racadm storage createvd:RAID.Slot.5-1 -rl r0 -rp ra -pdkey:Disk.Bay.7:Enclosure.Internal.0-1:RAID.Slot.5-1"
            VD_create8 = "racadm storage createvd:RAID.Slot.5-1 -rl r0 -rp ra -pdkey:Disk.Bay.8:Enclosure.Internal.0-1:RAID.Slot.5-1"
            VD_create9 = "racadm storage createvd:RAID.Slot.5-1 -rl r0 -rp ra -pdkey:Disk.Bay.9:Enclosure.Internal.0-1:RAID.Slot.5-1"
            VD_create10 = "racadm storage createvd:RAID.Slot.5-1 -rl r0 -rp ra -pdkey:Disk.Bay.10:Enclosure.Internal.0-1:RAID.Slot.5-1"
            VD_create11 = "racadm storage createvd:RAID.Slot.5-1 -rl r0 -rp ra -pdkey:Disk.Bay.11:Enclosure.Internal.0-1:RAID.Slot.5-1"
            VD_create12 = "racadm storage createvd:RAID.Slot.5-1 -rl r0 -rp ra -pdkey:Disk.Bay.12:Enclosure.Internal.0-1:RAID.Slot.5-1"
            VD_create13 = "racadm storage createvd:RAID.Slot.5-1 -rl r0 -rp ra -pdkey:Disk.Bay.13:Enclosure.Internal.0-1:RAID.Slot.5-1"
            VD_create14 = "racadm storage createvd:RAID.Slot.5-1 -rl r0 -rp ra -pdkey:Disk.Bay.14:Enclosure.Internal.0-1:RAID.Slot.5-1"
            VD_create15 = "racadm storage createvd:RAID.Slot.5-1 -rl r0 -rp ra -pdkey:Disk.Bay.15:Enclosure.Internal.0-1:RAID.Slot.5-1"
            VD_create16 = "racadm storage createvd:RAID.Slot.5-1 -rl r0 -rp ra -pdkey:Disk.Bay.16:Enclosure.Internal.0-1:RAID.Slot.5-1"
            VD_create17 = "racadm storage createvd:RAID.Slot.5-1 -rl r0 -rp ra -pdkey:Disk.Bay.17:Enclosure.Internal.0-1:RAID.Slot.5-1"
            VD_create18 = "racadm storage createvd:RAID.Slot.5-1 -rl r0 -rp ra -pdkey:Disk.Bay.18:Enclosure.Internal.0-1:RAID.Slot.5-1"
            VD_create19 = "racadm storage createvd:RAID.Slot.5-1 -rl r0 -rp ra -pdkey:Disk.Bay.19:Enclosure.Internal.0-1:RAID.Slot.5-1"
            VD_create20 = "racadm storage createvd:RAID.Slot.5-1 -rl r0 -rp ra -pdkey:Disk.Bay.20:Enclosure.Internal.0-1:RAID.Slot.5-1"
            VD_create21 = "racadm storage createvd:RAID.Slot.5-1 -rl r0 -rp ra -pdkey:Disk.Bay.21:Enclosure.Internal.0-1:RAID.Slot.5-1"
            VD_create22 = "racadm storage createvd:RAID.Slot.5-1 -rl r0 -rp ra -pdkey:Disk.Bay.22:Enclosure.Internal.0-1:RAID.Slot.5-1"
            VD_create23 = "racadm storage createvd:RAID.Slot.5-1 -rl r0 -rp ra -pdkey:Disk.Bay.23:Enclosure.Internal.0-1:RAID.Slot.5-1"

            Job_create = "racadm jobqueue create RAID.Slot.5-1"
            #Poweraction = "racadm serveraction powercycle"
            Verify = "racadm storage get vdisks"
            stdin, stdout, stderr = connection.exec_command(Verify)
            file.write('###########' + stdout.read() + '################################################' + '\n')
            Verify_raid = "racadm storage get vdisks -o -p layout"
            stdin, stdout, stderr = connection.exec_command(Verify_raid)
            print(stdout.read())
            file.write('###########' + stdout.read() + '################################################' + '\n')
            VD_commands = [VD_create1,VD_create2,VD_create3,VD_create4,VD_create5,VD_create6,VD_create7,VD_create8,VD_create9,VD_create10,VD_create11,VD_create12,VD_create13,VD_create14,VD_create15,VD_create16,VD_create17,VD_create18,VD_create19,VD_create20,VD_create21,VD_create22,VD_create23,Job_create]

            for commands in VD_commands:
                print(commands)
                stdin, stdout, stderr = connection.exec_command(commands)
                file.write('###########' + stdout.read() + '################################################' + '\n')
                stdin, stdout, stderr = connection.exec_command(Verify_raid)
                file.write('###########' + stdout.read() + '################################################' + '\n')
                file.write('############ Raid_config_compute ###################' + '\n')


        def Idrac_config_check():

            print(serverIP)
            print('Idrac_config_6152_check')
            file.write('############' + serverIP + '###################' + '\n')
            file.write('############ Idrac_config_6152_check ###################' + '\n')
            fwupdate = "racadm getversion -f idrac"
            VD_commands = [fwupdate]
            for commands in VD_commands:
                print(commands)
                stdin, stdout, stderr = connection.exec_command(commands)
                print(stdout.read())
                file.write(stdout.read()+'\n')

            file.write('############ Idrac_config_6152_check ###################' + '\n')


        def BIOS_upgrade():

            print(serverIP)
            print('BIOS_config_6152')
            file.write('############' + serverIP + '###################' + '\n')
            file.write('############ BIOS_config_6152 ###################' + '\n')
            fwupdate = "racadm update -f BIOS_MGGKF_WN64_137.EXE  -u root -p mavenir -l 10.251.142.10:/nfsshare"
            #Poweraction = "racadm serveraction powercycle"
            VD_commands = [fwupdate]
            # VD_commands = [Poweraction]
            for commands in VD_commands:
                print(commands)
                stdin, stdout, stderr = connection.exec_command(commands)
                print(stdout.read())
                file.write('###########' + stdout.read() + '################################################' + '\n')

            file.write('############ BIOS_config_6152 ###################' + '\n')


        def Autopower_controller_storage():
            file.write('############' + serverIP + '###################' + '\n')
            file.write('############ Autopower_controller_Dell ###################' + '\n')
            print(serverIP)
            print('Autopower_controller_Dell')
            check_command = "racadm get BIOS.SysSecurity.AcPwrRcvry"
            Disable_cmd = "racadm set BIOS.SysSecurity.AcPwrRcvry On"
            CreateJob = "racadm jobqueue create BIOS.Setup.1-1"
            #Powercycle = "racadm serveraction powercycle"
            stdin, stdout, stderr = connection.exec_command(check_command)
            print(stdout.read())
            file.write('Autopower status before enabling:' + stdout.read()+'\n')
            stdin, stdout, stderr = connection.exec_command(Disable_cmd)
            print(stdout.read())
            file.write('Autopower status before enabling:' + stdout.read() + '\n')
            stdin, stdout, stderr = connection.exec_command(CreateJob)
            print(stdout.read())
            file.write('Autopower status before enabling:' + stdout.read() + '\n')
            #stdin, stdout, stderr = connection.exec_command(Powercycle)
            #print(stdout.read())
            #file.write('\n Autopower Enabled \n output after enabling \n' + stdout.read())
            file.write('############ Autopower_controller_Dell ###################' + '\n')

        def Autopower_compute():
            file.write('############'+serverIP+'###################'+'\n')
            file.write('############ Autopower_compute_dell ###################' + '\n')
            print (serverIP)
            print('Autopower_compute_dell')
            check_command="racadm get BIOS.SysSecurity.AcPwrRcvry"
            Disable_cmd="racadm set BIOS.SysSecurity.AcPwrRcvry Off"
            CreateJob="racadm jobqueue create BIOS.Setup.1-1"
            #Powercycle="racadm serveraction powercycle"
            stdin, stdout, stderr=connection.exec_command(check_command)
            print(stdout.read())
            file.write('Autopower status before enabling:'+stdout.read()+'\n')
            print(Disable_cmd)
            stdin, stdout, stderr=connection.exec_command(Disable_cmd)
            print(stdout.read())
            file.write('Autopower status before enabling:' + stdout.read() + '\n')
            print(CreateJob)
            stdin, stdout, stderr=connection.exec_command(CreateJob)
            print(stdout.read())
            file.write('Autopower status before enabling:' + stdout.read() + '\n')
            #print(Powercycle)
            #stdin, stdout, stderr=connection.exec_command(Powercycle)
            #print(stdout.read())
            #file.write('\n Autopower Enabled \n output after enabling \n'+stdout.read())
            file.write('############ Autopower_compute_dell ###################' + '\n')

        def Boot_mode_bios():
            file.write('############'+serverIP+'###################'+'\n')
            file.write('############ Boot_mode_bios ###################' + '\n')
            command = "racadm set BIOS.BiosBootSettings.BootMode Bios"
            stdin, stdout, stderr=connection.exec_command(command)
            file.write('###########' + stdout.read() + '################################################' + '\n')

        def Raid_config_delete():
            file.write('############'+serverIP+'###################'+'\n')
            file.write('############ Raid_config_delete ###################' + '\n')
            print(serverIP)
            print('Raid_config_delete')
            delete_vd1="racadm raid deletevd:Disk.Virtual.0:RAID.Slot.5-1"
            Job_create= "racadm jobqueue create RAID.Slot.5-1"
            #Poweraction="racadm serveraction powercycle"
            Verify="racadm storage get vdisks"
            Verify_raid="racadm storage get vdisks -o -p layout"
            Delete_commands= [delete_vd1,Job_create]
            stdin, stdout, stderr=connection.exec_command(Verify)
            file.write('###########' + stdout.read() + '################################################' + '\n')
            stdin, stdout, stderr=connection.exec_command(Verify_raid)
            print(stdout.read())
            file.write('###########' + stdout.read() + '################################################' + '\n')

            for commands in Delete_commands:
                print(commands)
                stdin, stdout, stderr=connection.exec_command(commands)
                file.write('###########'+stdout.read()+'################################################'+'\n')

            file.write('############ Raid_config_delete ###################' + '\n')

        def set_ntp_snmp():
            print("=================="+serverIP+"==============================")
            print('snmp_ntp_autopower')
            file.write('############ snmp_ntp_autopower ###################' + '\n')
             #stdin, stdout, stderr = connection.exec_command("racadm set iDRAC.SNMP.Alert.1.Enable Enabled")
             #stdin, stdout, stderr = connection.exec_command("racadm set iDRAC.SNMP.Alert.1.DestAddr 5.104.4.28")
             #stdin, stdout, stderr = connection.exec_command("racadm get iDRAC.SNMP.Alert.1")
            stdin, stdout, stderr=connection.exec_command("racadm set iDRAC.SNMP.Alert.1.Enable Enabled")
            file.write('###########' + stdout.read() + '################################################' + '\n')
            stdin, stdout, stderr=connection.exec_command("racadm set iDRAC.SNMP.Alert.1.DestAddr 5.104.4.28")
            file.write('###########' + stdout.read() + '################################################' + '\n')
            stdin, stdout, stderr = connection.exec_command("racadm get iDRAC.SNMP.Alert.1")
            file.write('###########' + stdout.read() + '################################################' + '\n')
            print(stdout.readlines())

            #stdin, stdout, stderr = connection.exec_command("racadm set iDRAC.SNMP.Alert.2.Enable Enabled")
            #stdin, stdout, stderr = connection.exec_command("racadm set iDRAC.SNMP.Alert.2.DestAddr 5.112.2.27")
            #stdin, stdout, stderr = connection.exec_command("racadm get iDRAC.SNMP.Alert.2")
            stdin, stdout, stderr = connection.exec_command("racadm set iDRAC.SNMP.Alert.2.Enable Enabled")
            file.write('###########' + stdout.read() + '################################################' + '\n')
            stdin, stdout, stderr = connection.exec_command("racadm set iDRAC.SNMP.Alert.2.DestAddr 5.112.2.27")
            file.write('###########' + stdout.read() + '################################################' + '\n')
            stdin, stdout, stderr = connection.exec_command("racadm get iDRAC.SNMP.Alert.2")
            file.write('###########' + stdout.read() + '################################################' + '\n')
            print(stdout.readlines())

            #stdin, stdout, stderr = connection.exec_command("racadm set iDRAC.Time.Timezone UTC")
            #stdin, stdout, stderr = connection.exec_command("racadm get iDRAC.Time.Timezone")
            stdin, stdout, stderr = connection.exec_command("racadm set iDRAC.Time.Timezone UTC")
            file.write('###########' + stdout.read() + '################################################' + '\n')
            stdin, stdout, stderr = connection.exec_command("racadm get iDRAC.Time.Timezone")
            file.write('###########' + stdout.read() + '################################################' + '\n')
            print(stdout.readlines())

            #stdin, stdout, stderr = connection.exec_command("racadm set iDRAC.NTPConfigGroup.NTPEnable Enabled")
            #stdin, stdout, stderr = connection.exec_command("racadm set iDRAC.NTPConfigGroup.NTP1 5.196.0.121")
            #stdin, stdout, stderr = connection.exec_command("racadm set iDRAC.NTPConfigGroup.NTP2 5.196.0.122")
            #stdin, stdout, stderr = connection.exec_command("racadm set iDRAC.NTPConfigGroup.NTP3 5.198.0.121")
            #stdin, stdout, stderr = connection.exec_command("racadm get iDRAC.NTPConfigGroup")
            stdin, stdout, stderr = connection.exec_command("racadm set iDRAC.NTPConfigGroup.NTPEnable Enabled")
            file.write('###########' + stdout.read() + '################################################' + '\n')
            stdin, stdout, stderr = connection.exec_command("racadm set iDRAC.NTPConfigGroup.NTP1 5.196.0.121")
            file.write('###########' + stdout.read() + '################################################' + '\n')
            stdin, stdout, stderr = connection.exec_command("racadm set iDRAC.NTPConfigGroup.NTP2 5.196.0.122")
            file.write('###########' + stdout.read() + '################################################' + '\n')
            stdin, stdout, stderr = connection.exec_command("racadm set iDRAC.NTPConfigGroup.NTP3 5.198.0.121")
            file.write('###########' + stdout.read() + '################################################' + '\n')
            stdin, stdout, stderr = connection.exec_command("racadm get iDRAC.NTPConfigGroup")
            file.write('###########' + stdout.read() + '################################################' + '\n')
            print(stdout.readlines())
            file.write('############ snmp_ntp_autopower ###################' + '\n')

            # stdin, stdout, stderr = connection.exec_command("racadm set BIOS.SysSecurity.AcPwrRcvry Off")
            # stdin, stdout, stderr = connection.exec_command("racadm get BIOS.SysSecurity.AcPwrRcvry")

            # ssh.exec_command("racadm set BIOS.SysSecurity.AcPwrRcvry Off")
            # stdin, stdout, stderr = connection.exec_command("racadm get BIOS.SysSecurity.AcPwrRcvry")
            ## print stdout.readlines()


        def Idrac_upgrade():
            print(serverIP)
            print('Idrac_config_6152')
            file.write('############'+serverIP+'###################'+'\n')
            file.write('############ Idrac_config_6152 ###################' + '\n')
            fwupdate="racadm update -f iDRAC-with-Lifecycle-Controller_Firmware_FDMV1_WN64_3.21.26.22_A00.EXE  -u root -p mavenir -l 10.69.33.125:/NFSSHARE"
            #sleep 30
            #Poweraction="racadm serveraction powercycle"
            VD_commands = [fwupdate]
            for commands in VD_commands:
                print(commands)
                stdin, stdout, stderr=connection.exec_command(commands)
                file.write('###########'+stdout.read()+'################################################'+'\n')
                print(stdout.read())
                file.write('{}'.format(stdout.read())+'\n')

            file.write('############' + serverIP + '###################' + '\n')

        def server_restart():
            Poweraction = "racadm serveraction powercycle"
            print(Poweraction)
            stdin, stdout, stderr = connection.exec_command(Poweraction)


        dict_main = {'1': IPMIEnable, '2': Raid_config_compute_control , '3': Raid_config_storage, '4': Autopower_controller_storage,
            '5': Autopower_compute,
            '6': Boot_mode_bios, '7': set_ntp_snmp, '8': BIOS_upgrade,
            '9': Idrac_upgrade, '10': Raid_config_delete , '11':Idrac_config_check ,'12':Raid_config_check,'13':Idrac_config_checkbios,'14':server_restart}

        #for sel in selection:
        dict_main[option]()


    except:
        print('Connection to {} got failed '.format(serverIP))



if __name__ == '__main__':
    dict_user = {'1': 'IPMIEnable', '2': 'Raid_config_compute_control' , '3': 'Raid_config_storage', '4': 'Autopower_controller_storage',
            '5': 'Autopower_compute',
            '6': 'Boot_mode_bios', '7': 'set_ntp_snmp', '8': 'BIOS_upgrade',
            '9': 'Idrac_upgrade', '10': 'Raid_config_delete' , '11':'Idrac_config_check' ,'12':'Raid_config_check','13':'Idrac_config_checkbios','14':'server_restart'}

    for sr in range(1,len(dict_user)+1):
	print(str(sr)+'->'+dict_user['{}'.format(sr)])

    user = raw_input('Please select , which task you want to perform:\n')
    user=user.split()
    if '14' not in user:
	print('You have Missed the re-start option,It is recommended to restart the system after the changes\n')
	op=raw_input('So,do you want to add the restart option Y or N:\n')
	if op == 'y' or op == 'Y':
	    user.append('14')
	else:
	    print("*****You have gone through , without the restart option*****\n")

    def storage_controller(sel):
        with open(r"ipaddress_storage.txt",'r') as s:
            for ip in s.readlines():
                bio_congig(ip.strip('\n'),sel)


        with open(r"ipaddress_controller.txt",'r') as ct:
            for ip in ct.readlines():
                bio_congig(ip.strip('\n'),sel)


    def compute_controller(sel):
        with open(r"ipaddress_compute.txt",'r') as ctp:
            for ip in ctp.readlines():
                bio_congig(ip.strip('\n'),sel)


        with open(r"ipaddress_controller.txt",'r') as ct:
            for ip in ct.readlines():
                bio_congig(ip.strip('\n'),sel)

    def compute(sel):
        with open(r"ipaddress_compute.txt",'r') as ctp:
            for ip in ctp.readlines():
                bio_congig(ip.strip('\n'),sel)

    def storage(sel):
        with open(r"ipaddress_storage.txt",'r') as s:
            for ip in s.readlines():
                bio_congig(ip.strip('\n'),sel)

    def all_ip(sel):
        with open(r"ipaddress_compute.txt",'r') as ctp:
            for ip in ctp.readlines():
                bio_congig(ip.strip('\n'),sel)


        with open(r"ipaddress_controller.txt",'r') as ct:
            for ip in ct.readlines():
                bio_congig(ip.strip('\n'),sel)

        with open(r"ipaddress_storage.txt",'r') as s:
            for ip in s.readlines():
                bio_congig(ip.strip('\n'),sel)


    for sel in user:
        if sel == '2':
            compute_controller(sel)
        elif sel == '3':
            storage(sel)
        elif sel == '4':
            storage_controller(sel)
        elif sel =='5':
            compute(sel)
        else:
            all_ip(sel)




   



