#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""

"""

import subprocess
import sys
import os

myenv = os.environ.copy()

if sys.platform == 'win32':
    from core.util.win_interrupt import create_interrupt_event
    # Create a Win32 event for interrupting the kernel and store it in an environment variable.
    interrupt_event = create_interrupt_event()
    myenv["ASPWIN_INTERRUPT_EVENT"] = str(interrupt_event)
    try:
        from _winapi import DuplicateHandle, GetCurrentProcess, DUPLICATE_SAME_ACCESS, CREATE_NEW_PROCESS_GROUP
    except:
        from _subprocess import DuplicateHandle, GetCurrentProcess, DUPLICATE_SAME_ACCESS, CREATE_NEW_PROCESS_GROUP
    pid = GetCurrentProcess()
    handle = DuplicateHandle(pid, pid, pid, 0, True, DUPLICATE_SAME_ACCESS)
    myenv['ASPWIN_PARENT_PID'] = str(int(handle))
else:
    myenv['ASPWIN_PARENT_PID'] = str(os.getpid())

argv = [sys.executable, '-m', 'core'] + sys.argv[1:]

while True:
    process = subprocess.Popen(
        argv,
        close_fds=False,
        env=myenv,
        stdin=sys.stdin,
        stdout=sys.stdout,
        stderr=sys.stderr,
        shell=False)
    if sys.platform == 'win32':
        # Attach the interrupt event to the Popen object so it can be used later.
        process.win32_interrupt_event = interrupt_event
    try:
        retval = process.wait()
        if retval == 0:
            break
        elif retval == 42:
            print('Restarting...')
            continue
        elif retval == 2:
            # invalid commandline argument
            break
        elif retval == -6:
            # called if QFatal occurs
            break
        elif retval == 4:
            print('Import Error: ASP-Win could not be started due to missing packages.')
            sys.exit(retval)
        else:
            print('Unexpected return value {0}. Exiting.'.format(retval))
            sys.exit(retval)
    except KeyboardInterrupt:
        print('Keyboard Interrupt, quitting!')
        break
    except:
        process.kill()
        process.wait()
        raise
