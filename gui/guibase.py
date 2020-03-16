# -*- coding: utf-8 -*-

"""
This file contains the ASP-Win GUI module base class.
"""

from qtpy.QtCore import QObject
from core.module import BaseMixin
import warnings


class GUIBaseMixin(BaseMixin):
    """This is the GUI base class. It provides functions that every GUI module should have.
    """

    def show(self):
        warnings.warn('Every GUI module needs to reimplement the show() '
                'function!')

    def saveWindowPos(self, window):
        self._statusVariables['pos_x'] = window.pos().x()
        self._statusVariables['pos_y'] = window.pos().y()

    def restoreWindowPos(self, window):
        if 'pos_x' in self._statusVariables and 'pos_y' in self._statusVariables:
            window.move(self._statusVariables['pos_x'],  self._statusVariables['pos_y'])


class GUIBase(QObject, GUIBaseMixin):
    pass
