# IA, MCP et automates

Références à partir des sections [[README#15 — Autonomie : « il bouge tout seul » sans être incontrôlable|Autonomie]] (15 à 17) et [[README#24 — Moteur IA et limites de son rôle|Moteur IA]] (24 à 26) du cahier des charges. L’interprétation sélectionne des [[04_Animation_Emotion/ANIMATIONS|animations]] et transmet une commande au [[05_Electronique/SCHEMA_FUTUR|contrôleur local]].

IA texte → intention structurée → validateur → planificateur → contrôleur sécurisé → axes.

- Autodesk Assistant est visible dans Fusion.
- Serveur MCP Fusion : activer dans Préférences > Général > API si disponible ; endpoint par défaut `http://127.0.0.1:27182/mcp`.
- Ne pas confondre connexion MCP et contrôle moteur du robot physique.
- Ne pas utiliser les crédits API sans consentement explicite.
- L'autonomie signifie des gestes autorisés par automate, pas un accès illimité de l'IA aux moteurs.

## AURA-006 — Implantation embarquée

Le Pi 5 héberge perception et planification. Il demande des positions et des vitesses datées. Le contrôleur temps réel vérifie l’état du robot, les limites de l’axe, la plausibilité des commandes, le retour capteur et le délai de communication. Le MCU de main exécute seulement les consignes validées et ramène les sorties à l’état défini à la perte de liaison. Le frein de J2 et la coupure de puissance disposent d’une chaîne matérielle indépendante. [[02_Conception_Fusion/INTEGRATION_MECATRONIQUE_V3#E — Architecture embarquée|Bilan d’énergie et emplacements]] · [[05_Electronique/SCHEMA_FUTUR#AURA-006 — Batterie, arrêt et commande de la main|Schéma fonctionnel]].
