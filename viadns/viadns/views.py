from django.shortcuts import render, redirect

from account import functions

def index(request):
    session = functions.getSession(request)
    
    if session:
        response = redirect('account.views.dashboard')
    else:
        response = render(request, 'index.html')
    
    return response
