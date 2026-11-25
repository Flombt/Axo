# Contexte court pour un nouvel agent

La révision active **V5-stabilisation** compte quatre axes de bras et cinq doigts commandés par neuf servos. Les deux anciens roulis sont fixes. Le passage axial J1, les nouvelles butées, les rehausses et les ressorts sont intégrés dans Fusion v2. Le kit d’impression et les neuf essais hôte du firmware sont disponibles. [Version](../../../VERSION.md) · [Contexte technique](../../../docs/architecture/PROJECT_CONTEXT.md) · [Rapport des corrections](../../../RAPPORT_CORRECTIONS.md)

Le filament fourni compte pour 0 € au panier. Les **188,74 € TTC provisionnés** dépassent le plafond de 150 € avant devis d’intégration. La qualification commence au montage à blanc et sur charge factice selon la [[08_Tests/MATRICE_TESTS|matrice de validation]]. [Nomenclature](../../../purchases/NOMENCLATURE.md)

Les sections suivantes retracent les versions précédentes.

## Archive · Roulis d’épaule et de coude

[[02_Conception_Fusion/TABLE_V5_ROULIS|Reprise de la V5 approuvée visuellement]] avec deux arbres de roulis, deux MG90S déportés et deux axes indépendants de ±20° et ±24°. Fusion sauvegardé et F3D réouvert. Panier cible de mise au point de 149,48 € TTC. [Achats historiques](https://github.com/Flombt/Axo/blob/aura-01-v5-roulis-v1/purchases/NOMENCLATURE.md)

## Revue design de la V5

[[02_Conception_Fusion/TABLE_V5_REVUE_DESIGN|Variante enregistrée pour validation]] avec neuf servos, dont cinq affectés individuellement aux doigts, un coude affiné et un roulis motorisé. Le panier cible est de 148,98 € TTC livré selon les hypothèses de port. [Achats](../../../archives/v5-revue/ACHATS.md)

## Révision de développement r05

[[02_Conception_Fusion/TABLE_R05|AURA-01 r05 — Budget Edition]], Fusion v2. Six servos de position, Pico USB, socle borné, poignet manuel et cassette évolutive. 47 pièces imprimées et six coupons. Le montage à blanc et la qualification électrique et mécanique forment le prochain volet. [Rapport et budget](../../../archives/r05/OPTIMISATION_BUDGET_R05.md)

## Révision de développement r04

[[02_Conception_Fusion/TABLE_R04|Prototype de table r04]], Fusion v4. Socle motorisé à passage coaxial, cinq commandes indépendantes, 62 pièces de robot et 7 coupons. Les épreuves CAO et le tranchage sont réalisés. Les premiers essais se font au banc. [Rapport de fabrication](../../../archives/r04/VALIDATION_FABRICATION.md) · [Release GitHub](https://github.com/Flombt/Axo/releases/tag/aura-009-r04-fabrication).

Les 3MF individuels et les planches par couleur sont disponibles pour le transfert USB. [Guide des 3MF par couleur](../../../archives/r04/anycubic/README.md).

## Référence historique — Bras V3 de table

Le [[02_Conception_Fusion/TABLE_R03|kit AURA-009 de table r03]], est sauvegardé dans Fusion v2 et exporté en F3D/STEP. Épaule et coude portés, retenues passives à caractériser, J3 XC330 TTL, 58 pièces de robot tranchées en PETG. La campagne numérique couvre 59 poses globales et 72 poses du pouce. Le prochain montage est ancré, à blanc, après les coupons. L’alimentation, la commande et le maintien sous charge sont à qualifier. La [[02_Conception_Fusion/MONTAGE_V3|r02]] et la [[02_Conception_Fusion/MAIN_POIGNET_ECO|r01]] servent de références historiques.

## Références V3 complètes

La V3 r03 sert de référence de silhouette et de montage à blanc pour les 23 pièces. La branche AURA-006 est la version de travail mécatronique. Le doigt autonome et le banc d’épaule J2 disposent chacun de leur assemblage Fusion. La branche complète reste soumise à qualification mécanique, électrique et à l’essai de coupure. [[02_Conception_Fusion/INTEGRATION_MECATRONIQUE_V3|État et preuves V3]] · [[03_Impression_3D/NOTICE_BANCS_V3|Notice du doigt et de J2]] · [[05_Electronique/README_MOTEURS_V3|Références moteur]] · [[09_Gestion/TACHES#AURA-006 — Intégrer la mécatronique V3|Tâche active]].

## Références V1 et V2

**Projet :** AURA-01, bras robotisé expressif 5 axes (J1–J5) + pince G1, imprimable FDM.
**Utilisateur :** étudiant Epitech utilisant Windows 11, Autodesk Fusion Education et Codex.
**État sur la capture d’origine.** Projet `Robotic Arm — V1`, document `Assemblage final`, bras simplifié déjà visible, Autodesk Assistant ouvert.
**Objectif CAO.** Auditer la CAO, préserver le modèle existant, améliorer le squelette, les articulations, le design et l’imprimabilité.
**But ensuite :** animations d'émotions simulées, moteurs, contrôleur et application connectée.
**Design cible :** graphite/titane, bleu glacier, pince corail, coque effilée et maintenance accessible.
**Important :** dimensions et moteurs encore hypothétiques ; ne pas prétendre que les mouvements ou la sécurité sont validés.
**Budget IA :** utilisateur évoque ~200 € de crédits ; aucune dépense autorisée automatiquement.
**Travail.** Suivre [[AGENTS|les règles Codex]], lire [[README]], [[09_Gestion/ADR]], [[09_Gestion/JOURNAL]], [[09_Gestion/TACHES]] et la note technique de la tâche.

**Dernier état vérifié.** Le 21 novembre 2026, l’archive de la [[02_Conception_Fusion/audit_initial|v5 auditée]] a été restaurée dans un dossier indépendant. Le [[02_Conception_Fusion/CONCEPTION_MECANIQUE#V2 — Prototype mécanique enregistré|prototype V2 v5]] a été rouvert à HOME dans Fusion. J1 à J5 et les deux mors G1 ont été pilotés. Les 226 configurations contrôlées et les 21 exports 3MF constituent la preuve numérique actuelle.

**AURA-004 en cours.** La [[02_Conception_Fusion/CONCEPTION_MECANIQUE#AURA-004 — Assemblage de travail motorisé|copie motorisée v3]] ajoute plaque, six actionneurs de référence, engrenage J5 et vis G1. Dix transitions contrôlées en CAO. Les coupons, les attaches constructeur J1–J3, la commande et la protection près des pivots attendent les essais physiques. Reprendre dans [[09_Gestion/TACHES#AURA-004 — Valider les interfaces d’impression|AURA-004]] et la [[08_Tests/MATRICE_TESTS#AURA-004 — Essais de la branche motorisée|matrice]].
