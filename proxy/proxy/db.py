import MySQLdb, sys

import settings

class MySQLHandler(object):
    
    def __init__(self):
        pass
    
    def connect(self):
        try:
            self.__conn = MySQLdb.connect(host = settings.DATABASE['HOST'],
                                          user = settings.DATABASE['USER'],
                                          passwd = settings.DATABASE['PASSWORD'],
                                          db = settings.DATABASE['DB'])
        except MySQLdb.Error, e:
            self.__log('error', '%d: %s' % (e.args[0], e.args[1]))
    
    def disconnect(self):
        try:
            self.__conn.close()
        except MySQLdb.Error, e:
            self.__log('error', '%d: %s' % (e.args[0], e.args[1]))
    
    def getConnection(self):
        return self.__conn
    
    def isAlive(self):
        try:
            self.__conn.ping()
        except MySQLdb.Error, e:
            self.__log('error', '%d: %s' % (e.args[0], e.args[1]))
            
            self.disconnect()
        
        return self.__conn.open
    
    def __log(self, level, line):
        sys.stderr.write("[%s] MySQLHandler: %s\n" % (level, line))
    
    def execQuery(self, query):
        try:
            cursor = self.__conn.cursor()
            cursor.execute(query)
            affected_rows = self.__conn.affected_rows()
            result = cursor.fetchone()
            cursor.close()
            self.__conn.commit()
            cursor = None
        except MySQLdb.Error, e:
            self.__log('error', '%d: %s' % (e.args[0], e.args[1]))
            
            return None, None
        
        return affected_rows, result

class Queries(object):
    GET_ALL_SESSIONS = 'SELECT * FROM session'
    GET_SESSION = 'SELECT * FROM session WHERE ipaddr = \'%s\''
    UPDATE_SESSION = 'UPDATE session SET timeout_time = \'%s\' WHERE ipaddr = \'%s\''
    DELETE_SESSION = 'DELETE FROM session WHERE ipaddr = \'%s\' AND session_id = \'%s\''
