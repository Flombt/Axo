# Registre des problèmes · AURA-01 V5 roulis

Audit du 24 novembre 2026. Les cotes et contrôles renvoient aux [preuves](preuves/) et au [diagnostic](../../../DIAGNOSTIC_ROBOT_COMPLET.md). Les coûts chiffrés proviennent des prix fournisseurs ou des plafonds historiques identifiés dans le rapport. Les interfaces non spécifiées restent à chiffrer.

## P0 · Bloquants

### A01-P0-01

**Origine** — Ancien connu depuis la V5 revue.  
**Pièces ou fichiers** — J2, J3, `J2_Chape_Tangage`, `J3_Chape_Tangage`, main.  
**Preuve, cause et conséquence** — À −21°/−32°, le point bas de la main est à −56,68 mm dans Fusion. Les limites individuelles laissent entrer le bras dans le plan de pose. Les roulis modifient aussi la garde.  
**Correction proposée** — Définir une enveloppe couplée avec marge et une limitation mécanique indépendante adaptée au support.  
**Coût** — Étude et logiciel sans achat direct. Butées et essais à chiffrer.  
**Dépendances** — A01-P0-03, A01-P0-07.  
**Validation** — Rejouer la grille de poses, les transitions et l’arrêt en mouvement au-dessus d’un plateau réel.

### A01-P0-02

**Origine** — Nouveau avec J2R et J3R.  
**Pièces ou fichiers** — `01_Platine`, `05_Tourelle`, `Gaine_Socle_*`, `Gaine_Colonne_*`, `Coque_Socle`.  
**Preuve, cause et conséquence** — Les quatre segments fixes quittent leurs raccords de 33,31 à 39,45 mm à ±88°. Le profil neutre traverse des parois et d’autres gaines. Un débattement câblé utile reste indéterminé.  
**Correction proposée** — Dégager un passage central ou définir des boucles mesurables et des arrêts de gaine. Réduire la course jusqu’à qualification.  
**Coût** — Gaine Ø4/2 affichée à 2,20 €/m. Autres pièces et reprises à chiffrer.  
**Dépendances** — A01-P1-08, A01-P1-12.  
**Validation** — Calibres Ø4, faisceau réel, mesure de rayon, effort, longueur, courant et continuité à chaque borne.

### A01-P0-03

**Origine** — Ancien aggravé.  
**Pièces ou fichiers** — `Friction_J2_*`, `Friction_J3_*`, chapes, axes M5, butées.  
**Preuve, cause et conséquence** — Même à vide, la gravité calculée demande jusqu’à 0,314 N·m à J2 et 0,127 à J3. Les valeurs historiques de retenue r05 de 0,266 et 0,107 N·m sont inférieures. Retenue réelle et fluage inconnus.  
**Correction proposée** — Prévoir compensation ou retenue mécanique dimensionnée et un bras captif au banc. Séparer frein de sécurité, précharge et frottement en mouvement.  
**Coût** — Sur devis après choix du mécanisme et du besoin de charge.  
**Dépendances** — A01-P1-01, A01-P1-02, A01-P1-13.  
**Validation** — Mesurer décollage, dérive à chaud, coupure et déplacement résiduel aux poses défavorables, avec support indépendant.

### A01-P0-04

**Origine** — Ancien toujours présent.  
**Pièces ou fichiers** — Pico, rail externe, chaîne de coupure et réarmement.  
**Preuve, cause et conséquence** — L’USB peut maintenir le Pico armé pendant une coupure du 5 V moteur. Le code r05 est dépourvu de lecture du rail et aucun interverrouillage. Le retour d’énergie peut réappliquer une impulsion.  
**Correction proposée** — Inhibition matérielle du rail, signal d’état, sortie initialement inactive, réarmement manuel indépendant après contrôle de la pose.  
**Coût** — Sur devis pour la chaîne de coupure et sa distribution.  
**Dépendances** — A01-P0-03, A01-P0-05, A01-P0-07.  
**Validation** — Essais instrumentés de perte puis retour de rail, perte USB, reset, blocage et réarmement distinct.

### A01-P0-05

**Origine** — Ancien aggravé par deux micros.  
**Pièces ou fichiers** — AM5120, jack DC, distribution, onze servos.  
**Preuve, cause et conséquence** — Le modèle de pointe totalise 11,3 A sur un bloc donné pour 10 A. L’ampacité du jack et le comportement en surcharge sont inconnus. Tenue en position et démarrage restent simultanés même si les mouvements sont séquencés.  
**Correction proposée** — Mesurer les lots et qualifier rail, protections par départ, connecteurs et enveloppe d’usage. Dimensionner le rail selon les courants mesurés et les creux admissibles.  
**Coût** — AM5120 affiché à 23,77 € HT. Solution finale et port à chiffrer.  
**Dépendances** — A01-P0-04, A01-P1-12.  
**Validation** — Scope aux broches du servo distal et près de la source, courant, échauffement des bornes et comportement aux défauts.

### A01-P0-06

**Origine** — Réapparu après la r05.  
**Pièces ou fichiers** — 56 références FDM de la V5 roulis.  
**Preuve, cause et conséquence** — 69 occurrences imprimables dans le natif. Les recherches sur C: et D: ont retrouvé le F3D seul pour la V5 roulis. Il manque le kit correspondant à la géométrie réellement auditée.  
**Correction proposée** — Geler révision, quantités, orientations, coupons et plateaux par machine. Contrôler chaque pièce après corrections.  
**Coût** — Temps CAO et atelier à estimer. Un lot PETG blanc 1 kg est affiché à 11,95 € TTC.  
**Dépendances** — A01-P0-01, A01-P0-02, A01-P1-14.  
**Validation** — Empreintes CAD–STL–3MF, couches, supports retirables, contrôles dimensionnels sur coupons.

### A01-P0-07

**Origine** — Nouveau pour l’architecture à onze voies.  
**Pièces ou fichiers** — `firmware/r05/controle.py`, `main.py`, plans de brochage.  
**Preuve, cause et conséquence** — Le programme gère six axes, dont MAU groupé. Cinq commandes V5 manquent. Les contrôles d’angles r05 acceptent J2 −18° et J3 −22° ensemble, alors que la V5 demande une contrainte de pose couplée.  
**Correction proposée** — Écrire la commande ciblée V5 avec brochage, rapports, limites mesurées, planificateur et machine d’états sûre.  
**Coût** — Dépense matière logicielle nulle. Banc, câblage et développement à chiffrer.  
**Dépendances** — A01-P0-01, A01-P0-04, A01-P0-08.  
**Validation** — Compiler pour la cible, tester simulation de défauts puis asservissements individuels au banc.

### A01-P0-08

**Origine** — Nouveau constat sur le firmware r05.  
**Pièces ou fichiers** — `firmware/r05/main.py:26`.  
**Preuve, cause et conséquence** — La compilation croisée MicroPython 1.29.0 renvoie `SyntaxError: *x must be assignment target` sur le tuple de limites. La compilation CPython et les tests du parseur ne voient pas cette incompatibilité.  
**Correction proposée** — Écrire une itération compatible MicroPython et ajouter une compilation de la cible avant tout flashage.  
**Coût** — Aucun composant pour la correction du code. Temps de mise au point à chiffrer.  
**Dépendances** — A01-P0-07.  
**Validation** — Compiler les deux fichiers puis démarrer le Pico hors rail et vérifier état inactif, USB et watchdog.

### A01-P0-09

**Origine** — Nouveau sur le panier roulis.  
**Pièces ou fichiers** — Nomenclature TTC et port, quincaillerie, consommables.  
**Preuve, cause et conséquence** — Le panier de 149,48 € repose sur des plafonds, réemplois et retraits, hors filament et corrections. Une bobine à 11,95 € porte ce scénario à 161,43 € avant écarts.  
**Correction proposée** — Recalculer le panier complet après qualification sécurité et interfaces. Déduire uniquement un stock compatible compté.  
**Coût** — Écart de 11,43 € dans le scénario avec une bobine, avant autres coûts.  
**Dépendances** — A01-P0-02 à A01-P0-06, A01-P2-01.  
**Validation** — Total de lots TTC et livraisons pour les références figées, comparé au plafond de 150 €.

## P1 · Critiques

### A01-P1-01

**Origine** — Ancien aggravé.  
**Pièces ou fichiers** — J2, MG996R, tourillon, engrenages 18/54.  
**Preuve, cause et conséquence** — Le scénario PETG plein à 20 g donne 0,368 N·m de gravité seule. Reprendre les frottements r05 aboutit à ~0,648 N·m, au-dessus des 0,519 N·m de service purement hypothétiques.  
**Correction proposée** — Réduire le moment distal ou compenser la gravité. Caractériser le lot et le rendement avant toute substitution de servo.  
**Coût** — MG996R 7,99 € seul ou 7,59 € par deux. Compensation à chiffrer.  
**Dépendances** — A01-P0-03, A01-P1-11.  
**Validation** — Couple de sortie continu, vitesse, courant et température dans les deux sens et au maintien.

### A01-P1-02

**Origine** — Ancien, correction partielle.  
**Pièces ou fichiers** — J3, MG996R, tourillon, pignon/roue 18/36.  
**Preuve, cause et conséquence** — Le calcul donne 0,165 N·m statique pour 20 g. Avec frottement présumé, ~0,284 N·m. Le résultat dépend du lot, de la durée et du frottement réel.  
**Correction proposée** — Éprouver le système complet avec paliers et protection, puis fixer charge et cycle d’utilisation.  
**Coût** — Même prix moteur que J2. Remplacement ou compensation à chiffrer.  
**Dépendances** — A01-P0-03, A01-P1-11.  
**Validation** — Maintien prolongé et cycles sur articulation portée, contrôles de dérive, jeu et température.

### A01-P1-03

**Origine** — Ancien, cinq voies ajoutées.  
**Pièces ou fichiers** — `09_Cassette_SG90`, cinq `Bobine_*`, `Tendon_*`, `Traction_*`, paume.  
**Preuve, cause et conséquence** — Cinq bobines commandent les phalanges séparément en CAO. Le trajet n’est défini qu’au neutre, les quinze liens imposent des angles et les rappels ne sont pas éprouvés. Un point dur peut faire forcer le servo.  
**Correction proposée** — Spécifier terminaux, prétension, guides continus et rappels, puis construire un doigt instrumenté avant cinq.  
**Coût** — Bobine nylon documentée 2,49 €, disponibilité Ø0,40 à confirmer. Rappels à spécifier.  
**Dépendances** — A01-P1-04, A01-P1-07, A01-P1-14.  
**Validation** — Mesurer extension du brin, effort, course aller-retour, interaction entre doigts, arrêt sur obstruction.

### A01-P1-04

**Origine** — Nouveau constat quantifié.  
**Pièces ou fichiers** — `12_Chape_Pouce`, `P1–P3`, `I1–I3`, surfaces de contact.  
**Preuve, cause et conséquence** — À 92°+92° de tambours, P3/I3 laissent 17,68 mm et I3/paume 17,22 mm au poing. L’opposition requise pour les objets minces reste absente de la pose de fermeture.  
**Correction proposée** — Revoir angle d’opposition du pouce, pads et géométrie de préhension, avec cible d’objet explicitée.  
**Coût** — Reprise CAO. Pads et essais à chiffrer.  
**Dépendances** — A01-P1-03, A01-P1-14.  
**Validation** — Mesurer l’ouverture effective, saisir des éprouvettes dimensionnées, éprouver glissement puis réouverture.

### A01-P1-05

**Origine** — Nouveau avec J2R.  
**Pièces ou fichiers** — `J2_Chape_Tangage`, `Palier_J2R`, `07_Bras`, `But_J2R`.  
**Preuve, cause et conséquence** — Portée Ø15,92 dans alésage Ø16,42, soit 0,25 mm par côté. La butée-goupille Ø1,956 est dans un passage Ø2,17. La reprise d’efforts et le verrouillage physique ne sont pas établis.  
**Correction proposée** — Qualifer le palier fendu, axe retenu axialement, précharge/bagues et goupille retenue. Prévoir accès aux têtes et écrous.  
**Coût** — Coût matériau coupon, comparatif bague/axe sur devis.  
**Dépendances** — A01-P0-03, A01-P1-09, A01-P1-14.  
**Validation** — Mesurer jeu radial, axial et angulaire, voilage en charge, arrachement de la butée et usure de la portée.

### A01-P1-06

**Origine** — Nouveau avec J3R.  
**Pièces ou fichiers** — `J3_Chape_Tangage`, `Palier_J3R`, `08_Avant_bras`, `But_J3R`, `Raccord_J3R_*`.  
**Preuve, cause et conséquence** — Même jeu nominal de 0,25 mm radial. La gorge d’arrêt est dessinée et sa marge minimale calculée à 0,15 mm. Les gaines partagent des volumes avec le carénage et les supports.  
**Correction proposée** — Finir la conception de l’appui et des butées, séparer les parcours de gaine des pièces porteuses.  
**Coût** — Coût matériau coupon et éventuels paliers à chiffrer.  
**Dépendances** — A01-P0-02, A01-P1-05, A01-P1-14.  
**Validation** — Mesure de jeu et couple à plusieurs angles avec traction, et remplacement d’une gaine sans déposer l’axe.

### A01-P1-07

**Origine** — Réapparu avec le poignet motorisé.  
**Pièces ou fichiers** — `08_Avant_bras`, `11_Paume`, `Moteur_J7`, guide, cinq brins, faisceau.  
**Preuve, cause et conséquence** — Le roulis J7 ±32° déplace les points d’attache des doigts. Le routage CAO au neutre ne calcule ni changement de longueur ni force sur les doigts.  
**Correction proposée** — Caler les cinq entrées de gaine, définir réserve et rayon, mesurer une éventuelle compensation.  
**Coût** — Gaines et glissières additionnelles à chiffrer après maquette.  
**Dépendances** — A01-P1-03, A01-P1-12.  
**Validation** — Bloquer chaque consigne, balayer J7 puis J2R/J3R et mesurer variation d’angle et tension de chaque doigt.

### A01-P1-08

**Origine** — Ancien, rotation continue abandonnée en r05.  
**Pièces ou fichiers** — J1, `J1_Pignon` 38, `J1_Roue` 22, deux 608, deux vis d’arrêt M4.  
**Preuve, cause et conséquence** — La CAO atteint ±88° avec ±50,95° moteur. Elle laisse ≥0,50 mm entre vis et tourelle aux bornes testées. L’engagement des vis dans leurs supports est volontaire. Course utile câblée et arrêt physique restent ouverts.  
**Correction proposée** — Valider index et arrêt réel, régler la butée avec marge pour le faisceau, contrôler jeu et effort à la roue en charge.  
**Coût** — Vis/butées selon lot. 608.ZZ 3,95 € par dix si compatible après essai.  
**Dépendances** — A01-P0-02, A01-P1-13.  
**Validation** — Mesurer angle, jeu, couple résistant et déclenchement de la butée sous commande limitée. Vérifier la portée et la retenue de l’axe.

### A01-P1-09

**Origine** — Ancien, adaptation de quincaillerie à vérifier.  
**Pièces ou fichiers** — J1 M8×55, J2/J3 M5, axes M2, vis et écrous des paliers.  
**Preuve, cause et conséquence** — Le gabarit des deux M5 montre env. 57,1 mm hors tout. L’achat propose M5×70 sous tête. Les extensions, épaulements, filets et accès ne sont pas démontrés avec cette référence.  
**Correction proposée** — Relever cote sous tête, filetage et rondelles du lot. Contrôler appui lisse et dégagement sous coque. Spécifier les vis par repère.  
**Coût** — Plafonds historiques 3,00 € pour deux M5 et écrous, 2,35 € pour la pile M8, port à vérifier.  
**Dépendances** — A01-P1-05, A01-P1-10, A01-P2-01.  
**Validation** — Présenter les piles de vis et l’embout, relever portée, projection filetée et serrage.

### A01-P1-10

**Origine** — Ancien aggravé par les coques.  
**Pièces ou fichiers** — Pico, cassette, supports moteurs, carénages, visserie de pose.  
**Preuve, cause et conséquence** — L’assemblage CAO fixe des volumes sans outil, embout ni connecteur. Les fixations et la manoeuvre de dépose restent sensibles à l’ordre et aux fils.  
**Correction proposée** — Définir une vraie séquence, trajets, longueurs d’embouts, fixations captives et points de séparation de faisceau.  
**Coût** — Paires JR et vis selon inventaire. Coques à reprendre selon simulation et essai.  
**Dépendances** — A01-P0-02, A01-P1-09, A01-P2-04.  
**Validation** — Monter à blanc en manipulant les embouts retenus, déposer J2, J3, un servo de main et les deux tambours.

### A01-P1-11

**Origine** — Nouveau depuis le module 0,8.  
**Pièces ou fichiers** — Pignons 18 dents, roues J2/J3, interfaces palonniers et gardes.  
**Preuve, cause et conséquence** — La denture plus fine et la charge tangente sont sensibles au jeu, à l’état des couches et à l’alignement des servos. La simulation volumique ne caractérise pas le contact ni le rendement.  
**Correction proposée** — Gabariter les entraxes, orienter et qualifier chaque jeu de pignons. Évaluer le module et l’interface de palonnier si dégradation sous charge.  
**Coût** — Éprouvettes PETG et éventuellement pignons du commerce. Montant à fixer avec la variante.  
**Dépendances** — A01-P0-06, A01-P1-01, A01-P1-02.  
**Validation** — Essai d’engrènement sur un cycle, reprise du jeu et des températures, puis inspection après fatigue.

### A01-P1-12

**Origine** — Ancien aggravé.  
**Pièces ou fichiers** — AMPUL, tronc 1–1,5 mm², branche mobile 0,5 mm², JR et Pico.  
**Preuve, cause et conséquence** — Une boucle cuivre de 2 m à 1 mm² perd ~0,35 V à 10 A. Le lot peut tomber sous 4,8 V aux bornes. Les connecteurs et les sections des fils mobiles sont à établir.  
**Correction proposée** — Réduire les chutes, séparer retours/puissance, protéger les départs et qualifier seuil PWM 3,3 V et polarité.  
**Coût** — Fils et bornes au métrage par référence réelle. Enveloppes d’achat actuelles provisoires.  
**Dépendances** — A01-P0-04, A01-P0-05.  
**Validation** — Mesure Kelvin ou au connecteur et à la source, températures, creux, défaut de branche, arrêt réarmement.

### A01-P1-13

**Origine** — Ancien, platine améliorée.  
**Pièces ou fichiers** — `01_Platine`, quatre M5, établi ou planche.  
**Preuve, cause et conséquence** — Le calcul trouve une faible marge au bord d’appui et au rectangle d’ancrage pour certaines positions. Le poids seul ne couvre pas une traction extérieure ni les chocs.  
**Correction proposée** — Ancrer les quatre points sur support rigide éprouvé, traiter l’énergie de chute et mesurer l’effort réel appliqué.  
**Coût** — Plafond ancrages 1,60 € du panier. Support, brides et protections à chiffrer.  
**Dépendances** — A01-P0-01, A01-P0-03.  
**Validation** — Épreuve statique au cas défavorable avec charge et traction, puis déplacement contrôlé et contrôle du serrage.

### A01-P1-14

**Origine** — Ancien persistant.  
**Pièces ou fichiers** — Phalanges, vis M2, axe Ø2, conduits et attaches des brins.  
**Preuve, cause et conséquence** — Les corps repris comportent des conduits de faible diamètre et des attaches concentrant les efforts. Aucune coupe d’un tranchage V5 ne quantifie les lignes dans les ligaments.  
**Correction proposée** — Préparer le coupon phalange dans la même orientation et rendre les appuis, renvois et arêtes robustes.  
**Coût** — Coût du coupon et PETG, révision des ancrages à chiffrer.  
**Dépendances** — A01-P0-06, A01-P1-03.  
**Validation** — Mesurer sections, microdéfauts et effort d’arrachement du nœud. Refaire essais répétés à température d’usage.

### A01-P1-15

**Origine** — Ancien toujours présent.  
**Pièces ou fichiers** — Gardes J1/J2/J3, mécanismes des doigts et arrêt.  
**Preuve, cause et conséquence** — Les gardes modélisées protègent certaines dentures. La zone d’action des pivots, des phalanges et du bras reste ouverte. Coupure et absence d’énergie résiduelle sans validation.  
**Correction proposée** — Prévoir écran de banc, accès contrôlé et état sûr documenté pour pincement, perte d’objet et gravité.  
**Coût** — Écran, fixation et arrêt à chiffrer. Pièces à prévoir dans le budget complet.  
**Dépendances** — A01-P0-03, A01-P0-04.  
**Validation** — Protocole d’accès hors extension de la main, tests sous défaut et arrêt du banc avec charge retenue.

### A01-P1-16

**Origine** — Ancien côté autonomie.  
**Pièces ou fichiers** — Pico, retour d’état, course J1/J2/J3, détection des efforts.  
**Preuve, cause et conséquence** — Le PWM indique une consigne. L’état réel, la vitesse, le blocage et la perte de tension ne sont pas observés côté Pico.  
**Correction proposée** — Ajouter le retour indépendant suffisant pour l’usage retenu, interdire les ordres hors enveloppe et dégrader vers l’état sûr.  
**Coût** — Capteurs et fixation à chiffrer si autonomie retenue.  
**Dépendances** — A01-P0-04, A01-P0-07.  
**Validation** — Défauts injectés avec angle faux, servo bloqué ou débranché. Vérifier désarmement, télémétrie et reprise manuelle.

### A01-P1-17

**Origine** — Nouveau pour les deux axes de roulis.  
**Pièces ou fichiers** — MG90S RBS11204, `Support_J2R`, `Support_J3R`, tambours et nylon.  
**Preuve, cause et conséquence** — Les tambours exigent ±60° et ±72°. Le taux de réduction et les rayons CAO ne donnent ni course PWM garantie ni traction sous frottement. Couplage antagoniste sans réglage mesuré.  
**Correction proposée** — Mesurer angle utile, jeu, équilibrage des deux brins et rétention du palonnier sur un axe isolé.  
**Coût** — MG90S 3,95 € la pièce, deux exemplaires 7,90 €. Prétension et ancrages à chiffrer.  
**Dépendances** — A01-P0-02, A01-P1-05, A01-P1-06.  
**Validation** — Relever actionneur seul puis couple et course en bout de gaines au plus mauvais rayon.

## P2 · Importants

### A01-P2-01

**Origine** — Ancien récurrent.  
**Pièces ou fichiers** — Nomenclature, coffrets métriques, 608, nylon et rappel.  
**Preuve, cause et conséquence** — La liste reprend des quantités de stock non comptées. 608.ZZ à acheter et 608-2RS en CAO ont mêmes cotes nominales mais des protections différentes. La fiche du rappel Ø1 comporte une description Ø1,4.  
**Correction proposée** — Inventorier par longueur/type de tête/quantité et choisir références exactes de roulements et rappel.  
**Coût** — 3,95 € le lot 608.ZZ. Rappel affiché 5,99 € et variante à confirmer. Achats manquants sur devis.  
**Dépendances** — A01-P0-09, A01-P1-09.  
**Validation** — Gabarits, stock physique et confirmations vendeur dimension/lot avant panier global.

### A01-P2-02

**Origine** — Réapparu après r05.  
**Pièces ou fichiers** — README, contexte du coffre, GitHub `main`, exports et V5.  
**Preuve, cause et conséquence** — Le coffre mentionne encore la cible r05 et l’archive cloud active est la V5 roulis. `main` publie la r05 et les éléments CAO et fabrication sont désynchronisés.  
**Correction proposée** — Faire une fiche de diffusion d’une seule configuration après qualification, avec versions, inventaire et empreintes.  
**Coût** — Documentation sans achat direct.  
**Dépendances** — A01-P0-06, A01-P0-07.  
**Validation** — Rejouer la réouverture du document actif et comparer les empreintes du pack diffusé.

### A01-P2-03

**Origine** — Ancien aggravé.  
**Pièces ou fichiers** — Scripts V5 sur D:, ressources Fusion et profils.  
**Preuve, cause et conséquence** — La génération dépend de modules de révisions et de chemins hors dépôt. Le F3D V5 s’ouvre, la régénération indépendante de ses plans de fabrication n’est pas livrée.  
**Correction proposée** — Conserver les scripts associés, les cotes stables et un processus reproductible d’export contrôlé.  
**Coût** — Temps de documentation et de conditionnement.  
**Dépendances** — A01-P0-06, A01-P2-02.  
**Validation** — Exécuter sur une copie depuis un autre dossier et comparer la liste et les signatures de formes.

### A01-P2-04

**Origine** — Ancien, notice active absente.  
**Pièces ou fichiers** — Notice, schéma et séquence d’assemblage V5.  
**Preuve, cause et conséquence** — La notice illustrée r02 décrit quatre servos et Nano. Les documents V5 couvrent l’architecture et les achats, sans plan de connexion à onze voies ni guide complet de dépose.  
**Correction proposée** — Documenter pièces par repère, ordre, outillage, sens, longueurs, couple, gains et contrôle de coupure.  
**Coût** — Temps de dessin. Pièces de banc selon nomenclature corrigée.  
**Dépendances** — A01-P0-04, A01-P1-10.  
**Validation** — Monteur indépendant exécute chaque étape à blanc, y compris dépose et remise au neutre.

### A01-P2-05

**Origine** — Nouveau avec les roulis.  
**Pièces ou fichiers** — Coupes des paliers J2R/J3R et flancs des chapes.  
**Preuve, cause et conséquence** — La vis/goupille et la rainure nominales n’établissent pas le couple de butée, le chemin des chocs ou la répétabilité après usure.  
**Correction proposée** — Chiffrer l’énergie en fin de course et définir la fonction de la butée hors code. Réaliser coupon de tolérance et essai d’usure.  
**Coût** — Temps et matériau du coupon, fixation définitive à chiffrer.  
**Dépendances** — A01-P1-05, A01-P1-06, A01-P1-17.  
**Validation** — Contrôle de course maximale, déplacement axial et absence de dégradation après cycles protégés.

## P3 · Mineurs

### A01-P3-01

**Origine** — Nouveau constat sur fichiers d’historique.  
**Pièces ou fichiers** — 3MF Prusa r03 Châssis, r04 Socle J1 et Segments.  
**Preuve, cause et conséquence** — Quatre triangles dégénérés sur quatre maillages d’archives. Les maillages ferment après fusion des sommets et aucun fichier n’est concerné côté V5.  
**Correction proposée** — Lors d’un réemploi de ces anciens 3MF, retrancher et vérifier les interfaces ou repartir des STL historiques sains.  
**Coût** — Aucun achat direct.  
**Dépendances** — A01-P2-02.  
**Validation** — Répéter le contrôle de fermeture et comparer l’aperçu après tranchage.

### A01-P3-02

**Origine** — Ancien, écart de travail.  
**Pièces ou fichiers** — Profils r05 Kobra 3, documents de volumes.  
**Preuve, cause et conséquence** — Les 3MF Kobra 3 déclarent un plateau de 255 × 255 mm. Les objets mesurés restent dans 250 × 250 mm, la zone réelle doit néanmoins guider tout repositionnement.  
**Correction proposée** — Conserver le volume nominal applicable à la machine et fournir un fichier testé par plateau lors de la prochaine diffusion.  
**Coût** — Aucun achat direct.  
**Dépendances** — A01-P0-06.  
**Validation** — Contrôler objets, bordures et trajectoires imprimées avec le profil machine réel.

## P4 · Optimisations

### A01-P4-01

**Origine** — Ancien, à reprendre après qualification.  
**Pièces ou fichiers** — Coques, supports, cassette et masse distale.  
**Preuve, cause et conséquence** — La V5 réunit 69 pièces FDM sur 56 références. Les ensembles distaux contribuent au couple et comportent de nombreux raccords et capots.  
**Correction proposée** — Comparer capots intégrés démontables, rationalisation des vis et allègement par mesure, après validation de la tenue et des passages.  
**Coût** — Gains de matière et de temps après retranchage, économie inconnue.  
**Dépendances** — A01-P0-03, A01-P0-06, A01-P1-01.  
**Validation** — Peser les sous-ensembles et comparer rigidité, maintenance et temps à la version validée.

### A01-P4-02

**Origine** — Ancien, gains possibles après qualification.  
**Pièces ou fichiers** — Règles d’usage, alimentation, filaments, lots.  
**Preuve, cause et conséquence** — Le budget est tendu et certains achats de lot dépassent le nombre utilisé. La portée, la charge et le nombre de couleurs restent des variables de conception.  
**Correction proposée** — Regrouper devis, conserver une couleur au premier essai, mesurer et retirer seulement les éléments superflus ou déjà en stock.  
**Coût** — Valeur au prix payé du lot. Stock compatible et économies à vérifier.  
**Dépendances** — A01-P0-09, A01-P2-01.  
**Validation** — Renforcer la couverture du panier et recouper le prix avec la nomenclature réellement imprimée.
