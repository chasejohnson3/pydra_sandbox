import os
from pathlib import Path
import nest_asyncio
import time
import uuid

import attr
from nipype.interfaces.base import (
    Directory,
    File,
    InputMultiPath,
    OutputMultiPath,
    traits,
)
from pydra import ShellCommandTask
from pydra.engine.specs import SpecInfo, ShellSpec, ShellOutSpec, File

cmd = ["touch", "newfile_tmp.txt"]
my_input_spec = SpecInfo(
    name="Input",
    fields=[
        (
            "file1",
            str,
            {"help_string": "1st creadted file", "argstr": "", "position": 1},
        ),
        (
            "file2",
            str,
            {"help_string": "2nd creadted file", "argstr": "", "position": 2},
        ),
    ],
    bases=(ShellSpec,),
)

my_output_spec = SpecInfo(
    name="Output",
    fields=[
        (
            "newfile1",
            File,
            {"output_file_template": "{file1}", "help_string": "newfile 1"},
        ),
        (
            "newfile2",
            File,
            {"output_file_template": "{file2}", "help_string": "newfile 2"},
        ),
    ],
    bases=(ShellOutSpec,),
)
shelly = ShellCommandTask(
    name="shelly",
    executable=cmd,
    input_spec=my_input_spec,
    output_spec=my_output_spec,
)
shelly.inputs.file1 = "new_file_1.txt"
shelly.inputs.file2 = "new_file_2.txt"

res = shelly()
print(res)
