
#=============================PROJECT 2========================================
#==========================WEB PROGRAMMING========================
#=========================NAME: JONNATHAN FABRICIO CRESPO YAGUANA=============
#==========================DATE: DECEMBER 2019=================================


#=========IMPORT STATEMENTS======================
import os

from collections import deque

from flask import Flask, render_template, session, request, redirect
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from functools import wraps #Para login_required

app = Flask(__name__)
app.config["SECRET_KEY"] = "my secret key"
socketio = SocketIO(app)

#==============DEFINE A DECORATOR===================
@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("username") is None:
            return redirect("/signin")
        return f(*args, **kwargs)
    return decorated_function

#=========================================================


#==================GLOBAL VARIABLES=======================

#List of channels
channelsList=[]

#List of users
usersOnline=[]

#Messages of each channel
channelMessages=dict()
#============================================================

#=====================DEFINE ROUTES============================
@app.route("/")
@login_required
def index():
    """ #Session close
    session.pop('user', None) """
    return render_template("index.html", channels=channelsList, usersOnline=usersOnline)

@app.route("/signin", methods=["POST", "GET"])
def signin():
    
    #Session close
    #session.pop('user', None)\
    session.clear()

    #Get form information
    username = request.form.get("username") #variable recibida del campo username de indeX.html
    
    if request.method == "POST":
        if len(username)<1 or username is '':
            return render_template("error.html", message="Username invalid.")
        if username in usersOnline:
            return render_template("error.html", message="That username already exists!")
        
        usersOnline.append(username)

        #ACTIVE SESSION
        session['username']=username

        # Remember the user session on a cookie if the browser is closed.
        session.permanent = True

        return redirect("/") 
    else:
        return render_template("signin.html")

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    #Delete cookie to let user live the chat page
    #Remove from usersOnline
    try:
        usersOnline.remove(session['username'])
    except ValueError:
        pass
    #Delete cookie
    session.clear()

    return redirect("/")

@app.route("/create", methods=["GET", "POST"])
@login_required
def create():

    #Need to create a channel and go to this page

    newChannel=request.form.get("channel")

    if request.method=="POST":
        if newChannel in channelsList:
            return render_template("error.html", message="This channel already exist.")
    
        #Add the new channel to chanelsList:
        channelsList.append(newChannel)

        #Add channel to global dict of channels with messages
        #Every channel is a deque to use popleft() method

        channelMessages[newChannel]=deque()

        return redirect("/channels/" + newChannel)
    
    else:
        return render_template ("create.html", channels=channelsList)

@app.route("/channels/<channel>", methods=["GET", "POST"])
@login_required
def enter_channel(channel):
    #Particular channel to chat

    #Updates user current channel
    session['current_channel']=channel

    if request.method=='POST':
        return redirect("/")
    else:
        return render_template("channel.html", channels=channelsList, messages=channelMessages[channel])

#=====================================================================

#===========================SOCKETS=============================
@socketio.on("joined", namespace='/')
def joined():
    #Let to other users that a user has arrived to the current channel

    #Save current channel to join room
    chatroom=session.get('current_channel')

    join_room(chatroom)

    emit('status', {
        'userJoined': session.get('username'),
        'channel': chatroom,
        'msg': session.get('username')+ ' has entered to the channel'},
        room=chatroom)

@socketio.on("letf", namespace='/')
def left():
    #Announce that a user has left the channel

    chatroom=session.get('current_channel')

    leave_room(chatroom)

    emit('status', {
        'msg': session.get('username') + 'has left the current chatroom'},
        room=chatroom)

@socketio.on('send message')
def send_msg(msg, timestamp):

    """It let us receive a message with timestamp and brodcast on the channel"""

    #Share only with the users from the channel

    chatroom=session.get('current_channel')

    #We should save the last 100 messages and pass then when a user arrives to the channel

    if len(channelMessages[chatroom])>100:

        #Delete messages that are next to 100
        channelMessages[chatroom].popleft()

    channelMessages[chatroom].append([timestamp, session.get('username'), msg])

    emit('announce message', {
        'user':session.get('username'),
        'timestamp': timestamp,
        'msg': msg},
        room=chatroom)

#=================================================================

#===================CODE NECESSARY TO RUN FLASK AND SOCKET.IO WITH PYTHON

if __name__ == '__main__':
    socketio.run(app)
