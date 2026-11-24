# Suivi des tâches AURA-01

Partir de la [[09_Gestion/ROADMAP|roadmap]] pour l’ordre des phases. Lors d’une session, actualiser le statut de la tâche, conserver son identifiant et lier la preuve dans le [[09_Gestion/JOURNAL|journal]]. Les choix durables figurent dans les [[09_Gestion/ADR|ADR]].

## AURA-01 V5 — Roulis épaule et coude

- [x] Regrouper la CAO active, archiver les kits précédents et mettre en place le contrôle de cohérence. [Réorganisation](../../../docs/REORGANISATION_PROJET.md)
- [x] Auditer indépendamment la V5 roulis et comparer ses fichiers natifs à la fabrication publiée. [Diagnostic avant fabrication](../../../DIAGNOSTIC_ROBOT_COMPLET.md)
- [ ] Fermer les blocages du diagnostic avant achat de lot, impression générale et mise sous tension. Reprendre la garde au plan, le franchissement de J1, les retenues, le rail et le réarmement. [Registre P0](../../../docs/diagnostic/latest/REGISTRE_PROBLEMES.md#p0--bloquants)
- [x] Ajouter les pivots longitudinaux J2R et J3R. Vérifier les courses, le couplage des tambours et les cinq commandes de doigts.
- [x] Vérifier les dégagements sur les poses de revue, sauvegarder la variante Fusion et rouvrir le F3D.
- [x] Mettre à jour le matériel, son prix et le dimensionnement provisoire du rail moteur.
- [ ] Valider visuellement les deux colliers. Qualifier leur montage, leur tenue hors tension, le déplacement des gaines et l’enveloppe sur table. [[02_Conception_Fusion/TABLE_V5_ROULIS|Contrôles et preuves]]

## AURA-01 V5 — Revue design du bras de table

- [x] Enregistrer la variante Fusion et vérifier la réouverture du F3D.
- [x] Contrôler l’indépendance des cinq doigts, le débattement des solides et la garde au plan de table sur les poses prévues.
- [x] Chiffrer les neuf servos, le faisceau et la quincaillerie avec les pièces déjà disponibles.
- [ ] Obtenir la validation visuelle. Qualifier ensuite les supports de servos, le faisceau réel, le couple et la limite de descente sur table. [[02_Conception_Fusion/TABLE_V5_REVUE_DESIGN|Détail et preuves]]

## AURA-009 de table r05 — Prototype économique

- [x] Comparer trois architectures et refondre le modèle dans un document Fusion séparé.
- [x] Vérifier 85 poses et les butées, réouvrir le F3D, exporter STEP et STL.
- [x] Préparer les 3MF avec les profils Kobra 3, Kobra X et Kobra 3 Max en buse de 0,4 mm.
- [x] Préparer la commande Pico USB, les rendus et le panier. [[02_Conception_Fusion/TABLE_R05|Modèle et preuves]]
- [ ] Compter les pièces disponibles et confirmer les montants livrés.
- [ ] Qualifier les coupons, moteurs, retenues hors tension, câbles en service et la première charge au banc.

## AURA-009 de table r04 — Fabriquer le prototype indépendant

- [x] Intégrer le J1 porté à rotation continue, le passage coaxial et les cinq commandes de main.
- [x] Réimporter le F3D v4, vérifier les trajectoires, retrancher les STL et publier les fichiers.
- [x] Convertir les 53 STL en 3MF et vérifier les six planches Anycubic. [Guide des 3MF par couleur](../../../archives/r04/anycubic/README.md).
- [x] Comparer la visserie disponible avec la r04 et relever les références et les prix. [Visserie et liste d’achats r04](../../../archives/r04/achats/README.md).
- [ ] Qualifier les sept coupons, les portées, le premier doigt et le démontage du bloc J1.
- [ ] Vérifier rail 6 V, conducteurs et bus sous rotation. Mesurer tension de tendon, effort, usure, retenues et coupure.

[[02_Conception_Fusion/TABLE_R04|Prototype de table r04]] · [Rapport de fabrication](../../../archives/r04/VALIDATION_FABRICATION.md).

## AURA-009 de table r03 — Reconcevoir et qualifier le kit

- [x] Sauvegarder la r02 ouverte et créer un document r03 séparé.
- [x] Reprendre les portées J2/J3, les retenues, l’ancrage, J7, la main et les faisceaux.
- [x] Vérifier 59 poses globales, 72 poses ciblées du pouce, 149 positions de dépose et les butées. Réimporter les archives et trancher 9 plateaux PETG.
- [x] Rédiger la notice et le rapport pour les 43 constats, produire les rendus, coupes et 16 vues de contrôle du faisceau.
- [x] Rendre et publier la démonstration 4K à 60 i/s et le projet Blender. Contrôler 143 poses dans Fusion et les raccords du faisceau sur 3 960 images. [[04_Animation_Emotion/ANIMATIONS#AURA-009 r03 v2 — Démonstration cinématique|Démonstration r03 v2]]
- [ ] Qualifier à blanc les coupons, les interfaces, les courses, les butées, les protections et le démontage avec les composants achetés.
- [ ] Mesurer gravité, frottement, retenue à la coupure, courant, température, tension de tendon et tenue des couches.
- [ ] Porter la commande à trois PWM et un J3 TTL. Tester limites, arrêt matériel et réarmement avant la première prise sous charge.

[[02_Conception_Fusion/TABLE_R03|Modèle et preuves]] · [[05_Electronique/README_MOTEURS_V3|Références des moteurs]].

## AURA-009 — Rendre le kit V3 assemblable

- [x] Examiner le raccord pouce/paume dans Fusion et créer le montage r02 séparément.
- [x] Reprendre le pouce, la cassette J7, l’axe commun et les accès de fixation. Contrôler les poses, emboîtements et chemins d’outils.
- [x] Vérifier les STL et trancher les plateaux. Produire notice, manuel, inventaire, dépannage et vues éclatées.
- [x] Compiler le cycle Nano et documenter le câblage et la procédure progressive.
- [x] Centraliser le kit à la racine et exporter l’assemblage r02 en Blender.
- [x] Reprendre la démo Fusion en six clips Blender et préparer le fichier de présentation.
- [x] Relire la r02 v1 dans Fusion et relever les cotes d’achat. Ajouter les offres compatibles au panier Amazon et consigner les références et les quantités. [Relevé du 23 novembre](../../../archives/r02/kit/ACHATS_AMAZON_R02.md)
- [ ] Confirmer le lot de servos, leurs palonniers et leurs vis. Mesurer les empilements M3/M4, le renvoi du pouce et le rail 5 V en fonctionnement avant de compléter le panier.
- [ ] Imprimer coupon et index, vérifier les vis du lot, monter J2/J3 puis J7 et la main à blanc.
- [ ] Réaliser le faisceau, qualifier la coupure et vérifier le cycle, le courant et les jeux en mouvement sur le robot.

Voir les [[02_Conception_Fusion/MONTAGE_V3|preuves et documents du kit]].

## AURA-001 — Préparer la mémoire Obsidian

- **TERMINÉ** le 21 novembre 2026. Liens du coffre, chargement des règles Codex et vue Graphe vérifiés.
- **Preuve** — Compte rendu dans le [[09_Gestion/JOURNAL#2026-11-21 — Mise en place de la mémoire Obsidian|journal]] et résultat de T-052 dans la [[08_Tests/MATRICE_TESTS|matrice de validation]].

## AURA-002 — Auditer et sauvegarder Assemblage final

- **TERMINÉ** le 21 novembre 2026. Assemblage final v5 sauvegardé en F3Z avec ses huit références. Audit des composants, des liaisons et de 46 poses dans Fusion.
- **Preuve** — [[02_Conception_Fusion/audit_initial|Rapport d’audit et plan V2]], avec mesures, capture, limites et chemin de la sauvegarde. Voir la [[09_Gestion/ROADMAP#Phase 0 — Audit et sauvegarde|Phase 0]].

## AURA-003 — Préparer le squelette articulé

- **TERMINÉ** le 21 novembre 2026 pour le prototype numérique. Restauration F3Z vérifiée, V2 v5 enregistrée et rouverte à HOME. Cinq pivots indépendants, pince à deux mors couplés, coques démontables et interfaces de motorisation provisoires.
- **Preuves** — [[02_Conception_Fusion/CONCEPTION_MECANIQUE#V2 — Prototype mécanique enregistré|Note V2]], [[04_Animation_Emotion/ANIMATIONS#V2 — Poses de référence|poses]], [[08_Tests/MATRICE_TESTS#V2 — Contrôles de la conception mécanique|matrice]] et [[09_Gestion/JOURNAL#2026-11-21 — AURA-003 et prototype V2|journal]].

## AURA-004 — Valider les interfaces d’impression

- **EN COURS** — Copie v3 enregistrée et rouverte dans Fusion. Plaque et transmissions modélisées, actionneurs et alimentation proposés. Tranchage et 99 configurations CAO documentés. Cinq coupons préparés et tranchés virtuellement. [[09_Gestion/JOURNAL#2026-11-21 — AURA-004 motorisation et fabrication|Journal de la session]].
- **Essais ouverts** — Confirmer machine, buse, profil, lot de filament et autorisation d’imprimer les coupons. Montage à blanc, reprise des attaches fabricant J1–J3, filetage et retenue des guides G1, puis ancrage et protection contre la chute hors tension. Essais électriques et thermiques avant animation motorisée. [[08_Tests/MATRICE_TESTS#AURA-004 — Essais de la branche motorisée|Matrice AURA-004]].
- **Preuves du 22 novembre** — Archive locale F3Z vérifiée en v3, palonniers J1–J3 identifiés chez ROBOTIS et cinq coupons regroupés sur un plateau PrusaSlicer testé. [[09_Gestion/JOURNAL#2026-11-22 — AURA-004 reprise et préparation atelier|Reprise AURA-004]].
- **Ordre d’atelier** — Confirmer imprimante et profil. Mesurer les jeux sur les coupons après autorisation d’impression. Vérifier les interfaces J1–J3 et le guidage G1 au montage à blanc. Éprouver l’ancrage et la retenue avant le cycle en charge de J2/J3. [[03_Impression_3D/PROTOCOLes_FDM#Mesures et choix des ajustements|Fiche de mesures]] · [[08_Tests/MATRICE_TESTS#Mesure du couple utile de J2 et J3 au banc|Cibles au banc]].

## AURA-005 — Concevoir et éprouver le bras V3

- **CAO TESTÉE** — V3 r02 exportée depuis Fusion avec 22 pivots natifs. Les quinze ensembles boîtier/logement ont été contrôlés. Les trois mouvements ont été capturés et encodés. [[02_Conception_Fusion/DESIGN_V3|Livrables]] · [[08_Tests/MATRICE_TESTS#V3 — Contrôles du bras à main articulée|Preuves]].
- **EN COURS** — Valider le premier jeu phalange, servo, palonnier, bague et faisceau. Peser un doigt complet et mesurer le couple utile. Mettre au point les réductions et la retenue du bras avant les commandes du lot. [[05_Electronique/README_MOTEURS_V3|Nomenclature d’achat]].
- **R03 prête pour un montage à blanc** — Structure ramenée à 23 pièces imprimées et 11 références. Modèle rouvert dans Fusion, 165 poses échantillonnées sans collision volumique détectée. Six plateaux PETG retranchés en virtuel. [[03_Impression_3D/PROTOCOLes_FDM#AURA V3 r03 — Kit d’impression|Kit et surfaces d’impression]].
- **Impression complète en attente** — Concevoir les fixations et les transmissions des sept axes, le faisceau et les logements électroniques. Éprouver un doigt et un axe chargé avant de lancer les 23 pièces pour un robot autonome. [[05_Electronique/SCHEMA_FUTUR#AURA-01 V3 — Intégration avant impression complète|État et architecture candidate]].

## AURA-008 — Main et poignet articulés

- [x] Réaliser dans Fusion le bras avec cinq doigts à trois phalanges, roulis du poignet et quatre moteurs. Vérifier les 72 poses et les 26 pièces tranchées. [[02_Conception_Fusion/MAIN_POIGNET_ECO|Résultats]]
- [x] Actualiser les références d’achat et préparer la présentation avec le geste filmé.
- [ ] Imprimer un index. Régler les passages, le rappel et la prise groupée. Vérifier la boucle du poignet et la tenue du coude. Programmer le cycle au bouton après calibration.

## AURA-007 — Réaliser le bras V3 de table

- **Référence précédente.** Les travaux de motorisation suivent désormais AURA-008.

- [x] Définir les trois mouvements, le design conservé et les achats du [[02_Conception_Fusion/PROTOTYPE_TABLE|bras V3 de table]].
- [x] Créer une copie Fusion au format table et contrôler les trois pivots, les enveloppes et les 62 poses. [[02_Conception_Fusion/PROTOTYPE_TABLE#Maquette de présentation r01|Modèle et preuves]].
- [x] Préparer la présentation, les neuf STL et les trois plateaux PrusaSlicer. [Fiche de présentation](../../../archives/aura-007/fusion/Fiche_presentation.md).
- [ ] Vérifier les pattes et le palonnier des servos reçus, l’espace sous le bouton, l’accès aux vis et le montage à blanc. Ajuster les jeux sur l’imprimante de l’atelier.
- [ ] Préparer le programme. Tester l’épaule et ses besoins en courant, puis monter le bras et démontrer le cycle au bouton.

## AURA-006 — Intégrer la mécatronique V3

- **EN PAUSE** au profit du prototype de table. Les résultats et essais ouverts restent documentés ci-dessous.

- [x] Préserver la r03, créer une branche indépendante, importer les STEP ROBOTIS et relever les interfaces dans Fusion.
- [x] Modéliser le doigt, la CAO du banc J2 et exporter les kits de pièces. [[03_Impression_3D/NOTICE_BANCS_V3|Notice et protocole]].
- [x] Relever les prix et liens de vente des composants référencés. [README V2 — Éléments à acheter](../../../archives/v2/README_V2_ELEMENTS_A_ACHETER.md).
- [ ] Mesurer le palonnier, le servo et la quincaillerie effectivement achetés. Imprimer et mesurer le coupon d’ajustement, puis caractériser le doigt au banc.
- [ ] Confirmer l’interface Kendrion et résoudre l’alésage de la poulie 16 dents (Gates max. 7,95 mm, axe CAO Ø12). Choisir l’usinage ou reprendre l’arbre d’entrée. Adapter le moyeu de 64 dents à la poulie retenue. Mesurer le couple continu à chaud puis la retenue J2 hors tension à 5,68 N·m.
- [ ] Transposer les transmissions porteuses dans le bras, traiter les interférences des STEP aux six axes et qualifier les paliers, butées, accès de démontage et arrêts hors tension.
- [ ] Fabriquer le faisceau, mesurer son rayon en dynamique, valider l’électronique, le bilan des rails, l’arrêt et le redémarrage. Peser le bras équipé et vérifier l’ancrage, la stabilité et l’autonomie.
- [ ] Qualifier les pièces révisées et constituer le kit final des 23 solides. [[02_Conception_Fusion/INTEGRATION_MECATRONIQUE_V3|Branche et statut de chaque domaine]].
