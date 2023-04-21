import requests
import zipfile
import json
import io
import os
import xmltodict
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(message)s")

# Télécharger le fichier zip
url = "https://api.opendata.onisep.fr/tmp/d1/aa/f8ec0c12fcb8e7908dde50613b44/ideo-fiches_formations.zip"
response = requests.get(url)


# Extraire le fichier XML du zip
def extract_xml(response: requests) -> dict:
    with zipfile.ZipFile(io.BytesIO(response.content)) as myzip:
        with myzip.open(myzip.namelist()[0]) as myfile:
            logging.debug("File {} is extract to .XML.".format(myzip.namelist()[0]))
            return xmltodict.parse(myfile.read())


# Convertir le fichier XML en JSON
def convert_to_xml_to_json(xml: dict) -> bool:
    json_data = json.dumps(xml)
    filename = "data.json"
    path = "assets/formation/"
    try:
        with open(path + filename, "w") as json_file:
            json_file.write(json_data)
            logging.debug(
                "File {} is write in {}".format(
                    filename, os.path.abspath(path + filename)
                )
            )
            return True
    except Exception:
        logging.debug("Error in convert : " + Exception)
        return False


if __name__ == "__main__":
    convert_to_xml_to_json(extract_xml(response))
