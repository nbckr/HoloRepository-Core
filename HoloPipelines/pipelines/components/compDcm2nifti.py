import dicom2nifti
import os


def main(dicom_input_path, output_nifti_folder_path):
    # check if sub dirs exist
    if not os.path.exists(output_nifti_folder_path):
        os.makedirs(output_nifti_folder_path)
    # convert series of dicom to nifti
    dicom2nifti.convert_directory(dicom_input_path, output_nifti_folder_path)
    print("dcm2nifti: done")
    return output_nifti_folder_path


if __name__ == "__main__":
    print("component can't run on its own")
