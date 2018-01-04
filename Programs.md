# Programmes

## Objectif :

Un programme démon qui éxécute des programmes à des dates et heures précises. Ces programmes sont définis dans un fichier fbatch.

## Programme 1 : Main.py

Ce programme est le coeur du système. C'est lui qui lance le programme démon.

## Programme 2 : ExecProgram.py

Ce programme lance un progamme du fichier fbatch en fonction des paramètres.

## Programme 2 : UpdateFbatchFile.py

Ce programme met à jour le fichier fbatch à chaque éxécution de la commande `pgcycl`.

### Nécéssite : 

- Un parser pour la commande `pgcycl` afin d'identifier tous les paramètres.
- Une écriture dans le fichier