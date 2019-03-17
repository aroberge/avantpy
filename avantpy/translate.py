"""Provide mechanism to get translations of messages"""

from . import session

messages = session.state.messages


def get(msg):
    """Returns the translation of msg given lang"""
    default = "upper"
    lang = session.state.get_lang()
    messages
    if lang is not None and msg in messages[lang]:
        return messages[lang][msg]
    elif msg in messages[default]:
        response = [
            "Missing translation in language '%s'" % lang,
            "Using default.\n",
            messages[default][msg],
        ]
        return "\n".join(response)
    else:
        return "Translation of the following does not exist: %s" % msg
