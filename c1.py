import socket
from fin_utilities import msgget,msgstore,shutdown,logout,Quit,converting_str_to_asc,who,sendd
client_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = raw_input("please enter the host IP address for connection:")
server_port = 9809
client_s.connect((host,server_port))



while True:
    #choose one of the following command
    cmd = ["MSGGET", "MSGSTORE", "SHUTDOWN", "LOGIN", "LOGOUT", "QUIT","WHO","SEND"]
    print(cmd)
    choosing_option = raw_input("please choose a cmd from the above options: ")

    if choosing_option == "MSGGET":
        x=msgget(client_s)

    elif choosing_option == "MSGSTORE":
        x=msgstore(client_s)
        if x==0:
            msg_of_the_day = raw_input()
            client_s.send(msg_of_the_day.encode('utf-8'))
            ack = client_s.recv(1024)
            print(ack.decode('utf-8'))

    elif choosing_option == "SHUTDOWN":
        x = shutdown(client_s)
        if x == "200 OK\n210 the server is about to shutdown ...." or x=="210 the server is about to shutdown ...." or x == "200 OK\n":
            break

    elif choosing_option == "LOGIN":
        msg="LOGIN"
        x=str(converting_str_to_asc(msg))
        username=raw_input("please enter the username:")
        password=raw_input("please enter the password:")+"\n"
        total_cmd= x+" "+username+" "+password
        client_s.send(total_cmd.encode('utf-8'))
        res_msg = client_s.recv(1024)
        print(res_msg.decode('utf-8'))

    elif choosing_option == "LOGOUT":
        logout(client_s)

    elif choosing_option == "QUIT":
        res = Quit(client_s)
        print(res)
        client_s.close()
        exit(1)
    elif choosing_option == "WHO":
        who(client_s)
    elif choosing_option == "SEND":
        msg="SEND"
        x = str(converting_str_to_asc(msg))
        username=raw_input("please enter the username:")
        total_cmd= x+" "+username
        client_s.send(total_cmd.encode('utf-8'))
        res_msg = client_s.recv(1024)
        if res_msg.decode('utf-8') == "200 OK":
            print(res_msg.decode('utf-8'))
            msg_prompt = raw_input("please enter the secret message:")
            client_s.send(msg_prompt.encode('utf-8'))
        else:
            print(res_msg.decode('utf-8'))
    else:
        y = client_s.recv(1024)
        res = y.decode('utf-8')
        if res == "You have a new private message ":
            ack = client_s.recv(1024)
            print(ack.decode('utf-8'))
            print(" ")
            message = client_s.recv(1024)
            print(message)
            print("please re-enter the above command.......")
        elif res == "210 the server is about to shutdown ....":
            print(res)
            break
        else:
            print("please enter the options given above")
        break
client_s.close()
