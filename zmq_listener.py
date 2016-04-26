"""
A client/server code for Raspberry Pi ADC input

Xaratustrah
2016

adapted from:

https://wiki.python.org/moin/PyQt/Writing%20a%20client%20for%20a%20zeromq%20service


"""
from PyQt5.QtCore import pyqtSignal, QObject
import zmq

# calibration constant
CALIBRATION = 3.3

# resolution of the ADC
ADC_RES = 12
N_STEPS = 2 ** ADC_RES

def eformat(f, prec, exp_digits):
    s = "%.*e"%(prec, f)
    mantissa, exp = s.split('e')
    # add 1 to digits as 1 is taken by sign +/-
    return "%se%+0*d"%(mantissa, exp_digits+1, int(exp))



class ZMQListener(QObject):
    message = pyqtSignal(str)

    def __init__(self, host, port, topic):
        QObject.__init__(self)

        self.host = host
        self.port = port
        self.topic = topic
        context = zmq.Context()
        try:
            self.sock = context.socket(zmq.SUB)
            self.sock.connect("tcp://{}:{}".format(self.host, self.port))
            self.sock.setsockopt_string(zmq.SUBSCRIBE, topic)
        except(ConnectionRefusedError):
            print('Server not running. Aborting...')

        except(EOFError, KeyboardInterrupt):
            print('\nUser input cancelled. Aborting...')

        self.running = True

    def loop(self):
        while self.running:
            string = self.sock.recv()
            topic, time, value = string.split()
            value = float(value)
#            value = int(value * 100) / 100
#            value = eformat(value, 2, 2)
            self.message.emit(str(value))
