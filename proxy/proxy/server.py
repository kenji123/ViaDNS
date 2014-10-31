from portforward import ProxyFactory, ProxyServer, ProxyClientFactory, ProxyClient
from dpkt.ssl import TLSRecord, TLSHandshake, TLSClientHello

from db import MySQLHandler
from session import Session

class ProxyClient(ProxyClient):
    '''override'''
    def connectionMade(self):
        if self.peer.data != '':
            self.transport.write(self.peer.data)
            self.peer.data = ''
        
        super(ProxyClient, self).connectionMade()

class ProxyClientFactory(ProxyClientFactory):
    protocol = ProxyClient

class Client(object):
    
    def __init__(self, peer):
        self.ip = peer.host
        self.port = peer.port
        
        self.session = Session()
    
    def toString(self):
        return '%s:%d' % (self.ip, self.port)

class ProxyServer(ProxyServer):
    clientProtocolFactory = ProxyClientFactory
    
    data = ''
    sni = ''
    
    '''override'''
    def connectionMade(self):
        if not self.factory.dbHandler.isAlive(): self.factory.dbHandler.connect()
        
        self.model = Client(self.transport.getPeer())
        self.model.session.get(self.model.ip, self.factory.dbHandler)
        
        if not self.factory.isAuthenticated(self):
            self.transport.write(self.factory.getRedirect())
            self.transport.loseConnection()
            return
        
        if self.factory.port == 443:
            return
        
        super(ProxyServer, self).connectionMade()
    
    '''override'''
    def dataReceived(self, data):
        if self.factory.port != 443 or self.sni != '':
            super(ProxyServer, self).dataReceived(data)
            return
        
        if self.factory.port == 443 and self.sni == '':
            self.data += data
            sni = self.getSSLServerName(self.data)
            if sni != 'no_sni':
                self.sni = sni
                self.factory.host = self.sni
                super(ProxyServer, self).connectionMade()
    
    def getSSLServerName(self, data):
        sni = 'no_sni'
        try:
            tr = TLSRecord(data)
            th = TLSHandshake(str(tr.data))
            tch = TLSClientHello(str(th.data))
            server = tch.extensions[0].data[0]
            return server if len(server) > 2 else sni
        except:
            return sni

class ProxyFactory(ProxyFactory):
    protocol = ProxyServer
    
    '''override'''
    def __init__(self, host, port):
        super(ProxyFactory, self).__init__(host, port)
        
        self.dbHandler = MySQLHandler()
        self.dbHandler.connect()
    
    def isAuthenticated(self, client):
        found = False
        try:
            if client.model.session.isValid():
                found = True
                client.model.session.update(self.dbHandler)
        except:
            raise
        
        return found
    
    def getRedirect(self):
        return 'HTTP/1.1 302 Found\r\nLocation: http://www.kenshisoft.com/projects-resos/viadns/login\r\nCache-Control: no-cache\r\n\r\n'
