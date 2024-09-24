# https://pypi.org/project/onvif2-zeep
# https://pypi.org/project/WSDiscovery/

from wsdiscovery.discovery import ThreadedWSDiscovery as WSDiscovery
from onvif2 import ONVIFCamera
from urllib.parse import urlparse
import os

# Function to discover ONVIF devices on the network
def discover_onvif_devices():
    # Initialize the WS-Discovery instance
    wsd = WSDiscovery()
    wsd.start()
    
    services = wsd.searchServices()
    print("Discovering ONVIF devices on the network...")
    
    # Stop WS-Discovery (since we don’t need to search further)
    wsd.stop()
    
    # If no services are found, return an empty list
    if not services:
        print("No ONVIF devices found on the network.")
        return []
    
    # Display the discovered devices
    devices = []
    for index, service in enumerate(services):
        xaddrs = service.getXAddrs()[0]  # Taking the first XAddr (most cases have one) this is a URL
        devices.append(xaddrs)
        print(f"{index + 1}: XAddr: {xaddrs}, Types: {service.getTypes()}")
    
    return devices

# Function to connect to an ONVIF device using its discovered IP
def connect_to_onvif_device(ip_address, port, username='admin', password='admin'):
    print(f"Connecting to ONVIF device at {ip_address}:{port}...")
    wsdl_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'wsdl')
    print(f"wsdl_dir: {wsdl_dir}")
    try:
        # Connect to the ONVIF camera
        camera = ONVIFCamera(ip_address, int(port), username, password, wsdl_dir)
        media_service = camera.create_media2_service()
        
        # Get and display the available profiles
        profiles = media_service.GetProfiles()
        for profile in profiles:
            print(f"Profile Name: {profile.Name}, Token: {profile.token}")
        print("Successfully connected to the ONVIF device.")
    except Exception as e:
        print(f"Failed to connect to ONVIF device at {ip_address}:{port}: {e}")

# Main function to discover and connect
def main():
    devices = discover_onvif_devices()

    if devices:
        # Prompt the user to select a device to connect to
        selected = int(input(f"Select a device to connect (1-{len(devices)}): ")) - 1
        
        if 0 <= selected < len(devices):
            xaddr = devices[selected]
            p = urlparse(xaddr)
            ip_address = p.hostname
            # Port should be 80 if scheme is http, 443 if https else use the port from the URL
            port = p.port if p.port else 80 if p.scheme == 'http' else 443 if p.scheme == 'https' else None
            username = input("Enter username (default: 'admin'): ") or 'admin'
            password = input("Enter password (default: 'admin'): ") or 'admin'
            
            print(f"ip: {ip_address}:{port}, username: {username}, password: {password}")
            connect_to_onvif_device(ip_address, port, username, password)
        else:
            print("Invalid selection.")
    else:
        print("No devices found to connect to.")

# Run the script
if __name__ == "__main__":
    main()
