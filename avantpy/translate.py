'''Provide mechanism to get translations of messages'''

import glob
import os.path
import runpy

from . import session

messages = {}
default = 'upper'

def _collect_messages():
    """Find messages from known languages and create corresponding dictionaries"""
    languages = glob.glob(os.path.dirname(__file__) + "/translations/*.py")
    for f in languages:
        if os.path.isfile(f) and not f.endswith("__init__.py"):

            lang = os.path.basename(f).split(".")[0]
            _module = runpy.run_path(f)
            messages[lang] = _module[lang]

_collect_messages()


def get(msg):
    '''Returns the translation of msg given lang'''
    lang = session.state.get_lang()
    if lang is None:
        lang = default
    if msg in messages[lang]:
        return messages[lang][msg]
    else:
        return "Translation of the following does not exist: %s" % msg
