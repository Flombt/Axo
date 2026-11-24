# AURA-01 — Préparation industrielle du kit d'impression 3D Anycubic

## 1. Contexte de la mission

Tu viens de terminer les modifications mécaniques du bras robotique AURA-01 dans Fusion 360, notamment l'optimisation de sa conception, l'indépendance des cinq doigts et l'amélioration de la rotation du socle.

Nous allons désormais passer de la conception numérique à la préparation de la fabrication physique du robot.

Pars de la dernière révision du modèle et de ses résultats de validation. Vérifie néanmoins que les corrections précédentes sont effectivement présentes et qu'aucun problème bloquant de conception n'a été laissé de côté.

J'ai installé le logiciel de tranchage Anycubic sur mon ordinateur. Je souhaite que tu utilises Computer Use pour interagir directement avec ce logiciel, identifier les imprimantes disponibles et préparer l'intégralité des plateaux d'impression.

Je veux obtenir un kit de fabrication complet, organisé, optimisé et directement exploitable.

## 2. Identification de mon environnement d'impression

Utilise Computer Use pour ouvrir le logiciel Anycubic installé sur mon ordinateur.

Identifie précisément le logiciel et sa version, les imprimantes configurées, les profils disponibles, les dimensions utiles des plateaux, les diamètres de buse, les matériaux disponibles et les éventuelles restrictions propres à chaque machine.

Ne suppose pas que toutes les imprimantes Anycubic disposent des mêmes caractéristiques.

Si plusieurs imprimantes sont disponibles, analyse leurs différences et répartis intelligemment les pièces entre elles.

Ne confonds pas une imprimante simplement présente dans la liste des profils avec une imprimante que je possède réellement. Si cette information est impossible à déterminer, signale-le avant d'attribuer définitivement les plateaux.

Utilise les véritables profils des machines plutôt que des profils génériques lorsque cela est possible.

## 3. Vérification préalable du modèle final

Avant de préparer les impressions, vérifie une dernière fois la cohérence de la version finale du robot.

Assure-toi que les fichiers STL correspondent exactement au dernier modèle Fusion 360.

Vérifie que les modifications concernant les doigts indépendants, la rotation du socle, les articulations, les moteurs, les systèmes de fixation et les chemins de câbles sont présentes dans les exports.

Ne mélange pas les pièces provenant de différentes révisions.

Vérifie que les anciens problèmes mécaniques identifiés dans `DIAGNOSTIC_ROBOT.md` et `VALIDATION_FABRICATION.md` ont été traités ou clairement documentés.

Si un problème bloquant subsiste, ne prépare pas les pièces concernées comme si elles étaient définitivement validées.

## 4. Inventaire exhaustif des pièces

Recense l'intégralité des pièces devant être imprimées en 3D.

Pour chaque pièce, identifie son nom, sa référence, sa quantité nécessaire, ses dimensions, son rôle mécanique, son matériau recommandé et ses contraintes de fabrication.

Distingue les pièces uniques des pièces devant être imprimées plusieurs fois.

Vérifie qu'aucun élément nécessaire à l'assemblage n'a été oublié.

Sépare les composants imprimables des composants à acheter, tels que les moteurs, les roulements, les vis, les inserts, les axes et les éléments électroniques.

Crée un inventaire permettant de suivre la fabrication du robot sans ambiguïté.

## 5. Conversion des fichiers STL en 3MF

Convertis l'ensemble des fichiers STL de la dernière révision en fichiers 3MF compatibles avec le logiciel Anycubic installé.

Préserve les dimensions exactes, les proportions, l'échelle et la géométrie de chaque pièce.

Vérifie systématiquement que les unités correspondent aux millimètres attendus.

Je souhaite disposer de deux catégories de fichiers :

- Des fichiers 3MF individuels pour pouvoir réimprimer une pièce spécifique si elle casse ou si elle présente un défaut.
- Des projets 3MF complets contenant plusieurs pièces déjà positionnées et configurées sur les plateaux.

Les projets de plateaux doivent conserver, dans la mesure permise par le logiciel, le profil d'imprimante, le matériau, les orientations, les supports et les paramètres d'impression.

Ne réalise pas une simple conversion de format sans configuration du projet.

## 6. Vérification individuelle de l'imprimabilité

Importe chaque pièce dans le logiciel de tranchage et vérifie sa faisabilité réelle.

Analyse les éléments suivants :

- Intégrité du maillage.
- Dimensions compatibles avec le volume d'impression.
- Épaisseurs minimales.
- Parois trop fines.
- Petits détails susceptibles de disparaître.
- Porte-à-faux.
- Ponts difficiles à imprimer.
- Risques de déformation.
- Risques de décollement du plateau.
- Cavités et supports impossibles à retirer.
- Résistance mécanique dans la direction des couches.
- Précision des logements de moteurs.
- Précision des trous, axes et logements de roulements.
- Accessibilité des passages de câbles et de tendons.

Utilise la prévisualisation des couches après tranchage pour contrôler les zones critiques.

Vérifie particulièrement les phalanges, les points de fixation des moteurs, les supports des articulations, les passages de tendons et les composants du socle rotatif.

Si une pièce présente un défaut de conception incompatible avec une impression fiable, retourne dans Fusion 360 pour la corriger si cela est possible sans compromettre les autres composants.

Régénère ensuite les exports et réalise une nouvelle vérification.

## 7. Optimisation de l'orientation des pièces

Détermine individuellement la meilleure orientation d'impression pour chaque pièce.

Ne privilégie pas automatiquement l'orientation qui utilise le moins de supports.

Prends également en compte la résistance aux efforts mécaniques, l'adhérence au plateau, la précision dimensionnelle, la qualité des surfaces fonctionnelles, le sens des couches et la facilité de retrait des supports.

Les articulations porteuses, les supports de moteurs et les phalanges doivent recevoir une attention particulière.

Une pièce imprimée rapidement mais fragile dans sa direction principale de sollicitation constitue un mauvais résultat.

Documente les orientations retenues pour les composants critiques.

## 8. Optimisation de l'espace sur les plateaux

Utilise Computer Use pour organiser directement les pièces dans Anycubic Slicer.

Je souhaite exploiter au maximum la surface utile de chaque plateau afin de réduire le nombre de cycles d'impression et les manipulations manuelles.

Compare plusieurs dispositions, rotations et regroupements de pièces.

Utilise les fonctions de disposition automatique lorsqu'elles sont pertinentes, puis améliore manuellement les résultats si nécessaire.

Vérifie que les pièces ne se chevauchent pas et que les supports, les bordures d'adhérence, les zones d'exclusion et les marges de sécurité sont également pris en compte.

Ne surcharge pas artificiellement les plateaux au détriment de la fiabilité.

Évite de regrouper des pièces nécessitant des matériaux ou des paramètres incompatibles.

Évite également de placer toutes les pièces critiques sur un unique plateau très long si une défaillance locale risque de compromettre une grande partie de la fabrication.

Recherche le meilleur compromis entre :

- Taux d'occupation des plateaux.
- Nombre total de cycles.
- Temps d'impression cumulé.
- Quantité de filament.
- Risque d'échec.
- Qualité mécanique.
- Facilité de récupération des pièces.

Compare les estimations du logiciel pour différentes configurations avant de retenir la meilleure organisation.

## 9. Répartition entre les imprimantes

Si plusieurs imprimantes sont réellement disponibles, optimise la fabrication en parallèle.

Attribue les pièces volumineuses aux machines les mieux adaptées à leur encombrement.

Attribue les pièces petites et précises aux machines et profils présentant les meilleures caractéristiques pour ces composants.

Cherche à réduire le temps total nécessaire pour obtenir l'intégralité du robot, et pas uniquement la durée cumulée des plateaux.

Prépare un planning de fabrication permettant d'utiliser plusieurs imprimantes simultanément lorsque cela est possible.

Chaque fichier 3MF doit clairement indiquer l'imprimante à laquelle il est destiné.

## 10. Optimisation des paramètres d'impression

Analyse les matériaux disponibles et les matériaux recommandés dans la documentation technique du robot.

Le PETG constitue la référence initiale pour les pièces mécaniques, sauf justification technique contraire.

Configure les paramètres selon les caractéristiques réelles de l'imprimante et du filament :

- Hauteur de couche.
- Nombre de périmètres.
- Épaisseur des parois.
- Densité et motif de remplissage.
- Température de buse et de plateau.
- Vitesses et accélérations.
- Ventilation.
- Supports.
- Bordures d'adhérence.
- Paramètres de pontage.
- Compensation dimensionnelle.

Adapte les paramètres localement à chaque pièce lorsque cela est possible.

Une phalange, un capot décoratif et un support moteur ne doivent pas nécessairement utiliser les mêmes paramètres.

Évite d'augmenter systématiquement le remplissage lorsque des périmètres supplémentaires ou une meilleure orientation apportent une solution plus pertinente.

Ne modifie pas les paramètres matériels globaux de mes imprimantes sans justification.

## 11. Création des éprouvettes de validation

Avant l'impression complète du robot, prépare un plateau spécifique contenant les éprouvettes nécessaires pour vérifier les ajustements critiques.

Prévois notamment des tests représentatifs des trous horizontaux et verticaux, des axes de rotation, des inserts métalliques, des logements de roulements, des fixations de moteurs, des passages de tendons et des emboîtements.

Ajoute si nécessaire un doigt complet de test permettant de vérifier la mobilité des phalanges, la transmission du tendon et la qualité des articulations.

Ces éprouvettes doivent être rapides à imprimer et consommer peu de filament.

Fournis une procédure permettant de mesurer les résultats et d'ajuster les tolérances avant la fabrication complète.

## 12. Organisation logique des plateaux

Organise les plateaux selon les véritables sous-ensembles de la nouvelle version du robot.

Utilise, lorsque cela est pertinent, la structure suivante :

- Plateau 00 : éprouvettes et calibration.
- Plateau 01 : socle et structure porteuse.
- Plateau 02 : plateforme rotative et transmission J1.
- Plateau 03 : épaule et premier segment.
- Plateau 04 : coude et avant-bras.
- Plateau 05 : poignet.
- Plateau 06 : paume et supports.
- Plateau 07 : phalanges et doigts.
- Plateau 08 : transmissions indépendantes des doigts.
- Plateau 09 : capots et supports électroniques.

Cette organisation est indicative. Tu peux fusionner ou subdiviser les plateaux si cela améliore réellement la fabrication.

Le nombre final de plateaux doit découler de l'optimisation et des caractéristiques des imprimantes disponibles.

## 13. Tranchage et vérification finale

Tranche réellement chaque plateau avec le logiciel Anycubic.

Inspecte les résultats et les avertissements du logiciel.

Vérifie les premières couches, les surfaces d'appui, les supports, les zones de remplissage, les parois critiques et les éventuelles couches manquantes.

Contrôle les estimations de temps et de consommation de filament.

Réouvre ensuite chaque projet 3MF enregistré afin de confirmer que les pièces, leurs orientations et les paramètres compatibles ont correctement été sauvegardés.

Un plateau ne doit être déclaré prêt numériquement que si son tranchage a effectivement été réalisé et contrôlé.

Ne fabrique aucun résultat fictif.

## 14. Comparaison et optimisation chiffrée

Compare une organisation initiale des pièces avec l'organisation optimisée.

Mesure les différences concernant le nombre de plateaux, le taux d'occupation de la surface utile, le temps d'impression, la consommation de filament, la quantité de supports et le temps total de fabrication avec plusieurs imprimantes.

Utilise uniquement les données réellement obtenues depuis le logiciel de tranchage.

Génère des graphiques permettant de visualiser les économies réalisées.

Si une optimisation augmente légèrement le temps d'impression mais améliore significativement la résistance ou la fiabilité, explique pourquoi elle a été retenue.

## 15. Structure des fichiers de fabrication

Crée un dossier `manufacturing/anycubic/` dans le projet.

Organise-le de la manière suivante :

```text
manufacturing/
└── anycubic/
    ├── README.md
    ├── individual_parts/
    │   ├── base/
    │   ├── arm/
    │   ├── wrist/
    │   └── hand/
    ├── printer_profiles/
    ├── calibration/
    ├── plates/
    │   ├── printer_01/
    │   └── printer_02/
    ├── previews/
    ├── reports/
    ├── graphs/
    ├── inventory.csv
    └── PRINT_CHECKLIST.md
```

Adapte cette structure au nombre réel d'imprimantes.

Les fichiers 3MF individuels et les projets complets doivent être clairement séparés.

Utilise des noms explicites contenant le numéro du plateau, le sous-ensemble concerné, la révision du robot et le modèle d'imprimante.

## 16. Captures d'écran des plateaux

Utilise Computer Use pour réaliser des captures d'écran des véritables plateaux préparés dans Anycubic.

Pour chaque plateau, enregistre une vue supérieure de la disposition des pièces, une vue en perspective et une prévisualisation après tranchage.

Lorsque cela est possible, fais également apparaître les estimations de durée et de filament.

Je veux pouvoir consulter visuellement les plateaux sans devoir ouvrir chaque projet individuellement.

Ne génère pas d'images artificielles représentant des plateaux fictifs. Utilise les véritables résultats du logiciel.

## 17. Rapport final de fabrication

Crée à la racine du dépôt un fichier `RAPPORT_IMPRESSION_3D.md`.

Ce rapport doit contenir les caractéristiques des imprimantes, la révision exacte du robot, l'inventaire des pièces, les corrections effectuées, les paramètres retenus, les résultats du tranchage et les statistiques globales.

Pour chaque plateau, indique :

- Imprimante compatible.
- Liste et quantité des pièces.
- Matériau.
- Temps d'impression estimé.
- Consommation de filament.
- Taux d'occupation.
- Supports nécessaires.
- Difficulté d'impression.
- Risques identifiés.
- Contrôles à effectuer après impression.

Attribue à chaque pièce l'un des statuts suivants : prête numériquement, éprouvette nécessaire, correction nécessaire ou bloquée.

Termine par un verdict clair sur la possibilité de commencer la fabrication.

Ne garantis pas l'absence de défaut physique avant les premières impressions de validation.

## 18. Guide utilisateur de lancement

Crée un README spécifique au kit d'impression, destiné à une personne souhaitant fabriquer AURA-01.

Explique précisément dans quel ordre ouvrir les fichiers 3MF, quelles imprimantes utiliser, quel filament préparer, quels plateaux lancer en premier et quels contrôles réaliser entre les étapes.

Prévois une checklist permettant de cocher les pièces imprimées, contrôlées et prêtes à être assemblées.

Indique également comment réimprimer individuellement une pièce défectueuse.

Je souhaite pouvoir suivre ce guide sans devoir analyser toute la documentation technique du robot.

## 19. Publication GitHub

Ajoute l'intégralité du kit de fabrication au dépôt GitHub existant.

Actualise le README principal avec une section dédiée à l'impression 3D, des liens vers les fichiers 3MF, des captures des plateaux et un résumé des estimations de fabrication.

Préserve les fichiers sources Fusion 360, les anciens rapports et l'historique du projet.

Vérifie les fichiers avant publication, effectue les commits nécessaires et réalise le push sans force push.

## 20. Consignes impératives

Utilise ton niveau de réflexion maximal.

Exécute réellement les opérations dans Fusion 360 et dans le logiciel Anycubic lorsque cela est nécessaire et accessible.

Utilise Computer Use pour contrôler visuellement les dispositions, les paramètres et les résultats de tranchage.

Ne te contente pas de générer des scripts ou des fichiers Markdown décrivant les opérations à réaliser.

Ne lance aucune impression physique, n'envoie aucune tâche aux imprimantes et ne provoque aucun mouvement ou chauffage des machines sans mon autorisation explicite.

Ton rôle est de préparer, optimiser, vérifier et sauvegarder les fichiers.

À la fin de cette mission, je souhaite disposer d'un kit de fabrication AURA-01 complet que je pourrai ouvrir directement dans Anycubic Slicer, avec des plateaux organisés, des paramètres adaptés, des estimations vérifiées et un ordre de fabrication clair.
