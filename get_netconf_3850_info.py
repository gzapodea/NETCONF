

# developed by Gabi Zapodeanu, TSA, GPO, Cisco Systems


# !/usr/bin/env python3


# import the ncclient library

import xml.dom.minidom

from ncclient import manager

# use the IP address or hostname of your 3850 device

HOST = '172.16.10.105'

# use the NETCONF port for your IOS-XE device

PORT = 830

# use the user credentials for your IOS-XE device

USER = 'gzapode'

PASS = 'Clive@17'


def get_hostname():
    """
    This function will retrieve the hostname from config via NETCONF.
    :return hostname: device hostname
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
        device_hostname = hostname[0].firstChild.nodeValue
    return device_hostname


def get_sn():
    """
    This function will return the S/N of the network device using NETCONF
    :return serial_number - device serial number

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
        try:
            result = m.get_config('running', sn_filter)
            xml_doc = xml.dom.minidom.parseString(result.xml)
            serial_number = xml_doc.getElementsByTagName('sn')
            device_sn = serial_number[0].firstChild.nodeValue
        except:
            device_sn = 'NA'
    return device_sn


def get_interfaces():
    """
    This function will return the interfaces info via NETCONF.
    :return interfaces: list of device interfaces
    """

    with manager.connect(host=HOST, port=PORT, username=USER,
                         password=PASS, hostkey_verify=False,
                         device_params={'name': 'default'},
                         allow_agent=False, look_for_keys=False) as m:
        # XML filter to issue with the get operation
        # IOS-XE 16.5+        YANG model called yang:http://cisco.com/ns/yang/Cisco-IOS-XE-native

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


def get_interface_state(interface):
    """
    This function will get the interface state for the specified interface via NETCONF
    :param interface: interface name
    :return interface admin and operational state
    """

    with manager.connect(host=HOST, port=PORT, username=USER,
                         password=PASS, hostkey_verify=False,
                         device_params={'name': 'default'},
                         allow_agent=False, look_for_keys=False) as m:
        # XML filter to issue with the get operation
        # IOS-XE 16.5+        YANG model called yang:ietf-interfaces

        interface_state_filter = '''
                                     <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                                          <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                                                <interface>
                                                        <name>''' + interface + '''</name>
                                                </interface>
                                          </interfaces-state>
                                     </filter>
                                '''

        try:
            result = m.get(interface_state_filter)
            xml_doc = xml.dom.minidom.parseString(result.xml)
            admin_state = xml_doc.getElementsByTagName('admin-status')
            int_admin_state = admin_state[0].firstChild.nodeValue
            oper_state = xml_doc.getElementsByTagName('oper-status')
            int_oper_state = oper_state[0].firstChild.nodeValue
        except:
            int_admin_state = 'NA'
            int_oper_state = 'NA'
    return int_admin_state, int_oper_state


def get_interface_ip(interface):
    """
    This function will retrieve the IPv4 address configured on the interface via NETCONF
    :param interface: interface name
    :return: int_ip_add: the interface IPv4 address
    """

    with manager.connect(host=HOST, port=PORT, username=USER,
                         password=PASS, hostkey_verify=False,
                         device_params={'name': 'default'},
                         allow_agent=False, look_for_keys=False) as m:
        # XML filter to issue with the get operation
        # IOS-XE 16.5+        YANG model called yang:ietf-interfaces

        interface_state_filter = '''
                                    <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                                        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                                            <interface>
                                                <name>''' + interface + '''</name>
                                            </interface>
                                        </interfaces>
                                        </filter>
                                '''
        result = m.get(interface_state_filter)
        xml_doc = xml.dom.minidom.parseString(result.xml)
        ip_add = xml_doc.getElementsByTagName('ip')
        try:
            int_ip_add = ip_add[0].firstChild.nodeValue
        except:
            int_ip_add = 'not configured'

        return int_ip_add


def main():
    """
    This code will showcase how to get info about the network devices using NETCONF
    """

    print('\nThis simple code will use NETCONF to connect to a network device running 16.5.1a\n')

    print('\nIP address or hostname of your 3850 device: HOST = "172.16.11.10"',
          '\nUse the NETCONF port for your IOS-XE device -  PORT = ', PORT,
          '\nUse the user credentials for your IOS-XE device -  username = ', USER, ' password = xxxxx')

    print('\nThe device information that will be collected (if available): ',
          '\n - hostname',
          '\n - serial number'
          '\n - the list of all interfaces',
          '\n - interface names, configured IPv4 addresses, admin and operational state')

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

    # get the admin, operational state and IPv4 address for each interface

    interface_info = []
    for intf in interfaces_list:
        admin_state = get_interface_state(intf)[0]
        oper_state = get_interface_state(intf)[1]
        ip_address = get_interface_ip(intf)
        interface_info.append({'interface': intf, 'ip address': ip_address, 'admin': admin_state, 'protocol': oper_state})

    # print interface info

    print('\nThe device interfaces info:\n')
    print(' {0:25} {1:20} {2:20} {3:20}'.format('Interface', 'IP Address', 'Admin-State', 'Oper-State'))
    for intf in interface_info:
        print(' {0:25} {1:20} {2:20} {3:20}'.format(intf['interface'], intf['ip address'], intf['admin'],
                                                    intf['protocol']))

    print('\n\nEnd of application run')

if __name__ == '__main__':
    main()
