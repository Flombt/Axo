# Archives AURA-01

Le développement quotidien part de la [version active](../VERSION.md). Chaque dossier ci-dessous contient la documentation et le point de reprise de sa révision. Les fichiers lourds publiés peuvent être récupérés à la demande.

| Révision ou branche | Contenu |
|---|---|
| [V1](v1/README.md) | Assemblage final v5 et références internes |
| [V2](v2/README.md) | Squelette articulé, prototype motorisé AURA-004 et coupons |
| [V3](v3/README.md) | Grande V3, fabrication, intégration mécatronique et sauvegardes |
| [AURA-007](aura-007/README.md) et [AURA-008](aura-008/README.md) | Bancs et prototypes de table |
| [r02](r02/README.md) | Notice, premier diagnostic et kit Nano |
| [r03](r03/README.md) | Appuis portés, faisceau, animation et restauration des vidéos |
| [r04](r04/README.md) | Rotation continue et main à cinq commandes |
| [r05](r05/README.md) | Budget Edition, kit multimachines et firmware Pico |
| [V5 revue](v5-revue/README.md) | Variante parent immédiate de la V5 roulis |
| [Documents de gestion](gestion/README.md) | Cahier historique, démarrage et publication antérieure |

L’[index des chemins et empreintes](INDEX_REORGANISATION.csv) indique où retrouver chaque fichier déplacé, dédupliqué ou rapatrié. Le [manifeste de restauration](RESTORE_ASSETS.json) identifie les **116** projets du miroir USB et les **quatre** vidéos r03. Avec Python 3.11 ou plus récent, utiliser [restaurer_archive.py](../tools/restaurer_archive.py) avec **--miroir-usb** ou **--video NOM** et **--destination DOSSIER**. La restauration vérifie tailles et SHA-256 et refuse les fichiers déjà présents. Les seuls dossiers de sauvegarde locale sont réservés à la restauration, avec la [procédure et les vérifications](../docs/REORGANISATION_PROJET.md).
