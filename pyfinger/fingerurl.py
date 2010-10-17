import socket, urllib2, urlparse

class FingerHandler(urllib2.BaseHandler):
    def finger_open(self, req):
        host = req.get_host()
        try:
            host, port = host.split(":", 1)
            port = int(port)
        except ValueError:
            port = 79
        result = urlparse.urlsplit(req.get_full_url())
        path = result.path.lstrip("/")

        for res in socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            try:
                s = socket.socket(af, socktype, proto)
            except socket.error, msg:
                s = None
                continue
            try:
                s.connect(sa)
            except socket.error, msg:
                s.close()
                s = None
                continue
            break
        if s is None:
            raise

        s.send("%s\r\n" % path)

        class sock(object):
            def read(self, bufsize=None):
                if bufsize is None:
                    while True:
                        data = ""
                        bytes = s.recv(4096)
                        data += bytes
                        if len(data) < 4096:
                            break
                    return data
                else:
                    return s.recv(bufsize)
            def close(self):
                s.close()
            def info(self):
                return {"content-type": "text/plain"}

        return sock()

urllib2._opener = urllib2.build_opener(FingerHandler)
