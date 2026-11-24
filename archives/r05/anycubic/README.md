# AURA-01 r05 · 3MF pour Anycubic

Choisir le dossier correspondant à l’imprimante et à sa buse de **0,4 mm**. Chaque dossier contient le même jeu de pièces et son tranchage dédié. Les couleurs identifient les familles proposées. Toute la série peut être imprimée dans un seul PETG noir.

| Profil | Zone utilisée par le contrôle | Plateaux | Filament robot | Temps estimé |
|---|---|---:|---:|---:|
| [Anycubic Kobra X](Kobra_X) | 260 × 260 mm | 6 | 321,73 g | 19 h 37 |
| [Anycubic Kobra 3 Max](Kobra_3_Max) | 420 × 420 mm utiles | 6 | 338,04 g | 20 h 00 |
| [Anycubic Kobra 3](Kobra_3) | 250 × 250 mm utiles | 6 | 373,50 g | 20 h 18 |

Le filament et le temps du robot comprennent les supports et bordures. Les six coupons ajoutent environ 14,5 à 15,2 g et 46 à 48 min sur le plateau séparé. Les estimations varient selon le profil machine et ne représentent pas un temps mesuré.

| Planche dans chaque dossier | Pièces | Contenu |
|---|---:|---|
| `AURA_r05_01_Graphite_Platine.3mf` | 1 | Platine principale. |
| `AURA_r05_01_Graphite_Bras.3mf` | 5 | Bras, avant-bras et gardes. |
| `AURA_r05_02_Gris.3mf` | 13 | Tourelle, palier, cassette, guides et appuis. |
| `AURA_r05_03_Petrole.3mf` | 11 | Dentures, tambours, peigne et capot. |
| `AURA_r05_04_Blanc.3mf` | 17 | Paume, chape du pouce et les quinze phalanges. |
| `AURA_r05_05_Coupons.3mf` | 6 | Trois Ø22 pour 608, empreintes SG90/MG996R et axes M2/M5. |

Ouvrir un fichier comme **projet 3MF** dans Anycubic Slicer Next. Le profil intégré `AURA r05 PETG` indique une couche de **0,20 mm**, ou **0,16 mm** pour les dentelures et la main, et quatre parois. La planche grise active les supports automatiques sur le plateau et au besoin sur le modèle, notamment sous la tourelle. Dégager les portées avant montage. Les températures de tranchage viennent des profils Anycubic PETG installés. Le coupon sert à les confirmer avec le filament et la face de la plaque utilisés.

Les **18 planches** ont été tranchées et rouvertes par le moteur Anycubic Slicer Next 2.0.0.3. Les archives contiennent le projet, les réglages et le G-code calculé. Tous les objets imprimables correspondent aux STL, aux quantités et aux limites du plateau. La planche grise Kobra 3 a été retranchée dans l’interface et affichait les supports et les mêmes **136,86 g** que le résultat natif. La planche blanche Kobra X et les coupons Kobra 3 Max ont été ouverts avec leur machine et leurs paramètres corrects. Le moteur peut signaler le seuil de température du filament ou un mode de timelapse. Vérifier la plaque et le PETG au coupon.

Le lot local `miroir USB historique/r05` réunit les mêmes **57 fichiers 3MF** avec leur classement par modèle. Copier sur la clé la planche du modèle d’imprimante correspondant si son firmware lit les projets 3MF. Si son menu sélectionne les fichiers machine en G-code, ouvrir et exporter le plateau en format machine depuis Anycubic. La clé et la lecture physique par les trois imprimantes restent à essayer.

[3MF individuels](3MF_individuels) pour une éprouvette ou un remplacement, préparés sur le profil Kobra 3. [Contrôles des plateaux](plateaux_r05.json) · [Contrôles des fichiers individuels](individuels_r05.json) · [Inventaire STL et montage](../fusion/README.md)
