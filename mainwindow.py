"""
A client/server code for Raspberry Pi ADC input

Xaratustrah
2016

Modificated by HoSnoopy for the internal Gastarget in the ESR in GSI
2016



"""

from PyQt5.QtWidgets import QMainWindow, QDialog, QInputDialog, QLineEdit
from PyQt5.QtCore import Qt, QCoreApplication, QThread, QTimer
from mainwindow_ui import Ui_MainWindow
from aboutdialog_ui import Ui_AbooutDialog
from zmq_listener import ZMQListener
from version import __version__
from gasrechnung import *


class mainWindow(QMainWindow, Ui_MainWindow):
    """
    The main class for the GUI window
    """

    def __init__(self):
        """
        The constructor and initiator.
        :return:
        """
        # initial setup
        super(mainWindow, self).__init__()
        self.setupUi(self)

        # text, ok = QInputDialog.getText(self, 'Settings', 'Enter the host address:', QLineEdit.Normal, '140.181.97.133')
        # if ok:
        #    host = str(text)
        # text, ok = QInputDialog.getText(self, 'Settings', 'Enter the port number:', QLineEdit.Normal, '10000')
        # if ok:
        #    port = int(text)
        # text, ok = QInputDialog.getText(self, 'Settings', 'Enter the topic number for Dump-Pressure:', QLineEdit.Normal, '10001')
        # if ok:
        #   topic = str(text)
        host = '140.181.97.133'
        port = 10000
        topic = '10001'
        self.thread = QThread()
        self.zeromq_listener = ZMQListener(host, port)
        self.zeromq_listener.moveToThread(self.thread)
        self.thread.started.connect(self.zeromq_listener.loop)

        self.gas = Wasserstoff()
        # self.gasart_label.setText(self.gas.label)

        # Connect signals
        self.connect_signals()

        QTimer.singleShot(0, self.thread.start)
        self.show_message('Connected to server: {}:{}'.format(host, port))

    def connect_signals(self):
        """
        Connects signals.
        :return:
        """

        # Action about and Action quit will be shown differently in OSX

        self.actionAbout.triggered.connect(self.show_about_dialog)
        self.actionQuit.triggered.connect(QCoreApplication.instance().quit)
        self.zeromq_listener.message.connect(self.signal_received)

        # combo box

        self.comboBox.currentTextChanged.connect(self.schaffe_passendes_gas_objekt)

    @staticmethod
    def eformat(f, prec, exp_digits):
        s = "%.*e" % (prec, f)
        mantissa, exp = s.split('e')
        # add 1 to digits as 1 is taken by sign +/-
        return "%se%+0*d" % (mantissa, exp_digits + 1, int(exp))

    def signal_received(self, message):
        l = len(message)
        l = l - 1
        message = message[2:l]
        dichte, temperatur = self.gas.rechne_dichte_aus(message)
        label_temperatur = 'Düsentemperatur: ' + str(round(temperatur, 2)) + 'K'
        self.label_temperatur.setText(label_temperatur)
        self.lcdNumber.setDigitCount(8)
        self.lcdNumber.display(dichte)

    def closeEvent(self, event):
        self.zeromq_listener.running = False
        self.thread.quit()
        self.thread.wait()

    def show_message(self, message):
        """
        Implementation of an abstract method:
        Show text in status bar
        :param message:
        :return:
        """
        self.statusbar.showMessage(message)

    def schaffe_passendes_gas_objekt(self, gasart):
        if gasart == 'Helium':
            self.gas = Helium()

        elif gasart == 'Neon':
            self.gas = Neon()

        elif gasart == 'Argon':
            self.gas = Argon()

        elif gasart == 'Krypton':
            self.gas = Krypton()

        elif gasart == 'Xenon':
            self.gas = Xenon()

        elif gasart == 'Wasserstoff':
            self.gas = Wasserstoff()

        elif gasart == 'Deuterium':
            self.gas = Deuterium()

        elif gasart == 'Stickstoff':
            self.gas = Stickstoff()

    def show_about_dialog(self):
        """
        Show about dialog
        :return:
        """
        about_dialog = QDialog()
        about_dialog.ui = Ui_AbooutDialog()
        about_dialog.ui.setupUi(about_dialog)
        about_dialog.ui.labelVersion.setText('Version: {}'.format(__version__))
        about_dialog.exec_()
        about_dialog.show()
