from ipaddress import ip_address
from paramiko import SSHClient, AutoAddPolicy
from datetime import datetime
import time
import re
from database.models import Pool, Address, Policy, Tunnel, AccessList, AccessHour


# parse_asa function will take a file path as an argument.
# It will parse pool, tunnel, policy, ACL and few time-range configuration
# from the file. This fuction is very specific to Cisco ASA Version 9.8(4)26.
# Other version's configuration will not work most likely.

def parse_asa(config_file):
    start = datetime.now()
    policy_found = False
    tunnel_found = False
    time_found = False
    acl_name = 'notAaclName'

    
    with open(config_file, 'r') as pointer:
        lines = pointer.readlines()
        
        ###-------       Clearing old data       -------###
        Address.objects.all().delete()
        Pool.objects.all().delete()
        Policy.objects.all().delete()
        Tunnel.objects.all().delete()
        AccessList.objects.all().delete()
        AccessHour.objects.all().delete()

        ###-------- Inspecting the configuration -------###
        for line in lines:

            #---- Processing IP Pools ----#
            if 'ip local pool' in line:
                pool_line = line.split()
                pool = Pool(name=pool_line[3], address_range=pool_line[4])
                pool.save()
                
                if '-' in pool_line[4]:
                    address_range = pool_line[4].split('-')
                    first_address = ip_address(address_range[0])
                    last_address = ip_address(address_range[-1])
                    while first_address <= last_address:
                        Address(ipv4=first_address, pool=pool).save()
                        first_address = first_address + 1
                else:
                    Address(ipv4=ip_address(pool_line[4]), pool=pool).save()

            #---- Processing Time-Range ----#
            if 'time-range ' in line and '_VALIDITY' in line:
                time_section = []
                time_found = True
                time_section.append(line.rstrip('\n'))
                continue
            if time_found:
                if line.startswith(' '):
                    time_section.append(line.rstrip('\n'))
                else:
                    time_found = False
                    for time_line in time_section:
                        if 'time-range ' in time_line:
                            access_hour = AccessHour(name = time_line.split()[1])
                        if 'absolute end ' in time_line:
                            access_hour.date = datetime.strptime(time_line[14:], '%I:%M %d %B %Y')
                    access_hour.save()

            #---- Processing Access Lists ----#
            if 'access-list ' in line and ' extended' in line:
                if acl_name not in line:
                    access_list = AccessList(name = line.split()[1])
                    access_list.line = line
                    access_list.save()
                    acl_name = line.split()[1]
                else:
                    access_list = AccessList.objects.filter(name = line.split()[1]).first()
                    access_list.add_line(line)
                    access_list.save()

            #---- Processing Group Policy ----#
            if 'group-policy ' in line and ' attributes' in line:
                policy_section = []
                policy_found = True
                policy_section.append(line.rstrip('\n'))
                continue
            if policy_found:
                if line.startswith(' '):
                    policy_section.append(line.rstrip('\n'))
                else:
                    policy_found = False
                    for policy_line in policy_section:
                        if 'group-policy' in policy_line:
                            policy = Policy(name=policy_line.split()[1])
                        if 'vpn-access-hours ' in policy_line:
                            policy.access_hours = policy_line.split()[2]
                        if 'vpn-simultaneous-logins' in policy_line:
                            policy.sim_login = int(policy_line.split()[1])
                        if 'vpn-filter value' in policy_line:
                            access_list = AccessList.objects.filter(name=policy_line.split()[2]).first()
                            policy.access_lists.add(access_list)
                        policy.save()

            #---- Processing Tunnel Group ----#
            if 'tunnel-group ' in line and ' general-attributes' in line:
                tunnel_section = []
                tunnel_found = True
                tunnel_section.append(line.rstrip('\n'))
                continue
            if tunnel_found:
                if line.startswith(' ') or ' webvpn-attributes' in line:
                    tunnel_section.append(line.rstrip('\n'))
                else:
                    tunnel_found = False
                    for tunnel_line in tunnel_section:
                        if 'tunnel-group ' in tunnel_line and ' general-attributes' in tunnel_line:
                            tunnel = Tunnel(name=tunnel_line.split()[1])
                        if 'address-pool ' in tunnel_line:
                            pool = Pool.objects.filter(name__iexact=str(tunnel_line.split()[1])).first()
                            tunnel.pools.add(pool)
                        if 'authentication-server-group ' in tunnel_line:
                            tunnel.auth_server = tunnel_line.split()[1]
                        if 'default-group-policy ' in tunnel_line:
                            policy = Policy.objects.filter(name__iexact=str(tunnel_line.split()[1])).first()
                            tunnel.policies.add(policy)
                        if 'group-url ' in tunnel_line:
                            tunnel.url = tunnel_line.split()[1]
                            approval = re.search('DVTP[N]?\d{1,4}', tunnel_line.split()[1])
                            if approval:
                                tunnel.approval = approval.group(0)
                        tunnel.save()
    end = datetime.now()
    return (end-start)


def run_config(username, password, host, port = 22, encoding = 'utf-8'):
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.connect(host, port, username, password, look_for_keys=False, allow_agent=False)
    ssh_shell = client.invoke_shell()
    time.sleep(5)

    ssh_shell.send('en\n')
    ssh_shell.send(password + '\n')
    time.sleep(2)
    ssh_shell.send('terminal pager 0\n')
    ssh_shell.send('show run\n')

    filename = f'./config_output/output-{str(datetime.now().strftime("%I%M%S%d%B%Y"))}.txt'

    with open(filename, 'w', newline='') as pen:
        while True:
            output = ssh_shell.recv(65535)
            output = str(output, encoding)
            pen.write(output)
            if ": end" in str(output):
                break
    ssh_shell.close()
    client.close()
    filepath = f'{filename[:2]}database/fw_cmd/{filename[2:]}'
    return filepath