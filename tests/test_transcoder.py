import os
from avantpy import converter


def test_transcoding():
    cwd = os.path.dirname(__file__)
    source_path = os.path.normpath(os.path.abspath(os.path.join(cwd, "pyfr/pyfr.pyfr")))
    assert os.path.isfile(source_path)

    with open(source_path, encoding="utf8") as f:
        original = f.read()

    english = converter.transcode(original, "pyfr", "pyen")
    french = converter.transcode(english, "pyen", "pyfr")

    assert french == original
