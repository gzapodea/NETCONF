# NETCONF

NETCONF sample code folder


 - Download the video files to play locally.
 - Code tested with 16.5.1a, CSR 1000v.
 - Change the HOST, PORT, USER, PASS to use with your lab.



FILES:

 - get_netconf_info.py

Device access:
 - IP address or hostname of your CSR1000V device: HOST = "172.16.11.10"
 - Use the NETCONF port for your IOS-XE device -  PORT =  830 
 - Use the user credentials for your IOS-XE device - 
    - username =  cisco  
    - password =  cisco

The sample code will collect information about the device hostname and the S/N. 
The list of all interfaces will be printed.
Interface names, configured IPv4 addresses, admin and protocol state are displayed.

