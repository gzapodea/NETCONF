# NETCONF

NETCONF sample code folder


 - Download the video file to play locally.
 - Code tested with 16.5.1b, CSR 1000v, and 16.5.1a Catalyst 3850
 - Change the HOST, PORT, USER, PASS to use with your lab.



FILES:


 - get_netconf_csr_info.py - sample code for CSR
 - get_netconf_3850_info.py - sample code for 3850
 - get_netconf_info.py - module to be used with netconf_info.py
 - netconf_info.py - sample code that will use the same function - get_netconf_info.py, to access both CSRs and 3850s
    - change the device access info in the file netconf_init.py
 - get_netconf_9300_info.py - the code will find out:
    - Internal switch temperature
    - outdoor temperature for the location of the switch
    - interfaces that are operational state "up"
    - post the above information on twitter
    - IP addresses (if configured) for the "up" interfaces

Device access:

 - IP address of your IOS-XE device: HOST 
 - Use the NETCONF port for your IOS-XE device:  PORT 
 - Use the user credentials for your IOS-XE device:
    - USER - your username
    - PASS - your password


The sample code will ask the user to select which device to collect information from.

The device information that will be collected (if available):
 - hostname
 - serial number
 - the list of all interfaces
 - interface names, configured IPv4 addresses, admin and operational state

