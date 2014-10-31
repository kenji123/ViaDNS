#!/usr/bin/python

import sys

from twisted.internet import reactor

from server import ProxyFactory

if __name__ == '__main__':
    sys.stdout = file('/var/log/viadns/stdout.log', 'a')
    sys.stderr = file('/var/log/viadns/stderr.log', 'a')
    
    proxies = [
                # listen on port 80 on all interfaces and forward to Squid listening on 3128
               [80, ProxyFactory('127.0.0.1', 3128), ''],

               # listen on port 443 on all interfaces and forward to 'signup.netflix.com' on port 443 if SNI fails
               [443, ProxyFactory('signup.netflix.com', 443), '']

               # configure individual interfaces for different hostnames in case SNI fails or is not supported by the client
               #[443, ProxyFactory('secure.hulu.com', 443), '10.0.0.11'],
               #[443, ProxyFactory('play.hulu.com', 443), '10.0.0.12'],
               #[443, ProxyFactory('www.pandora.com', 443), '10.0.0.13'],
               #[443, ProxyFactory('tuner.pandora.com', 443), '10.0.0.14']
               ]
    
    for p in proxies:
        reactor.listenTCP(p[0], p[1], interface=p[2])
    
    reactor.run()
