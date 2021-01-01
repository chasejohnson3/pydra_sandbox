import pydra
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
from pydra.engine.specs import SpecInfo, ShellSpec, File


wf = pydra.Workflow(name="wf", input_spec=["cmd1", "cmd2", "args"])

wf.inputs.cmd1 = "touch"
wf.inputs.cmd2 = "cp"
wf.inputs.args = "newfile.txt"

my_input_spec1 = SpecInfo(
    name="Input",
    fields=[
        (
            "file",
            attr.ib(
                type=str,
                metadata={
                    "output_file_template": "{args}",
                    "help_string": "output file",
                },
            ),
        )
    ],
    bases=(ShellSpec,),
)

my_input_spec2 = SpecInfo(
    name="Input",
    fields=[
        (
            "orig_file",
            attr.ib(
                type=str,
                metadata={
                    "position": 1,
                    "help_string": "output file",
                    "argstr": "",
                },
            ),
        ),
        (
            "out_file",
            attr.ib(
                type=str,
                metadata={
                    "position": 2,
                    "argstr": "",
                    "output_file_template": "{orig_file}_cp",
                    "help_string": "output file",
                },
            ),
        ),
    ],
    bases=(ShellSpec,),
)

wf.add(
    ShellCommandTask(
        name="shelly1",
        input_spec=my_input_spec1,
        executable=wf.lzin.cmd1,
        args=wf.lzin.args,
    )
)
wf.add(
    ShellCommandTask(
        name="shelly2",
        input_spec=my_input_spec2,
        executable=wf.lzin.cmd2,
        orig_file=wf.shelly1.lzout.file,
    )
)

wf.set_output(
    [
        ("touch_file", wf.shelly1.lzout.file),
        ("out1", wf.shelly1.lzout.stdout),
        ("cp_file", wf.shelly2.lzout.out_file),
        ("out2", wf.shelly2.lzout.stdout),
    ]
)

with pydra.Submitter(plugin="cf") as sub:
    wf(submitter=sub)
