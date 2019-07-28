# Holo FHIR Tool
A tool that generates FHIR schema for HoloRepository and also inserts it into a FHIR API server.

This uses an Azure FHIR server created from the following [deployment template](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FMicrosoft%2Ffhir-server%2Fmaster%2Fsamples%2Ftemplates%2Fdefault-azuredeploy-sql.json).

Security is disabled for development with the following additional parameter during spin up.
- "FhirServer:Security:Enabled": false

## Installation
Install using `pipenv install` or `pip install -r requirements.txt`.

## Usage
Usage:
    fhir_interactions.py --base-url <FHIR_SERVER_URL> delete-all
    fhir_interactions.py --base-url <FHIR_SERVER_URL> upload-bundle <FHIR bundle file>
    fhir_interactions.py --base-url <FHIR_SERVER_URL> upload-folder <FHIR bundle directory>

Options:
    --base-url      the base url of the fhir server needs to be provided (e.g. https://fhirserver.azurewebsites.net)
    delete-all      delete all resources on the fhir server
    upload-bundle   upload a single FHIR bundle json file
    upload-folder   upload all FHIR bundles stored within a folder
