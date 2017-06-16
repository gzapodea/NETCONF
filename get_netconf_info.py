

# developed by Gabi Zapodeanu, TSA, GSS, Cisco Systems


# !/usr/bin/env python3


# import the ncclient library

from ncclient import manager
import sys
import xml.dom.minidom



# use the IP address or hostname of your CSR1000V device

HOST = '172.16.11.10'

# use the NETCONF port for your IOS-XE device

PORT = 830

# use the user credentials for your IOS-XE device

USER = 'cisco'
PASS = 'cisco'


def get_hostname():
    """
    This function will retrieve the hostname from config via NETCONF.
    """

    with manager.connect(host=HOST, port=PORT, username=USER,
                         password=PASS, hostkey_verify=False,
                         device_params={'name': 'default'},
                         allow_agent=False, look_for_keys=False) as m:

        # XML filter to issue with the get operation
        # IOS-XE 16.5+        YANG model called http://cisco.com/ns/yang/Cisco-IOS-XE-native
        hostname_filter = '''
                          <filter>
                              <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                                  <hostname></hostname>
                              </native>
                          </filter>
                          '''
        result = m.get_config('running', hostname_filter)
        xml_doc = xml.dom.minidom.parseString(result.xml)
        hostname = xml_doc.getElementsByTagName('hostname')
        return hostname[0].firstChild.nodeValue


def get_interfaces():
    """
    This function will return the interfaces info via NETCONF.
    """
    with manager.connect(host=HOST, port=PORT, username=USER,
                         password=PASS, hostkey_verify=False,
                         device_params={'name': 'default'},
                         allow_agent=False, look_for_keys=False) as m:
        # XML filter to issue with the get operation
        # IOS-XE 16.5+        YANG model called http://cisco.com/ns/yang/Cisco-IOS-XE-native

        interface_filter = '''
                            <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                                <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"/>
                                <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                                    <license>
                                        <udi>
                                            <sn/>
                                        </udi>
                                    </license>
                                </native>
                            </filter>
                            '''

        result = m.get_config('running', interface_filter)
        xml_doc = xml.dom.minidom.parseString(result.xml)
        interfaces = []
        interface_name = xml_doc.getElementsByTagName('name')
        number_int = len(interface_name)
        index = 0
        while index < number_int:
            interfaces.append(interface_name[index].firstChild.nodeValue)
            index += 1
        return interfaces


def get_interface_state(interface_list):
    """

    :param interface_list:
    :return:
    """


def get_sn():
    """
    This function will return the S/N of the network device using NETCONF
    """

    with manager.connect(host=HOST, port=PORT, username=USER,
                         password=PASS, hostkey_verify=False,
                         device_params={'name': 'default'},
                         allow_agent=False, look_for_keys=False) as m:

        # XML filter to issue with the get operation
        # IOS-XE 16.5+        YANG model called http://cisco.com/ns/yang/Cisco-IOS-XE-native

        sn_filter = '''
                    <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                          <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                                <license>
                                      <udi>
                                            <sn/>
                                      </udi>
                                </license>
                          </native>
                    </filter>
                    '''
        result = m.get_config('running', sn_filter)
        xml_doc = xml.dom.minidom.parseString(result.xml)
        serial_number = xml_doc.getElementsByTagName('sn')
        return serial_number[0].firstChild.nodeValue


def main():
    """
    This code will showcase how to get info about the network devices using NETCONF
    """

    print('\nThis simple code will use NETCONF to connect to a network device running 16.5.1\n')

    print('\nIP address or hostname of your CSR1000V device: HOST = "172.16.11.10",'
          '\nUse the NETCONF port for your IOS-XE device PORT = 830',
          '\nUse the user credentials for your IOS-XE device, username = "cisco", password = "cisco"')

    print('\nIt will collect information about the device hostname, S/N, and the interface names')

    # get the device hostname

    device_hostname = get_hostname()
    print('\nThe network device hostname is:', device_hostname)

    # get the device S/N

    device_sn = get_sn()
    print('\nThe network device S/N is:', device_sn)

    # get the device interfaces
    interfaces_list = get_interfaces()
    print('\nThe network device has these interfaces:')
    for intf in interfaces_list:
        print('    ', intf)

    print('\n\nEnd of application run')

if __name__ == '__main__':
    main()
