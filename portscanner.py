import socket
from termcolor import colored
import os
import threading

open_port_found = False
lock = threading.Lock()

def clear_screen(os_choice):
    if os_choice == "1":
        os.system("cls")
    elif os_choice == "2":
        os.system("clear")

def print_banner():
    banner = """ @@@@@@@   @@@@@@  @@@@@@@  @@@@@@@       @@@@@@  @@@@@@@  @@@@@@  @@@  @@@ @@@  @@@ @@@@@@@@ @@@@@@@ 
 @@!  @@@ @@!  @@@ @@!  @@@   @@!        !@@     !@@      @@!  @@@ @@!@!@@@ @@!@!@@@ @@!      @@!  @@@
 @!@@!@!  @!@  !@! @!@!!@!    @!!         !@@!!  !@!      @!@!@!@! @!@@!!@! @!@@!!@! @!!!:!   @!@!!@! 
 !!:      !!:  !!! !!: :!!    !!:            !:! :!!      !!:  !!! !!:  !!! !!:  !!! !!:      !!: :!! 
  :        : :. :   :   : :    :         ::.: :   :: :: :  :   : : ::    :  ::    :  : :: :::  :   : :"""
    print(colored(banner, "red"))

def scan_port(target_ip, port_number):
    global open_port_found
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    result = sock.connect_ex((target_ip, port_number))
    if result == 0:
        with lock:
            open_port_found = True
        print(colored(f"[+] Port {port_number} is open", "green"))
    sock.close()

def main():
    global open_port_found
    os.system("cls")
    print("(1) Windows")
    print("(2) Linux")

    os_choice = input("Select your operating system > ")

    if os_choice not in ["1", "2"]:
        print("Invalid option. Exiting.")
        return

    clear_screen(os_choice)
    print_banner()

    target_ip = input("Enter the target IP >>> ")
    clear_screen(os_choice)
    print_banner()

    ports = input("Port range (e.g., 1,20) >>> ")
    try:
        start_port, end_port = map(int, ports.split(","))
    except:
        print("Invalid port range. Use the correct format, e.g., 1,20")
        return

    open_port_found = False

    threads = []
    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=scan_port, args=(target_ip, port))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    if not open_port_found:
        print(colored("No open ports found.", "yellow"))

if __name__ == "__main__":
    main()
