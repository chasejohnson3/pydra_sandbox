import nest_asyncio
nest_asyncio.apply()

import pydra
import attr
import re

cmd = "echo"
args = ["newfile_1.txt", "newfile_2.txt"]

def get_file_index(stdout):
    stdout = re.sub(r'.*_', "", stdout)
    stdout = re.sub(r'.txt', "", stdout)
    print(stdout)
    return int(stdout)

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
            "out_file_index",
            attr.ib(
                type=int,
                metadata={
                    "help_string": "output file",
                    "callable": get_file_index,
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
print(shelly.result())
#results = shelly.result()
#for result in results:
#    print(result.output.stdout)
