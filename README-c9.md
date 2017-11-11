## Modifictions for cloud9

Cloud9 is web IDE system that can proxy web & websockets connections
to applications. Because of the proxying, the base REMI system does
not work -- for example, the original REMI code uses the IP address of
the server to configure the JavaScript code to specify the host that
the WS should connect to. In C9, this is the internal (non-routed) IP
address. Thus, a number of small changes are made to make the code work
better in C9.

Another change has to do with the key exchange in WS. For reasons not
completely clear to me, the C9 proxy appears to lower-case the HTTP
response received by the server. This causes the base REMI code to
fail, so I added a specific for extracting the WS key when the lower
can version on C9.

To install on C9, use `sudo pip install git+https://github.com/dirkcgrunwald/remi.git@c9`

You should then be able to run any of the examples.
