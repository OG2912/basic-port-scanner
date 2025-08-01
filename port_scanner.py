#!/usr/bin/env python3
import socket
import threading
import argparse

print_lock = threading.Lock()

def scan_port(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            with print_lock:
                print(f"[+] Port {port} is open")
        sock.close()
    except KeyboardInterrupt:
        exit("\n[!] Interrupted by user")
    except socket.gaierror:
        exit("[!] Hostname could not be resolved")
    except socket.error:
        exit("[!] Couldn't connect to server")

def run_scanner(target, ports):
    print(f"[*] Scanning target: {target}")
    threads = []

    for port in ports:
        thread = threading.Thread(target=scan_port, args=(target, port))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Basic Port Scanner (TCP)")
    parser.add_argument("-t", "--target", required=True, help="Target IP address")
    parser.add_argument("-p", "--ports", default="1-100", help="Port range to scan (e.g. 1-1000)")
    args = parser.parse_args()

    start_port, end_port = map(int, args.ports.split("-"))
    port_range = range(start_port, end_port + 1)

    run_scanner(args.target, port_range)
