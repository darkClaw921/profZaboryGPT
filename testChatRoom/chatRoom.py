from flask import Flask, request, render_template, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room, send
import random
from pprint import pprint
from loguru import logger
from workTelegram import send_message_to_telegram, set_isSend
app = Flask(__name__)
app.config["SECRET_KEY"] = "supersecretkey"
# app.config['SERVER_CERT'] = 'cert.pem'
# app.config['SERVER_KEY'] = 'key.pem'
socketio = SocketIO(app)

# A mock database to persist data
rooms = {}

# def send_message_to_telegram():
    
    # pass

def generate_room_code(length: int, existing_codes: list[str]) -> str:
    while True:
        code_chars = [random.choice('1213ASD213123') for _ in range(length)]
        # code_chars = [23]
        code = ''.join(code_chars)
        if code not in existing_codes:
            return code

@app.route('/', methods=["GET", "POST"])
def home():
    session.clear()
    pprint(request.form)
    if request.method == "POST":
        name = request.form.get('name')
        create = request.form.get('create', False)
        code = request.form.get('code')
        join = request.form.get('join', False)
        if not name:
            return render_template('home.html', error="Name is required", code=code)
        if create != False:
            # room_code = generate_room_code(6, list(rooms.keys()))
            room_code = '23'
            new_room = {
                'members': 0,
                'messages': []
            }
            rooms[room_code] = new_room

        if join != False:
            # no code
            if not code:
                return render_template('home.html', error="Please enter a room code to enter a chat room", name=name)
            # invalid code
            if code not in rooms:
                return render_template('home.html', error="Room code invalid", name=name)
            room_code = code
        session['room'] = room_code
        session['name'] = name
        return redirect(url_for('room'))
    else:
        return render_template('home.html')


@app.route('/create/room/<int:roomID>',methods=["POST"])
def create_room(roomID):
    global rooms
    room_code = str(roomID)
    new_room = {
        'members': 0,
        'messages': []
    }
    rooms[room_code] = new_room
    return rooms

@app.route('/room')
def room():
    room = session.get('room')
    name = session.get('name')
    if name is None or room is None or room not in rooms:
        return redirect(url_for('home'))
    messages = rooms[room]['messages']
    return render_template('room.html', room=room, user=name, messages=messages)


#отправка сообщения в комнату (из телеги)
@app.route('/message/<string:userID>/<string:text>', methods=["POST"])
def add_message_to_chat(userID, text):
    # global rooms
    # mess = {'message':text, 'sender':str(userID)}
    # rooms[23]['messages'].append(mess)
    userID = str(userID)
    session.clear()
    session['room'] = userID
    session['name'] = userID
    # session['namespace']= 23
    message = {
        "sender": userID,
        "message": text 
    }
    # send(message, to=userID)
    rooms[userID]["messages"].append(message)

    # send(text, to=str(userID), namespace='/')
    logger.debug(rooms)

    #NOTE имитирует вызов сокета
    # try: create_room(userID)
    socketio.emit('message',{'name': userID, 'room': userID, 'message':text},namespace='/')

    # socketio.emit('ping event', {'data': 42}, namespace='/chat')
    return rooms

#подключение к комнате 
@app.route('/room/<string:room>')
def room23(room):
    # room = session.get('room')
    session.clear()
    # name = session.get('name')
    # room = '23'
    name = 'Менеджер'
    session['room'] = room
    session['name'] = name
    if name is None or room is None or room not in rooms:
        return redirect(url_for('home'))
    
    messages = rooms[room]['messages']
    return render_template('room.html', room=room, user=name, messages=messages)
    

@socketio.on('connect')
def handle_connect():
    name = session.get('name')
    room = session.get('room')
    if name is None or room is None:
        return
    if room not in rooms:
        1+0
        # leave_room(room)
    join_room(room)
    send({
        "sender": "",
        "message": f"{name} присоеденился к чату"
    }, to=room)
    rooms[room]["members"] += 1
    pprint(rooms)

@socketio.on('message')
def handle_message(payload):
    #NOTE
    #{23: {'members': 1,
    #  'messages': [{'message': 'asff', 'sender': 'as'},
    #               {'message': 'xxc', 'sender': 'as'}]}}
    #массив с сообщениями
    #rooms[room]["messages"]
    #создаем список из базы 
    
    room = session.get('room')
    logger.debug(room)
    name = session.get('name')
    logger.debug(session)
    # logger.debug(session['namespace'])
    # logger.debug(session.get('namespace'))
    if room not in rooms:
        return
    
    if name == 'Менеджер':
        chatID = room
        text = payload["message"]

        send_message_to_telegram(userID=chatID, message=text)
        set_isSend()

    message = {
        "sender": name,
        "message": payload["message"]
    }
    send(message, to=room)
    rooms[room]["messages"].append(message)
    pprint(rooms)

# @socketio.on('disconnect')
# def handle_disconnect():
#     room = session.get("room")
#     name = session.get("name")
#     # leave_room(room)
#     if room in rooms:
#         rooms[room]["members"] -= 1
#         if rooms[room]["members"] <= 0:
#             del rooms[room]
#         send({
#         "message": f"{name} has left the chat",
#         "sender": ""
#     }, to=room)
    # socketio.call()
    
if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port='5004', debug=False)
    
    # socketio.run(app, host='0.0.0.0', ssl_context=('cert.pem','key.pem'),port='5004', debug=False)
    