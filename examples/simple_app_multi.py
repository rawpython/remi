import time

import remi.server as server

from simple_app import MyApp

s1 = server.Server(MyApp, start=True, port=8000, multiple_instance=True, userdata=('foo',))
s2 = server.Server(MyApp, start=True, port=9000, multiple_instance=True, userdata=('bar',))
s3 = server.Server(MyApp, start=True, port=0, multiple_instance=True, userdata=('baz',))

while 1:
    time.sleep(1)
