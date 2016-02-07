#!/usr/bin/env python
import socket
from argparse import ArgumentParser


class Request():
    def __init__(self, input_file, validate):
        self.bytes = self.get_req_from_file(input_file)
        if validate:
            self.validate()

    def get_req_from_file(self, input_file):
        # Read the input file as a byte array, and convert to Unix line
        # endings if required.
        file_handle = open(input_file, "rbU")
        sip_bytes = file_handle.read()
        file_handle.close()

        return sip_bytes

    def validate(self):
        self.add_blank_lines()

    def add_blank_lines(self):
        while (self.bytes[-2:] != '\n\n'.encode()):
            self.bytes += '\n'.encode()


def get_socket(src_address, src_port, timeout):
    # Create an IPv4 UDP socket.  If no source address or source port is
    # provided, the socket module assigns this automatically.
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s.bind((src_address, src_port))
    s.settimeout(timeout)
    return s


def get_args():
    parser = ArgumentParser()
    parser.add_argument('-f',
                        '--input_file',
                        dest='input_file',
                        default=None,
                        help='*Required - Input file',
                        required=True)
    parser.add_argument('-d',
                        '--dest-ip',
                        dest='dest_addr',
                        default=None,
                        help='*Required - Destination address.  IP or FQDN.',
                        required=True)
    parser.add_argument('-p',
                        '--dest-port',
                        dest='dest_port',
                        type=int,
                        default=5060,
                        help='Destination port.  Default 5060.')
    parser.add_argument('-S',
                        '--src-ip',
                        dest='src_ip',
                        default='',
                        help='Source IP address.')
    parser.add_argument('-P',
                        '--src-port',
                        dest='src_port',
                        type=int,
                        default=0,
                        help='Source port.')
    parser.add_argument('--timeout',
                        dest='timeout',
                        type=float,
                        default=1.0,
                        help='Seconds to wait for a response.  Default 1s.')
    parser.add_argument('--no-validation',
                        dest='validate_request',
                        action='store_false',
                        default=True,
                        help='Disable line ending validation.')

    args = parser.parse_args()

    return args


def main():
    args = get_args()

    try:
        request = Request(args.input_file, args.validate_request)

        s = get_socket(args.src_ip, args.src_port, args.timeout)
        s.sendto(request.bytes, (args.dest_addr, args.dest_port))

        print("\nRequest sent to %s:%d:\n" % (args.dest_addr, args.dest_port))
        print(request.bytes.decode())

        response = s.recv(65535)

        print("Response from %s:%d:\n" % (args.dest_addr, args.dest_port))
        print(response.decode())

    except socket.timeout:
        print('No response received within %0.1f seconds' % args.timeout)

    except socket.error as e:
        print("Error - could not create socket:\n    " + str(e))
        exit(-1)

    except Exception as e:
        print("Error:\n    " + str(e))
        exit(-1)

    finally:
        try:
            s.close()
        except UnboundLocalError:
            # Socket has not been assigned.
            pass

if __name__ == '__main__':
    main()
