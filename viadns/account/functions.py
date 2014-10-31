from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

import pyrad.packet

from account import models, settings as app_settings

def getClientIp(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ipaddr = x_forwarded_for.split(',')[0]
    else:
        ipaddr = request.META.get('REMOTE_ADDR')
    
    return ipaddr

def sendAuthPacket(srv, username, password, ipaddr):
    req = srv.CreateAuthPacket(code=pyrad.packet.AccessRequest, User_Name=username)
    req["User-Password"] = req.PwCrypt(password)
    req["Framed-IP-Address"] = ipaddr
    req["NAS-IP-Address"] = app_settings.NAS_IP_ADDRESS
    req["NAS-Port"] = app_settings.NAS_PORT
    req["NAS-Identifier"] = app_settings.NAS_IDENTIFIER
    
    return srv.SendPacket(req)

def sendAcctPacket(srv, username, ipaddr, session_id, status_type=None, session_secs=0, terminate_cause=""):
    req = srv.CreateAcctPacket(User_Name=username)
    req["Framed-IP-Address"] = ipaddr
    req["NAS-IP-Address"] = app_settings.NAS_IP_ADDRESS
    req["NAS-Port"] = app_settings.NAS_PORT
    req["NAS-Identifier"] = app_settings.NAS_IDENTIFIER
    req["Acct-Session-Id"] = session_id
    if not status_type:
        req["Acct-Status-Type"] = "Start"
    else:
        req["Acct-Status-Type"] = status_type
        req["Acct-Session-Time"] = session_secs
        #req["Acct-Input-Octets"] = random.randrange(2**10, 2**30)
        #req["Acct-Output-Octets"] = random.randrange(2**10, 2**30)
        req["Acct-Terminate-Cause"] = terminate_cause #random.choice(["User-Request", "Idle-Timeout"])
    
    return srv.SendPacket(req)

def saveSession(username, ipaddr, session_id, timeout_secs, start_time, timeout_time):
    session = models.Session(username = username, 
                             ipaddr = ipaddr, 
                             session_id = session_id, 
                             timeout_secs = timeout_secs, 
                             start_time = start_time, 
                             timeout_time = timeout_time)
    session.save(using='default')

def getSession(request):
    model = models.Session.objects.using('default')
    
    session = None
    
    try:
        if request.COOKIES.get('session_id'):
            session = model.get(session_id=request.COOKIES.get('session_id'))
        else:
            session = model.get(ipaddr=getClientIp(request))
    except ObjectDoesNotExist:
        pass
    except:
        pass
    
    if session:
        if not session.isValid():
            session.delete()
            session = None
    
    return session

def getDnsServerIP():
    return settings.DATABASES['default']['HOST']
