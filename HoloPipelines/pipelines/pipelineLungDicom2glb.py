from components import compCommonPath
from components import compDicom2nifti
from components.lungSegment.main import main as lungSegment
from components import compNifti2numpy
from components import compNumpy2obj
from components import compObj2glbWrapper
import pathlib
import sys


def main(dicomPath, outputGlbPath):
    generatedNiftiPath = compDicom2nifti.main(
        str(dicomPath),
        str(compCommonPath.nifti.joinpath(str(pathlib.PurePath(dicomPath).parts[-1]))),
    )  # convert dcm and move to temp path inside nifti folder. nifti will be in a sub folder named after the input dicom folder
    generatedSegmentedLungsNiftiPath = lungSegment(
        generatedNiftiPath, str(compCommonPath.nifti.joinpath("segmentedLungs"))
    )
    generatedNumpyList = compNifti2numpy.main(
        str(pathlib.Path(generatedSegmentedLungsNiftiPath).joinpath("lung.nii.gz"))
    )
    generatedObjPath = compNumpy2obj.main(
        generatedNumpyList,
        0.5,
        str(compCommonPath.obj.joinpath("nifti2glb_tempObj.obj")),
    )
    generatedGlbPath = compObj2glbWrapper.main(
        generatedObjPath,
        str(pathlib.Path(outputGlbPath)),
        deleteOriginalObj=True,
        compressGlb=False,
    )
    print("lungDicom2glb: done, glb saved to {}".format(generatedGlbPath))


if __name__ == "__main__":
    main(str(sys.argv[1]), str(sys.argv[2]))
