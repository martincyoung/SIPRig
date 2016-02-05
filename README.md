# SIPRig

SIPRig is a lightweight tool for sending a SIP message.

## Motivation

[SIPp](http://sipp.sourceforge.net) is a fantastic tool for generating SIP dialogs.  However there is a slight learning curve and setup overhead.

If you don't care for valid SIP dialog, or even valid SIP, then SIPRig is for you!  Construct your SIP message in an input file and send it to an unsuspecting address of your choosing.

## Limitations

SIPRig is written in python 2.7.  It works functionaly in python 3, however several `print` statements will need to be removed/updated.  This will be rectified in a future version.

## Example Usage

    $ cat message.txt 
    OPTIONS sip:192.168.1.1:8000 SIP/2.0
    Via: SIP/2.0/UDP 192.168.0.26:8000
    Max-Forwards: 70
    From: "Dummy" <sip:dummy@192.168.0.26>
    To: <sip:192.168.1.1:8000>
    Contact: <sip:dummy@192.168.0.26:8000>
    Call-ID: call-id@192.168.0.26
    CSeq: 1 OPTIONS
    Accept: application/sdp
    Content-Length: 0

    $ python siprig.py -f message.txt -d 192.168.1.1
    > SIP message sent successfully

## Full Usage

    $ python siprig.py -h
    Usage: siprig.py [OPTIONS]

    Options:
      -h, --help            show this help message and exit
      -f INPUT_FILE, --input_file=INPUT_FILE
                            *Required - Input file
      -d DEST_IP, --dest-ip=DEST_IP
                            *Required - Destination IP address.
      -p DEST_PORT, --dest-port=DEST_PORT
                            Destination port.  Defaults to 5060.
      -S SRC_IP, --src-ip=SRC_IP
                            Source IP address.
      -P SRC_PORT, --src-port=SRC_PORT
                            Source port.  Defaults to 5060.

## Installation

Download it using the 'Download ZIP' option in the top right, clone it, or just copy it right from the page.

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
