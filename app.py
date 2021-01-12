from flask import Flask, jsonify, render_template, request, redirect, url_for
import RPi.GPIO as GPIO
import time
import webbrowser
from us import desky

app = Flask(__name__)
@app.route('/', methods=['GET'])
#This send current from 17 to the transistor for 0.5 seconds, activating the remote
def home():
#    message=request.get_data()
    #I use this BCM thing all the time to set up the board, it's essentially a board framework
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(17, GPIO.OUT)
    #these are printed to the terminal of the RPi when I run the python file (i dont use the RPi GUI)
    print("Light One")
    GPIO.output(17,GPIO.HIGH)
    time.sleep(0.5)
    print("Light Two")
    GPIO.output(17,GPIO.LOW)
    return 'light twiggered'

@app.route('/stuff', methods = ['GET'])
def rc_time ():
    count = 0
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(8, GPIO.OUT)
    GPIO.output(8, GPIO.LOW)
    time.sleep(0.1)
    GPIO.setup(8, GPIO.IN)
    #I believe this counts while the energy is flowing from the capaciter that is storing energy
    while (GPIO.input(8) == GPIO.LOW):
        count += 1
    mystr = 'ON'
    if (count > 15000):
        mystr = 'OFF'
    #I have to return these variables in this certain form, it has to be called and read by the JQuery
    mystr = jsonify(result=mystr)
    return mystr

@app.route('/fanon', methods=['GET'])
def other():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(18, GPIO.OUT)
    print("fanon on")
    GPIO.output(18,GPIO.HIGH)
    time.sleep(0.5)
    print("fanon off")
    GPIO.output(18,GPIO.LOW)
    return "Fan turned on"

@app.route('/fanoff', methods=['GET'])
def wack():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(27, GPIO.OUT)
    print("fanoff on")
    GPIO.output(27, GPIO.HIGH)
    time.sleep(0.5)
    print("fanoff off")
    GPIO.output(27, GPIO.LOW)
    return "Fan turned off"

@app.route('/door', methods=['GET'])
def door():
    import RPi.GPIO as GPIO
    import time
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    input_state = GPIO.input(14)
    tbr = "error"
    #This reads what the input state is, comes directedly from the GPIO.setup (essentually ive just returned True in electricity)
    if input_state == False:
        tbr = "closed"
    else:
        tbr = "open"
    tbr = jsonify(result=tbr)
    return tbr


@app.route('/us', methods=['GET'])
def desk():
    import RPi.GPIO as GPIO
    import time
    from us import desky
    GPIO.setmode(GPIO.BCM)
    GPIO_TRIGGER = 23
    GPIO_ECHO = 24
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)
    myArr = []
    #I chose to run this 5 times as I was having trouble shaping it to "on" or "off", this lets me account for errors
    for x in range(5):
        close = "False"
        GPIO.output(GPIO_TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)
        #these are the varuables where we'll be storing the start and end values
        StartTime = time.time()
        StopTime = time.time()
        while GPIO.input(GPIO_ECHO) == 0:
            StartTime = time.time()
        while GPIO.input(GPIO_ECHO) == 1:
            StopTime = time.time()
        TimeElapsed = StopTime - StartTime
        # NOT MY COMMENT, TAKEN FROM TUTORIAL - multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
        #Checks if someone is within 60 cm of my desk (pointed at my chair)
        if (distance < 60):
            close = "True"
            myArr.append(close)
        time.sleep(0.75)
    tbr = "UNKNOWN"
    if 'True' in myArr:
        tbr = "DESK"
    mystr = jsonify(result=tbr)
    return mystr

#Main one, calls all the methods and loads the html!
@app.route('/hub', methods=['GET'])
def hub():
    return render_template('PythonBigTech.html')


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')