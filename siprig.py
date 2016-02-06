#!/usr/bin/env python
import socket
from optparse import OptionParser


class SIPRigException(Exception):
    pass


class SIPRigRequestException(SIPRigException):
    pass


class SIPRigBlankLineException(SIPRigRequestException):
    pass


class Request():
    def __init__(self, input_file):
        self.bytes = self.get_req_from_file(input_file)
        self.validate()

    def get_req_from_file(self, input_file):
        file_handle = open(input_file, "rb")
        sip_bytes = file_handle.read()
        file_handle.close()

        return sip_bytes

    def validate(self):
        if (self.bytes[-2:] == '\n\n') or (self.bytes[-4:] == '\r\n\r\n'):
            return True
        else:
            raise SIPRigBlankLineException("File must end with 2 blank lines")


def get_socket(src_address, src_port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s.bind((src_address, src_port))
    s.settimeout(0.0)
    return s


def get_options():
    usage = "%prog [OPTIONS]"
    parser = OptionParser(usage=usage)
    parser.add_option('-f',
                      '--input_file',
                      dest='input_file',
                      type='string',
                      default=None,
                      help='*Required - Input file')
    parser.add_option('-d',
                      '--dest-ip',
                      dest='dest_ip',
                      type='string',
                      default=None,
                      help='*Required - Destination IP address.')
    parser.add_option('-p',
                      '--dest-port',
                      dest='dest_port',
                      type='int',
                      default=5060,
                      help='Destination port.  Defaults to 5060.')
    parser.add_option('-S',
                      '--src-ip',
                      dest='src_ip',
                      type='string',
                      default='',
                      help='Source IP address.')
    parser.add_option('-P',
                      '--src-port',
                      dest='src_port',
                      type='int',
                      default=0,
                      help='Source port.')

    (options, args) = parser.parse_args()

    if (options.input_file is None):
        print "No input file specified\n"
        parser.print_help()
        exit(-1)

    if (options.dest_ip is None):
        print "No destination IP specified\n"
        parser.print_help()
        exit(-1)

    return options


def main():
    options = get_options()

    try:
        sip_req = Request(options.input_file)
    except SIPRigRequestException, e:
        print "Error - could not load from file:\n    " + str(e)
        exit(-1)

    try:
        s = get_socket(options.src_ip, options.src_port)
    except Exception, e:
        print "Error - could not create socket:\n    " + str(e)
        exit(-1)

    try:
        s.sendto(sip_req.bytes, (options.dest_ip, options.dest_port))
    except Exception, e:
        print "Error - could not send packet.\n    " + str(e)
        exit(-1)

    print "SIP message sent successfully"

if __name__ == '__main__':
    main()
