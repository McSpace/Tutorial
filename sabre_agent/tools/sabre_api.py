#!/usr/bin/env python3
"""
Sabre Red 360 SOAP API Client
Provides authentication and command execution for Sabre Red 360 terminal commands
"""

import requests
import sys
import json
from datetime import datetime
from xml.etree import ElementTree as ET

class SabreAPIClient:
    """Client for Sabre SOAP API interactions"""

    def __init__(self, username, password, pcc, environment='cert'):
        """
        Initialize Sabre API client

        Args:
            username: Sabre API username
            password: Sabre API password
            pcc: Pseudo City Code (Office ID)
            environment: 'cert' for testing, 'prod' for production
        """
        self.username = username
        self.password = password
        self.pcc = pcc
        self.environment = environment

        if environment == 'cert':
            self.base_url = "https://webservices.cert.platform.sabre.com"
        else:
            self.base_url = "https://webservices.platform.sabre.com"

        self.security_token = None
        self.conversation_id = None
        self.session_created = False

    def create_session(self):
        """
        Create a new Sabre API session

        Returns:
            bool: True if session created successfully, False otherwise
        """
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

        # SessionCreateRQ SOAP envelope
        soap_envelope = f"""<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
                   xmlns:eb="http://www.ebxml.org/namespaces/messageHeader"
                   xmlns:xlink="http://www.w3.org/1999/xlink"
                   xmlns:xsd="http://www.w3.org/1999/XMLSchema">
    <SOAP-ENV:Header>
        <eb:MessageHeader SOAP-ENV:mustUnderstand="1" eb:version="1.0">
            <eb:From>
                <eb:PartyId eb:type="urn:x12.org:IO5:01">Agency</eb:PartyId>
            </eb:From>
            <eb:To>
                <eb:PartyId eb:type="urn:x12.org:IO5:01">Sabre</eb:PartyId>
            </eb:To>
            <eb:CPAId>{self.pcc}</eb:CPAId>
            <eb:ConversationId>SabreSession</eb:ConversationId>
            <eb:Service eb:type="OTA">SessionCreateRQ</eb:Service>
            <eb:Action>SessionCreateRQ</eb:Action>
            <eb:MessageData>
                <eb:MessageId>mid:123456@sabre.com</eb:MessageId>
                <eb:Timestamp>{timestamp}</eb:Timestamp>
            </eb:MessageData>
        </eb:MessageHeader>
        <wsse:Security xmlns:wsse="http://schemas.xmlsoap.org/ws/2002/12/secext"
                       xmlns:wsu="http://schemas.xmlsoap.org/ws/2002/12/utility"
                       SOAP-ENV:mustUnderstand="1">
            <wsse:UsernameToken>
                <wsse:Username>{self.username}</wsse:Username>
                <wsse:Password>{self.password}</wsse:Password>
                <Organization>{self.pcc}</Organization>
                <Domain>DEFAULT</Domain>
            </wsse:UsernameToken>
        </wsse:Security>
    </SOAP-ENV:Header>
    <SOAP-ENV:Body>
        <SessionCreateRQ xmlns="http://www.opentravel.org/OTA/2002/11">
            <POS>
                <Source PseudoCityCode="{self.pcc}"/>
            </POS>
        </SessionCreateRQ>
    </SOAP-ENV:Body>
</SOAP-ENV:Envelope>"""

        headers = {
            'Content-Type': 'text/xml; charset=utf-8',
            'SOAPAction': 'SessionCreateRQ'
        }

        try:
            response = requests.post(self.base_url, data=soap_envelope, headers=headers)

            if response.status_code == 200:
                # Parse response to extract security token
                root = ET.fromstring(response.content)

                # Find BinarySecurityToken
                ns = {
                    'wsse': 'http://schemas.xmlsoap.org/ws/2002/12/secext',
                    'eb': 'http://www.ebxml.org/namespaces/messageHeader'
                }

                token_elem = root.find('.//wsse:BinarySecurityToken', ns)
                conv_id_elem = root.find('.//eb:ConversationId', ns)

                if token_elem is not None:
                    self.security_token = token_elem.text
                    self.conversation_id = conv_id_elem.text if conv_id_elem is not None else 'SabreSession'
                    self.session_created = True
                    return True
                else:
                    print(f"Error: Could not extract security token from response")
                    print(f"Response: {response.text}")
                    return False
            else:
                print(f"Error creating session: HTTP {response.status_code}")
                print(f"Response: {response.text}")
                return False

        except Exception as e:
            print(f"Exception during session creation: {str(e)}")
            return False

    def execute_command(self, command):
        """
        Execute a Sabre terminal command

        Args:
            command: Sabre terminal command string (e.g., "101JUNNYCDFW")

        Returns:
            dict: Response containing 'success', 'response_text', and 'raw_response'
        """
        if not self.session_created:
            if not self.create_session():
                return {
                    'success': False,
                    'error': 'Failed to create session',
                    'response_text': None,
                    'raw_response': None
                }

        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

        # SabreCommandLLSRQ SOAP envelope
        soap_envelope = f"""<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
                   xmlns:eb="http://www.ebxml.org/namespaces/messageHeader"
                   xmlns:xlink="http://www.w3.org/1999/xlink"
                   xmlns:xsd="http://www.w3.org/1999/XMLSchema">
    <SOAP-ENV:Header>
        <eb:MessageHeader SOAP-ENV:mustUnderstand="1" eb:version="1.0">
            <eb:From>
                <eb:PartyId eb:type="urn:x12.org:IO5:01">Agency</eb:PartyId>
            </eb:From>
            <eb:To>
                <eb:PartyId eb:type="urn:x12.org:IO5:01">Sabre</eb:PartyId>
            </eb:To>
            <eb:CPAId>{self.pcc}</eb:CPAId>
            <eb:ConversationId>{self.conversation_id}</eb:ConversationId>
            <eb:Service eb:type="OTA">SabreCommandLLSRQ</eb:Service>
            <eb:Action>SabreCommandLLSRQ</eb:Action>
            <eb:MessageData>
                <eb:MessageId>mid:command@sabre.com</eb:MessageId>
                <eb:Timestamp>{timestamp}</eb:Timestamp>
            </eb:MessageData>
        </eb:MessageHeader>
        <wsse:Security xmlns:wsse="http://schemas.xmlsoap.org/ws/2002/12/secext"
                       xmlns:wsu="http://schemas.xmlsoap.org/ws/2002/12/utility"
                       SOAP-ENV:mustUnderstand="1">
            <wsse:BinarySecurityToken>{self.security_token}</wsse:BinarySecurityToken>
        </wsse:Security>
    </SOAP-ENV:Header>
    <SOAP-ENV:Body>
        <SabreCommandLLSRQ xmlns="http://webservices.sabre.com/sabreXML/2003/07"
                           Version="2.0.0">
            <Request Output="SCREEN" CDATA="true">
                <HostCommand>{command}</HostCommand>
            </Request>
        </SabreCommandLLSRQ>
    </SOAP-ENV:Body>
</SOAP-ENV:Envelope>"""

        headers = {
            'Content-Type': 'text/xml; charset=utf-8',
            'SOAPAction': 'SabreCommandLLSRQ'
        }

        try:
            response = requests.post(self.base_url, data=soap_envelope, headers=headers)

            if response.status_code == 200:
                # Parse response
                root = ET.fromstring(response.content)

                # Find Response element
                ns = {'ns': 'http://webservices.sabre.com/sabreXML/2003/07'}
                response_elem = root.find('.//ns:Response', ns)

                if response_elem is not None:
                    response_text = response_elem.text if response_elem.text else ""
                    return {
                        'success': True,
                        'response_text': response_text,
                        'raw_response': response.text,
                        'command': command
                    }
                else:
                    return {
                        'success': False,
                        'error': 'Could not parse response',
                        'response_text': None,
                        'raw_response': response.text,
                        'command': command
                    }
            else:
                return {
                    'success': False,
                    'error': f'HTTP {response.status_code}',
                    'response_text': None,
                    'raw_response': response.text,
                    'command': command
                }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'response_text': None,
                'raw_response': None,
                'command': command
            }

    def close_session(self):
        """Close the current Sabre API session"""
        if not self.session_created:
            return True

        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

        # SessionCloseRQ SOAP envelope
        soap_envelope = f"""<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
                   xmlns:eb="http://www.ebxml.org/namespaces/messageHeader"
                   xmlns:xlink="http://www.w3.org/1999/xlink"
                   xmlns:xsd="http://www.w3.org/1999/XMLSchema">
    <SOAP-ENV:Header>
        <eb:MessageHeader SOAP-ENV:mustUnderstand="1" eb:version="1.0">
            <eb:From>
                <eb:PartyId eb:type="urn:x12.org:IO5:01">Agency</eb:PartyId>
            </eb:From>
            <eb:To>
                <eb:PartyId eb:type="urn:x12.org:IO5:01">Sabre</eb:PartyId>
            </eb:To>
            <eb:CPAId>{self.pcc}</eb:CPAId>
            <eb:ConversationId>{self.conversation_id}</eb:ConversationId>
            <eb:Service eb:type="OTA">SessionCloseRQ</eb:Service>
            <eb:Action>SessionCloseRQ</eb:Action>
            <eb:MessageData>
                <eb:MessageId>mid:close@sabre.com</eb:MessageId>
                <eb:Timestamp>{timestamp}</eb:Timestamp>
            </eb:MessageData>
        </eb:MessageHeader>
        <wsse:Security xmlns:wsse="http://schemas.xmlsoap.org/ws/2002/12/secext"
                       xmlns:wsu="http://schemas.xmlsoap.org/ws/2002/12/utility"
                       SOAP-ENV:mustUnderstand="1">
            <wsse:BinarySecurityToken>{self.security_token}</wsse:BinarySecurityToken>
        </wsse:Security>
    </SOAP-ENV:Header>
    <SOAP-ENV:Body>
        <SessionCloseRQ xmlns="http://www.opentravel.org/OTA/2002/11"/>
    </SOAP-ENV:Body>
</SOAP-ENV:Envelope>"""

        headers = {
            'Content-Type': 'text/xml; charset=utf-8',
            'SOAPAction': 'SessionCloseRQ'
        }

        try:
            response = requests.post(self.base_url, data=soap_envelope, headers=headers)
            self.session_created = False
            return response.status_code == 200
        except:
            return False


def main():
    """CLI interface for Sabre API client"""
    if len(sys.argv) < 2:
        print("Usage: python sabre_api.py <command> [--json]")
        print("Example: python sabre_api.py '101JUNNYCDFW'")
        print("Example: python sabre_api.py '101JUNNYCDFW¥AA' --json")
        sys.exit(1)

    command = sys.argv[1]
    output_json = '--json' in sys.argv

    # Load credentials from environment or use defaults
    username = "302596"
    password = "lon23don"
    pcc = "U3VL"

    client = SabreAPIClient(username, password, pcc, environment='cert')

    # Execute command
    result = client.execute_command(command)

    if output_json:
        print(json.dumps(result, indent=2))
    else:
        if result['success']:
            print(f"Command: {result['command']}")
            print(f"\nResponse:\n{result['response_text']}")
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
            if result.get('raw_response'):
                print(f"\nRaw response:\n{result['raw_response']}")

    # Close session
    client.close_session()


if __name__ == '__main__':
    main()
