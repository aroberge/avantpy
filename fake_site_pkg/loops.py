""" loops.py implements four transformations::

    repeat (n)  -> for var in range(n)
    repeat forever -> while True
    repeat until  -> while not
    repeat while -> while

.. todo::

    Right now, () are required for repeat (n). It might be worth looking at
    treating this case last, removing the requirements to put in () and, instead
    do something like::

        repeat expr :->

        assert isinstance(eval("expr"), int), "repeat must be followed by an integer"
        for var in range(expr):

"""

from io import StringIO
import tokenize


def transform_source(text):
    """Replaces instances of repeat as follows::

        repeat (n)  -> for __VAR_i in range(n)
        repeat forever -> while True
        repeat until  -> while not
        repeat while -> while

    where __VAR_i is a string that does not appear elsewhere
    in the code sample.
    """

    loop_keyword = "repeat"

    nb = text.count(loop_keyword)
    if nb == 0:
        return text

    var_names = get_unique_variable_names(text, nb)

    toks = tokenize.generate_tokens(StringIO(text).readline)
    result = []
    replacing_keyword = False
    for toktype, tokvalue, _, _, _ in toks:
        if replacing_keyword:
            replacing_keyword = False
            if toktype == tokenize.OP and tokvalue == "(":
                result.extend(
                    [
                        (tokenize.NAME, "for"),
                        (tokenize.NAME, var_names.pop()),
                        (tokenize.NAME, "in"),
                        (tokenize.NAME, "range"),
                        (tokenize.OP, "("),
                    ]
                )
            elif toktype == tokenize.NAME and tokvalue == "forever":
                result.extend([(tokenize.NAME, "while"), (tokenize.NAME, True)])
            elif toktype == tokenize.NAME and tokvalue == "while":
                result.extend([(tokenize.NAME, "while")])
            elif toktype == tokenize.NAME and tokvalue == "until":
                result.extend([(tokenize.NAME, "while"), (tokenize.NAME, "not")])
            else:
                raise SyntaxError(f"repeat is not followed {tokvalue} is not allowed.")
        elif toktype == tokenize.NAME and tokvalue == loop_keyword:
            replacing_keyword = True
        else:
            result.append((toktype, tokvalue))
    return tokenize.untokenize(result)


ALL_NAMES = []


def get_unique_variable_names(text, nb):
    """returns a list of possible variables names that
       are not found in the original text."""
    base_name = "__VAR_"
    var_names = []
    i = 0
    j = 0
    while j < nb:
        tentative_name = base_name + str(i)
        if text.count(tentative_name) == 0 and tentative_name not in ALL_NAMES:
            var_names.append(tentative_name)
            ALL_NAMES.append(tentative_name)
            j += 1
        i += 1
    return var_names


if __name__ == "__main__":
    sample = """# comment with repeat in it
repeat (3):  # first loop
    print('__VAR_1')
    repeat (2*2):
        pass"""

    comparison = """# comment with repeat in it
for __VAR_3 in range (3 ):# first loop
    print ('__VAR_1')
    for __VAR_2 in range (2 *2 ):
        pass """

    transformed = transform_source(sample)
    if comparison == transformed:
        print("Transformation done correctly")
    else:
        print("Transformation done incorrectly")
        import difflib

        d = difflib.Differ()
        diff = d.compare(comparison.splitlines(), transformed.splitlines())
        print("\n".join(diff))
