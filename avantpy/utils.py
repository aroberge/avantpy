"""utils.py

Classes or functions used in various other files.
"""


class Token:
    """Token as generated from tokenize.generate_tokens written here in
       a more convenient form for our purpose.
    """

    def __init__(self, token):
        self.type = token[0]
        self.string = token[1]
        self.start_line, self.start_col = token[2]
        self.end_line, self.end_col = token[3]
        # ignore last parameter which is the logical line
