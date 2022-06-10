# Connect4
**Impémentation de différentes stratégies pour le jeu puissance 4**

## Le jeu

- La grille de jeu est codée sous la forme d'une liste de liste d'entiers (liste des colones)
- La grille est initialisée par la grille remplie de 0
- Les pions du premier et deuxième joueur sont représenté respectivement par les entiers 1 et 2
- Les joueurs sont codés par des fonctions qui à une grille de jeu renvoie une position de jeu possible

## Les joueurs

- ```human_player``` montre la grille de jeu à l'utilisateur et lui demande un placement possible
- ```bot_random``` joue aléatoirement (selon une loi uniforme implémenté par une méthode de rejet) parmis les postions possibles indépendamment de la grille de jeu
- ```bot``` prends en argument une fonction d'évaluation sur la grille et renvoie un joueur utilisant une stratégie expliquée plus loin
- ```dynamic_bot``` est une version similaire de la fonction ```bot``` mais utilisant la programmation dynamique

## Méthode de l'ordinateur

La fonction ```bot``` utilise une impplémentation intuitive de l'algorithme Minimax de Von Neumann. Elle prends en argument une fonction d'évaluation sur la grille de jeu et un entier décrivant la profondeur jusqu'à laquelle l'arbre de jeu est exploré. Elle renvoie une fonction qui à une grille de jeu et un joueur associe le placement qui cherche à maximiser le score du joueur pour ce tour. Le score est ici un nombre réel compris entre -1 et 1, 1 correspondant à une victoire et -1 à une défaite. L'arbre de jeu est explorer à l'aide de la fonction ```tree_explore```

La fonction ```dynamic_bot``` fonctionne de façon identique au détail près que l'exploration de l'arbre utilise la programation dynamique. En effet, une même grille de jeu est atteinte plusieurs fois dans chaque exploration de l'arbre? Chaque grille est donc également représentée par une chaine de caratère décrivant les coups successifs dans chaques colones et le score associé à ce coup, pour cette exploration, est stocké dans un dictionnaire à la clé associée à la grille.

## Différentes stratégies (fonctions d'évaluation)

- ```naive_eval``` est la fonction d'évaluation naïve qui se contente de renvoyer $1$ si le joueur est gagnant, $-1$ si il est perdant et $0$ sinon.
- ```count_attack_eval``` compte le nombre "d'attaques" des deux joueurs. Une "attaque" est une successiohn de 3 jetons du joueur avec une case libre sur une des deux extrémités de l'alignement. Cette première version renvoie $1$ si le joueur est gagnant, $0.5$ s'il a plus d'attaques que son adversaire, $0$ s'il en a autant, $-0.5$ s'il en a moins et $-1$ s'il est perdant.
- ```count_attack_eval2``` compte également le nombre d'attaques mais renvoie, en nottant $x$ la différence entre le nombre d'attaques du joureur par rapport à son adversaire : $\frac{2}{\pi}\arctan(x)$. Cette fonction réalisant une bijection strictement croissante de $\mathbb{R}$ dans $[0, 1]$  qui s'annule en $0$ elle donne une évaluation similaire à la fonction ```count_attack_eval``` mais cherche à avoir le plus d'attauque de plus que l'adversaire possible.
- ```capacity_eval``` associe à chaque case de la grille un entier positif qui désigne le nombre de façon d'aligner 4 jetons sur la grille dont l'un est sur la case considérée. Intuitivement, on comprends que les cases du centre ont donc un entier plus grand que les cases sur les bords ou même dans les coins. La fonction d'évaluation compte positivement, pour chaque jeton du joueur, et négativement pour les jetons de son adversaire, la somme des entiers associés à la case des jetons. Cette évaluation est ensuite normalisée entre $-1$ et $1$ en calculant le score maximal d'un joueur (inatteignable en pratique) si la grille était remplie de ses jetons. L'évaluation de la grille classique (7 colones et 6 lignes) donne :

<p align="center">
  <img src="https://user-images.githubusercontent.com/83034156/173144320-c68221a6-a82b-4202-a395-1b6042f88b49.png" />
</p>

## Quelques résultats

### complexité

La complexité en temps pour l'exploration de l'arbre est exponentielle en la profondeur maximale atteinte, ainsi si il est difficile d'observer des résultats pour une exploration très profonde. On peut optenir une estimation de l'évolution du temps de calcul en faisant joué ```bot(n, naive_eval)``` pour quelques valeurs de ```n``` contre ```bot_random``` : 
Temps d'execution de 100 parties pour ```n``` =
- 1 : 1.6 s
- 2 : 8.3 s
- 3 : 48.9 s
- 4 : 283.42 s

### stratégie naïve

On peut également observer l'éfficacité d'explorer l'arbre plus ou moins profondémment, pour l'évaluation ```naive_eval``` en réalisant différentes parties, pour 100 parties on a :

| n de Joueur 1      |     n de Joueur 2   |        Victoires du joueur 1 | Victoires du joueur 2 | Parties nulles |
| :----------------: | :-----------------: | :--------------------------: | :-------------------: | :------------: |
| 1                  | 2                   | 30                           | 64                    | 6              |
| 2                  | 1                   | 64                           | 32                    | 4              |
| 2                  | 3                   | 23                           | 68                    | 9              |
| 3                  | 2                   | 79                           | 19                    | 4              |

### remarques

On constate l'asymetrie bien connue du puissance 4, le premier joueur étant toujours avantagée (même gagnant en conaissant la solution exacte). En faisant joué quelques stratégies contre elles même on trouve ce déséquilibre : 
- ```bot_random``` sur 10 000 parties : le joueur 1 gagne 55.8% du temps et perds 43.9% du temps
- ```bot(2, naive_eval)``` sur 100 parties : le joueur 1 gagne 49% du temps et perds 47ù du temps
