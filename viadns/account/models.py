import time

from django.db import models

# Create your models here.
class Session(models.Model):
    username = models.CharField(max_length=64)
    ipaddr = models.CharField(max_length=64)
    session_id = models.CharField(max_length=64)
    timeout_secs = models.IntegerField()
    start_time = models.DateTimeField()
    timeout_time = models.DateTimeField()
    
    class Meta:
        db_table = 'session'
    
    def isValid(self):
        try:
            timeout_time = time.mktime(time.strptime(str(self.timeout_time), '%Y-%m-%d %H:%M:%S+00:00'))
            
            if timeout_time < time.time():
                return False
        except ValueError:
            return False
        except:
            raise
        
        return True

class UserInfo(models.Model):
    username = models.CharField(max_length=128)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    workphone = models.CharField(max_length=200)
    homephone = models.CharField(max_length=200)
    mobilephone = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    zip = models.CharField(max_length=200)
    notes = models.CharField(max_length=200)
    changeuserinfo = models.CharField(max_length=128)
    portalloginpassword = models.CharField(max_length=128)
    enableportallogin = models.IntegerField()
    creationdate = models.DateTimeField()
    creationby = models.CharField(max_length=128)
    updatedate = models.DateTimeField()
    updateby = models.CharField(max_length=128)
    
    class Meta:
        db_table = 'userinfo'

class RadiusCheck(models.Model):
    username = models.CharField(max_length=64)
    attribute = models.CharField(max_length=64)
    op = models.CharField(max_length=2)
    value = models.CharField(max_length=253)
    
    class Meta:
        db_table = 'radcheck'
