# AURA-01

Bras robotique de table imprimable en FDM, avec quatre axes motorisés de bras et cinq doigts indépendants. La **V5-stabilisation** documente un prototype numérique à qualifier sur banc ancré. [Version active](VERSION.md) · [Rapport des corrections](RAPPORT_CORRECTIONS.md)

![Vue de la V5 stabilisée à partir des solides Fusion](docs/diagnostic/corrections/visuels/06_blender_ensemble.png)

| Domaine | Point d’entrée |
|---|---|
| Fusion et cinématique | [Modèle F3D, reproduction et animation](fusion/README.md) |
| Impression | [STEP, STL, 3MF, plateaux et éprouvettes](manufacturing/README.md) |
| Assemblage | [Montage à blanc, dépose et qualification](assembly/README.md) |
| Électronique | [Rail, brochage, câblage et coupure](electronics/README.md) |
| Commande | [Firmware Pico 2, calibration et protocole](firmware/README.md) |
| Budget | [Nomenclature, prix TTC, stocks et ports](purchases/NOMENCLATURE.md) |
| Documentation | [Contexte de reprise](docs/architecture/PROJECT_CONTEXT.md) · [Coffre Obsidian](AURA-01_Obsidian/AURA-01_Obsidian/LISEZ_MOI_D_ABORD.md) |
| Audit et historique | [Diagnostic V5 roulis](DIAGNOSTIC_ROBOT_COMPLET.md) · [Archives](archives/README.md) · [Changelog](CHANGELOG.md) |

La commande passe par le Pico 2, l’arrêt matériel et le réarmement local. La phase physique commence par les éprouvettes, les retenues et une charge factice. Le budget opérationnel reste à confirmer sous **150 €**. [Critères de qualification](RAPPORT_CORRECTIONS.md)

Pour modifier le projet, suivre les [règles permanentes](AGENTS.md), puis lancer `python -B -X utf8 tools/verifier_projet.py` à la racine.
