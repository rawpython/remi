try:
    # Python 2.x
    import BaseHTTPServer as server
    from StringIO import StringIO as IO
except ImportError:
    # Python 3.x
    from http import server
    from io import BytesIO as IO


class MockRequest(object):
    def makefile(self, *args, **kwargs):
        return IO(b"GET / HTTP/1.0")

    def getsockname(self):
    	return '/'

    def sendall(self):
        pass


class MockServer(object):
    def __init__(self):
    	self.auth = None
    	self.multiple_instance = None
    	self.update_interval = 0
    	self.title = None
    	self.server_address = ('0.0.0.0', 8888)
    	self.websocket_timeout_timer_ms = None
    	self.pending_messages_queue_length = None
    	self.userdata = {}