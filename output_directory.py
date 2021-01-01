import nest_asyncio
nest_asyncio.apply()
import pydra
import attr

cmd = "echo"

my_input_spec = pydra.specs.SpecInfo(
        name="Input",
        fields=[
            (
                "outputFile",
                attr.ib(
                    type=pydra.specs.Directory,
                    metadata={"help_string": "The name of a file to be created."},
                ),
            )
        ],
        bases=(pydra.specs.ShellSpec,),
    )

my_output_spec = pydra.specs.SpecInfo(
        name="Output",
        fields=[
            (
                "outputFile",
                attr.ib(
                    type=pydra.specs.File,
                    metadata={
                        "help_string": "The output file",
                        "output_file_template": "{outputFile}"
                    },
                ),
            ),
        ],
        bases=(pydra.specs.ShellOutSpec,),
    )



shelly = pydra.ShellCommandTask(name="shelly", executable=cmd, input_spec=my_input_spec, output_spec=my_output_spec)
shelly.inputs.outputFile = "{shelly.inputs.outputFile}/out_file.txt"

print("cmndline = ", shelly.cmdline)

with pydra.Submitter(plugin="cf") as sub:
    sub(shelly)
shelly.result()
