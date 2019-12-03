# Project 2

=====NAME: JONNATHAN FABRICIO CRESPO=================
=======WEB PROGRAMMING=======================
========DECEMBER 2019==========================

Project number two is about the creation of a web page that let people
chat with other. For this project, we use FLASK and SOCKET.IO.

To enhence my project, I created one file for flask in python. It is called application. Here, I wrote the principal functions of my project (app.routes) like index, logout, sigin, create a channel. etc.

Also, in this file is included the sockets like joined, send message.

Inside the templates folder there are a few html files/templates that include layout, error, channel, sigin, etc.

Finally, in the static folder there are some images that I used in my html files. The most important file from here is channel.js which has the socket instructions and socket emits. These instructions taker the funcionality of the different components of the web applications like buttons, inputs. etc.

My personal touch is add a list of users connected to the chat application. This list appears in the firs page that the user sees after it sigin up. Maybe, on a knowledge enviroment people can recognize other people to chat.

#==================RUN THE PROGRAM=======================
FLASK_APP=application.py
export FLASK_DEBUG=1
python application.py