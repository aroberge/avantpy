import subprocess

sessions = [
    (
        "python -m avantpy",
        "a = 41 \na+=1\nprint(a)\nd=e\n",
        ["42"],
        ["-->1: d=e", "NameError"],
    )
]


def test_console():
    """Function discoverable and run by pytest"""
    for command, inp, out, err in sessions:
        print("out = ", out)
        print("err =", err)
        process = subprocess.Popen(
            command,
            shell=False,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,  # use strings as input
        )
        # I have found comparisons with stderr problematic, so I ignore it
        # However, since all tests are supposed not to raise exceptions
        # but only valid output, this does not impact the reliability
        # of these tests: if stdout is not as expected, we have a problem.
        stdout, stderr = process.communicate(inp)
        process.wait()
        print("stdout =", stdout)
        print("stderr =", stderr)

        for item in out:
            print("item in out = ", item in stdout)
            assert item in stdout, f"{item} not in stdout"
        for item in err:
            print("iten in err = ", item, item in stderr)
            assert item in stderr, f"{item} not in stderr"


# test_console()
