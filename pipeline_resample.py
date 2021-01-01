import pydra
from pathlib import Path
import nest_asyncio
import time
from shutil import copyfile

import attr
from nipype.interfaces.base import (
    Directory,
    File,
)
from pydra import ShellCommandTask
from pydra.engine.specs import SpecInfo, ShellSpec

from registration import BRAINSResample
from segmentation.specialized import BRAINSConstellationDetector

@pydra.mark.task
def append_filename(filename="", appended_str="", extension="", directory=""):
    new_filename = f"{Path(Path(directory) / Path(Path(filename).with_suffix('').with_suffix('').name))}{appended_str}{extension}"
    return new_filename 

@pydra.mark.task
def copy_from_cache(cache_path, output_dir):
    copyfile(cache_path, Path(output_dir) / Path(cache_path).name)

if __name__ == "__main__":
    # This serves as an example input a pipeline may be given
    subject1_json = {
        "in": {
          "t1":             "/localscratch/Users/cjohnson30/BCD_Practice/t1w_examples2/sub-066260_ses-21713_run-002_T1w.nii.gz", 
          "templateModel":  "/Shared/sinapse/CACHE/20200915_PREDICTHD_base_CACHE/Atlas/20141004_BCD/T1_50Lmks.mdl",
          "llsModel":       "/Shared/sinapse/CACHE/20200915_PREDICTHD_base_CACHE/Atlas/20141004_BCD/LLSModel_50Lmks.h5",
          "landmarkWeights":"/Shared/sinapse/CACHE/20200915_PREDICTHD_base_CACHE/Atlas/20141004_BCD/template_weights_50Lmks.wts",
          "landmarks":      "/Shared/sinapse/CACHE/20200915_PREDICTHD_base_CACHE/Atlas/20141004_BCD/template_landmarks_50Lmks.fcsv",
        },
        "out": {"output_dir": "/localscratch/Users/cjohnson30/output_dir"},
    }
    subject2_json = {
        "in": {
          "t1":             "/localscratch/Users/cjohnson30/BCD_Practice/t1w_examples2/sub-066217_ses-29931_run-003_T1w.nii.gz", 
          "templateModel":  "/Shared/sinapse/CACHE/20200915_PREDICTHD_base_CACHE/Atlas/20141004_BCD/T1_50Lmks.mdl",
          "llsModel":       "/Shared/sinapse/CACHE/20200915_PREDICTHD_base_CACHE/Atlas/20141004_BCD/LLSModel_50Lmks.h5",
          "landmarkWeights":"/Shared/sinapse/CACHE/20200915_PREDICTHD_base_CACHE/Atlas/20141004_BCD/template_weights_50Lmks.wts",
          "landmarks":      "/Shared/sinapse/CACHE/20200915_PREDICTHD_base_CACHE/Atlas/20141004_BCD/template_landmarks_50Lmks.fcsv",
        },
        "out": {"output_dir": "/localscratch/Users/cjohnson30/output_dir"},
    }  
    
    nest_asyncio.apply()

    # Create the inputs to the workflow
    wf = pydra.Workflow(name="wf", 
                        input_spec=["t1", "templateModel", "llsModel", "landmarkWeights", "landmarks", "output_dir"], 
                        output_spec=["output_dir"])
    
    wf.split("t1", t1=[subject1_json["in"]["t1"], subject2_json["in"]["t1"]])
#t1=["/localscratch/Users/cjohnson30/BCD_Practice/t1w_examples2/sub-066260_ses-21713_run-002_T1w.nii.gz",
#                       "/localscratch/Users/cjohnson30/BCD_Practice/t1w_examples2/sub-066217_ses-29931_run-003_T1w.nii.gz"])

    print(wf.inputs.t1)
    # Set the inputs of Resample
    resample = BRAINSResample("BRAINSResample").get_task()
    resample.inputs.inputVolume =       wf.lzin.t1 #wf.BRAINSConstellationDetector.lzout.outputResampledVolume
    resample.inputs.interpolationMode = "Linear"
    resample.inputs.pixelType =         "binary"
    resample.inputs.referenceVolume =   "/localscratch/Users/cjohnson30/resample_refs/t1_average_BRAINSABC.nii.gz" 
    resample.inputs.warpTransform =     "/localscratch/Users/cjohnson30/resample_refs/atlas_to_subject.h5"
    resample.inputs.outputVolume =      "out.nii.gz"#wf.resampledOutputVolumeName.lzout.out 
#    resample.split(("intputVolume")) 
    wf.add(resample)

    # Set the outputs of the entire workflow
    wf.set_output(
        [
           ("resampledOutputVolume",             wf.BRAINSResample.lzout.outputVolume),
        ]
    )
   
    t0 = time.time() 
    # Run the pipeline
    with pydra.Submitter(plugin="cf") as sub:
        sub(wf)
    result = wf.result()
    print(result)
    print(f"total time: {time.time() - t0}")
