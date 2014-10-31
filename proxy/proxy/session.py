#!/usr/bin/python

import datetime, time

from db import MySQLHandler, Queries

class Session(object):
    username = ''
    ipaddr = ''
    session_id = ''
    timeout_secs = ''
    start_time = ''
    timeout_time = ''
    
    def set(self, data):
        self.username = data[1]
        self.ipaddr = data[2]
        self.session_id = data[3]
        self.timeout_secs = data[4]
        self.start_time = data[5]
        self.timeout_time = data[6]
    
    def get(self, ipaddr, dbHandler):
        result = dbHandler.execQuery(Queries.GET_SESSION % (ipaddr))[1]
        
        if result is not None:
            self.username = result[1]
            self.ipaddr = result[2]
            self.session_id = result[3]
            self.timeout_secs = result[4]
            self.start_time = result[5]
            self.timeout_time = result[6]
    
    def update(self, dbHandler):
        new_timeout_time = datetime.datetime.fromtimestamp(time.time() + self.timeout_secs)
        dbHandler.execQuery(Queries.UPDATE_SESSION % (new_timeout_time.isoformat(' '), self.ipaddr))
    
    def isValid(self):
        try:
            timeout_time = time.mktime(time.strptime(str(self.timeout_time), '%Y-%m-%d %H:%M:%S'))
            
            if timeout_time < time.time():
                return False
        except ValueError:
            return False
        except:
            raise
        
        return True
    
    def delete(self, dbHandler):
        dbHandler.execQuery(Queries.DELETE_SESSION % (self.ipaddr, self.session_id))

if __name__ == '__main__':
    dbHandler = MySQLHandler()
    dbHandler.connect()
    
    cursor = dbHandler.getConnection().cursor()
    cursor.execute(Queries.GET_ALL_SESSIONS)
    
    result = cursor.fetchone()
    while result is not None:
        if not dbHandler.isAlive(): dbHandler.connect()
        
        session = Session()
        session.set(result)
        
        if not session.isValid():
            session.delete(dbHandler)
        
        result = cursor.fetchone()
    
    cursor.close()
    dbHandler.getConnection().commit()
    cursor = None
