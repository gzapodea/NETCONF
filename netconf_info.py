

# developed by Gabi Zapodeanu, TSA, GSS, Cisco Systems


# !/usr/bin/env python3


# import the ncclient library

from ncclient import manager
import xml.dom.minidom
import json
import netconf_init
import get_netconf_info

from netconf_init import HOST_CSR, PORT_CSR, USER_CSR, PASS_CSR
from netconf_init import HOST_3850, PORT_3850, USER_3850, PASS_3850


def main():

    user_input = False
    while not user_input:
        print('\nSelect one option:\n\n1. CSR\n2. 3850\n3. Quit')
        user_input = input('\nEnter your selection: ')
        if user_input == '1':
            get_netconf_info.get_info(HOST_CSR, PORT_CSR, USER_CSR, PASS_CSR)
        elif user_input == '2':
            get_netconf_info.get_info(HOST_3850, PORT_3850, USER_3850, PASS_3850)
        elif user_input == '3':
            break
        user_input = False

    print('\nEnd of application run')

if __name__ == '__main__':
    main()
