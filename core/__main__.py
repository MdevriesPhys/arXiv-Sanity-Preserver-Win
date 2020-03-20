import sys

import faulthandler
faulthandler.disable()
faulthandler.enable(all_threads=True)

# parse commandline parameters
import argparse
parser = argparse.ArgumentParser(prog='start.py')
group = parser.add_mutually_exclusive_group()
parser.add_argument('-c', '--config', default='default.cfg', help='configuration file')
parser.add_argument('-l', '--logdir', default='', help='log directory')
args = parser.parse_args()

from .logger import initialize_logger
initialize_logger(args.logdir)
import logging
logger = logging.getLogger(__name__)
logger.info('Loading ASP-Win...')
print("Loading arXiv Sanity Preserver - Win")
print("Reticulating splines")
print('Preserving Sanity...')

# define a global variable for the manager
man = None

# install logging facility for Qt errors
import qtpy
from qtpy import QtCore
def qt_message_handler(msgType, msg):
    """
    A message handler handling Qt messages.
    """
    logger = logging.getLogger('Qt')
    if qtpy.PYQT4:
        msg = msg.decode('utf-8')
    if msgType == QtCore.QtDebugMsg:
        logger.debug(msg)
    elif msgType == QtCore.QtWarningMsg:
        logger.warning(msg)
    elif msgType == QtCore.QtCriticalMsg:
        logger.critical(msg)
    else:
        import traceback
        logger.critical('Fatal error occurred: {0}\n'
                'Traceback:\n'
                '{1}'.format(msg, ''.join(traceback.format_stack())))
        global man
        if man is not None:
            logger.critical('Asking manager to quit.')
            try:
                man.quit()
                QtCore.QCoreApplication.instance().processEvents()
            except:
                logger.exception('Manager failed quitting.')

if qtpy.PYQT4 or qtpy.PYSIDE:
    QtCore.qInstallMsgHandler(qt_message_handler)
else:
    def qt5_message_handler(msgType, context, msg):
        qt_message_handler(msgType, msg)
    QtCore.qInstallMessageHandler(qt5_message_handler)


# instantiate Qt Application (gui or non-gui)
from qtpy import QtWidgets
app = QtWidgets.QApplication(sys.argv)

class AppWatchdog(QtCore.QObject):
    """This class periodically runs a function for debugging and handles
      application exit.
    """
    sigDoQuit = QtCore.Signal(object)

    def __init__(self):
        super().__init__()
        self.alreadyQuit = False

        self.exitcode = 0
        # Run python code periodically to allow interactive debuggers to interrupt
        # the qt event loop
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.donothing)
        self.timer.start(1000)
        self.sigDoQuit.connect(self.quitApplication)

    def donothing(self):
        """This function does nothing for debugging purposes.
        """
        #print('-- beat -- thread:', QtCore.QThread.currentThreadId())
        x = 0
        for i in range(0, 100):
            x += i

    def quitProxy(self, obj):
        """ Helper function to emit doQuit signal

            @param obj object: object passed to doQuit
        """
        print('Parent process is daed, committing sudoku...')
        self.sigDoQuit.emit(obj)

    def quitApplication(self, manager, restart = False):
        """Clean up threads and windows, quit application.

          @param object manager: manager belonging to this application

        """
        if restart:
            # exitcode of 42 signals to start.py that this should be restarted
            self.exitcode = 42
        if not self.alreadyQuit:    # Need this because multiple triggers can
                                    # call this function during quit.
            self.alreadyQuit = True
            self.timer.stop()
            logger.info('Closing windows...')
            print('Closing windows...')
            if manager.hasGui:
                manager.gui.closeWindows()
            QtCore.QCoreApplication.instance().processEvents()
            logger.info('Stopping threads...')
            print('Stopping threads...')
            manager.tm.quitAllThreads()
            QtCore.QCoreApplication.instance().processEvents()
            logger.info('ASP-Win is closed!')
            print("\n I'm scared, will I dream? \n Daiiiiissssyyyyyyy......")
        QtCore.QCoreApplication.instance().quit()

from .manager import Manager
#watchdog = AppWatchdog()
man = Manager(args=args)
#watchdog.setupParentPoller(man)
#man.sigManagerQuit.connect(watchdog.quitApplication)