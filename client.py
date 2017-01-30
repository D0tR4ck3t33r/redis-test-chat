import redis

_DEBUG = True

r = redis.Redis(
        host='127.0.0.1',
        port=6379)

# Call chat_client._keepAlive everytime a method is used
def _keep_client_alive(fn):

    # The wrapper method which will get called instead of the decorated method:
    def wrapper(self, *args, **kwargs):
        self._keepAlive()   # call the additional method
        return fn(self, *args, **kwargs)           # call the decorated method
        

    return wrapper  # return the wrapper method


class chat_client(object):
    def __init__(self, name):
        self.name = name
        self.username = 'user_' + name
        r.set(self.username, 1)
        if _DEBUG:
            print("~SET " + self.username + " 1")
        r.expire(self.username, 120)
        if _DEBUG:
            print("~EXPIRE " + self.username + " 120")
    
    #Methods for the online status of the client
    def checkIfAlive(self):
        if _DEBUG:
            print("~GET " + self.username)
        status = r.get(self.username)
        if _DEBUG:
            print("~~" + status)
        if status == "1":
            return True
        else:
            return False

    def _keepAlive(self):
        r.set(self.username, 1)
        r.expire(self.username, 120)
        if _DEBUG:
            print("~SET " + self.username + ' ' + str(1))
            print("~EXPIRE " + self.username + ' ' +str(120))

    #General Methods e.g. List all Users

    @_keep_client_alive
    def listAllUsersRaw(self):
        keys = r.keys('user_*')
        if _DEBUG:
            print("~KEYS user_*")
            print("~~"+str(keys))
        return keys

    def listAllUsers(self):
        raw_user_list = self.listAllUsersRaw()
        user_list = []
        for u in raw_user_list:
            user_list += [u[5:]]
        return user_list

    #Methods Message Releated
    @_keep_client_alive
    def sendMessageTo(self, name, message):
        key = '$user_' + name + '$' + self.username
        if _DEBUG:
            print("~RPUSH " + key + " \"" + message + " \"")
        r.rpush(key, message)
    
    @_keep_client_alive
    def getMessagesFrom(self, name):
        key = '$' + self.username + "$" + "user_" + name
        messages = r.lrange(key, 0, -1)
        r.delete(key)
        if _DEBUG:
            print("~LRANGE " + key)
            print("~~" + ' '.join(messages))
            print("~DEL " + key)
        return messages
        
    def getMessagesFromAll(self):
        user_list = self.listAllUsers()
        message_list = []
        for u in user_list:
            mes = self.getMessagesFrom(u)
            for m in mes:
                message_list += [(u, m)]
        return message_list
 
