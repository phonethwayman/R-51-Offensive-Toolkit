import socket
import sys
from datetime import datetime
from termcolor import colored 

QUICK_SCAN_PORTS = [
    80,443,22,21,25,53,110,139,445,135,23,143,3306,3389,995,993,111,161,587,
    5900,8080,20,1723,389,137,138,514,1433,119,162,500,873,1900,69,37,113,1521,
    2049,2181,3000,5000,5432,5601,5985,5986,6379,7001,7002

]

DEEP_SCAN_PORTS = [
    80,443,22,21,25,53,110,139,445,135,23,143,3306,3389,995,993,111,161,587,5900,8080,
    20,1723,389,137,138,514,1433,119,162,500,873,1900,69,37,113,1521,2049,2181,3000,5000,5432,
    5601,5985,5986,6379,7001,7002,8000,8008,8081,8086,8200,8443,8888,9000,9001,9200,10000,1080,
    11211,1883,2375,2376,27017,4444,50000,548,631,512,513,902,1434,1812,1813,2000,2001,2002,2003,
    2004,2005,2006,2007,2008,2009,2010,2404,2601,2604,2628,3260,3400,3541,3632,3689,3690,4369,4786,
    5009,5222,5269,5353,5431,5555,5567,5631,5666,5901,6000,6001,6002,6003,6004,6100,6112,6123,6129,
    625,626,6400,6463,648,6500,6566,6580,6646,6666,6667,7007,7070,7100,7144,7161,7200,7300,7400,7435,
    7443,7512,7625,7741,7777,8001,8002,8010,8042,8069,8082,8083,8084,8087,8090,8091,8118,8123,8161,8192,
    8193,8194,8201,8211,8222,8254,8280,8281,8291,8333,8400,8402,8444,8500,8600,8649,8651,8652,8654,8701,8800,
    8834,8887,8899,8999,9002,9003,9004,9010,9040,9050,9100,9160,9201,9300,9443,9500,9600,9696,9800,9898,9900

]


def run_port_scanner():
    """
    Scans a target IP address based on user-selected Quick or Deep mode and prints results in a table.
    """
    
    print(colored("\n===================================", 'cyan'))
    print(colored("   🔍 R51 TCP Port Scanner Tool 🔍   ", 'cyan', attrs=['bold']))
    print(colored("===================================", 'cyan'))
    
    # 1. Get user input
    try:
        target = input(colored(">> Enter Target IP Address (e.g., 127.0.0.1): ", 'yellow'))
        mode_choice = input(colored(">> Choose Scan Mode: (Q)uick or (D)eep? ", 'yellow')).upper()
        
        if mode_choice == 'Q':
            ports_to_scan = QUICK_SCAN_PORTS
            mode_name = "Quick"
        elif mode_choice == 'D':
            ports_to_scan = DEEP_SCAN_PORTS
            mode_name = "Deep"
        else:
            print(colored("[-] Invalid mode choice. Aborting.", 'red')); return

        if not target:
             print(colored("[-] Missing target IP. Aborting.", 'red')); return
            
    except Exception as e:
        print(colored(f"[-] An unexpected error occurred during input: {e}", 'red')); return
        

    # 2. Resolve Target Name to IP
    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print(colored(f"[-] Hostname could not be resolved: {target}", 'red')); return

    print(colored("-" * 50, 'magenta'))
    print(colored(f"[+] Starting {mode_name} Scan on: {target_ip} ({len(ports_to_scan)} ports)", 'green'))
    print(colored(f"[+] Scan started at: {datetime.now().strftime('%m-%d-%Y %H:%M:%S')}", 'green'))
    print(colored("-" * 50, 'magenta'))

    # 3. Port Scanning Loop
    open_ports_list = [] # <-- List to store tuples of (port, service)
    total_ports = len(ports_to_scan)
    
    for count, port in enumerate(ports_to_scan, 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5) 

        result = s.connect_ex((target_ip, port))

        if result == 0:
            try:
                service = socket.getservbyport(port, 'tcp')
            except OSError:
                service = 'Unknown'
            
            open_ports_list.append((port, service))
            
            sys.stdout.write('\r' + ' ' * 60 + '\r') 
            print(colored(f"[OPEN] Port {port: <5} found! (Service: {service})", 'green'))
        
        if count < total_ports:
            sys.stdout.write(colored(f"\r[SCAN - {mode_name}] Checking Port {port} ({count}/{total_ports})... ", 'yellow'))
            sys.stdout.flush()
        
        s.close()
        
    sys.stdout.write('\r' + ' ' * 60 + '\r')
    sys.stdout.flush() 

    # 4. Final Results Table Output
    print(colored("\n" + "=" * 50, 'cyan'))
    print(colored(f"[SCAN COMPLETE] Total Open Ports Found: {len(open_ports_list)}", 'white', attrs=['bold']))
    print(colored("=" * 50, 'cyan'))

    if open_ports_list:
        PORT_WIDTH = 12
        SERVICE_WIDTH = 15
        TABLE_LINE = colored('-' * (PORT_WIDTH + SERVICE_WIDTH + 5), 'blue')
        
        print(TABLE_LINE)
        # Print header
        header = f"|{'OPEN PORT': <{PORT_WIDTH}} | {'SERVICE': <{SERVICE_WIDTH}} |"
        print(colored(header, 'red', attrs=['bold']))
        print(TABLE_LINE)
        
        # Print rows
        for port, service in open_ports_list:
            row = f"|{str(port): <{PORT_WIDTH}} | {service: <{SERVICE_WIDTH}} |"
            print(colored(row, 'white'))
        
        print(TABLE_LINE)
    else:
        print(colored("[INFO] No open ports found in this scan mode.", 'blue'))

if __name__ == '__main__':
    run_port_scanner()
    input(colored("Press Enter to exit...", 'blue'))