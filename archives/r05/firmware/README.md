# Commande USB du Pico AURA-01 r05

Le Pico lit du texte UTF-8 sur l’USB série. Il émet six sorties PWM de position à 50 Hz sur GP6 à GP11. Elles correspondent à J1, J2, J3, P, I et MAU. Le +5 V des servos vient du bloc protégé. Relier la masse logique et la masse des servos sur la distribution. Vérifier au premier essai que chaque servo reconnaît les signaux 3,3 V du Pico.

Le programme démarre avec sorties coupées et configuration d’étalonnage vide. Copier `controle.py` et `main.py` sur un Pico avec [MicroPython](https://micropython.org/download/RPI_PICO/). L’activation demande les six profils mesurés. Le sens d’un servo se corrige par le signe de sa pente. Aligner le robot sur son repère neutre avec les servos hors tension avant chaque `ARM`.

| Ligne | Effet local |
|---|---|
| `STATUS` | État d’armement et raison de l’arrêt. |
| `ARM` | Autorise les sorties au neutre si les six profils passent les limites. |
| `MOVE J1=20 J2=-6 P=30` | Remplace les cibles demandées après validation de toute la ligne. Les autres cibles restent celles déjà reçues. |
| `PING` | Rafraîchit la temporisation. Envoyer à 10 Hz depuis l’ordinateur pendant l’armement. |
| `STOP` | Met les six sorties à zéro au cycle suivant. |

La boucle traite une quantité bornée d’octets par tour. Les cibles restent dans les limites locales et avancent par pas toutes les 20 ms. Après 350 ms sans demande valide, les impulsions passent à zéro. Le watchdog réinitialise la carte si la boucle s’immobilise. Une coupure 5 V matérielle et la retenue des pivots restent nécessaires. Le retour de position est interne à chaque servo et le Pico ne mesure pas le mouvement réel.

Au premier banc, caractériser chaque servo seul. Avec les pièces ancrées et retenues, vérifier la course, le courant et l’arrêt en charge hors tension avant d’activer le robot complet. Sur l’ordinateur, le parseur, les bornes, la rampe, le délai de 350 ms, le refus d’un armement sans étalonnage et la conversion des rapports ont été testés directement. Le test d’USB sur un Pico et la mise sous charge restent à faire.
