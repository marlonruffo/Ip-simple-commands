import pyfiglet
import os
import sys
import socket
import threading
import re
import colorama
import ipaddress
import ping3
import subprocess
import nmap


from datetime import datetime
pattern = r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"
regex = re.compile(pattern)

colorama.init()


while True: # loop until the user enters a valid IP
  target = input(str("Target IP: "))

  # check if the target matches the pattern
  if regex.fullmatch(target):
    print("Valid IP")
    break
  else:
    print("Invalid IP. Please try again.")
print(colorama.Fore.BLACK + "_"*82 + colorama.Style.RESET_ALL)
print(colorama.Fore.BLUE + "1 - Scan de portas" + colorama.Style.RESET_ALL)
print(colorama.Fore.BLUE + "2 - Verificar Classe do Ip" + colorama.Style.RESET_ALL)
print(colorama.Fore.BLUE + "3 - Ping no Ip" + colorama.Style.RESET_ALL)
print(colorama.Fore.BLUE + "4 - Traceroute no Ip" + colorama.Style.RESET_ALL)
print(colorama.Fore.BLUE + "5 - Hostname" + colorama.Style.RESET_ALL)
print(colorama.Fore.BLUE + "6 - hosts disponíveis" + colorama.Style.RESET_ALL)

print(colorama.Fore.RED + "5 - Sair" + colorama.Style.RESET_ALL)
print(colorama.Fore.BLACK + "_"*82 + colorama.Style.RESET_ALL)

option = input("Escolha uma opção: ")
if option == "1":
    start_port = int(input("Enter the start port to scan: "))
    end_port = int(input("Enter the final port to scan: "))
    print("Scanning Target: " + target)
    start_time = datetime.now()
    print("Time Started: " + str(datetime.now()))
    print("Aguarde...")

    open_ports = []
    closed_ports = []
    threads = []

    def scan_port(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex((target, port))
        if result == 0:
            open_ports.append(port)
        else:
            closed_ports.append(port)
        s.close()

    try:
        for port in range(start_port, end_port+1):
            t = threading.Thread(target=scan_port, args=(port,))
            threads.append(t)
            t.start()

        # wait for all threads to finish
        for t in threads:
            t.join()

    except KeyboardInterrupt:  # if user press ctrl+c
        print("Exiting Program !!!!")
        sys.exit()

    except socket.error:  # if host is unreachable
        print("Couldn't connect to server")
        sys.exit()

    # print the results
    open_ports.sort()
    closed_ports.sort()
    print("Open ports are: ", open_ports)

    end_time = datetime.now()  # store the end time
    total_time = end_time - start_time  # calculate the total time taken
    total_time_formatted = total_time.total_seconds()  # format the total time taken
    print("Total time taken to read all the ports: {}".format(
        total_time_formatted)+" seconds")  # print the total time taken

    while True:
        user_input = input(
            "Enter 'see' to see closed ports or press 'n' to continue: ")
        if user_input == "see":
            print("Closed ports are: ", closed_ports)
            break
        else:
            print("Certo, você escolheu continuar e nao ver as portas fechadas")
            break

if option == "2":
    ip = ipaddress.IPv4Address(target)
    if ip.is_private:
        # ip.packet transforms the ip into a binary format
        print("Private address")
    # check which class the address belongs to
        if ip.packed >= ipaddress.IPv4Address("10.0.0.0").packed and ip.packed <= ipaddress.IPv4Address("10.255.255.255").packed:
            print("Class A address")
        elif ip.packed >= ipaddress.IPv4Address("172.16.0.0").packed and ip.packed <= ipaddress.IPv4Address("172.31.255.255").packed:
            print("Class B address")
        elif ip.packed >= ipaddress.IPv4Address("192.168.0.0").packed and ip.packed <= ipaddress.IPv4Address("192.168.255.255").packed:
            print("Class C address")
    elif ip.is_reserved:
        if ip.packed >= ipaddress.IPv4Address("224.0.0.0").packed and ip.packed <= ipaddress.IPv4Address("239.255.255.255").packed:
            print("Class D address")
        elif ip.packed >= ipaddress.IPv4Address("240.0.0.0").packed and ip.packed <= ipaddress.IPv4Address("255.255.255.254").packed:
            print("Class E address")
        else:
            print("Reserved address")
    else:
        print("Public address")

if option == "3":
    ip = target
    response = ping3.ping(ip)
    if response == None:
        print("Host is down")
    else:
        print("Host is up")
        
if option == "4": # Traceroute - trace the path to the target

    ip = target
    traceroute = subprocess.run(["tracert", ip], capture_output=True)
    try: # Try to decode the output as UTF-8
        output = traceroute.stdout.decode('utf-8')
    except UnicodeDecodeError:
    # try to decode the output as latin-1
        output = traceroute.stdout.decode('latin-1')
    print(colorama.Fore.BLACK + "_"*82 + colorama.Style.RESET_ALL)
    print(output)
    print(colorama.Fore.BLACK + "_"*82 + colorama.Style.RESET_ALL)
    print("Done")
if option == "5":
    try:
        hostname = socket.gethostbyaddr(target)
        name = hostname[0]
        ip = hostname[2]
        ip_string = ', '.join(ip)
        
    except socket.herror:
        print("Host not found")
    else:
        print("Hostname: " + name)
        print("IP: " + ip_string)

if option == "6":
    ip=target
    prefix_lenght = int(input("Digite o prefixo: "))
    ip_network = ipaddress.IPv4Network((ip,prefix_lenght), strict=False)
    num_hosts = ip_network.num_addresses-2
    print("numero de hosts: " + str(num_hosts))

if option == "7":
    sys.exit()