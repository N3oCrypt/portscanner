import socket
from termcolor import colored
import os
import threading

puerto_abierto_encontrado = False
lock = threading.Lock()  

def clear_screen(sys):
    if sys == "1":
        os.system("cls")
    elif sys == "2":
        os.system("clear")

def print_banner():
    banner = """ @@@@@@@   @@@@@@  @@@@@@@  @@@@@@@       @@@@@@  @@@@@@@  @@@@@@  @@@  @@@ @@@  @@@ @@@@@@@@ @@@@@@@ 
 @@!  @@@ @@!  @@@ @@!  @@@   @@!        !@@     !@@      @@!  @@@ @@!@!@@@ @@!@!@@@ @@!      @@!  @@@
 @!@@!@!  @!@  !@! @!@!!@!    @!!         !@@!!  !@!      @!@!@!@! @!@@!!@! @!@@!!@! @!!!:!   @!@!!@! 
 !!:      !!:  !!! !!: :!!    !!:            !:! :!!      !!:  !!! !!:  !!! !!:  !!! !!:      !!: :!! 
  :        : :. :   :   : :    :         ::.: :   :: :: :  :   : : ::    :  ::    :  : :: :::  :   : :"""
    print(colored(banner, "red"))

def escanports(ip, port):
    global puerto_abierto_encontrado
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    r = s.connect_ex((ip, port))
    if r == 0:
        with lock:
            puerto_abierto_encontrado = True
        print(colored(f"[+] Puerto {port} abierto", "green"))
    s.close()

def main():
    global puerto_abierto_encontrado
    os.system("cls")
    print("(1) Windows")
    print("(2) Linux")

    sys = input("Selecciona tu OS > ")

    if sys not in ["1", "2"]:
        print("Opción inválida. Saliendo.")
        return

    clear_screen(sys)
    print_banner()

    ip = input("Introduce la IP objetiva >>> ")
    clear_screen(sys)
    print_banner()

    puertos = input("Rango de puertos EJ: 1,20 >>> ")
    try:
        start, end = map(int, puertos.split(","))
    except:
        print("Rango de puertos inválido. Usa el formato correcto, ej: 1,20")
        return

    puerto_abierto_encontrado = False  

    threads = []
    for port in range(start, end + 1):
        t = threading.Thread(target=escanports, args=(ip, port))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    if not puerto_abierto_encontrado:
        print(colored("No se encontraron puertos abiertos. ", "yellow"))

if __name__ == "__main__":
    main()
