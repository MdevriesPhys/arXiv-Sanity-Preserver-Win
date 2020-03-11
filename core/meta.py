# -*- coding: utf-8 -*-
"""
Definition of various metaclasses
"""

import copy
from abc import ABCMeta
from qtpy.QtCore import QObject
from collections import OrderedDict
from .connector import Connector
from .statusvariable import StatusVar
from .configoption import ConfigOption


QObjectMeta = type(QObject)


class ModuleMeta(QObjectMeta):
    """
    Metaclass for Qudi modules
    """

    def __new__(cls, name, bases, attrs):
        """
        Collect declared Connectors, ConfigOptions and StatusVars into dictionaries.

            @param mcs: class
            @param name: name of class
            @param bases: list of base classes of class
            @param attrs: attributes of class

            @return: new class with collected connectors
        """

        # collect meta info in dicts
        connectors = OrderedDict()
        config_options = OrderedDict()
        status_vars = OrderedDict()

        # Accumulate Connector, ConfigOption and StatusVar info from parent classes
        for base in reversed(bases):
            if hasattr(base, '_connectors'):
                connectors.update(copy.deepcopy(base._connectors))
            if hasattr(base, '_config_options'):
                config_options.update(copy.deepcopy(base._config_options))
            if hasattr(base, '_stat_var'):
                status_vars.update(copy.deepcopy(base._stat_var))

        # Collect this classes Connector and ConfigOption and StatusVar into dictionaries
        for key, value in attrs.items():
            if isinstance(value, Connector):
                connectors[key] = value.copy(name=key)
            elif isinstance(value, ConfigOption):
                config_options[key] = value.copy(var_name=key)
            elif isinstance(value, StatusVar):
                status_vars[key] = value.copy(var_name=key)

        attrs.update(connectors)
        attrs.update(config_options)
        attrs.update(status_vars)

        # create a new class with the new dictionaries
        new_class = super().__new__(cls, name, bases, attrs)
        new_class._conn = connectors
        new_class._config_options = config_options
        new_class._stat_vars = status_vars

        return new_class


class TaskMetaclass(QObjectMeta, ABCMeta):
    """
    Metaclass for interfaces.
    """
    pass


class InterfaceMetaclass(ModuleMeta, ABCMeta):
    """
    Metaclass for interfaces.
    """
    pass
