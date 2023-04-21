import requests
import zipfile
import json
import io
import xmltodict

# Télécharger le fichier zip
url = "https://api.opendata.onisep.fr/tmp/d1/aa/f8ec0c12fcb8e7908dde50613b44/ideo-fiches_formations.zip"
response = requests.get(url)

# Extraire le fichier XML du zip
with zipfile.ZipFile(io.BytesIO(response.content)) as myzip:
    with myzip.open(myzip.namelist()[0]) as myfile:
        data_dict = xmltodict.parse(myfile.read())

# Convertir le fichier XML en JSON
json_data = json.dumps(data_dict)
with open("assets/formation/data.json", "w") as json_file:
    json_file.write(json_data)
