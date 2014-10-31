# ViaDNS
A proxy server that also acts as an authorization gateway for HTTP and TLS requests redirected by a DNS server. It works as a selective proxy by only forwarding traffic that originates from authenticated and authorized IP addresses.

## Components
 * [Web App](https://github.com/kenji123/viadns/tree/master/viadns): Provides end user authentication and account management.
 * [Proxy](https://github.com/kenji123/viadns/tree/master/proxy): Checks authorization of incoming requests before forwarding them. For TLS requests, the destination hostname is extracted from the SNI extension then forwareded. For HTTP, requests are forwarded to another defined proxy server.

## Dependencies
 * A DNS server: configure it to redirect traffic to the proxy server in response for certian hostnames
 * A MySQL server
 * MySQL-Python
 * __Web App__
    * [Django](https://www.djangoproject.com/)
    * [FreeRADIUS](http://freeradius.org/)
    * [pyrad](https://pypi.python.org/pypi/pyrad)
 * __Proxy__
    * A proxy server for HTTP requests, such as [Squid](http://www.squid-cache.org/) or [Tinyproxy](https://banu.com/tinyproxy/)
    * [dpkt](https://code.google.com/p/dpkt/)
    * [Twisted](https://twistedmatrix.com/trac/)

## dpkt SNI Patch
At the time, for some reason, using dpkt to get the hostname seemed like a good choice. However, using pyOpenSSL's `set_tlsext_servername_callback()` would be better. dpkt will be removed in favour of pyOpenSSL in the future.

The patch originated from [here](https://code.google.com/p/dpkt/issues/detail?id=73).
```
patch dpkt/ssl.py < dpkt-ssl-sni.patch
```

## Quick Setup
Create ViaDNS's database.
```
mysql -u user < sql/viadns.sql
```

### Web App
Configure settings for `viadns` and `account` apps.
```
cp account/settings-template.py account/settings.py
cp viadns/settings-template.py viadns/settings.py
```

Generate a new secret key for the main settings module.  
Set `SECRET_KEY` in `viadns/settings.py` to the result of the following command.
```
python manage.py generatesecretkey
```

### Proxy
Configure settings.
```
cp proxy/settings-template.py proxy/settings.py
```

In `proxy/main.py`, modify the proxies list as needed.  
For HTTPS (443), if the destination hostname is successfully obtained through the SNI, the predefined host specified to the  ProxyFactory instance is ignored.
```
proxies = [
            # listen on port 80 on all interfaces and forward to Squid on port 3128
           [80, ProxyFactory('127.0.0.1', 3128), ''],
           
           # listen on port 443 on all interfaces and forward to 'signup.netflix.com' on port 443 if SNI fails
           [443, ProxyFactory('signup.netflix.com', 443), '']]
```

## Possible Future Changes
 * dpkt will be removed in favour of pyOpenSSL's `set_tlsext_servername_callback()`
 * Proxy DNS requests to only allow requests from authorized IP addresses so that the redirecting DNS server could operate as a recursor
 * Use a predefined list of allowed hostnames for non-DNS requests as a check list in the proxy
 * General code improvements
