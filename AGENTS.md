# AURA-01 · Règles permanentes du projet

Commencer par [VERSION.md](VERSION.md), le [contexte projet](docs/architecture/PROJECT_CONTEXT.md) et les [règles du coffre Obsidian](AURA-01_Obsidian/AURA-01_Obsidian/AGENTS.md). Appliquer la configuration RTK de la session lorsqu’elle est fournie.

1. Identifier la révision active et l’origine des fichiers avant toute modification.
2. Travailler dans les dossiers principaux indiqués dans le [README](README.md).
3. Effectuer les modifications mineures dans l’arborescence principale et conserver leur historique dans Git.
4. Actualiser les fichiers techniques existants lorsque cela convient.
5. Pour un changement important, prendre un point de reprise identifiable et archiver les versions significatives avec un manifeste de restauration.
6. Séparer les fichiers de révisions différentes et tracer le statut des livrables absents.
7. Régénérer les exports touchés après une modification CAO et enregistrer la révision et l’empreinte de la source.
8. Mettre à jour la nomenclature et le budget dès qu’un composant, une quantité ou un fournisseur change.
9. Revalider les orientations, 3MF, plateaux et coupons après un changement géométrique concerné.
10. Actualiser les vues et rendus lorsqu’ils ne représentent plus l’état actif.
11. Maintenir un point de référence par domaine technique et relier les données d’essai à leur révision.
12. Vérifier les liens et les dépendances avant et après un déplacement.
13. Actualiser [VERSION.md](VERSION.md), [CHANGELOG.md](CHANGELOG.md), le [contexte](docs/architecture/PROJECT_CONTEXT.md) et le [manifeste](docs/architecture/revision.json) selon le changement.
14. Consulter les archives lorsqu’une dépendance historique ou une restauration le justifie.
15. Retirer les fichiers temporaires de la mission après vérification. Conserver les preuves destinées au projet.
16. Respecter le plafond de **150 €** sur un panier TTC avec quantités, port, consommables et stock justifiés.
17. Distinguer les mesures CAO, hypothèses, résultats numériques et essais physiques. Consigner uniquement les essais effectués.
18. Pour toute donnée unique, vérifier la sauvegarde et la restauration avant suppression éventuelle.
19. Exécuter **python -B -X utf8 tools/verifier_projet.py** depuis la racine avant clôture. Ajouter **--complet** après une migration et examiner les résultats. Le script travaille en lecture seule.
20. Identifier les travaux simultanés et les changements locaux. Coordonner toute opération qui affecte leurs fichiers. Préserver l’historique Git et utiliser des tags pour les révisions significatives.

Toute tâche Sprinter nécessite une demande explicite pour lancer ou relancer une compilation IPA.
