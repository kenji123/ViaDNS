from django import forms
from django.core.exceptions import ObjectDoesNotExist

import models

class SignUpForm(forms.Form):
    username = forms.CharField(max_length=64)
    password = forms.CharField(widget=forms.PasswordInput, max_length=64)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, max_length=64)
    
    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if len(str(username)) < 4:
            self._errors['username'] = self.error_class(['Username must be at least 4 characters.'])
        
        if len(str(password)) < 8:
            self._errors['password'] = self.error_class(['Password must be at least 8 characters.'])
        
        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError('Passwords do not match.')
        
        try:
            user_info = models.UserInfo.objects.using('radius').only("username").get(username__exact=username)
            if user_info:
                self._errors['username'] = self.error_class(['Username already taken.'])
                '''raise forms.ValidationError('Username already taken.')'''
        except ObjectDoesNotExist:
            pass
        
        return cleaned_data

class LogInForm(forms.Form):
    username = forms.CharField(max_length=64)
    password = forms.CharField(widget=forms.PasswordInput, max_length=64)
    
    def clean(self):
        cleaned_data = super(LogInForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        if len(str(username)) < 4:
            self._errors['username'] = self.error_class(['Username must be at least 4 characters.'])
        
        if len(str(password)) < 8:
            self._errors['password'] = self.error_class(['Password must be at least 8 characters.'])
        
        return cleaned_data
