import platform
import psutil
import os
import socket
import subprocess
import time
import uuid
from colorama import Fore, Style, init

# Initialize Colorama
init(autoreset=True)

# User Information 
def get_user_info():
    user = os.getlogin()
    if platform.system() == "Windows":
        return user, "N/A", "N/A"
    else:
        return user, os.getuid(), os.getgid()

# OS Information
def get_os_info():
    return platform.system(), platform.release()

# System Date and Time 
def get_system_date():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

# Disk Information
def get_disk_info():
    partitions = psutil.disk_partitions()
    disk_info = []
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_info.append({
                "Device": partition.device,
                "Mountpoint": partition.mountpoint,
                "File system": partition.fstype,
                "Total Size": usage.total,
                "Used": usage.used,
                "Free": usage.free,
                "Percentage Used": usage.percent
            })
        except PermissionError:
            print(Fore.RED + f"Skipping inaccessible drive: {partition.device}")
    return disk_info

# Ram Information
def get_ram_info():
    memory = psutil.virtual_memory()
    return memory.total, memory.available, memory.percent

# CPU Information
def get_cpu_info():
    return platform.processor(), psutil.cpu_count(logical=True), psutil.cpu_percent(interval=1)

# System Version
def get_system_version():
    return platform.version()

# Installled Applications (Windows Only)
def get_installed_apps():
    if platform.system() == "Windows":
        try:
            apps = subprocess.check_output(['wmic', 'product', 'get', 'name']).decode().split('\n')
            return [app.strip() for app in apps if app.strip()]
        except:
            return "Unable To Retrieve Installed Applications ."
    return "Installed Apps List Is Not Supported On This OS ."

# System Uptime 
def get_system_uptime():
    uptime_seconds = time.time() - psutil.boot_time()
    uptime_string = time.strftime("%H:%M:%S", time.gmtime(uptime_seconds))
    return uptime_string

# Battery Status
def get_battery_status():
    if hasattr(psutil, "sensors_battery"):
        battery = psutil.sensors_battery()
        if battery:
            return battery.percent, battery.power_plugged
        return "Battery Not Found"
    return "Battery Information Not Supported On This OS ."

# GPU Information for Nvidia 
def get_gpu_info():
    try:
        gpu_info = subprocess.check_output(['nvidia-smi', '--query-gpu=name,memory.total,memory.free,memory.used', '--format=csv,nounits,noheader']).decode().strip().split('\n')
        gpus = []
        for gpu in gpu_info:
            name, total_mem, free_mem, used_mem = gpu.split(',')
            gpus.append({
                "GPU": name.strip(),
                "Totall Memory": f"{total_mem.strip()} MB",
                "Free Memory": f"{free_mem.strip()} MB",
                "Used Memory": f"{used_mem.strip()} MB"
            })
        return gpus
    except:
        return "GPU Information Not Availablel Or Not Supported In OS ."

# IP Address
def get_ip_address():
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

# MAC Address
def get_mac_address():
    mac = hex(uuid.getnode()).replace('0x', '').upper()
    return ':'.join(mac[i:i+2] for i in range(0, 12, 2))

# Connected Devices
def get_connected_devices():
    return [device.device for device in psutil.disk_partitions()]

# Network Information
def get_network_info():
    addrs = psutil.net_if_addrs()
    net_info = {}
    for interface, addr in addrs.items():
        net_info[interface] = addr[0].address
    return net_info

# Network Status 
def get_network_status():
    stats = psutil.net_if_stats()
    status = {}
    for interface, data in stats.items():
        status[interface] = "Connected" if data.isup else "Desconnected"
    return status

# Display Information 
def display_system_info():
    print(Fore.CYAN + "\n\nUser: " + Fore.YELLOW + f"{get_user_info()[0]} (UID: {get_user_info()[1]}, GID: {get_user_info()[2]})")
    print(Fore.CYAN + "\nOperating System: " + Fore.YELLOW + f"{get_os_info()[0]} {get_os_info()[1]}")
    print(Fore.CYAN + "\nSystem Date: " + Fore.YELLOW + f"{get_system_date()}")
    print(Fore.CYAN + "\nDisk Information: ")
    for disk in get_disk_info():
        print(Fore.YELLOW + f"  {disk['Device']}: " + Fore.GREEN + f"{disk['Total Size'] / (1024 ** 3):.2f} GB Total, {disk['Free'] / (1024 ** 3):.2f} GB Free ({disk['Percentage Used']}% Used)")
    print(Fore.CYAN + "\nRAM: " + Fore.YELLOW + f"{get_ram_info()[0] / (1024 ** 3):.2f} GB Total, {get_ram_info()[1] / (1024 ** 3):.2f} GB Available - {get_ram_info()[2]}% usage")
    print(Fore.CYAN + "\nCPU: " + Fore.YELLOW + f"{get_cpu_info()[0]} ({get_cpu_info()[1]} cores) - {get_cpu_info()[2]}% usage")
    print(Fore.CYAN + "\nSystem Version: " + Fore.YELLOW + f"{get_system_version()}")

    print(Fore.CYAN + "\nInstalled Applications: ")
    installed_apps = get_installed_apps()
    if isinstance(installed_apps, list):
        for app in installed_apps:
            print(Fore.YELLOW + f"  {app}")
    else:
        print(Fore.YELLOW + f"  {installed_apps}")

    print(Fore.CYAN + "\nSystem Uptime: " + Fore.YELLOW + f"{get_system_uptime()}")
    battery_status = get_battery_status()
    if isinstance(battery_status, tuple):
        print(Fore.CYAN + "\nBattery: " + Fore.YELLOW + f"{battery_status[0]}% {'(Plugged in)' if battery_status[1] else '(On battery)'}")
    else:
        print(Fore.CYAN + "Battery: " + Fore.YELLOW + f"{battery_status}")
    
    gpu_info = get_gpu_info()
    if isinstance(gpu_info, list):
        print(Fore.CYAN + "\nGPU Information: ")
        for gpu in gpu_info:
            print(Fore.YELLOW + f"  {gpu['GPU']}: " + Fore.GREEN + f"{gpu['Total Memory']} Total, {gpu['Used Memory']} Used")
    else:
        print(Fore.CYAN + "\nGPU Information: " + Fore.YELLOW + f"{gpu_info}")
   
    print(Fore.CYAN + "\nIP Address: " + Fore.YELLOW + f"{get_ip_address()}")
    print(Fore.CYAN + "\nMAC Address: " + Fore.YELLOW + f"{get_mac_address()}")
    print(Fore.CYAN + "\nConnected Devices: " + Fore.YELLOW + f"{get_connected_devices()}")
    print(Fore.CYAN + "\nNetwork Information: ")
    for interface, address in get_network_info().items():
        print(Fore.YELLOW + f"  {interface}: " + Fore.GREEN + f"{address}")
    print(Fore.CYAN + "\nNetwork Status: ")
    for interface, status in get_network_status().items():
        print(Fore.YELLOW + f"  {interface}: " + Fore.GREEN + f"{status}")

display_system_info()