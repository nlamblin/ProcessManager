# Programmes

## Objectif :

Un programme démon qui éxécute des programmes à des dates et heures précises. Ces programmes sont définis dans un fichier fbatch.

## Programme 1 : gobatch.py

Ce programme lance un progamme du fichier fbatch en fonction des paramètres

## Programme 2 : install.py

Ce programme permet l'installation du démon sur le système. Une fois lancé il va demandé de renseigner des informations afin de configurer le démon.

https://openclassrooms.com/courses/faire-un-demon-sous-linux

## Programme 3 : updateFbatchFile.py

Ce programme met à jour le fichier fbatch à chaque éxécution de la commande `pgcycl`.

### Nécéssite : 
- Un parser pour la commande `pgcycl` afin d'identifier tous les paramètres.
- Une écriture dans le fichier