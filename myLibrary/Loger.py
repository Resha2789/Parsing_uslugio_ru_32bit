from PyQt5.QtCore import QObject
from PyQt5 import QtCore
import sys

class Communicate(QObject):
    uslugio_outputLogger = QtCore.pyqtSignal(str, int)

class ExceptHook:
    def __init__(self):
        self.init_except_hook()

    def init_except_hook(self):
        import sys
        sys.excepthook = self.show_exception_and_exit

    @staticmethod
    def show_exception_and_exit(exc_type, exc_value, tb):
        import traceback
        traceback.print_exception(exc_type, exc_value, tb)
        input("Press key to exit.")
        sys.exit(-1)


class OutputLogger:
    class Severity:
        DEBUG = 0
        ERROR = 1

    def __init__(self, io_stream, severity):
        super().__init__()
        self.Communicate = Communicate()
        self.emit_write = self.Communicate.uslugio_outputLogger
        self.io_stream = io_stream
        self.severity = severity

    def write(self, text):
        self.io_stream.write(text)
        self.emit_write.emit(text, self.severity)

    def flush(self):
        self.io_stream.flush()


class OutLogger:
    OUTPUT_LOGGER_STDOUT = OutputLogger(sys.stdout, OutputLogger.Severity.DEBUG)
    OUTPUT_LOGGER_STDERR = OutputLogger(sys.stderr, OutputLogger.Severity.ERROR)
    sys.stdout = OUTPUT_LOGGER_STDOUT
    sys.stderr = OUTPUT_LOGGER_STDERR