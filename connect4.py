import random
import math

#main game

def new_grid(n, m):
    """Créer une nouvelle grille de n colones et m lignes
    usuellement le jeu se joue sur une grille (7 x 6) """
    return [[0 for i in range(m)] for j in range(n)]

def playable(grid, play):
    """Renvoie True si il est possible de jouer sur "play", False sinon"""
    if not (0 <= play < len(grid)):
        return False
    else:
        i, imax = 0, len(grid[play])
        res = False
        while (not res) and i < imax:
            if grid[play][i] == 0:
                res = True
            i += 1
        return res

def play_at(grid, play, player):
    """Renvoie la grille avec un nouveau pion "player" dans la colone "play" """
    newGrid = [colone.copy() for colone in grid]
    i, imax = 0, len(grid[play])
    while newGrid[play][i] != 0:
        i += 1
    newGrid[play][i] = player
    return newGrid

def display_grid(grid):
    """Affiche la grille de jeu"""
    res = [str(i) + "\t" for i in range(len(grid))]
    res.append("\n")
    for l in range(len(grid[0]) - 1, -1, -1):
        for c in range(len(grid)):
            res.append([".", "O", "X"][grid[c][l]])
            res.append("\t")
        res.append("\n")
    print("".join(res))
    return None

def connected(grid, n):
    """Test si l'un des joueurs à gagner et renvoie:
    0 si aucun n'a gagner, le numéro associer au joueur gagnant sinon"""
    winner = 0
    #test des colones
    cmax, lmax = len(grid), len(grid[0])
    c = 0
    while winner == 0 and c < cmax:
        l = 0
        consecutive = 1
        while consecutive < n and l < lmax - 1:
            if grid[c][l] == grid[c][l + 1] and grid[c][l] != 0:
                consecutive += 1
            else:
                consecutive = 1
            l += 1
        if consecutive == n:
            winner = grid[c][l]
        c += 1

    #test des lignes
    l = 0
    while winner == 0 and l < lmax - 1:
        c = 0
        consecutive = 1
        while consecutive < n and c < cmax - 1:
            if grid[c][l] == grid[c + 1][l] and grid[c][l] != 0:
                consecutive += 1
            else:
                consecutive = 1
            c += 1
        if consecutive == n:
            winner = grid[c][l]
        l += 1

    #test des diagonales /
    #en partant de la première colone:
    c, l = 0, 0
    while winner == 0 and l < lmax - 1:
        dc, dl = 0, l
        consecutive = 1
        while consecutive < n and dc < cmax - 1 and dl < lmax - 1:
            if grid[dc][dl] == grid[dc + 1][dl + 1] and grid[dc][dl] != 0:
                consecutive += 1
            else:
                consecutive = 1
            dc += 1
            dl += 1
        if consecutive == n:
            winner = grid[dc][dl]
        l += 1
    #en partant de la première ligne:
    c, l = 0, 0
    while winner == 0 and c < cmax - 1:
        dc, dl = c, 0
        consecutive = 1
        while consecutive < n and dc < cmax - 1 and dl < lmax - 1:
            if grid[dc][dl] == grid[dc + 1][dl + 1] and grid[dc][dl] != 0:
                consecutive += 1
            else:
                consecutive = 1
            dc += 1
            dl += 1
        if consecutive == n:
            winner = grid[dc][dl]
        c += 1
    #test des diagonales \
    #en partant de la dernière colone:
    c, l = cmax - 1, 0
    while winner == 0 and l < lmax - 1:
        dc, dl = c, l
        consecutive = 1
        while consecutive < n and dc > 0 and dl < lmax - 1:
            if grid[dc][dl] == grid[dc - 1][dl + 1] and grid[dc][dl] != 0:
                consecutive += 1
            else:
                consecutive = 1
            dc -= 1
            dl += 1
        if consecutive == n:
            winner = grid[dc][dl]
        l += 1
    #en partant de la première ligne:
    c, l = cmax - 1, 0
    while winner == 0 and c > 0:
        dc, dl = c, 0
        consecutive = 1
        while consecutive < n and dc > 0 and dl < lmax - 1:
            if grid[dc][dl] == grid[dc - 1][dl + 1] and grid[dc][dl] != 0:
                consecutive += 1
            else:
                consecutive = 1
            dc -= 1
            dl += 1
        if consecutive == n:
            winner = grid[dc][dl]
        c -= 1
    return winner

def has_win(grid):
    return connected(grid, 4)

def game(player1, player2, result = False, n = 7, m = 6):
    """Lance un jeu sur une grille à n colones et m lignes"""
    grid = new_grid(n, m)
    winner = 0
    turn = 1
    nbTurn, nbTurnMax = 0, n * m
    while winner == 0:
        #vérification égalité
        nbTurn += 1
        if nbTurn > nbTurnMax:
            break
        #début du tour
        if turn == 1:
            grid = play_at(grid, player1(grid, turn), turn)
        else:
            grid = play_at(grid, player2(grid, turn), turn)
        winner = has_win(grid)
        turn = [2, 1][turn - 1]
    #résultats de la partie
    turn = [2, 1][turn - 1]
    if result:
        print(["DRAW ...", "O WIN !", "X WIN !"][turn])
    return winner

def tournois(player1, player2, nbGame, n = 7, m = 6):
    """Réalise un tournois entre deux stratégies pour "nbGames" parties,
    les resultats sont en % de victoires et sont affichés selon : [égalité, premier joueur, deuxième joueur]"""
    res = [0, 0, 0]
    prog = 0
    for i in range(nbGame):
        if i / nbGame >= (prog/100):
            print(str(prog) + "%")
            prog += 10
        res[game(player1, player2)] += 1
    for i in range(len(res)):
        res[i] = (res[i] * 100) / nbGame
    return res

#players

def human_player(grid, turn):
    """Demande à un joueur humain son placement et le renvoie"""
    display_grid(grid)
    play = -1
    while True:
        play = int(input("play with " + ["O", "X"][turn - 1] + " : "))
        if playable(grid, play):
            break
    return play

def bot_random(grid, turn):
    """bot choisissant son placement aléatoirement parmis les placements disponibles"""
    play = random.randrange(0, len(grid))
    i = 0
    while not playable(grid, play):
        play = random.randrange(0, len(grid))
    return play

def bot(n, evalFunc):
    """Renvoie l'ordinateur jouant en explorant l'arbre dans une profondeur au plus n selon "tree_explore" """
    def bot_player(grid, turn):
        res = tree_explore(grid, n, turn, turn, evalFunc)
        best = best_score(res)
        return random.choice([i for i in range(len(res)) if res[i] == best])
    return bot_player

def dynamic_bot(n, evalFunc):
    """Renvoie l'ordinateur jouant en explorant l'arbre dans une profondeur au plus n selon "tree_explore" """
    def bot_player(grid, turn):
        res = dynamic_tree_explore(grid, n, turn, turn, evalFunc)
        best = best_score(res)
        return random.choice([i for i in range(len(res)) if res[i] == best])
    return bot_player

#exploration de l'arbre de jeu pour les fonctions "bot" et "dynamic_bot"

def best_score(scores):
    """Renvoie la plus grande des valeurs du tableau qui ne sont pas None"""
    return max([score for score in scores if score != None])

def worst_score(scores):
    """Renvoie la plus petite des valeurs du tableau qui ne sont pas None"""
    return min([score for score in scores if score != None])

def tree_explore(grid, imax, turn, player, evalFunc):
    """Renvoie la lite des évaluations pour chaque coups possible en parcourant l'arbre a l'aide de "evalFunc"
    -> utilise la liste "scores" qui attribue à chaque coups une valure suivant : [None = injouable, -1 = défaite, 1 = gagnant, entre -1 et 1 = indeterminé]"""
    continueExplore = imax != 0
    scores = [None for c in grid]
    testedGrid = [[] for c in grid]
    for play in range(len(grid)):
        if playable(grid, play):
            testGrid = play_at(grid, play, turn)
            testedGrid[play] = testGrid
            scores[play] = evalFunc(testGrid, player)
    #continuer si les valeurs max ne sont pas atteintes
    if continueExplore and (scores != [None for c in grid]):
        if turn == player:
            continueExplore = best_score(scores) != 1
        else:
            continueExplore = worst_score(scores) != -1
    if continueExplore:
        for play in range(len(grid)):
            if scores[play] != None:
                nextTurn = [2, 1][turn - 1]
                nextScores = tree_explore(testedGrid[play], imax - 1, nextTurn, player, evalFunc)
                if nextScores != [None for c in grid]:
                    if turn == player:
                        scores[play] = worst_score(nextScores)
                    else:
                        scores[play] = best_score(nextScores)
    return scores

def new_key(oldKey, play, turn):
    """Renvoie une clé décrivant l'évolution du jeu après le début de l'exploration de l'arbre
     -> chaque point '.' de la clé correspond à une colone, les nombres successifs entre les points donnent les coups, dans l'ordre, joués dans la colone associée"""
    i = 0
    newKey = ''
    for char in oldKey:
        if char == '.':
            if i == play:
                newKey += str(turn)
            i += 1
        newKey += char
    return newKey

def dynamic_tree_explore(grid, imax, initTurn, player, evalFunc):
    """Utilise la fonction "tree_explore" avec une mémoire des configuration déjà calculées pour se tour"""
    mem = {}
    def aux(grid, imax, turn, key):
        if key in mem:
            return mem[key]
        continueExplore = imax != 0
        scores = [None for c in grid]
        testedGrid = [[] for c in grid]
        for play in range(len(grid)):
            if playable(grid, play):
                testGrid = play_at(grid, play, turn)
                testedGrid[play] = testGrid
                scores[play] = evalFunc(testGrid, player)
        if continueExplore and (scores != [None for c in grid]):
            if turn == player:
                continueExplore = best_score(scores) != 1
            else:
                continueExplore = worst_score(scores) != -1
        if continueExplore:
            for play in range(len(grid)):
                if scores[play] != None:
                    nextTurn = [2, 1][turn - 1]
                    nextKey = new_key(key, play, turn)
                    nextScores = aux(testedGrid[play], imax - 1, nextTurn, nextKey)
                    if nextScores != [None for c in grid]:
                        if turn == player:
                            scores[play] = worst_score(nextScores)
                        else:
                            scores[play] = best_score(nextScores)
        mem[key] = scores
        return scores

    key = ''.join(['.' for c in grid])
    return aux(grid, imax, initTurn, key)

#fonctions d'évaluations pour le parcour de l'arbre de jeu par "tree_explore"

def naive_eval(grid, player):
    """Evaluation naive de la grille de jeu: -1 si perdant, 1 si gagnant, 0 sinon"""
    winner = has_win(grid)
    if winner == 0:
        return 0
    elif winner == player:
        return 1
    else:
        return -1

def count_attack_list(list, n):
    """Compte le nombre d'attaques sur une ligne / colone / diagonale (list) et renvoie le nombre d'attaques pour chaques joueurs : (j1, j2)"""
    attacks = []
    indexStart = 0
    indexEnd = 0
    consecutive = 1
    for i in range(len(list) - 1):
        if list[i] == list[i+1]:
            if consecutive == 1:
                indexStart = i
            consecutive += 1
        else:
            if consecutive >= n:
                indexEnd = i
                if indexStart > 0:
                    if list[indexStart - 1] == 0:
                        if not (indexStart - 1, list[indexStart]) in attacks:
                            attacks.append((indexStart - 1, list[indexStart]))
                if list[indexEnd +1] == 0:
                    if not (indexEnd + 1, list[indexEnd]) in attacks:
                        attacks.append((indexEnd + 1, list[indexEnd]))
            consecutive = 1
    if consecutive >= n:
        if indexStart > 0:
            if list[indexStart - 1] == 0:
                if not (indexStart - 1, list[indexStart]) in attacks:
                    attacks.append((indexStart - 1, list[indexStart]))
    attacks1 = len([e for e in attacks if e[1] == 1])
    attacks2 = len(attacks) - attacks1
    return (attacks1, attacks2)

def count_attack(grid, n):
    """Compte le nombre d'attaque sur la grille de jeu en utilisant "count_attack_list" """
    res = [0, 0]
    cmax, lmax = len(grid), len(grid[0])
    #test des colones
    for c in grid:
        resColone = count_attack_list(c, n)
        res[0] += resColone[0]
        res[1] += resColone[1]
    #test des lignes
    for i in range(len(grid[0])):
        resLigne = count_attack_list([c[i] for c in grid], n)
        res[0] += resLigne[0]
        res[1] += resLigne[1]
    #test des diagonales /
    #en partant de la première colone:
    for l in range(1, lmax):
        dc, dl = 0, l
        diag = []
        while dc < cmax and dl < lmax:
            diag.append(grid[dc][dl])
            dc += 1
            dl += 1
        resDiag = count_attack_list(diag, n)
        res[0] += resDiag[0]
        res[1] += resDiag[1]
    #en partant de la première ligne:
    for c in range(cmax):
        dc, dl = c, 0
        diag = []
        while dc < cmax and dl < lmax:
            diag.append(grid[dc][dl])
            dc += 1
            dl += 1
        resDiag = count_attack_list(diag, n)
        res[0] += resDiag[0]
        res[1] += resDiag[1]
    #test des diagonales \
    #en partant de la dernière colone:
    for l in range(1, lmax):
        dc, dl = cmax - 1, l
        diag = []
        while dc >= 0 and dl < lmax:
            diag.append(grid[dc][dl])
            dc -= 1
            dl += 1
        resDiag = count_attack_list(diag, n)
        res[0] += resDiag[0]
        res[1] += resDiag[1]
    #en partant de la première ligne:
    for c in range(cmax):
        dc, dl = c, 0
        diag = []
        while dc >= 0 and dl < lmax:
            diag.append(grid[dc][dl])
            dc -= 1
            dl += 1
        resDiag = count_attack_list(diag, n)
        res[0] += resDiag[0]
        res[1] += resDiag[1]
    return res

def count_attack_eval(grid, player):
    """Evaluation qui compte le nombre d'attaque (3 jetons alignés avec 1 emplacement vide) et ranvoie:
    1 si gagnant, -1 si perdant, 0.5 si le joueur possède plus d'attaques, -0.5 si l'autre joueur en possède plus, 0 sinon"""
    winner = has_win(grid)
    if winner == 0:
        attacks = count_attack(grid, 3)
        otherPlayer = [2, 1][player - 1]
        if attacks[player - 1] > attacks[otherPlayer - 1]:
            return 0.5
        elif attacks[player - 1] < attacks[otherPlayer - 1]:
            return -0.5
        else:
            return 0
    elif winner == player:
        return 1
    else:
        return -1

def count_attack_eval2(grid, player):
    """Version de "count_attack_eval" qui favorise les configurations avec plus d'attaques"""
    winner = has_win(grid)
    if winner == 0:
        attacks = count_attack(grid, 3)
        otherPlayer = [2, 1][player - 1]
        diff = attacks[player - 1] - attacks[otherPlayer - 1]
        return 2 * math.atan(diff) / math.pi
    elif winner == player:
        return 1
    else:
        return -1

def point_capa(c, l, n, m):
    """Evaluation du nombre de configurations gagnantes possible avec un pion sur la case (c, l) dans une grille (n*m)"""
    res = 0
    for i in range(4):
        colone, ligne = False, False
        #colone
        if l - 3 + i >= 0 and l + i < m:
            colone = True
            res += 1
        #ligne
        if c - 3 + i >= 0 and c + i < n:
            ligne = True
            res += 1
        #diagonale /
        if ligne and colone:
            res += 1
        #diagonale \
        if ligne and (l + 3 - i < m) and (l - i >= 0):
            res += 1
    return res

def grid_capa(n, m):
    """calcul l'ensemble des "capacités" sur la grille (n*m) en utilisant "point_capa" """
    grid = new_grid(n, m)
    for c in range(n):
        for l in range(m):
            grid[c][l] = point_capa(c, l, n, m)
    return grid

def sum_grid(grid):
    """Renvoie la somme des elements d'une gille"""
    res = 0
    for c in grid:
        for e in c:
            res += e
    return res

classicGridEval = grid_capa(7, 6)
sumClassicGrid = sum_grid(classicGridEval)

def capacity_eval(grid, player):
    """Evaluation sans mémoire de la grille de jeu, somme des "capacités" de chaque pions posés sur la grille,
    compté positivement pour le joueur "player" et négativement pour l'adversaire de "player" """
    winner = has_win(grid)
    if winner == 0:
        score = 0
        for c in range(len(grid)):
            for l in range(len(grid[0])):
                if grid[c][l] == player:
                    score += classicGridEval[c][l]
                elif grid[c][l] == 0:
                    None
                else:
                    score -= classicGridEval[c][l]
        return score / sumClassicGrid
    elif winner == player:
        return 1
    else:
        return -1
