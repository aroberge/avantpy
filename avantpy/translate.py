'''Provide mechanism to get translations of messages'''

from . import session

def get(msg):
    '''Returns the translation of msg given lang'''
    lang = session.state.get_lang()
    if lang is None:
        lang = 'upper'
    if msg in session.state.messages[lang]:
        return session.state.messages[lang][msg]
    else:
        return "Translation of the following does not exist: %s" % msg
