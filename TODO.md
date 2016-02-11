## TODO

- EASY.  Add warning if validation is disabled and the input does not end in two blank lines.
- EASY.  Add a suite of example SIP messages.
- EASY.  Refactor and improve argument validation.
- MEDIUM.  Automatically populate SIP values based on destination and source values.
- MEDIUM.  Some tests would be nice...
- MEDIUM.  Automatically calculate the Content-Length header.
- DOCUMENTATION.  Full functional description.

#### Rejected Ideas

- Vaildate the input is valid SIP.

  SIPRig is not intended to be a SIP message validator, but rather a tool to send SIP, valid or not.  If you're not sure that you have a valid SIP message then it is recommended to use one of the many excellent SIP parsers available.

  An exception to this rule is the Content-Length header.  It is very easy to get this wrong unintentionally when manually editing the body of a SIP message.

- Populate a set of default headers if they're not specified in the input.

  As above.  Missing headers are crucial test cases, so it makes sense for SIPRig to defer control of this to the user.
