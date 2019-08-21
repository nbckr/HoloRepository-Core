import json
import logging
from datetime import datetime
from os import path

import requests

from config import HOLOSTORAGE_ACCESSOR_HOST, HOLOSTORAGE_ACCESSOR_PORT
from jobs.jobs_io import get_result_file_path_for_job

# Note: Could be refactored such that more data is kept in job-specific temp
# directories and less stuff has to be handed from component to component.

holostorage_baseurl = f"{HOLOSTORAGE_ACCESSOR_HOST}:{HOLOSTORAGE_ACCESSOR_PORT}"
holograms_endpoint = f"{holostorage_baseurl}/api/v1/holograms"


def send_file_request_to_accessor(job_id: str, plid: str, medical_data: dict):
    output_file_path = get_result_file_path_for_job(job_id)
    file_size_in_kb = int(path.getsize(output_file_path) / 1024)

    meta_data = create_meta_data(file_size_in_kb, plid)
    request_body = {**medical_data, **meta_data}

    # Stringify nested dicts
    request_body["patient"] = json.dumps(request_body["patient"])
    request_body["author"] = json.dumps(request_body["author"])

    # Just by including files, requests will set 'Content-Type' to 'multipart/form-data
    files = {"hologramFile": open(output_file_path, "rb")}

    response = requests.post(holograms_endpoint, data=request_body, files=files)

    if response.status_code == 200:
        logging.info(f"Success! Created hologram: {response.json()}")
        return True
    else:
        raise Exception(f"Failed to created hologram: {response.json()}")


def create_meta_data(file_size_in_kb: int, plid: str):
    """
    Returns a dict with the metadata fields defined HoloStorageAccessor API v1.1.0
    (fileSizeInKb, creationDate, creationDescription, contentType, creationMode)
    """
    return {
        "fileSizeInKb": file_size_in_kb,
        "creationDate": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "contentType": "model/gltf-binary",
        "creationDescription": f"Generated by HoloPipelines with the {plid} pipeline",
        "creationMode": "GENERATE_FROM_IMAGING_STUDY",
    }