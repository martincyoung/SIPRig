# SIPRig

SIPRig is a lightweight tool for sending a SIP message.

## Motivation

[SIPp](http://sipp.sourceforge.net) is a fantastic tool for generating SIP dialogs.  However there is a slight learning curve and setup overhead.

If you don't care for valid SIP dialog, or even valid SIP, then SIPRig is for you!  Construct your SIP message in an input file and send it anywhere.

## Limitations

SIPRig works under both python 2.7 and python 3.

## Example Usage

    $ cat message.txt 
    OPTIONS sip:sip.iptel.org SIP/2.0
    Via: SIP/2.0/UDP 192.168.0.26:55220
    Max-Forwards: 70
    From: "Test" <sip:test@192.168.0.26>;tag=98765
    To: <sip:sip.iptel.org>
    Contact: <sip:dummy@192.168.0.26:55220>
    Call-ID: 1234567@192.168.0.26
    CSeq: 1 OPTIONS
    Accept: application/sdp
    Content-Length: 0

    $ python siprig.py -f message.txt -d sip.iptel.org -p 5060 -P 55220 -v

    Request sent to sip.iptel.org:5060

    OPTIONS sip:sip.iptel.org SIP/2.0
    Via: SIP/2.0/UDP 192.168.0.26:55220
    Max-Forwards: 70
    From: "Test" <sip:test@192.168.0.26>;tag=98765
    To: <sip:sip.iptel.org>
    Contact: <sip:dummy@192.168.0.26:55220>
    Call-ID: 1234567@192.168.0.26
    CSeq: 1 OPTIONS
    Accept: application/sdp
    Content-Length: 0


    Response from sip.iptel.org:5060

    SIP/2.0 200 OK
    Via: SIP/2.0/UDP 192.168.0.26:55220
    From: "Test" <sip:test@192.168.0.26>;tag=98765
    To: <sip:sip.iptel.org>;tag=0D4E4EA6-56B7B180000D950B-55778700
    Call-ID: 1234567@192.168.0.26
    CSeq: 1 OPTIONS
    Accept: */*
    Accept-Language: en
    Server: ser (3.3.0-pre1 (i386/linux))
    Contact: <sip:0D4E4EA6-56B7B180000D950B-55778700@212.79.111.155;transport=udp>
    Content-Length: 0

## Full Usage

    $ python siprig.py -h
    usage: siprig.py [-h] -f INPUT_FILE -d DEST_ADDR [-p DEST_PORT] [-S SRC_IP]
                     [-P SRC_PORT] [-q] [-v] [--tcp] [--udp] [--timeout TIMEOUT]
                     [--no-validation]

    optional arguments:
      -h, --help            show this help message and exit
      -f INPUT_FILE, --input_file INPUT_FILE
                            *Required - Input file
      -d DEST_ADDR, --dest-ip DEST_ADDR
                            *Required - Destination address. IP or FQDN.
      -p DEST_PORT, --dest-port DEST_PORT
                            Destination port. Default 5060.
      -S SRC_IP, --src-ip SRC_IP
                            Source IP address.
      -P SRC_PORT, --src-port SRC_PORT
                            Source port.
      -q, --quiet           Suppress all output.
      -v, --verbose         Show request and response in stdout.
      --tcp                 Force TCP protocol.
      --udp                 Force UDP protocol.
      --timeout TIMEOUT     Seconds to wait for a response. Default 1s.
      --no-validation       Disable line ending validation.

## Installation

    $ git clone git://github.com/martincyoung/SIPRig

## License

The MIT License (MIT)

Copyright (c) 2016 Martin Craig Young

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
