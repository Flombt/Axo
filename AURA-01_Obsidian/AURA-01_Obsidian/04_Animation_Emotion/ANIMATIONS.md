# Bibliothèque émotionnelle

Référence à partir de la [[README#14 — Expression émotionnelle : modèle créatif et technique|section Expression émotionnelle]] du cahier des charges (sections 14 à 17). Relier les commandes à l’[[06_IA_Logiciel/ARCHITECTURE_IA|architecture logicielle]] et les essais à la [[08_Tests/MATRICE_TESTS|matrice de validation]].

## AURA-009 r04 — Socle et doigts indépendants

Deux vidéos à partir de la CAO r04 v4. J1 fait deux tours dans chaque sens devant une caméra fixe. La main montre chaque doigt, puis les flexions combinées et les éprouvettes géométriques. [[02_Conception_Fusion/TABLE_R04|Prototype de table r04]] · [Release GitHub](https://github.com/Flombt/Axo/releases/tag/aura-009-r04-fabrication).

## AURA-009 r03 v2 — Démonstration cinématique

Film de 66 secondes en 4K à 60 i/s, issu du [[02_Conception_Fusion/TABLE_R03|modèle Fusion r03 v2]]. J1 reste manuel. Les cinq doigts suivent la commande commune T1. La chronologie présente HOME en orbite, les axes séparés, la main et sa transmission, les mécanismes internes, le filaire et un cycle coordonné à vide.

Les 143 poses distinctes ont été vérifiées de deux façons dans Fusion, par les liaisons et par rejeu des matrices exactes sur les solides. Le raccordement du faisceau a été contrôlé sur les 3 960 images. Les essais en charge, la tension et le chemin détaillé des tendons souples restent à qualifier.

[Film local](https://github.com/Flombt/Axo/releases/download/aura-009-r03-v2-cinematique/AURA-01_Cinematic_Demonstration.mp4) · [Projet Blender](../../../archives/r03/animations/AURA-01_Animation.blend) · [Rapport cinématique](../../../archives/r03/animations/RAPPORT_CINEMATIQUE.md) · [Couverture](../../../archives/r03/animations/AURA-01_Cover.png) · [Film, extraits et projet Blender sur GitHub](https://github.com/Flombt/Axo/releases/tag/aura-009-r03-v2-cinematique).

## V1

| Clé | Geste dominant | Couleur |
|---|---|---|
| `joy` | Redressement, salut, ouverture | Ambre |
| `sadness` | Repli lent et sûr | Indigo |
| `anger` | Tension ferme sans violence | Corail |
| `fear` | Rétraction contrôlée | Violet |
| `curiosity` | Exploration douce, pauses | Turquoise |

Chaque animation nécessite une pose d'entrée, keyframes, limites de vitesse/accélération, absence de collision et sortie sûre.

**Important :** le robot exprime des émotions par métaphore, il ne les ressent pas.

## V2 — Poses de référence

Valeurs testées le 21 novembre 2026 dans [[02_Conception_Fusion/CONCEPTION_MECANIQUE#V2 — Prototype mécanique enregistré|le prototype Fusion V2]]. Les angles sont donnés en degrés. G1 désigne le déplacement signé d’un mors en millimètres depuis HOME, positif à l’ouverture. Fusion applique le déplacement opposé au second mors. La hauteur se mesure au centre de prise par rapport au plan de table.

| Référence | J1 | J2 | J3 | J4 | J5 | G1 (mm) | Ouverture (mm) | Hauteur (mm) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| HOME | 0 | 0 | 0 | 0 | 0 | 0 | 13,60 | 127,73 |
| Joie | −15 | −12 | −10 | −15 | +38 | +4,5 | 22,60 | 216,02 |
| Tristesse | −10 | +5 | +16 | +22 | −22 | −1,5 | 10,60 | 37,85 |
| Colère | −4 | +6 | −4 | +5 | +6 | −5 | 3,60 | 108,40 |
| Peur | −15 | −24 | −14 | +26 | −26 | −3,5 | 6,60 | 223,26 |
| Curiosité | +26 | +3 | −6 | +10 | −21 | +2 | 17,60 | 120,91 |
| Salut · départ | +12 | −15 | −5 | −8 | −34 | +3 | 19,60 | 207,26 |
| Salut · arrivée | +12 | −15 | −5 | −8 | +34 | +3 | 19,60 | 207,26 |

La joie relève et ouvre la pince. La tristesse l’incline vers le plan d’appui. La colère resserre les mors dans une pose ferme. La peur ramène le centre de prise de 236 à 172 mm environ en distance horizontale à J1 tout en relevant et repliant le poignet. La curiosité tourne la pince vers le côté. Le salut utilise un mouvement du bras à l’entrée, puis 68° de roulis entre les deux positions du poignet.

Le groupe d’attributs `AURA_01_V2_Poses` du composant racine Fusion contient les huit références et persiste après réouverture. Il est accessible via le MCP. Les dix transitions mettent en jeu HOME vers les sept autres positions, les deux extrémités de Salut, Joie vers Curiosité et Curiosité vers Peur. Les 137 états distincts ont été vérifiés pour les interférences dans Fusion. Leur profil quintique sert de référence d’interpolation. La vitesse, la fluidité motorisée, le retour sûr depuis toute position et la lecture publique des gestes restent à éprouver.

![[assets/fusion_aura_v2_joie_2026-11-21.png|520]]

![[assets/fusion_aura_v2_tristesse_2026-11-21.png|520]]

## AURA-004 — Démonstration de la branche motorisée

Les six gestes reprennent les huit références Fusion. La vidéo montre les corps CAO de la nouvelle copie, avec la plaque, les moteurs, l’engrenage J5 et l’entraînement de la pince. L’affichage accélère les six gestes sur 16 s. Les temps de commande de premier essai figurent ci-dessous.

![[assets/fusion_aura004_demonstration_2026-11-21.mp4]]

| Chemin | États dans ce chemin | Temps minimal du profil d’essai, s |
|---|---:|---:|
| HOME → Joie | 10 | 6,20 |
| HOME → Tristesse | 10 | 2,10 |
| HOME → Colère | 11 | 6,85 |
| HOME → Peur | 10 | 4,80 |
| HOME → Curiosité | 10 | 2,75 |
| HOME → Salut · départ | 10 | 4,15 |
| HOME → Salut · arrivée | 10 | 4,15 |
| Salut · départ → Salut · arrivée | 15 | 2,10 |
| Joie → Curiosité | 13 | 3,45 |
| Curiosité → Peur | 12 | 7,55 |

Le profil en temps normalisé est `s(u) = 35u⁴ − 84u⁵ + 70u⁶ − 20u⁷`, appliqué à chaque axe de manière synchrone. Vitesse, accélération et à-coup s’annulent aux extrémités. La durée est choisie à partir des maximums théoriques `2,1875×Δq/T`, `7,5132×Δq/T²` et `52,5×Δq/T³`. Les plafonds provisoires en sortie J1 à J5 sont 35/24/30/42/72 °/s, 65/45/65/90/150 °/s² et 200/140/200/290/470 °/s³. Pour un mors G1, 1,6 mm/s, 3 mm/s² et 12 mm/s³.

Fusion a calculé **99 états distincts** et n’a détecté aucune interférence volumique entre les composants mobiles et fixes de l’assemblage aux états échantillonnés. Les contacts internes issus des géométries fournisseur du même boîtier ont été écartés. Le maximum d’écart de lecture à la consigne était de 0,050 ° ou mm selon la commande. Les combinaisons avec lacet et élévation J2 négative ont révélé un blocage du solveur Fusion lorsque ses butées J2 sont actives. Pour l’échantillonnage et la capture, les bornes du profil ont été contrôlées explicitement et les butées natives J2 ont été temporairement désactivées. Elles sont présentes dans le document enregistré. Le robot est revenu à HOME. Garder la vérification des limites côté contrôleur.

En test depuis le pignon, −42° ont donné +18° au rotor J5. Depuis la vis G1 lancée par incréments, 360° et 720° ont produit 2 et 4 mm par mors, avec déplacements opposés. Les temps de suivi réels, le jeu, les à-coups, le faisceau, les efforts de pince et l’arrêt restent à éprouver.

## V3 — Vidéo du poignet, des doigts et du bras

Ouvrir `Exports_Fusion/AURA_V3/AURA-01_V3_Demonstration.mp4` depuis la racine Aura. Le MP4 de 10,5 s provient de 168 images du viewport Fusion sur la V3 r02. Les chapitres servent à retrouver chaque mouvement.

| Début | Mouvement |
|---|---|
| 00:00 | Roulis du poignet, jusqu’à environ ±55°, avec déviation et flexion légères. |
| 00:03 | Flexion décalée des cinq doigts, dont le pouce oblique, puis retour vers l’ouverture. |
| 00:07 | Lacet du socle et flexion coordonnée des trois segments, puis retour en pose de référence. |

Chaque pose anime les liaisons natives de l’[[02_Conception_Fusion/DESIGN_V3|assemblage V3]]. Les charges, lissage sur le contrôleur réel et essais physiques restent ouverts. [[08_Tests/MATRICE_TESTS#V3 — Contrôles du bras à main articulée|Résultats CAO]].
