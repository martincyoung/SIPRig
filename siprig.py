#!/usr/bin/env python
import re
import socket
import sys
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

    def protocol(self):
        pattern = re.compile(b"Via: SIP/2.0/(UDP|TCP)")
        try:
            return pattern.search(self.bytes).group(1).lower().decode()
        except AttributeError:
            # The regex didn't match anything in the source file.  Default to
            # UDP.
            return "udp"


class Arguments():
    def __init__(self):
        self.parser = ArgumentParser()
        self.add_arguments()
        self.parse_args()
        self.validate()

    def parse_args(self):
        # Parse the supplied arguments and map each one to an attribute on
        # the Argument object.
        for k, v in self.parser.parse_args().__dict__.items():
            setattr(self, k, v)

    def validate(self):
        if self.tcp and self.udp:
            sys.stderr.write("Please specify only one of TCP or UDP\n")
            exit(-1)

    def add_arguments(self):
        self.parser.add_argument('-f',
                                 '--input_file',
                                 dest='input_file',
                                 default=None,
                                 help='*Required - Input file',
                                 required=True)
        self.parser.add_argument('-d',
                                 '--dest-ip',
                                 dest='dest_addr',
                                 default=None,
                                 help='*Required - Destination address.  IP or FQDN.',
                                 required=True)
        self.parser.add_argument('-p',
                                 '--dest-port',
                                 dest='dest_port',
                                 type=int,
                                 default=5060,
                                 help='Destination port.  Default 5060.')
        self.parser.add_argument('-S',
                                 '--src-ip',
                                 dest='src_ip',
                                 default='',
                                 help='Source IP address.')
        self.parser.add_argument('-P',
                                 '--src-port',
                                 dest='src_port',
                                 type=int,
                                 default=0,
                                 help='Source port.')
        self.parser.add_argument('-q',
                                 '--quiet',
                                 dest='quiet',
                                 action='store_true',
                                 default=False,
                                 help='Suppress all output.')
        self.parser.add_argument('-v',
                                 '--verbose',
                                 dest='verbose',
                                 action='store_true',
                                 default=False,
                                 help='Show request and response in stdout.')
        self.parser.add_argument('--tcp',
                                 dest='tcp',
                                 action='store_true',
                                 default=False,
                                 help='Force TCP protocol.')
        self.parser.add_argument('--udp',
                                 dest='udp',
                                 action='store_true',
                                 default=False,
                                 help='Force UDP protocol.')
        self.parser.add_argument('--timeout',
                                 dest='timeout',
                                 type=float,
                                 default=1.0,
                                 help='Seconds to wait for a response.  Default 1s.')
        self.parser.add_argument('--no-validation',
                                 dest='validate_request',
                                 action='store_false',
                                 default=True,
                                 help='Disable line ending validation.')

def get_socket(src_address, src_port, timeout, protocol):
    if protocol == "tcp":
        # Create an IPv4 TCP socket.  Set REUSEADDR so that the port can be
        # reused without waiting for the TIME_WAIT state to pass.
        s = socket.socket(socket.AF_INET,
                          socket.SOCK_STREAM,
                          socket.IPPROTO_TCP)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    else:
        # Create an IPv4 UDP socket.
        s = socket.socket(socket.AF_INET,
                          socket.SOCK_DGRAM,
                          socket.IPPROTO_UDP)

    # If no source address or source port is provided, the socket module
    # assigns this automatically.
    s.bind((src_address, src_port))
    s.settimeout(timeout)
    return s


def main():
    args = Arguments()

    try:
        request = Request(args.input_file, args.validate_request)

        protocol = "udp"

        if not args.tcp and not args.udp:
            protocol = request.protocol()
        elif args.tcp:
            protocol = "tcp"

        s = get_socket(args.src_ip, args.src_port, args.timeout, protocol)
        s.connect((args.dest_addr, args.dest_port))
        s.send(request.bytes)

        if not args.quiet:
            sys.stdout.write("\nRequest sent to %s:%d\n\n" %
                             (args.dest_addr, args.dest_port))
            if args.verbose:
                sys.stdout.write(request.bytes.decode() + "\n")

        response = s.recv(65535)

        if not args.quiet:
            sys.stdout.write("Response from %s:%d\n\n" %
                             (args.dest_addr, args.dest_port))
            if args.verbose:
                sys.stdout.write(response.decode() + "\n")

    except socket.timeout:
        if not args.quiet:
            sys.stdout.write("No response received within %0.1f seconds\n" %
                             args.timeout)

    finally:
        try:
            s.shutdown(1)
            s.close()
        except UnboundLocalError:
            # Socket has not been assigned.
            pass

if __name__ == '__main__':
    main()
