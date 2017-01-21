import readline
from client import chat_client

chat_commands = ["list", "send"]




class CommandCompleter(object):
   
    def __init__(self, options):
        self.options = sorted(options)
        self.matches = None

    def complete(self, text, state):
        if state == 0:  # on first trigger, build possible matches
            if text:  # cache matches (entries that start with entered text)
                self.matches = [s for s in self.options 
                                    if s and s.startswith(text)]
            else:  # no text entered, all matches possible
                self.matches = self.options[:]

        # return match indexed by state
        try: 
            return self.matches[state]
        except IndexError:
            return None

def parse(line):
    line = line.strip()
    return line.split()




#TODO: Gui
def main():
    #Get login
    username = raw_input("username: ")
    user = chat_client(username)
    allusers = user.listAllUsers()

    #Set the commpleter for command completion inside our chat
    completer = CommandCompleter(chat_commands)
    readline.set_completer(completer.complete)
    readline.parse_and_bind('tab: complete')
    for kw in chat_commands:
        readline.add_history(kw)

    #Input processing starts here
    while True:
        line = raw_input('>')
        print(parse(line))
    



if __name__ == "__main__":
    main()
