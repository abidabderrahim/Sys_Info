# System Information Tool

## Description

The System Information Tool is a Python script that collects and displays detailed information about your system, including OS name, system date, CPU, RAM, disk usage, network status, and more. It also includes additional details like GPU information, system uptime, battery status, and MAC address.

## Features

- **Operating System**: Displays the OS name and version.
- **System Date**: Shows the current date and time.
- **CPU Information**: Provides details about the CPU, including the processor type, number of cores, and usage percentage.
- **RAM Information**: Displays the total, available, and used RAM.
- **Disk Information**: Lists all disk partitions, their total size, used space, free space, and usage percentage.
- **Network Information**: Shows IP addresses associated with all network interfaces and their connection status.
- **MAC Address**: Displays the MAC address of the primary network interface.
- **Connected Devices**: Lists all connected disk devices.
- **User Information**: Displays the current user, user ID (UID), and group ID (GID).
- **Installed Applications**: Provides a list of installed applications (Windows only).
- **System Version**: Displays the system version.
- **System Uptime**: Shows how long the system has been running since the last boot.
- **Battery Status**: Displays the current battery percentage and charging status.
- **GPU Information**: Shows GPU details, including total and used memory (requires NVIDIA GPU and `nvidia-smi`).

## Requirements

- Python 3.x
- `psutil` library (Install using `pip install psutil`)
- `nvidia-smi` for GPU information (optional)

## How It Works

1. **System Information Collection**: The script gathers various system details using the `platform`, `psutil`, and `subprocess` modules.
2. **Cross-Platform Compatibility**: The script is designed to work on multiple operating systems, but certain features (like installed applications and GPU information) may only work on specific platforms.

## How to Run

1. **Install Required Libraries**: Make sure you have the necessary Python libraries installed:

    ```bash
    pip install platform psutil soeckts subprocess uuid colorama
    ```

2. **Run the Script**: Execute the script using Python:

    ```bash
    python Sys_Info.py
    ```
