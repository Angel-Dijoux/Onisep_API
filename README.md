# Onisep API
⚠️ Cette API n'est pas une API offcielle de l'[onisep](https://www.onisep.fr/)

---

![](https://arago.paysdelaloire.e-lyco.fr/wp-content/uploads/2019/11/Logotype_Onisep_Horizontal_RVB.png)

L'API Onisep vous fournis une authentification avec token JWT, et la posibilité d'enregistrer des liens onisep, elle sert dans le cadre des applications React et React Native reconstruite de l'Onisep.

[![License](https://img.shields.io/packagist/l/dingo/api.svg?style=flat-square)](LICENSE)
[![StyleCI](https://github.styleci.io/repos/512832807/shield?branch=main)](https://github.styleci.io/repos/512832807?branch=main)
[![Build](https://img.shields.io/github/actions/workflow/status/Angel-Dijoux/Onisep_API/deployment.yml?style=flat-square)]()
[![Status](https://github.com/Angel-Dijoux/Onisep_API/actions/workflows/status.yml/badge.svg?event=status)](https://github.com/Angel-Dijoux/Onisep_API/actions/workflows/status.yml)


## Fonctionnalités

Cette API fournit : 

 - L'enregistrement d'un utilisateur
 - Connexion d'un utilisateur
 - Une authentification avec token JWT
 - rafraichissement du token JWT
 - Enregistrement d'une formation *(pour les formations favorites)*
 
 ## Usages
 
 Cloner le repositorie
 ``` 
 gh repo clone Angel-Dijoux/Onisep_API && cd Onisep_API
 ```
 ### Sans docker
 Lancer l'environnement virtuel python
 ```
 source /onisep_api/bin/activate
 ```
 Installer les modules
 
``` 
pip install -r requirement.txt
```
 
 Lancer le serveur flask
 ```
 flask run -h 0.0.0.0 -p 5005
 ```
 Vous avez un serveur SQL remplacez ``` sqlite:///onisepapi.db ``` par ```mysql+mysqlconnector://{username}:{password}@{host}/{database} ``` dans [.flaskenv](.flaskenv)
 ### Avec docker
 ```
 docker-compose up -d
 ```
 Vous avez un serveur SQL remplacez ``` sqlite:///onisepapi.db ``` par ```mysql+mysqlconnector://{username}:{password}@{host}/{database} ``` dans [docker-compose.yml](docker-compose.yml)
 
 
 l'API est maintenant disponible sur http://localhost:5005
 
 ### En production 

Générez un clé secrète comme ceci :
```
$ python -c 'import secrets; print(secrets.token_hex())' 
a4ecf55f5ef3b9943ab655939d5637b92fbcad2037af231fcc7d0946dac280ae
```
Et remplacez ```mysecretkey``` par la clée obtenue dans [.env](.env) ou [docker-compose.yml](docker-compose.yml)

Enfin remplacez ``` development ``` par ``` production ``` dans [.flaskenv](.flaskenv) ou [docker-compose.yml](docker-compose.yml)
 
 Docker repositorie : https://hub.docker.com/r/elki97413/onisepapi

 
 ## Licence 
 
 Cette API est sous licence [BSD 3-Clause license](http://opensource.org/licenses/BSD-3-Clause).
 
