import readline





class CommandCompleter(object):
    def __init__(self, options):
        self.options = sorted(options)
        self.matches = []

    def complete(self, text, state):
        if state == 0:
            if text:
                self.matches = [s for s in self.options if s and
                        s.startwith(text)]
            else:
                self.matches = self.options[:]
        try:
            return self.matches[state]
        except IndexError:
            return None

#TODO: Gui
def main():
    #Set the commpleter for command completion inside our chat
    chat_commands = ["list", "send"]
    completer = CommandCompleter(chat_commands)
    readline.set_completer(completer.complete)
    readline.parse_and_bind('tab: complete')
    for kw in chat_commands:
        readline.add_history(kw)

    #Input processing starts here
    
    



if __name__ == "__main__":
    main()
