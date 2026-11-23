# AURA-009 · CAO de table r03

Le document Fusion r03 est enregistré en version 2, avec le faisceau raccordé. Le fichier [AURA-009_Table_r03.f3d](AURA-009_Table_r03.f3d) est la référence éditable. Le [STEP](AURA-009_Table_r03.step) représente le robot à HOME. Les dossiers [STL](STL) et [3MF PETG](Plateaux_PrusaSlicer) contiennent les pièces, les plateaux de comparaison et trois coupons.

- [Nomenclature CSV](Nomenclature_r03.csv) · [Inventaire géométrique et empreintes](Inventaire_CAO_r03.json)
- [Vérifications des poses et câbles](Verification_Mouvements_r03.json) · [Butées et dépose](Verification_Assemblage_r03.json) · [Pouce](Verification_Pouce_r03.json)
- [Tranchage](Verification_Tranchage_r03.json) · [Réimport de l’archive](Verification_Sauvegarde_r03.json) · [Vues d’inspection](../../docs/wireframes/r03/08_controle_tous_les_angles.png)
- [Notice d’assemblage](../../docs/ASSEMBLAGE_R03.md) · [Rapport de correction](../../RAPPORT_AMELIORATIONS_R03.md)

## Régénération

Dans Fusion, exécuter le point d’entrée de **construire_table_r03.py** depuis un document de travail. Les modules hérités proviennent de la r02 et de ses générateurs de géométrie. Dans le dépôt, ils peuvent se trouver dans **sources_heritage** sous les noms de leur arborescence d’origine. Placer le STEP XC330 constructeur à côté de ces modules sous **sources_heritage/XC330_ROBOTIS.step**. Empreinte du fichier de référence **e2f7b060801a1d6a21f23bca2554f29a402f7d73b8498cb201c9e6adf3139eb6**. [Plan constructeur](https://emanual.robotis.com/docs/en/dxl/x/xc330-m288/#drawings)

1. Exécuter les contrôles dans **verification_table_r03.py** sur le nouveau document. Les conditions et les résultats de chaque pose sont écrits en JSON.
2. Appeler **export_all**, puis **export_step** dans **livrables_table_r03.py**. La source des rendus est une tessellation de la scène Fusion à HOME.
3. Exécuter **trancher_table_r03.py** avec le chemin du binaire PrusaSlicer. Vérifier le G-code en répertoire temporaire. Le profil virtuel doit être adapté à l’imprimante et au filament retenus.
4. Exécuter **rendre_table_r03.py** dans Blender en mode arrière-plan, avec la racine du projet passée après le séparateur d’arguments **--**.

Le fichier Fusion intègre une esquisse et une extrusion pilotées de la platine. Le reste des organes reprend des fonctions de base avec composants distincts, cotes de génération et liaisons natives.
