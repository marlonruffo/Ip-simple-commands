import sys
import socket
import re
import colorama
import ipaddress
import ping3
import subprocess
import time
import getmac


from datetime import datetime
pattern = r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"
regex = re.compile(pattern)

colorama.init()


while True: # loop until the user enters a valid IP
  target = input(str(colorama.Fore.MAGENTA+"Target IP: "))

  # check if the target matches the pattern
  if regex.fullmatch(target):
    print(colorama.Fore.GREEN+"Valid IP")
    print(colorama.Fore.MAGENTA+"Wait a moment...")
    time.sleep(1.5)
    break
  else:
    print(colorama.Fore.RED+"Invalid IP. Please try again.")
    print(colorama.Fore.MAGENTA+"What do you want to do with the IP?: "+target+" ?")
    print(colorama.Fore.RED + "1"+colorama.Fore.GREEN+ "- Check for open ports")
    print(colorama.Fore.RED + "2"+colorama.Fore.GREEN+ "- Check the class of the IP")
    print(colorama.Fore.RED + "3" +colorama.Fore.GREEN+"- Ping the target")
    print(colorama.Fore.RED + "4"+colorama.Fore.GREEN+ "- Trace the route to the target")
    print(colorama.Fore.RED + "5"+colorama.Fore.GREEN+ "- Get the hostname")
    print(colorama.Fore.RED + "6"+colorama.Fore.GREEN+ "- Calculate Subnet")
    print(colorama.Fore.RED + "7"+colorama.Fore.GREEN+ "- Get the MAC address")
    print(colorama.Fore.RED + "8" +colorama.Fore.WHITE+ "- Exit" )


option = input(colorama.Fore.MAGENTA +"Choose an option: ")
if option == "1":
    print(colorama.Fore.MAGENTA + "You selected option 1:" +colorama.Fore.RED +"'Check for open ports'")

    print(colorama.Fore.GREEN+"Scanning Target: " + target)
    start_time = datetime.now()
    print(colorama.Fore.GREEN+"Time Started: " + str(datetime.now()))
    print(colorama.Fore.MAGENTA+"it might take a while Wait a moment...")
# execute the nmap command and scan the network
    nmap_output = subprocess.run(["nmap", "-sV", target], capture_output=True).stdout.decode()
    # extract the open ports from the nmap output
    open_ports = []
    for line in nmap_output.split("\n"):
        if "open" in line and "unrecognized" not in line:
            open_ports.append(line)

    # print the open ports
    print(colorama.Fore.MAGENTA + "Informations of open ports on host " +colorama.Fore.CYAN+ target + ":" + colorama.Style.RESET_ALL)
    print(colorama.Fore.RED + "PORT   STATE  SERVICE        VERSION" + colorama.Style.RESET_ALL)
    for port in open_ports:
        print(colorama.Fore.GREEN + port + colorama.Style.RESET_ALL)

    end_time = datetime.now()  # store the end time
    total_time = end_time - start_time  # calculate the total time taken
    total_time_formatted = total_time.total_seconds()  # format the total time taken
    print(colorama.Fore.MAGENTA +"Total time taken to read all the ports: {}".format(
        total_time_formatted)+colorama.Fore.MAGENTA +" seconds")  # print the total time taken

if option == "2":
    print(colorama.Fore.MAGENTA + "You selected option 2:" +colorama.Fore.RED + "'Check the class of the IP'")
    ip = ipaddress.IPv4Address(target)
    print(colorama.Fore.RED+"IP address: " +colorama.Fore.GREEN + str(ip))
    # check which class the address belongs to
    if ip.is_global:
        print(colorama.Fore.RED+"Type:"+colorama.Fore.GREEN+"Public IP address")
    elif ip.is_private:
        print(colorama.Fore.RED+"Type:"+colorama.Fore.GREEN+"Private IP address")
    elif ip.is_reserved:
        print(colorama.Fore.RED+"Type:"+colorama.Fore.GREEN+"Reserved IP address")
    else:
        print(colorama.Fore.MAGENTA+"Could not determine the type of the IP address")
    if ip.packed >= ipaddress.IPv4Address("0.0.0.0").packed and ip.packed <= ipaddress.IPv4Address("127.255.255.255").packed:
        print(colorama.Fore.RED+"Class A address")
    elif ip.packed >= ipaddress.IPv4Address("128.0.0.0").packed and ip.packed <= ipaddress.IPv4Address("191.255.255.255").packed:
        print(colorama.Fore.RED+"Class B address")
    elif ip.packed >= ipaddress.IPv4Address("192.0.0.0").packed and ip.packed <= ipaddress.IPv4Address("223.255.255.255").packed:
        print(colorama.Fore.RED+"Class C address")
    elif ip.packed >= ipaddress.IPv4Address("224.0.0.0").packed and ip.packed <= ipaddress.IPv4Address("239.255.255.255").packed:
        print(colorama.Fore.RED+"Class D address")
    elif ip.packed >= ipaddress.IPv4Address("240.0.0.0").packed and ip.packed <= ipaddress.IPv4Address("255.255.255.254").packed:
        print(colorama.Fore.RED+"Class E address")
    else:
        print(colorama.Fore.MAGENTA+"Could not determine the class of the IP address")


if option == "3":
    print(colorama.Fore.MAGENTA + "You selected option 3:"+colorama.Fore.RED+ "'Ping the target'")
    ip = target
    response = ping3.ping(ip)
    if response == None:
        print(colorama.Fore.RED+"STATUS: "+colorama.Fore.GREEN+"Host is "+colorama.Fore.RED+ "down")
    else:
        print(colorama.Fore.RED+"STATUS: "+colorama.Fore.GREEN+"Host is up")
        
if option == "4": # Traceroute - trace the path to the target
    print(colorama.Fore.MAGENTA + "You selected option 4:"+colorama.Fore.RED+ "'Trace the route to the target'")
    print(colorama.Fore.MAGENTA+"Wait...")
    ip = target
    traceroute = subprocess.run(["tracert", ip], capture_output=True)
    try: # Try to decode the output as UTF-8
        output = traceroute.stdout.decode('utf-8')
    except UnicodeDecodeError:
    # try to decode the output as latin-1
        output = traceroute.stdout.decode('latin-1')
    print(colorama.Fore.BLACK + "_"*82 + colorama.Style.RESET_ALL)
    print(colorama.Fore.GREEN+output)
    print(colorama.Fore.MAGENTA+"Done")
    print(colorama.Fore.BLACK + "_"*82 + colorama.Style.RESET_ALL)

if option == "5":
    print(colorama.Fore.MAGENTA + "You selected option 5:"+colorama.Fore.RED+ "'Get the hostname'")
    try:
        hostname = socket.gethostbyaddr(target)
        name = hostname[0]
        ip = hostname[2]
        ip_string = ', '.join(ip)
        
    except socket.herror:
        print(colorama.Fore.RED+"Host not found")
    else:
        print(colorama.Fore.RED+"Hostname: "+colorama.Fore.GREEN + name)
        print(colorama.Fore.RED+"IP: " +colorama.Fore.GREEN+ ip_string)

if option == "6":
    print(colorama.Fore.MAGENTA + "You selected option 6:" +colorama.Fore.RED+"'Number of possible hosts in the target IP's subnet'")
    ip=target
    prefix_lenght = int(input(colorama.Fore.MAGENTA+"Digite o prefixo: "))
    ip_network = ipaddress.IPv4Network((ip,prefix_lenght), strict=False)
    
    
    print(colorama.Fore.RED + "network address: " + colorama.Fore.GREEN + str(ip_network.network_address))
    print(colorama.Fore.RED + "broadcast address: " + colorama.Fore.GREEN + str(ip_network.broadcast_address))
    print(colorama.Fore.MAGENTA + "Available IP range:")
    first_ip = ip_network.network_address + 1
    last_ip = ip_network.broadcast_address - 1
    print(colorama.Fore.RED + "First available IP: " + colorama.Fore.GREEN + str(first_ip))
    print(colorama.Fore.RED + "Last available IP: " + colorama.Fore.GREEN + str(last_ip))
    num_hosts = len(list(ip_network.hosts()))
    print(colorama.Fore.RED + "Number of available hosts: " + colorama.Fore.GREEN + str(num_hosts))


if option =="7":
    print(colorama.Fore.MAGENTA + "You selected option 7:" +colorama.Fore.RED+"'Get the MAC address'")
    ip = target
    mac = getmac.get_mac_address(ip=ip)
    if mac is not None:
        print(colorama.Fore.RED+"MAC address: " +colorama.Fore.GREEN + mac)
    else:
        print(colorama.Fore.RED+"Unable to retrieve MAC address for the given IP")

if option == "8":
    print(colorama.Fore.MAGENTA + "You selected option 8:" +colorama.Fore.RED+"'Exit'")
    print(colorama.Fore.GREEN+"Bye!")
    sys.exit()



