

import os
import subprocess
import socket
import platform
import sys
def get_DG():
    if(sys.platform.startswith('win')):
        cmd = subprocess.check_output('ipconfig | findstr /i "Gateway"', shell = True)
        cmd = cmd.decode()
        cmd_spl = cmd.split(":")
        return cmd_spl[1]
    else:
        cmd = subprocess.check_output('ip route | grep default', shell = True)
        cmd = cmd.decode()
        cmd_spl = cmd.split(" ")
        return cmd_spl[2]
def check_connection(defaultgateway):
    try:
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping',param,'3',defaultgateway]
        status = subprocess.call(command,stdout = subprocess.PIPE)
        if status == 0:
            return "HOST IS UP!"
        else:

            return "HOST IS DOWN!"
    except Exception as e:
        print("[!!!ERR] " + str(e))
def test_dns_res(hostname):
    try:
        result = (socket.gethostbyname(hostname))
        resolution = (f"[+] Hostname {hostname} resolved to {result}")
        return "DNS RESOLUTION SUCESSFUL! \n(" + resolution + ")"
    except socket.error:
        return "DNS RESOLUTION FAILED!"

def main(): 
    print("---- Starting ----")
    print("[!] Finding default gateway")
    dg = get_DG()
    print("[!] Checking Default Gateway connection please wait")
    dg_status = check_connection(dg)
    print("[!] Checking connection to RIT DNS (129.21.3.17) please wait")
    rit_dns_status = check_connection("129.21.3.17")
    print("[!] Checking connection to GOOGLE DNS (8.8.8.8) please wait")
    google_dns_status = check_connection("8.8.8.8")
    print("[!] Checking dns Resolution to GOOGLE (www.google.com) please wait")
    dns_res = test_dns_res("www.google.com")
    # if(sys.platform.startswith('win')):
    #     os.system("cls")
    # else:
    #     os.system("clear")
    print("-------- < results > -----")
    print(f"[done] Default gatway : {dg}")
    print(f'[done] Status of Default Gatway connection: {dg_status}')
    print(f'[done] Status of RIT DNS server connection: {rit_dns_status}')
    print(f'[done] Status of Google DNS server connection: {google_dns_status}') 
    print(f'[done] DNS resolution test: {dns_res}') 
    
if __name__ == '__main__':
    main()
