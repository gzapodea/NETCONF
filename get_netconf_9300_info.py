# developed by Gabi Zapodeanu, TSA, GPO, Cisco Systems

# !/usr/bin/env python3


import requests
import xml.dom.minidom
import lxml.etree as ET
from twython import Twython

from ncclient import manager
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from twitter_init import APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # Disable insecure https warnings

# use the IP address or hostname of your 9300 switch

HOST = '10.93.130.41'

# use the NETCONF port for your 9300 switch

PORT = 830

# use the user credentials for your 9300 switch

USER = 'cisco'
PASS = 'cisco'


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


def get_up_interfaces():
    """
    This function will return the interfaces that are operational state up, via NETCONF.
    :return interfaces: list of device interfaces
    """

    with manager.connect(host=HOST, port=PORT, username=USER,
                         password=PASS, hostkey_verify=False,
                         device_params={'name': 'default'},
                         allow_agent=False, look_for_keys=False) as m:
        # XML filter to issue with the get operation
        # IOS-XE 16.5+        YANG model called yang:http://cisco.com/ns/yang/Cisco-IOS-XE-native

        interface_up_filter = '''
                            <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                                <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                                    <interface>
                                        <oper-status>up</oper-status>
                                    </interface>
                                </interfaces-state>
                            </filter>
                           '''

        result = m.get(interface_up_filter)

        xml_doc = xml.dom.minidom.parseString(result.xml)
        # data = ET.fromstring(xml_doc)
        interfaces = []
        interface_name = xml_doc.getElementsByTagName('name')
        number_int = len(interface_name)
        index = 0
        while index < number_int:
            interfaces.append(interface_name[index].firstChild.nodeValue)
            index += 1
    return interfaces


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
                                                <name> ''' + interface + '''</name>
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


def get_temperature(sensor_number):
    """
    This function will get the temperature for the sensor with the {sensor_number}
    :param sensor_number: switch sensor number
    :return: temperature in Celsius degrees
    """
    with manager.connect(host=HOST, port=PORT, username=USER,
                         password=PASS, hostkey_verify=False,
                         device_params={'name': 'default'},
                         allow_agent=False, look_for_keys=False) as m:
        # XML filter to issue with the get operation
        # IOS-XE 16.6+        YANG model called "http://cisco.com/ns/yang/Cisco-IOS-XE-environment-oper"
        sensor_filter = '''
                        <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                            <environment-sensors xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-environment-oper">
                                <environment-sensor>
                                    <name>''' + sensor_number + ''' </name>
                                </environment-sensor>
                            </environment-sensors>
                        </filter>
                        '''
        result = m.get(sensor_filter)
        xml_doc = xml.dom.minidom.parseString(result.xml)
        temp = xml_doc.getElementsByTagName('current-reading')
        temperature = temp[0].firstChild.nodeValue
        status = xml_doc.getElementsByTagName('state')
        state = status[0].firstChild.nodeValue
    return temperature, state


def get_outside_temperature():
    """
    This function will collect the outside temperature for the office located at the GPS coordinates {x,y}
    :return: current temperature
    """
    url = "https://api.weather.gov/points/45.4176,-122.7331/forecast/hourly"
    header = {'accept': 'application/ld+json'}
    response = requests.get(url, headers=header, verify=False)
    outside_temp_json = response.json()
    outside_temp = int(((outside_temp_json["periods"][0]["temperature"]) - 32) / 1.8)
    return outside_temp


def main():
    """
    This code will showcase how to get info about the network devices using NETCONF
    """

    print('\nThis simple code will use NETCONF to connect to a network device running 16.6.1\n')

    print('\nIP address or hostname of your Catalyst 9300 switch: HOST = "172.16.11.10"',
          '\nUse the NETCONF port -  PORT = ', PORT,
          '\nUse the user credentials -  username = ', USER, ' password = xxxxx')

    print('\nThe device information that will be collected (if available): ',
          '\n - hostname',
          '\n - the list of all interfaces operational state up',
          '\n - interface names, configured IPv4 addresses',
          '\n - switch temperature and outside temperature (from weather.gov)')

    # get the outside temp
    outside_temperature = get_outside_temperature()
    print('\nLake Oswego, OR, Temperature is : ', outside_temperature, ' Celsius')

    # get the device hostname

    device_hostname = get_hostname()
    print('\nThe network device hostname is:', device_hostname)

    # get temperature state

    temp = get_temperature("Temp Sensor 2")[0]
    state = get_temperature("Temp Sensor 2")[1]
    print('\nSwitch Temperature: ', temp, ' Celsius')
    print('\nSwitch Temperature: ', state)

    # tweet the temperature info, see https://github.com/ryanmcgrath/twython for documentation
    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    twitter_temp = 'Lake Oswego, OR, Outside Temp (in Celsius): ' + str(outside_temperature) + ', Cat 9K Switch Temp (in Degrees): ' + str(temp) + ', Cat 9K Switch Temp state: ' + state
    try:
        twitter.update_status(status=twitter_temp)
    except:
        pass
    print('\nTwitter temp status update')

    # get the device interfaces operational state up

    interfaces_up_list = get_up_interfaces()
    print('\nThe network device has these interfaces in a operational state "up" :')
    twitter_intf_up = "Cat 9k Switch Intf up: "
    for intf in interfaces_up_list:
        print('', intf)
        twitter_intf_up += intf + ", "

    # twitter intf up message
    try:
        twitter.update_status(status=twitter_intf_up)
    except:
        pass
    print('\nTwitter temp status update')
    print(twitter_intf_up)

    # get the admin, operational state and IPv4 address for each interface

    interface_info = []
    for intf in interfaces_up_list:
        ip_address = get_interface_ip(intf)
        interface_info.append({'interface': intf, 'ip address': ip_address})

    # print interface info

    print('\nThe network device "up" interfaces info:\n')
    print(' {0:25} {1:20} '.format('Interface', 'IP Address'))
    for intf in interface_info:
        print(' {0:25} {1:20} '.format(intf['interface'], intf['ip address']))

    print('\n\nEnd of application run')


if __name__ == '__main__':
    main()
