import socket
import time
import psutil

name = socket.gethostname()
ip_address = socket.gethostbyname_ex(name)

verde = "\033[32m"
vermelho = "\033[31m"

process_ip = {}

for ip in ip_address[2]:
    process_ip[ip] = {}

while True:
    time.sleep(10)

    fd = psutil.net_connections()
    ports_found = {}

    for service in fd:
        ip = service.laddr[0]
        port = service.laddr[1]
        proc_name = "Unknown"
        try:
            process = psutil.Process(service.pid)
            proc_name = process.name()
        except:
            pass

        if not ip in ports_found:
            ports_found[ip] = {}

        ports_found[ip][port] = proc_name

    for ip in ip_address[2]:
        if ip not in ports_found:
            continue

        for port in range(65536):
            if port not in process_ip[ip] and port in ports_found[ip]:
                service_name = ports_found[ip][port]
                process_ip[ip][port] = service_name
                print(f"{verde}ip: {ip}| port: {port}| name: {service_name}| Opened")
            elif port in process_ip[ip] and port not in ports_found[ip]:
                service_name = process_ip[ip][port]
                print(f"{vermelho}ip: {ip}| port: {port}| name: {service_name}| Closed")
                del process_ip[ip][port]