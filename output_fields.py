import nest_asyncio
nest_asyncio.apply()

import pydra
import attr

cmd = "echo"
args = ["newfile_1.txt", "newfile_2.txt"]

my_output_spec = pydra.specs.SpecInfo(
    name="Output",
    fields=[
        (
            "out1",
            attr.ib(
                type=pydra.specs.File,
                metadata={
                    "output_file_template": "{args}",
                    "help_string": "output file",
                },
            ),
        ),
        (
            "out_len",
            attr.ib(
                type=pydra.specs.Int,
                metadata={
                    "help_string": "output file",
                    "value": "3",
                },
            ),    
        )
    ],
    bases=(pydra.specs.ShellOutSpec,),
)


shelly = pydra.ShellCommandTask(name="shelly", executable=cmd, args=args, output_spec=my_output_spec).split("args")

print("cmndline = ", shelly.cmdline)

with pydra.Submitter(plugin="cf") as sub:
    sub(shelly)
shelly.result()
