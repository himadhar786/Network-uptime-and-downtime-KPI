import os
import subprocess
import pandas as pd
from datetime import datetime

# List of devices and their IP addresses
devices = [
    {'name': 'Router', 'ip': '192.168.1.1'},
    {'name': 'Switch', 'ip': '192.168.1.2'},
    {'name': 'Server', 'ip': '192.168.1.3'},
    {'name': 'Printer', 'ip': '192.168.1.4'},
    {'name': 'Access Point', 'ip': '192.168.1.5'},
    {'name': 'Firewall', 'ip': '192.168.1.6'}
]

def ping_device(ip_address, retries=3):
    """
    Ping a device and return True if it's up, False if down.
    Retries multiple times to ensure accuracy.
    """
    for _ in range(retries):
        response = subprocess.run(
            ['ping', '-n' if os.name == 'nt' else '-c', '1', ip_address],
            stdout=subprocess.PIPE,
            text=True
        )
        if response.returncode == 0:
            return True
    return False

def gather_network_data(devices):
    """
    Gather the network status for each device in the list.
    Returns a pandas DataFrame.
    """
    data = []
    for device in devices:
        status = "Up" if ping_device(device['ip']) else "Down"
        data.append({
            'Device': device['name'],
            'IP': device['ip'],
            'Status': status,
            'Time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    return pd.DataFrame(data)

def save_network_data(df, file_path='network_status.csv'):
    """
    Save the gathered network data to a CSV file.
    """
    df.to_csv(file_path, mode='a', header=not os.path.exists(file_path), index=False)
    print(f"Data saved to {file_path}")

# Main execution
if __name__ == "__main__":
    df = gather_network_data(devices)
    save_network_data(df)
    print(df)
