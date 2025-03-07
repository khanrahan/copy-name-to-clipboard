"""
Script Name: Copy Name to Clipboard
Written By: Kieran Hanrahan

Script Version: 3.0.0
Flame Version: 2025

URL: http://www.github.com/khanrahan/copy-name-to-clipboard

Creation Date: 10.12.23
Update Date: 08.28.24

Description:

    Copy names of selected items to clipboard.

Menus:

    Right-click selected items on the Desktop -> Copy... -> Name to Clipboard
    Right-click selected items in the Media Hub -> Copy... -> Name to Clipboard
    Right-click selected items in the Media Panel -> Copy... -> Name to Clipboard
    Right-click selected items in a Timeline -> Copy... -> Name to Clipboard

To Install:

    For all users, copy this file to:
    /opt/Autodesk/shared/python

    For a specific user, copy this file to:
    /opt/Autodesk/user/<user name>/python
"""

import os

import flame
from PySide6 import QtWidgets

TITLE = 'Copy Name to Clipboard'
VERSION_INFO = (3, 0, 0)
VERSION = '.'.join([str(num) for num in VERSION_INFO])
TITLE_VERSION = f'{TITLE} v{VERSION}'
MESSAGE_PREFIX = '[PYTHON]'


def message(string):
    """Print message to shell window and append global MESSAGE_PREFIX."""
    print(' '.join([MESSAGE_PREFIX, string]))


def copy_to_clipboard(text):
    """Self explanitory.  Only takes a string."""
    qt_app_instance = QtWidgets.QApplication.instance()
    qt_app_instance.clipboard().setText(text)


def startup():
    """Messages to print at start of script run."""
    message(TITLE_VERSION)
    message(f'Script called from {__file__}')


def copy_names_mediahub(selection):
    """The main function for MediaHub selections."""
    startup()

    results = []

    for item in selection:
        results.append(os.path.splitext(os.path.basename(item.path))[0])

    copy_to_clipboard('\n'.join(results))
    message('Done!')


def copy_names_media_panel(selection):
    """The main function for Media Panel selections."""
    startup()

    results = []

    for item in selection:
        results.append(item.name.get_value())

    copy_to_clipboard('\n'.join(results))
    message('Done!')


def copy_names_timeline(selection):
    """The main function for Timeline selections."""
    startup()

    results = []

    for item in selection:
        results.append(item.name.get_value())

    copy_to_clipboard('\n'.join(results))
    message('Done!')


def scope_mediahub_object(selection):
    """Filter out only supported MediaHub exobjects."""
    valid_objects = (
            flame.PyMediaHubFilesEntry,
            flame.PyMediaHubFilesFolder)

    return all(isinstance(item, valid_objects) for item in selection)


def scope_media_panel_object(selection):
    """Filter out only supported Media Panel objects."""
    valid_objects = (
            flame.PyClip,
            flame.PySequence,
            flame.PyDesktop,
            flame.PyFolder,
            flame.PyLibrary,
            flame.PyReel,
            flame.PyReelGroup,
            flame.PyWorkspace)

    return all(isinstance(item, valid_objects) for item in selection)


def scope_timeline_object(selection):
    """Filter out only supported Timeline objects."""
    valid_objects = (
            flame.PyClip,
            flame.PySegment)

    return all(isinstance(item, valid_objects) for item in selection)


def get_mediahub_files_custom_ui_actions():
    """Python hook to add custom right click menu item to MediaHub."""
    return [{'name': 'Copy...',
             'actions': [{'name': 'Name to Clipboard',
                          'isVisible': scope_mediahub_object,
                          'execute': copy_names_mediahub,
                          'minimumVersion': '2025'}]
            }]


def get_media_panel_custom_ui_actions():
    """Python hook to add custom right click menu item to Media Panel or Desktop."""
    return [{'name': 'Copy...',
             'actions': [{'name': 'Name to Clipboard',
                          'isVisible': scope_media_panel_object,
                          'execute': copy_names_media_panel,
                          'minimumVersion': '2025'}]
            }]


def get_timeline_custom_ui_actions():
    """Python hook to add custom right click menu item to Timeline."""
    return [{'name': 'Copy...',
             'actions': [{'name': 'Name to Clipboard',
                          'isVisible': scope_timeline_object,
                          'execute': copy_names_timeline,
                          'minimumVersion': '2025'}]
           }]
