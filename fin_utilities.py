#This is a package that we making for the use of the protocol

def converting_str_to_asc(strr,res=0):
    for char in strr:
        res += ord(char)
    return res

def msgget(client_s):
    data_to_send = "MSGGET\n"
    x=str(converting_str_to_asc(data_to_send))
    client_s.send(x.encode('utf-8'))
    serv_msg1 = client_s.recv(1024)
    print(serv_msg1.decode('utf-8'))
    # serv_msg2 = client_s.recv(1024)
    # print(serv_msg2.decode('utf-8'))
    return

def msgstore(client_s):
    mesg_mode = "MSGSTORE\n"
    x=str(converting_str_to_asc(mesg_mode))
    client_s.send(x.encode('utf-8'))
    # serv_msg = client_s.recv(1024)
    # print(serv_msg.decode('utf-8'))
    # username = input()
    # client_s.send(username.encode('utf-8'))
    serv_msg1 = client_s.recv(1024)
    x = serv_msg1.decode('utf-8')
    print(x)
    if x == "200 OK\nplease enter the message of the day:":
        return 0
    else:
        return 1

def shutdown(client_s):
    mesg_mode = "SHUTDOWN\n"
    x=str(converting_str_to_asc(mesg_mode))
    client_s.send(x.encode('utf-8'))
    msg = client_s.recv(1024)
    print(msg.decode('utf-8'))
    return msg.decode('utf-8')


def logout(client_s):
    mesg_mode = "LOGOUT"
    x=str(converting_str_to_asc(mesg_mode))
    client_s.send(x.encode('utf-8'))
    # serv_msg = client_s.recv(1024)
    # resv_msg = serv_msg.decode('utf-8')
    # print(resv_msg)
    # use = input()
    # client_s.send(use.encode('utf-8'))
    resv_msg1 = client_s.recv(1024)
    x=resv_msg1.decode('utf-8')
    if x == "your not logged in.":
        print(resv_msg1.decode('utf-8'))
    else:
        print(x)
        use1 = raw_input()
        client_s.send(use1.encode('utf-8'))
        resv_msg3 = client_s.recv(1024)
        print(resv_msg3)
def Quit(client_s):
    mesg_mode = "QUIT\n"
    x=str(converting_str_to_asc(mesg_mode))
    client_s.send(x.encode('utf-8'))
    return client_s.recv(1024)

def who(clien_s):
    mesg_mode = "WHO\n"
    x=str(converting_str_to_asc(mesg_mode))
    clien_s.send(x.encode('utf-8'))
    print(clien_s.recv(1024))
    return

def sendd(clien_s,username):
    mesg_mode = "SEND"
    x=str(converting_str_to_asc(mesg_mode))
    clien_s.send(x.encode('utf-8'))
    username.send(x.encode('utf-8'))
    y=clien_s.recv(1024)
    res = y.decode('utf-8')
    if res == "200 OK":
        print(res)
    else:
        print(res)
        return
