import socket
import random
import threading



def handle_client(s,connection,filter_day_msg,active_users,current_user,current_user_pass,users_loggedin,users_list,client_connections,connection_list,current_port,present_users):
    client_ip, client_port = connection.getpeername()
    current_user = client_port
    print("printing the ",current_user)
    connection_list[client_port] = connection
    print("printing thr connection_list:",connection_list)
    print(client_port)
    ack_message = ""
    while True:
        client_ip, client_port = connection.getpeername()
        current_user = client_port
        print("printing the current_user",current_user)
        connection.send(ack_message.encode('utf-8'))
        data_from_client = connection.recv(1024)
        x = data_from_client.decode('utf-8')
        print(x)
        print(filter_day_msg)
        fil_string = x.split()
        print(fil_string)
        if len(fil_string)<1:
            print("Session ends, something went, please try again later")
            break
        conv = int(fil_string[0])
        print(conv)
        # if current_user == "" and len(users_loggedin) >= 1:
        #     current_user = users_loggedin[0]
        if conv == 465:
            ser_m = random.choice(filter_day_msg)
            connection.send(("200 OK\n"+ser_m).encode('utf-8'))

        elif conv == 638:
            # data_send = "please enter username before doing this:"
            # connection.send(data_send.encode('utf-8'))
            # data_recv1 = connection.recv(1024)
            # user_nam = data_recv1.decode('utf-8')
            # print("printing user name",user_nam)
            res_name = ""
            print(client_port)
            for k,v in active_users.items():
                if v == client_port:
                    res_name = k
            print(res_name)
            if res_name in users_loggedin:
                msg = "200 OK\nplease enter the message of the day:"
                connection.send(msg.encode('utf-8'))
                data_from_client = connection.recv(1024)
                x = data_from_client.decode('utf-8')
                if len(filter_day_msg)>20: print("no messages can be added")
                else:
                    filter_day_msg.append(x)
                    print(filter_day_msg)
                    connection.send("200 OK".encode('utf-8'))
            else:
                msg = "401 You are not currently logged in, login first."
                connection.send(msg.encode('utf-8'))

        elif conv==377:
            for k,v in users_list.items():
                if k == fil_string[1] and v==fil_string[2]:
                    msg = "200 OK"
                    connection.send(msg.encode('utf-8'))
                    current_user = k
                    current_user_pass = v
                    print(current_user)
                    users_loggedin.append(k)
                    active_users[k]= client_port
                    present_users[k]= client_ip
            if current_user != fil_string[1] and current_user_pass!=fil_string[2]:
                msg = "410 Wrong UserID or Password"
                connection.send(msg.encode('utf-8'))
            print(users_loggedin)

        elif conv == 474:
            # msg = "please share the username that you want to logout from the device"
            # connection.send(msg.encode('utf-8'))
            # usen = connection.recv(1024)
            # usename = usen.decode('utf-8')
            res_name = ""
            print(client_port)
            for k,v in active_users.items():
               if v == client_port:
                   res_name = k
            print(res_name)
            if res_name not in users_loggedin:
                msg = "your not logged in."
                connection.send(msg.encode('utf-8'))
            else:
                msg = "please enter the password:"
                connection.send(msg.encode('utf-8'))
                passcode = connection.recv(1024)
                real_passcode = passcode.decode('utf-8')
                if users_list[res_name] == real_passcode:
                    users_loggedin.remove(res_name)
                    active_users.pop(res_name)
                    present_users.pop(res_name)
                    msg = "200OK,cheers you logged out successfully!!."
                    connection.send(msg.encode('utf-8'))
                    print(users_loggedin)
                    print(active_users)
                    print(present_users)
                else:
                    msg = "Passcode or username is wrong"
                    connection.send(msg.encode('utf-8'))

        elif conv == 646:
                res_name = ""
                print(client_port)
                for k,v in active_users.items():
                    if v == client_port:
                        res_name = k
                print(res_name)
                if res_name == "root":
                    connection.send("200 OK\n".encode('utf-8'))
                    for i,x in connection_list.items():
                        msg = "210 the server is about to shutdown ...."
                        x.send(msg.encode('utf-8'))
                        x.close()
                    s.close()
                    break
                else:
                     msg = "402 User not allowed to execute this command."
                     connection.send(msg.encode('utf-8'))
        elif conv == 248:
            connection.send(("200 OK\n" + str(present_users)).encode('utf-8'))

        elif conv == 333:
            connection.send("200 OK".encode('utf-8'))
            s.close()
            break

        elif conv == 298:
            print(fil_string)
            print(users_loggedin)
            if fil_string[1] in users_loggedin:
                connection.send("200 OK".encode('utf-8'))
                secret = connection.recv(1024)
                secret_message = secret.decode('utf-8')
                print("the secret message:{}".format(secret_message))
                port_num = active_users[fil_string[1]]
                fin_connection = connection_list[port_num]
                res_name = ""
                print(client_port)
                for k,v in active_users.items():
                     if v == client_port:
                         res_name = k
                print(res_name)
                ack_message = "You have a new private message "+res_name
                fin_connection.send(ack_message.encode('utf-8'))
                fin_connection.send((res_name+":"+secret_message).encode('utf-8'))
            else:
                msg= "420 either the user does not exist or is not logged in"
                connection.send(msg.encode('utf-8'))
        else:
            break


def main():
    current_port=0
    connection_list = {}
    client_connections = {}
    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    host = "127.0.0.1"
    Server_Port = 9809
    current_user_pass = ""
    try:
        s.bind((host, Server_Port))
        s.listen(10)
    except s.error as msg:
        print("connetion is not successful!! please try again later")
        return
    active_users = {}
    present_users = {}
    server_datastructure = ""
    print("server is up and running")


    current_user = ""
    current_user_pass = ""

    users_list = {
        "root": "root01",
        "john": "john01",
        "david": "david01",
        "mary": "mary01"
    }

    users_loggedin = []

    fo = open("Message_of_day", "r")
    server_datastructure = server_datastructure+(fo.read())
    fo.close()
    filter_day_msg=server_datastructure.split(",")
    print("server_datastructure",filter_day_msg)
    length_of_server_data = len(filter_day_msg)
    print("length of the message on the server", length_of_server_data)
    if length_of_server_data > 20:
        print("Further messages are not allowed, either delete some or do not prompt other messages")

    while True:
        connection,addr = s.accept()
        try:
            if connection:
                print("200 OK ")
                print("connection is successful")
        except socket.error as msg:
                print("socket connection failed")
        print('Accepted connection from {}:{}'.format(addr[0], addr[1]))
        client_handler = threading.Thread(target= handle_client, args=(s,connection,filter_day_msg,active_users,current_user,current_user_pass,users_loggedin,users_list,client_connections,connection_list,current_port,present_users))
        client_handler.start()


    handle_client(s,connection,filter_day_msg,active_users,current_user,current_user_pass,users_loggedin,users_list,client_connections,connection_list,current_port,present_users)

if __name__ == "__main__":
    main()
