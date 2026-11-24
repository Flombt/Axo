# Réorganisation et maintenance d’AURA-01

**24 novembre 2026 · V5-roulis-v1**

Le dossier accueille une seule révision principale. La CAO active est **fusion/AURA-01.f3d**, avec le même SHA-256 que l’archive V5 roulis auditée. Les 154 occurrences, 31 pivots et 20 liens ont été relus dans Fusion après réimport du fichier déplacé. Le document hébergé est resté en v1 et présente zéro composant référencé et zéro fichier enfant. Les exports et le firmware V5 restent à produire après corrections. [État de la version](../VERSION.md) · [Diagnostic avant fabrication](../DIAGNOSTIC_ROBOT_COMPLET.md)

## Ancienne et nouvelle organisation

| Ancien emplacement | Nouvel emplacement |
|---|---|
| Exports_Fusion pour toutes les générations | [Source active Fusion](../fusion/README.md) et [archives par révision](../archives/README.md) |
| manufacturing/anycubic et manufacturing/r05 | [Anycubic r04](../archives/r04/anycubic/README.md) et [Anycubic r05](../archives/r05/anycubic/README.md) |
| Firmware r05 au premier niveau | [État actif](../firmware/README.md) et [code r05 historique](../archives/r05/firmware/README.md) |
| Montage r02, documents de fabrication et notes d’achat éparses | [Montage actif](../assembly/README.md), [achats](../purchases/NOMENCLATURE.md) et archives r02 à V5 revue |
| Rendus, animations et anciens diagnostics à plusieurs niveaux | [Vues V5](diagnostic/latest/wireframes/), diagnostic V5 à la racine, [r02](../archives/r02/README.md) et [r03](../archives/r03/README.md) |
| Règles et documentation de reprise dispersées | [AGENTS.md](../AGENTS.md), [VERSION.md](../VERSION.md), [CHANGELOG.md](../CHANGELOG.md) et [contexte](architecture/PROJECT_CONTEXT.md) |

Le coffre Obsidian reste au même emplacement pour conserver ses liens et réglages de travail. Son tableau de bord et son contexte renvoient à la source active. Le dossier principal contient des fichiers actuels, des preuves datées et des documents de travail aux différents états. Les dossiers de production bloqués donnent leurs conditions d’ouverture. Les dossiers temporaires sur D: sont extérieurs au périmètre de déplacement.

**Déplacements exécutés** — 807 fichiers, dont le F3D actif, le premier diagnostic, les kits et les archives natives. **GitHub** — 10 fichiers absents du dossier local ont été restaurés. 62 autres objets GitHub manquants correspondaient à des exemplaires locaux de même empreinte et ont été associés à leurs chemins conservés. Le [manifeste](../archives/INDEX_REORGANISATION.csv) conserve le chemin initial, le nouveau chemin et le SHA-256 initial. Les originaux précédant les corrections de liens sont conservés dans la sauvegarde locale.

## Nettoyage vérifié et restauration

- **116 projets Anycubic de transfert** ont été identifiés par empreinte SHA-256 et remplacés par les 116 correspondances vers les fichiers historiques canoniques. Le test de reconstruction USB a restauré et validé les 116 fichiers. Volume logique des copies retirées **147 466 846 octets**.
- **Quatre vidéos r03**, **722 724 558 octets**, sont reprises par la release r03. Les SHA-256 et tailles des exemplaires correspondaient aux métadonnées GitHub. Chaque URL a renvoyé une plage valide commençant par l’en-tête MP4. La vidéo de rotation a été restaurée entièrement et vérifiée par SHA-256. [Release](https://github.com/Flombt/Axo/releases/tag/aura-009-r03-v2-cinematique) · [Manifeste](../archives/RESTORE_ASSETS.json)
- **8 caches Python** ont été retirés après vérification du fichier source homonyme. Les sauvegardes uniques, dont l’état Blender local distinct, sont conservées. Les réglages de session et l’archive de secours locale sont ignorés par Git.
- Le fichier local **archives/.local/avant-reorganisation.zip** contient l’inventaire initial, le plan de migration et les versions originales des documents dont les liens ont été réécrits, dont le premier diagnostic. L’archive a passé son contrôle d’intégrité. Les fichiers déplacés et récupérés ont été rapprochés de leurs empreintes. [Index de restauration](../archives/README.md)

## Volumes mesurés

Mesure du contenu utile du dossier Aura après l’audit, avant et après la migration. Le relevé exclut les métadonnées Git et les fichiers temporaires extérieurs, et inclut la sauvegarde locale interne. Les unités reflètent la taille logique des fichiers. OneDrive, les copies déjà présentes hors du projet et le stockage Git influent sur l’espace effectivement alloué.

| Mesure | Avant | Après |
|---|---:|---:|
| Fichiers | 1 051 | 962 |
| Dossiers sous Aura | 122 | 136 |
| Taille logique | 1 545 198 394 octets | 677 368 327 octets |

**Réduction nette du dossier** — **867 830 067 octets (827,63 Mio)**. Les copies USB et vidéo retirées représentent ensemble **870 191 404 octets**. Les dossiers de manifeste et le regroupement par version expliquent la hausse du nombre de dossiers. Les documents ajoutés et les objets rapatriés expliquent l’écart entre les volumes. Les doublons historiques restants servent notamment aux kits, sources et dossiers de restauration conservés.

## Dépendances et maintenance

- 309 liens locaux ou historiques ont été convertis par la migration dans 42 documents. Les cas restants ont été relus. L’image de l’état initial du cahier des charges renvoie à son exemplaire dans le coffre.
- Les lectures du firmware r05, les graphiques du diagnostic et les comparaisons de vues r03 utilisent les chemins d’archives. Le comparatif historique et les huit graphiques ont été recalculés. Le code MicroPython r05 et l’état de la CAO sont inchangés.
- Le [vérificateur](../tools/verifier_projet.py) contrôle les liens, le manifeste, les fichiers manquants, les signatures, les exports et commandes périmés, les doublons et les caches en lecture seule. Le mode **--complet** couvre les archives. Il a contrôlé 92 documents sans erreur de lien et relevé deux états techniques ouverts. Les 64 scripts Python passent la lecture syntaxique. La création d’un kit ou d’un firmware de production exige une révision et des empreintes déclarées dans le [manifeste courant](architecture/revision.json).
- Le dossier Aura est relié à l’historique **main** de Flombt/Axo, à partir de l’ancienne tête **ecc2308ec4521cbc6c49ad148433d983fa783578**. Cette tête reçoit le point de reprise **aura-01-r05-budget-edition**. Les tags r03/r04 préexistants restent les points d’accès à leurs révisions.

**Anomalies ouvertes de la version** — dossier de fabrication V5 et firmware V5 à produire. Le budget complet et les validations physiques restent ouverts. Les étapes de fermeture figurent dans le [rapport d’audit](../DIAGNOSTIC_ROBOT_COMPLET.md#16-verdict-avant-fabrication).
