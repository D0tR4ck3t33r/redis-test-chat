import redis

DEBUG = False

r = redis.Redis(
        host='127.0.0.1',
        port=6379)

# Call chat_client.keepAlive everytime a method is used
def keep_client_alive(fn):

    # The wrapper method which will get called instead of the decorated method:
    def wrapper(self, *args, **kwargs):
        fn(self, *args, **kwargs)           # call the decorated method
        self.keepAlive()   # call the additional method

    return wrapper  # return the wrapper method


class chat_client(object):
    def __init__(self, name):
        self.name = name
        self.username = 'user_' + name
        r.set(self.username, 1)
        if DEBUG:
            print("~SET " + self.username + " 1")
        r.expire(self.username, 120)
        if DEBUG:
            print("~EXPIRE " + self.username + " 120")
    
    #Methods for the online status of the client
    def checkIfAlive(self):
        if DEBUG:
            print("~GET " + self.username)
        status = r.get(self.username)
        if DEBUG:
            print("~~" + status)
        if status == "1":
            return True
        else:
            return False

    @keep_client_alive()
    def keepAlive(self):
        r.set(self.username, 1)

    #General Methods e.g. List all Users

    @keep_client_alive()
    def listAllUsers(self):
        keys = r.keys('user_*')
        if DEBUG:
            print("~KEYS user_*")
            print("~~"+keys)
        return keys    

    #Methods Message Releated
    @keep_client_alive()
    def sendMessageTo(name, message):
        key = 'user_' + name + '$' + self.username
        if DEBUG:
            print("~RPUSH " + key + " \"" + message + " \"")
        r.rpush(key, message)
    
    @keep_client_alive
    def getMessagesFrom(name):
        key = self.username + "$" + "user_" + name
        messages = r.lrange(key, 0, -1)
        r.delete(key)
        if DEBUG:
            print("~LRANGE " + key)
            print("~~" + messages)
            print("~DEL " + key)
        return messages
        
        

def main():
    user1 = chat_client("gunter")
    print(user1.checkIfAlive())
#    r.set('user_jfnskan', 1)
#    user_list = r.keys('user_*')
#    print(user_list)

if __name__ == "__main__":
    main()
