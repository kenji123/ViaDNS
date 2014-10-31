import hashlib, random, datetime, time

from django.shortcuts import render, redirect
from django.utils.timezone import utc

import pyrad.packet
from pyrad.client import Client
from pyrad.dictionary import Dictionary

import functions, forms, models, settings as app_settings

def signup(request):
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            cleaned_data = form.clean()
            
            current_time = datetime.datetime.utcnow().replace(tzinfo=utc)
            
            user_info = models.UserInfo(username = cleaned_data.get('username'), 
                                        changeuserinfo = '0', 
                                        enableportallogin = 0, 
                                        creationdate = current_time, 
                                        creationby = 'administrator', 
                                        updatedate = current_time, 
                                        updateby = 'administrator')
            user_info.save(using='radius')
            
            radius_check = models.RadiusCheck(username = cleaned_data.get('username'), 
                                              attribute = 'User-Password', 
                                              op = ':=', 
                                              value = cleaned_data.get('password'))
            radius_check.save(using='radius')
            
            response = redirect('account.views.login')
            
            return response
    else:
        form = forms.SignUpForm()
    
    session = functions.getSession(request)
    
    if session:
        response = redirect('account.views.dashboard')
    else:
        response = render(request, 'signup.html', { 
            'form': form })
        response.delete_cookie('session_id')
    
    return response

def login(request):
    message = ''
    
    if request.method == 'POST':
        form = forms.LogInForm(request.POST)
        if form.is_valid():
            cleaned_data = form.clean()
            username = cleaned_data.get('username')
            password = cleaned_data.get('password')
            
            srv = Client(server=app_settings.CLIENT_SERVER, secret=app_settings.CLIENT_SECRET, dict=Dictionary(app_settings.DICTIONARY_PATH))
            ipaddr = functions.getClientIp(request)
            session_id = 'pyrad-' + hashlib.md5(username+str(random.randrange(2**30))).hexdigest()
            timeout_secs = app_settings.SESSION_TIMEOUT
            
            reply = functions.sendAuthPacket(srv, username, password, ipaddr)
            if reply.code == pyrad.packet.AccessAccept:
                for key, value in reply.iteritems():
                    if key == 'Session-Timeout':
                        timeout_secs = int(value)
                
                current_time = time.time()
                start_time = datetime.datetime.fromtimestamp(current_time).replace(tzinfo=utc)
                timeout_time = datetime.datetime.fromtimestamp(current_time + timeout_secs).replace(tzinfo=utc)
                functions.saveSession(username, ipaddr, session_id, timeout_secs, start_time, timeout_time)
                
                reply = functions.sendAcctPacket(srv, username, ipaddr, session_id)
                if not reply.code == pyrad.packet.AccountingResponse:
                    message = 'Failed to start accounting.'
                else:
                    response = redirect('account.views.dashboard')
                    response.set_cookie('session_id', session_id, expires=timeout_time)
                    
                    return response
            else:
                message = 'Invalid username or password.'
    else:
        form = forms.LogInForm()
    
    session = functions.getSession(request)
    
    if session:
        response = redirect('account.views.dashboard')
    else:
        data = { 'form': form }
        if message: data['message'] = message
        
        response = render(request, 'login.html', data)
        response.delete_cookie('session_id')
    
    return response

def logout(request):
    session = functions.getSession(request)
    
    if not session:
        return redirect('account.views.login')
    
    success = False
    message = ''
    
    srv = Client(server=app_settings.CLIENT_SERVER, secret=app_settings.CLIENT_SECRET, dict=Dictionary(app_settings.DICTIONARY_PATH))
    reply = functions.sendAcctPacket(srv, session.username, session.ipaddr, session.session_id, 
                           'Stop', 
                           (datetime.datetime.utcnow().replace(tzinfo=utc)-session.start_time).seconds, 
                           'User-Request')
    if reply.code == pyrad.packet.AccountingResponse:
        success = True
        message = 'Accounting stopped'
    
    session.delete()
    message += '<br />Logged out'
    
    response = render(request, 'logout.html', {
            'success': success,  
            'message': message })
    response.delete_cookie('session_id')
    
    return response

def dashboard(request):
    session = functions.getSession(request)
    
    if session:
        user_info = models.UserInfo.objects.using('radius').get(username=session.username)
        
        response = render(request, 'dashboard.html', { 
            'user_info': user_info, 
            'session': session, 
            'dns_server_ip': functions.getDnsServerIP() })
    else:
        response = redirect('account.views.login')
        response.delete_cookie('session_id')
    
    return response
