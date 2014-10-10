import zmq
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5006")
 
while True:
    try:
        msg = socket.recv()
        print "Got", msg
        socket.send(msg)
    except:
        quit()

