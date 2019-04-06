"""replicate_tests.py

Converts all the tests found in tests/pyupper into each dialect
and adds them to the apprpriate folder.
"""

import glob
import os
import sys
import tokenize


this_dir = os.path.dirname(__file__)
root_dir = os.path.abspath(os.path.join(this_dir, ".."))
source_dir = os.path.abspath(os.path.join(this_dir, "pyupper"))

sys.path.insert(0, root_dir)

# set up import hook
import avantpy  # noqa

pyupper_files = glob.glob(source_dir + "/*")
dialects = ["pyen", "pyes", "pyfr"]

nb_new = 0
nb_updated = 0

for filename in pyupper_files:
    path, ext = os.path.splitext(filename)
    basename = os.path.basename(path)
    if basename.startswith("__p"):
        continue
    source_creation_time = os.path.getmtime(filename)
    with open(filename, encoding="utf8") as f:
        source = f.read()
    for dialect in dialects:
        error_msg = None
        other_file = filename.replace("pyupper", dialect)
        if ext == ".py":
            content = source
        else:
            try:
                content = avantpy.converter.transcode(source, "pyupper", dialect)
            except Exception as exc:
                error_msg = repr(exc) + "\ncouldn't convert " + filename
                error_msg += "\n   Simply copied the content of the original file."
                content = source
        if os.path.isfile(other_file):
            target_creation_time = os.path.getmtime(other_file)
            newer = source_creation_time > target_creation_time
            if newer:
                nb_updated += 1
                with open(other_file, "w", encoding="utf8") as new_file:
                    new_file.write(content)
        else:
            nb_new += 1
            if error_msg is not None:
                print(error_msg)
                print("   Created: ", other_file)
            with open(other_file, "w", encoding="utf8") as new_file:
                new_file.write(content)

print("files updated:", nb_updated)
print("new files:", nb_new)
