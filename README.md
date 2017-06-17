# NETCONF

NETCONF sample code folder


 - Download the video files to play locally.
 - Code tested with 16.5.1a, CSR 1000v.
 - Change the HOST, PORT, USER, PASS to use with your lab.



FILES:


 - get_netconf_csr_info.py - sample code for CSR
 - get_netconf_3850_info.py - sample code for 3850
 - get_netconf_info.py - module to be used with netconf_info.py
 - netconf_info.py - sample code that will use the same function - get_netconf_info.py, to access both CSRs and 3850s
    - change the device access info in the file netconf_init.py


Device access:
 - IP address or hostname of your IOS-XE device: HOST 
 - Use the NETCONF port for your IOS-XE device:  PORT 
 - Use the user credentials for your IOS-XE device:
    - username: USER  
    - password: PASS


The sample code will ask user to select which device to collect information from.
This device information will be collected (if available):
 - hostname
 - the list of all interfaces
 - interface names, configured IPv4 addresses, admin and operational state

