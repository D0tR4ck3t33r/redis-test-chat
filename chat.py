import readline
import sys
from client import chat_client

chat_commands = ["help", "list", "send", "receive", "exit"]




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
    #Parses the different commands into lists always starting with the command
    #name. Lists can have different lenghts
    l = line.strip()
    if l.startswith("send"):
        if l.split() == False:
            return None
        return l.split(' ', 2)
    elif l.startswith("list")or l.startswith("help")or l.startswith("receive"):
        return l.split()[:1]
    elif l.startswith("exit"):
        return l.split()[:1]
    else:
        return None

def run_command(parsed_line, user):
    #Used for the different commands to handle
    command = parsed_line[0]
    if command == 'help':
        print("Help for the simple Chat using redis")
        print("list - Lists all users")
        print("send <user> <message> - Send a message to a user")
        print("receive - Receive all messages send to you")
    elif command == 'list':
        print("Users online: ")
        allonline = user.listAllUsers()
        print(' '.join(allonline))
    elif command == 'send': 
        try:
            receiver = parsed_line[1]
            message = parsed_line[2]
        except IndexError:
            print('''Invalid Syntax. Check the help for more information on this
            command''')
        user.sendMessageTo(receiver, message)
    elif command == 'receive':
        messages = user.getMessagesFromAll()
        for m in messages:
            print("From: " + m[0])
            print("Message: " + m[1])
    elif command == "exit":
        sys.exit(0)



def main():
    #Get login
    username = raw_input("username: ")
    user = chat_client(username)

    #Set the commpleter for command completion inside our chat
    completer = CommandCompleter(chat_commands)
    readline.set_completer(completer.complete)
    readline.parse_and_bind('tab: complete')
    for kw in chat_commands:
        readline.add_history(kw)

    #Input processing starts here
    while True:
        line = raw_input('>')
        parsed_line = parse(line)
        if parsed_line is None:
            print("Error: No command with that name found")
            print("Check help for available commands")
            continue
        run_command(parsed_line, user)
    



if __name__ == "__main__":
    main()
