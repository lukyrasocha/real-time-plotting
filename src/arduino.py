import warnings
import serial
import serial.tools.list_ports
import time

# Find the Arduino ports: they should be automatically detected
# for Mac the device is seen as network interface 'usbmodem'
arduino_ports = [
    p.device for p in serial.tools.list_ports.comports()
    if ('Arduino' in p.description) or ('usbmodem' in p.device) # may need tweaking to match new arduinos
]

if not arduino_ports:
    raise IOError("No Arduino found")
if len(arduino_ports) > 1:
    warnings.warn('Multiple Arduinos found - using the first')


arduinoPort = serial.Serial(arduino_ports[0], 9600) #, timeout=0) 
arduinoStr = ''

def prepareArduino():
    '''
    Prepares the Arduino to start receiving values from the sensors.
    '''
    # Initialize Arduino
    initArduino()
    print('Waiting for response from Arduino...')
    time.sleep(2)

    # Send 65
    print('Sending 65 to Arduino...')
    writeArduino('65')
    time.sleep(10)

    # Send 66
    print('Sending 66 to Arduino...')
    writeArduino('66')
    time.sleep(10)

    # Wait until start receiving sensor measurements
    while True:
        try:
            read_value = float(readArduino().split('\t')[1])
            print(f'Reading from Arduino: {read_value}')
            break
        except:
            pass
    print('Started Receiving Serial Values')


def initArduino():
    '''
    Initializes the Arduino to start reading from all its ports.
    ''' 
    arduinoPort.read_all()


def writeArduino(str):
    '''
    Writes command to serial port encoded in utf-8 format.
    '''
    for c in str:
        arduinoPort.write(bytes(c, 'utf-8'))
        time.sleep(0.01) 
    
    arduinoPort.write(bytes('\n\r', 'utf-8'))


def readArduino():
    '''
    Reads one line from the serial port.
    ''' 
    global arduinoStr
    while arduinoPort.inWaiting() > 0:
        c = arduinoPort.read().decode('utf-8')
        arduinoStr += c
        if c == '\n' or c == '\r':
            res = arduinoStr.rstrip().lstrip()  ## eliminate endline and newline terminators ("/r,/n" type stuff) 
            arduinoStr = ''
            return res

    return ''

def readArduino2():
    '''
    Reads one value from serial.
    ''' 
    while arduinoPort.inWaiting() > 0:
        c = arduinoPort.read().decode('utf-8')
        return c
    return ''

def readArduino3():
    """Reads a value from a serial port and parses it into a float

    Returns
    -------
    float
        sensor value as a float
    """
    data = arduinoPort.readline().decode().strip()
    if data != '':
        res = float(data)
    else:
        res = 0
    return res

def resetBuffer():
    """
    Resets the port's input buffer
    """
    arduinoPort.reset_input_buffer()
