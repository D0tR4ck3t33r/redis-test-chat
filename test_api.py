from client import *
def tests():
    username1 = "gunter"
    username2 = "peter"
    username3 = "petra"

    user1 = chat_client(username1)
    user2 = chat_client(username2)
    user3 = chat_client(username3)

    assert(user1.checkIfAlive())
    
    assert(username1 in user1.listAllUsers())
    assert(username2 in user1.listAllUsers())
    assert(username3 in user3.listAllUsers())


    _1to2mes = "Ya whats up"
    _1to3mes = "Ayy lmao"
    _1to1mes = "It's me Mario"
    _2to3mes = "Yeee"

    user1.sendMessageTo(username2, _1to2mes)
    user1.sendMessageTo(username3, _1to3mes)
    user1.sendMessageTo(username1, _1to1mes)
    user2.sendMessageTo(username3, _2to3mes)

    user1_messages = user1.getMessagesFromAll()
    assert(user1_messages == [(username1, _1to1mes)])
    user2_messages = user2.getMessagesFrom(username1)
    assert(user2_messages == [_1to2mes])
    user3_messages = user3.getMessagesFromAll()
    assert(user3_messages == [(username1, _1to3mes), (username2, _2to3mes)])


if __name__ == "__main__":
    tests()
