import numpy as np
import pydicom as dicom
import os
import scipy.ndimage
import SimpleITK as sitk
import pathlib
import sys
import logging


def load_scan(scan_path):
    slices = [
        dicom.read_file(str(pathlib.Path(scan_path, s)))
        for s in os.listdir(str(scan_path))
    ]
    slices.sort(key=lambda x: int(x.InstanceNumber))
    try:
        slickThickness = np.abs(
            slices[0].ImagePositionscan[2] - slices[1].ImagePositionscan[2]
        )

    except Exception as e:
        logging.warning(
            "Unable to load sclice's image positon, using slice location instead: {}".format(
                str(e)
            )
        )
        slickThickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)

    for s in slices:
        s.SliceThickness = slickThickness

    return slices


def load_pixel_array(input_path):
    reader = sitk.ImageSeriesReader()

    dicomName = reader.GetGDCMSeriesFileNames(input_path)
    reader.SetFileNames(dicomName)

    image = reader.Execute()
    numpyArrayImage = sitk.GetArrayFromImage(image)

    return numpyArrayImage


def resample(data_path, new_spacing=[1, 1, 1]):
    scan = load_scan(data_path)
    image = load_pixel_array(data_path)
    logging.info("Shape before resampling\t", image.shape)
    # Determine current pixel spacing
    try:
        spacing = map(
            float,
            (
                [scan[0].SliceThickness]
                + [scan[0].PixelSpacing[0], scan[0].PixelSpacing[1]]
            ),
        )
        spacing = np.array(list(spacing))
    except Exception as e:
        logging.warn("error in resample data: " + e.message)
        logging.info(len(scan[0].PixelSpacing))
        logging.info(
            "Pixel Spacing (row, col): (%f, %f) "
            % (scan[0].PixelSpacing[0], scan[0].PixelSpacing[1])
        )
        sys.exit("dicom2numpy: error loading scan: {}".format(str(e)))

    # calculate resize factor
    resize_factor = spacing / new_spacing
    new_real_shape = image.shape * resize_factor
    new_shape = np.round(new_real_shape)
    real_resize_factor = new_shape / image.shape
    new_spacing = spacing / real_resize_factor

    image = scipy.ndimage.interpolation.zoom(image, real_resize_factor)
    logging.info("Shape after resampling\t", image.shape)

    return image, new_spacing


def main(dicom_path):
    logging.info("dicom2numpy: resampling dicom...")
    imgs_after_resamp, spacing = resample(dicom_path)
    logging.info("dicom2numpy: resampling done")
    return imgs_after_resamp


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)
    logging.info("component can't run on its own")
