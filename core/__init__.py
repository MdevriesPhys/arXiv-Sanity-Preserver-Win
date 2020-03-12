# -*- coding: utf-8 -*-
"""
This file contains the ASP-Win Manager class.
"""

__version__ = '0.1'

# import Qt
import os

if not 'QT_API' in os.environ:
    # use PyQt4 as default
    os.environ['QT_API'] = 'pyqt5'
else:
    print('Specified Qt API:', os.environ['QT_API'])
    # if pyqt4 check environment variable is 'pyqt' and not 'pyqt4' (ipython,
    # matplotlib, etc)
    if os.environ['QT_API'].lower() == 'pyqt4':
        os.environ['QT_API'] = 'pyqt'

import qtpy
print('Used Qt API:', qtpy.API_NAME)

import sys
# Make icons work on non-X11 platforms, import a custom theme
if sys.platform == 'win32':
    try:
        import ctypes
        myappid = 'test'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except:
        print('SetCurrentProcessExplicitAppUserModelID failed! This is '
              'probably not Microsoft Windows!')