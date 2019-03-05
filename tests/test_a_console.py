'''A simple test just to ensure that the console is drastically broken'''

import subprocess
from avantpy import console

prompt = console.prompt

### sessions items:
### (command, input, expected_output, expected_error)

sessions = [
    ("python -im avantpy -s tests.test_french",
     'Vrai',
     'Success.\nTrue'),
]

def compare_output(real, expected):
    '''The output from the console includes the prompt.
       To make tests less brittle and easier to write, we strip the prompt
       and remove leading and trailing spaces.
    '''
    real = real.replace(prompt, '').strip()
    print("real = ", real, len(real))
    print("expected = ", expected, len(expected))
    return real == expected.strip()

def test_console():
    '''Function discoverable and run by pytest'''
    for command, inp, out in sessions:
        process = subprocess.Popen(
            command,
            shell=False,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True  # use strings as input
        )
        stdout, _ = process.communicate(inp)
        process.wait()
        assert compare_output(stdout, out)


if __name__ == "__main__":
    test_console()
    print("Ok")
